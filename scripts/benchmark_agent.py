"""Measure the workloads an AI computer-use agent puts on the wrapper, on the bundled test applications.

Backs the "agent workloads" item of GH-85. ``scripts/benchmark.py`` times single finds and actions,
which is what a test does. An agent driving a desktop (for example through an MCP server, GH-145)
does different work on every step: it dumps the accessibility tree, takes screenshots, and often
runs in a short-lived process. This script times that work on the UIA2/UIA3 x WinForms/WPF matrix:

1. **snapshot**: walk the whole main window and collect name, automation id, control type,
   bounding rectangle and enabled state for every element, three ways: wrapper property reads, a
   wrapper ``CacheRequest``, and raw C#. Where pywinauto is installed (``bench`` group) the same
   walk also runs through pywinauto's ``uia`` ``descendants()`` and through raw comtypes
   ``IUIAutomation`` (the approach Windows-MCP and pathlight-mcp take), against the same process.
2. **cold start**: fresh interpreters that import ``flaui``, set up the PythonNet bridge, create the
   automation object, attach to the running app and run a first find.
3. **capture**: screenshot the window and one element, then encode to PNG bytes in memory.
4. **scaling**: ``find_all_descendants`` on the largest list and grid controls in the apps.
5. **reliability**: repeated find-then-toggle cycles, counting the ones that fail.

Usage::

    uv run python scripts/benchmark_agent.py                       # flaui only
    uv run --group bench python scripts/benchmark_agent.py         # add pywinauto / comtypes
    uv run --group bench python scripts/benchmark_agent.py --json agent.json
    uv run python scripts/benchmark_agent.py --sections snapshot capture -n 20

The script needs an interactive desktop: it launches the test apps and toggles a checkbox.
"""

from __future__ import annotations

import argparse
import gc
import io
import json
from pathlib import Path
import platform
import statistics
import subprocess  # nosec B404  # runs this interpreter on a fixed script, no user input
import sys
import time
from typing import Any, Callable

# pywinauto initialises COM (multithreaded) at import time, so it must be imported before the CLR
# starts. --skip-pywinauto skips the import too, so FlaUI runs exactly as it would on its own.


def _preload_pywinauto() -> bool:
    """Import pywinauto now, before the CLR starts, unless ``--skip-pywinauto`` was given.

    :return: Whether pywinauto is available for the comparisons.
    """
    if "--skip-pywinauto" in sys.argv:
        return False
    try:
        import pywinauto  # noqa: F401  # pylint: disable=import-outside-toplevel,unused-import
    except ImportError:  # pragma: no cover - depends on the optional bench group
        return False
    return True


HAVE_PYWINAUTO = _preload_pywinauto()

try:
    from PIL import ImageGrab

    HAVE_PIL = True
except ImportError:  # pragma: no cover - Pillow is optional
    HAVE_PIL = False

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO))

# isort: off
# Importing benchmark also sets up the PythonNet bridge.
from benchmark import APPS, _time  # noqa: E402  # pylint: disable=wrong-import-position
from flaui.core.cache_request import CacheRequest  # noqa: E402  # pylint: disable=wrong-import-position
from flaui.core.automation_elements import AutomationElement  # noqa: E402  # pylint: disable=wrong-import-position
from flaui.core.capturing import Capture  # noqa: E402  # pylint: disable=wrong-import-position
from flaui.core.definitions import ToggleState, TreeScope  # noqa: E402  # pylint: disable=wrong-import-position
from flaui.lib.enums import UIAutomationTypes  # noqa: E402  # pylint: disable=wrong-import-position
from flaui.lib.exceptions import ElementNotFound  # noqa: E402  # pylint: disable=wrong-import-position
from flaui.modules.automation import Automation  # noqa: E402  # pylint: disable=wrong-import-position

# isort: on

Stats = dict[str, float]
Record = tuple[str, str, Any, tuple[int, int, int, int], bool]

SECTIONS = ("snapshot", "cold", "capture", "scaling", "reliability")

# Child process for the cold-start measurement. It prints one JSON line of phase timings (seconds).
COLD_CHILD = r"""
import json, sys, time
t0 = time.perf_counter()
sys.path.insert(0, sys.argv[3])
import flaui
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
t1 = time.perf_counter()
setup_pythonnet_bridge()
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
t2 = time.perf_counter()
automation = Automation(UIAutomationTypes[sys.argv[1]])
t3 = time.perf_counter()
automation.application.attach(int(sys.argv[2]))
window = automation.application.get_main_window(automation)
t4 = time.perf_counter()
found = window.find_first_descendant(automation.cf.by_automation_id("SimpleCheckBox"))
t5 = time.perf_counter()
assert found is not None
print(json.dumps({"import": t1 - t0, "bridge": t2 - t1, "automation": t3 - t2, "attach": t4 - t3,
                  "first_find": t5 - t4, "in_process": t5 - t0}))
"""

COLD_CHILD_PYWINAUTO = r"""
import json, sys, time
t0 = time.perf_counter()
from pywinauto import Application
t1 = time.perf_counter()
app = Application(backend="uia").connect(handle=int(sys.argv[1]))
window = app.window(handle=int(sys.argv[1]))
window.wrapper_object()
t2 = time.perf_counter()
window.child_window(auto_id="SimpleCheckBox").wrapper_object()
t3 = time.perf_counter()
print(json.dumps({"import": t1 - t0, "attach": t2 - t1, "first_find": t3 - t2, "in_process": t3 - t0}))
"""

NOTES = {
    "snapshot": (
        "Every snapshot reads name, automation id, control type, bounding rectangle and enabled for "
        "every control-view descendant of the main window and builds Python tuples, which is what an "
        "agent serialises. 'wrapper' is find_all_descendants() plus Properties.*.value_or_default (one "
        "COM round trip per property); 'cached' activates a CacheRequest (TreeScope.Element) for those "
        "five properties, so FindAll returns them with each element; 'cached subtree' re-fetches the "
        "window under a TreeScope.Subtree request and walks CachedChildren, one UIA call for the whole "
        "tree. 'raw C#' makes the same calls on the FlaUI objects directly. 'pywinauto uia' is "
        "descendants() plus element_info reads; 'comtypes' uses pywinauto's IUIAutomation directly "
        "(FindAll then Current* reads, and FindAllBuildCache then Cached* reads)."
    ),
    "cold": (
        "Each run is a new Python process attaching to an already running app. 'import' is "
        "`import flaui` (loads pythonnet and pydantic), 'bridge' is setup_pythonnet_bridge() plus the "
        "first imports of C#-backed modules, 'process total' is measured by the parent and includes "
        "interpreter start-up and exit."
    ),
    "capture": (
        "Capture.element() returns a System.Drawing bitmap. 'PNG bytes' saves it to a MemoryStream "
        "and copies the array into a Python bytes object; there is no to-bytes helper in the wrapper "
        "yet, so this is what a caller writes today. 'PIL ImageGrab' grabs the same rectangle with "
        "Pillow and saves PNG to BytesIO, which is what pyautogui-based agents do."
    ),
    "scaling": (
        "find_all_descendants() with no condition on each list or grid, through the wrapper and raw "
        "C#. WPF virtualises its lists, so only realised rows exist in the UIA tree; the element "
        "count is what UIA reports, not the number of data rows."
    ),
}


def _wait_for(find: Callable[[], Any], what: str, timeout: float = 15.0) -> Any:
    """Call ``find`` until it returns something other than ``None``, untimed.

    :param find: Zero-argument lookup.
    :param what: Description used in the timeout error.
    :param timeout: Seconds to keep trying.
    :return: Whatever ``find`` returned.
    :raises RuntimeError: When nothing is found in time.
    """
    deadline = time.monotonic() + timeout
    while True:
        try:
            found = find()
            if found is not None:
                return found
        except Exception:  # pylint: disable=broad-exception-caught  # not ready yet
            pass
        if time.monotonic() > deadline:
            raise RuntimeError(f"{what} never appeared")
        time.sleep(0.25)


def _window_handle(window: Any) -> int:
    """Return the native handle of a wrapper window as an int.

    :param window: Wrapper ``Window``.
    :return: The HWND.
    """
    return int(window.raw_element.Properties.NativeWindowHandle.Value.ToInt64())


def _percentiles(samples: list[float]) -> Stats:
    """Return median and p95 of ``samples``.

    :param samples: Measurements in any unit.
    :return: ``{"median": ..., "p95": ...}`` in the same unit.
    """
    ordered = sorted(samples)
    return {"median": statistics.median(ordered), "p95": ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))]}


# --------------------------------------------------------------------------------------------- snapshot


def _wrapper_record(element: Any) -> Record:
    """Read the five snapshot properties through the wrapper.

    UIA2 does not support AutomationId on every element, so every read goes through
    ``value_or_default`` rather than the plain properties, which raise on unsupported ones.

    :param element: Wrapper ``AutomationElement``.
    :return: (name, automation id, control type, (x, y, w, h), enabled).
    """
    props = element.properties
    rect = props.bounding_rectangle.value_or_default
    return (
        props.name.value_or_default,
        props.automation_id.value_or_default,
        props.control_type.value_or_default,
        (rect.left, rect.top, rect.width, rect.height),
        props.is_enabled.value_or_default,
    )


def _raw_record(element: Any) -> Record:
    """Read the five snapshot properties straight off a C# element.

    :param element: Raw C# ``AutomationElement``.
    :return: (name, automation id, control type, (x, y, w, h), enabled).
    """
    props = element.Properties
    rect = props.BoundingRectangle.ValueOrDefault
    return (
        props.Name.ValueOrDefault,
        props.AutomationId.ValueOrDefault,
        props.ControlType.ValueOrDefault,
        (rect.X, rect.Y, rect.Width, rect.Height),
        props.IsEnabled.ValueOrDefault,
    )


def _cached_root(cs_window: Any) -> Any:
    """Re-fetch ``cs_window`` under the active cache request, so its subtree arrives in one call.

    :param cs_window: Raw C# window element.
    :return: Raw C# element whose ``CachedChildren`` hold the cached tree.
    """
    from FlaUI.Core.Conditions import TrueCondition  # pyright: ignore

    return cs_window.FindFirst(TreeScope.Element.value, TrueCondition.Default)


def _walk_cached(root: Any, children: Callable[[Any], Any], record: Callable[[Any], Record]) -> list[Record]:
    """Collect records for every cached descendant of ``root``, depth first.

    :param root: Element whose cached children to walk.
    :param children: Returns an element's cached children.
    :param record: Builds the record for one element.
    :return: One record per descendant.
    """
    records, stack = [], list(children(root))
    while stack:
        element = stack.pop()
        records.append(record(element))
        stack.extend(children(element))
    return records


def _cache_request(automation: Automation, scope: TreeScope) -> CacheRequest:
    """Build a CacheRequest for the five snapshot properties.

    :param automation: Automation the properties come from.
    :param scope: ``Element`` to cache each element a FindAll returns, ``Subtree`` to cache a
        whole tree under the element being fetched.
    :return: Configured, inactive cache request.
    """
    from FlaUI.Core.Conditions import PropertyCondition as CSPropertyCondition  # pyright: ignore

    library = automation.cs_automation.PropertyLibrary.Element
    request = CacheRequest()
    request.tree_scope = scope
    # FlaUI's CacheRequest filters on the raw view by default, which returns more elements than an
    # uncached FindAll (control view). Use the control view so every method walks the same tree.
    request.tree_filter = CSPropertyCondition(library.IsControlElement, True)
    for prop in (library.Name, library.AutomationId, library.ControlType, library.BoundingRectangle, library.IsEnabled):
        request.add_property(prop)
    return request


def _comtypes_walks(handle: int) -> dict[str, Callable[[], list[Record]]]:  # pylint: disable=too-many-locals
    """Build the pywinauto and raw-comtypes snapshot walks for the window ``handle``.

    :param handle: Native handle of the test app's main window.
    :return: ``{label: walk}``.
    """
    from pywinauto import Application as PywinautoApplication  # pylint: disable=import-outside-toplevel
    from pywinauto.uia_defines import IUIA  # pylint: disable=import-outside-toplevel

    # Connect by handle: top_window() enumerates every top-level window on the desktop, which blocks
    # for its full timeout when any window there stops responding.
    app = PywinautoApplication(backend="uia").connect(handle=handle)
    win = app.window(handle=handle).wrapper_object()
    iuia = IUIA()
    dll = iuia.UIA_dll
    root = win.element_info.element
    scope = iuia.tree_scope["descendants"]
    true_condition = iuia.true_condition
    prop_ids = [
        dll.UIA_NamePropertyId,
        dll.UIA_AutomationIdPropertyId,
        dll.UIA_ControlTypePropertyId,
        dll.UIA_BoundingRectanglePropertyId,
        dll.UIA_IsEnabledPropertyId,
    ]
    cache = iuia.iuia.CreateCacheRequest()
    for prop_id in prop_ids:
        cache.AddProperty(prop_id)

    def pywinauto_walk() -> list[Record]:
        """Walk with pywinauto ``descendants()``."""
        records = []
        for wrapper in win.descendants():
            info = wrapper.element_info
            r = info.rectangle
            records.append(
                (info.name, info.automation_id, info.control_type, (r.left, r.top, r.width(), r.height()), info.enabled)
            )
        return records

    def _rect(r: Any) -> tuple[int, int, int, int]:
        """Convert a UIA ``tagRECT`` to (x, y, w, h)."""
        return (r.left, r.top, r.right - r.left, r.bottom - r.top)

    def current_walk() -> list[Record]:
        """Walk with FindAll and per-element Current* reads (one COM call per property)."""
        found = root.FindAll(scope, true_condition)
        records = []
        for i in range(found.Length):
            e = found.GetElement(i)
            records.append(
                (
                    e.CurrentName,
                    e.CurrentAutomationId,
                    e.CurrentControlType,
                    _rect(e.CurrentBoundingRectangle),
                    bool(e.CurrentIsEnabled),
                )
            )
        return records

    def cached_walk() -> list[Record]:
        """Walk with FindAllBuildCache and Cached* reads."""
        found = root.FindAllBuildCache(scope, true_condition, cache)
        records = []
        for i in range(found.Length):
            e = found.GetElement(i)
            records.append(
                (
                    e.CachedName,
                    e.CachedAutomationId,
                    e.CachedControlType,
                    _rect(e.CachedBoundingRectangle),
                    bool(e.CachedIsEnabled),
                )
            )
        return records

    return {"pywinauto uia": pywinauto_walk, "comtypes Current*": current_walk, "comtypes cached": cached_walk}


def run_snapshot(  # pylint: disable=too-many-locals
    automation: Automation, window: Any, iterations: int, with_pywinauto: bool
) -> dict[str, Any]:
    """Time full accessibility-tree snapshots of ``window``.

    :param automation: Automation that owns ``window``.
    :param window: Wrapper main window.
    :param iterations: Timed snapshots per method.
    :param with_pywinauto: Also time the pywinauto and comtypes walks.
    :return: ``{method: {"elements": n, "stats": ms stats, "ms_per_element": float}}``.
    """
    per_element = _cache_request(automation, TreeScope.Element)
    subtree = _cache_request(automation, TreeScope.Subtree)
    cs_window = window.raw_element

    def wrapper_cached() -> list[Record]:
        """FindAll with a per-element CacheRequest active, wrapper reads."""
        with per_element.activate():
            return [_wrapper_record(e) for e in window.find_all_descendants()]

    def wrapper_subtree() -> list[Record]:
        """One cached fetch of the whole tree, wrapper reads over cached_children."""
        with subtree.activate():
            root = AutomationElement(raw_element=_cached_root(cs_window))
            return _walk_cached(
                root, lambda e: [AutomationElement(raw_element=c) for c in e.cached_children], _wrapper_record
            )

    def raw_cached() -> list[Record]:
        """FindAll with a per-element CacheRequest active, raw C# reads."""
        with per_element.activate():
            return [_raw_record(e) for e in cs_window.FindAllDescendants()]

    def raw_subtree() -> list[Record]:
        """One cached fetch of the whole tree, raw C# reads over CachedChildren."""
        with subtree.activate():
            return _walk_cached(_cached_root(cs_window), lambda e: e.CachedChildren, _raw_record)

    walks: dict[str, Callable[[], list[Record]]] = {
        "wrapper": lambda: [_wrapper_record(e) for e in window.find_all_descendants()],
        "wrapper cached": wrapper_cached,
        "wrapper cached subtree": wrapper_subtree,
        "raw C#": lambda: [_raw_record(e) for e in cs_window.FindAllDescendants()],
        "raw C# cached": raw_cached,
        "raw C# cached subtree": raw_subtree,
    }
    if with_pywinauto:
        walks.update(_comtypes_walks(_window_handle(window)))
    results = {}
    for label, walk in walks.items():
        gc.collect()
        count = len(walk())
        stats = _time(walk, iterations, warmup=1)
        results[label] = {"elements": count, "stats": stats, "ms_per_element": stats["median"] / max(count, 1)}
    return results


# ------------------------------------------------------------------------------------------- cold start


def run_cold(  # pylint: disable=too-many-locals
    uia: UIAutomationTypes, pid: int, handle: int, runs: int, with_pywinauto: bool
) -> dict[str, Stats]:
    """Time fresh processes that attach to ``pid`` and run a first find.

    :param uia: UIA2 or UIA3.
    :param pid: Process id of the running test app.
    :param handle: Native handle of its main window (pywinauto connects by handle).
    :param runs: Number of fresh processes.
    :param with_pywinauto: Also time a pywinauto cold start (once per app, under UIA3).
    :return: ``{tool: {phase: {"median": ms, "p95": ms}}}``.
    """
    jobs = {
        "bare python": [sys.executable, "-c", 'print("{}")'],
        "flaui": [sys.executable, "-c", COLD_CHILD, uia.name, str(pid), str(REPO)],
    }
    if with_pywinauto and uia == UIAutomationTypes.UIA3:
        jobs["pywinauto uia"] = [sys.executable, "-c", COLD_CHILD_PYWINAUTO, str(handle)]
    results: dict[str, Any] = {}
    for tool, cmd in jobs.items():
        phases: dict[str, list[float]] = {}
        for _ in range(runs):
            start = time.perf_counter()
            out = subprocess.run(cmd, capture_output=True, text=True, check=False, cwd=REPO)  # nosec B603
            if out.returncode:
                raise RuntimeError(f"{tool} cold-start child failed:\n{out.stderr}")
            total = time.perf_counter() - start
            sample = json.loads(out.stdout.strip().splitlines()[-1])
            sample["process total"] = total
            for phase, seconds in sample.items():
                phases.setdefault(phase, []).append(seconds * 1000)
        results[tool] = {phase: _percentiles(values) for phase, values in phases.items()}
    return results


# ---------------------------------------------------------------------------------------------- capture


def _png_bytes(image: Any) -> bytes:
    """Encode a wrapper ``CaptureImage`` to PNG bytes in memory.

    :param image: Wrapper ``CaptureImage``.
    :return: PNG file contents.
    """
    from System.Drawing.Imaging import ImageFormat  # pyright: ignore
    from System.IO import MemoryStream  # pyright: ignore

    stream = MemoryStream()
    try:
        image.bitmap.Save(stream, ImageFormat.Png)
        return bytes(stream.ToArray())
    finally:
        stream.Dispose()


def run_capture(window: Any, element: Any, iterations: int) -> dict[str, Any]:
    """Time window and element screenshots, with and without PNG encoding.

    :param window: Wrapper main window.
    :param element: A small wrapper element on screen.
    :param iterations: Timed runs per operation.
    :return: ``{operation: {"stats": ms stats, "png_bytes": size, "pixels": "WxH"}}``.
    """
    results: dict[str, Any] = {}
    for target_name, target in (("window", window), ("element", element)):

        def grab(t: Any = target) -> None:
            """Capture and dispose."""
            Capture.element(t).dispose()

        def grab_png(t: Any = target) -> bytes:
            """Capture, encode to PNG bytes, dispose."""
            with Capture.element(t) as image:
                return _png_bytes(image)

        png = grab_png()
        rect = target.bounding_rectangle
        size = {"png_bytes": len(png), "pixels": f"{rect.width}x{rect.height}"}
        gc.collect()
        results[f"{target_name}: capture"] = {"stats": _time(grab, iterations), **size}
        results[f"{target_name}: capture + PNG bytes"] = {"stats": _time(grab_png, iterations), **size}
        if HAVE_PIL:
            bbox = (rect.left, rect.top, rect.right, rect.bottom)

            def pil_png(b: tuple[int, int, int, int] = bbox) -> bytes:
                """Grab with Pillow and encode to PNG bytes."""
                buffer = io.BytesIO()
                ImageGrab.grab(bbox=b, all_screens=True).save(buffer, format="PNG")
                return buffer.getvalue()

            results[f"{target_name}: PIL ImageGrab + PNG"] = {
                "stats": _time(pil_png, iterations),
                "png_bytes": len(pil_png()),
                "pixels": size["pixels"],
            }
    return results


# ---------------------------------------------------------------------------------------------- scaling

SCALING_TARGETS = (
    ("Complex Controls", "LargeListView"),
    ("Complex Controls", "dataGridView"),
    ("More Controls", "LargeListBox"),
)


def run_scaling(automation: Automation, window: Any, iterations: int) -> dict[str, Any]:
    """Time ``find_all_descendants`` on the largest lists and grids in the app.

    :param automation: Automation that owns ``window``.
    :param window: Wrapper main window.
    :param iterations: Timed runs per control.
    :return: ``{control: {"elements": n, "python": stats, "csharp": stats}}``; controls that are
        not exposed on this combo map to ``{"skipped": reason}``.
    """
    cf = automation.cf
    results: dict[str, Any] = {}
    for tab_name, automation_id in SCALING_TARGETS:
        try:
            tab_item = window.find_first_descendant(cf.by_name(tab_name))
        except ElementNotFound:
            results[automation_id] = {"skipped": f"tab '{tab_name}' not exposed"}
            continue
        tab_item.as_tab_item().select()
        try:
            control = _wait_for(
                lambda a=automation_id: window.find_first_descendant(cf.by_automation_id(a)), automation_id, 5
            )
        except RuntimeError:
            results[automation_id] = {"skipped": "control not found"}
            continue
        cs_control = control.raw_element
        count = len(control.find_all_descendants())
        gc.collect()
        results[automation_id] = {
            "elements": count,
            "python": _time(control.find_all_descendants, iterations),
            "csharp": _time(lambda c=cs_control: list(c.FindAllDescendants()), iterations),
        }
    return results


# ------------------------------------------------------------------------------------------ reliability


def run_reliability(automation: Automation, window: Any, cycles: int) -> dict[str, Any]:
    """Find the checkbox from the window and toggle it ``cycles`` times, verifying each toggle.

    :param automation: Automation that owns ``window``.
    :param window: Wrapper main window.
    :param cycles: Number of find-plus-toggle cycles.
    :return: Success count, rate, cycle latency and the first few errors.
    """
    by_id = automation.cf.by_automation_id("SimpleCheckBox")
    samples, errors, ok = [], [], 0
    for _ in range(cycles):
        start = time.perf_counter()
        try:
            checkbox = window.find_first_descendant(by_id).as_check_box()
            before = checkbox.toggle_state
            checkbox.toggle()
            after = checkbox.toggle_state
            if after != before and after in (ToggleState.On, ToggleState.Off, ToggleState.Indeterminate):
                ok += 1
            else:
                errors.append(f"state stayed {before}")
        except Exception as exc:  # pylint: disable=broad-exception-caught  # counting failures is the point
            errors.append(repr(exc))
        samples.append((time.perf_counter() - start) * 1000)
    return {
        "cycles": cycles,
        "ok": ok,
        "success_rate": ok / cycles,
        "stats": _percentiles(samples),
        "errors": errors[:5],
    }


# ------------------------------------------------------------------------------------------------- main


def run_combo(uia: UIAutomationTypes, app_name: str, args: argparse.Namespace) -> dict[str, Any]:
    """Run the selected in-process sections for one combo.

    :param uia: UIA2 or UIA3.
    :param app_name: Key of :data:`benchmark.APPS`.
    :param args: Parsed command line.
    :return: ``{section: results}``.
    """
    automation = Automation(uia)
    automation.application.launch(str(APPS[app_name].resolve()))
    try:
        window = automation.application.get_main_window(automation)
        by_id = automation.cf.by_automation_id("SimpleCheckBox")
        checkbox = _wait_for(lambda: window.find_first_descendant(by_id), "SimpleCheckBox")
        time.sleep(1)  # let the window finish painting before snapshots and screenshots
        results: dict[str, Any] = {}
        if "snapshot" in args.sections:
            results["snapshot"] = run_snapshot(
                automation, window, args.iterations, HAVE_PYWINAUTO and not args.skip_pywinauto
            )
        if "cold" in args.sections:
            results["cold"] = run_cold(
                uia,
                automation.application.process_id,
                _window_handle(window),
                args.cold_runs,
                HAVE_PYWINAUTO and not args.skip_pywinauto,
            )
        if "capture" in args.sections:
            results["capture"] = run_capture(window, checkbox, args.iterations)
        if "reliability" in args.sections:
            results["reliability"] = run_reliability(automation, window, args.cycles)
        if "scaling" in args.sections:  # last: it switches tabs
            results["scaling"] = run_scaling(automation, window, args.iterations)
        return results
    finally:
        automation.application.kill()
        automation.application.dispose()
        time.sleep(0.5)


def _print_combo(combo: str, results: dict[str, Any]) -> None:
    """Print one combo's results.

    :param combo: ``UIA3_WPF`` style label.
    :param results: Output of :func:`run_combo`.
    """
    for label, r in results.get("snapshot", {}).items():
        s = r["stats"]
        print(
            f"{combo:<15} snapshot {label:<26} {r['elements']:>6} el {s['median']:>9.1f} {s['p95']:>9.1f}   {r['ms_per_element']:.3f} ms/el"
        )
    for tool, phases in results.get("cold", {}).items():
        for phase, s in phases.items():
            print(f"{combo:<15} cold {tool:<13} {phase:<16} {'':>9} {s['median']:>9.1f} {s['p95']:>9.1f}")
    for label, r in results.get("capture", {}).items():
        s = r["stats"]
        print(
            f"{combo:<15} capture {label:<34} {s['median']:>9.1f} {s['p95']:>9.1f}   {r['pixels']}, {r['png_bytes'] / 1024:.0f} KiB"
        )
    for control, r in results.get("scaling", {}).items():
        if "skipped" in r:
            print(f"{combo:<15} scaling {control:<20} skipped: {r['skipped']}")
            continue
        py, cs = r["python"], r["csharp"]
        print(
            f"{combo:<15} scaling {control:<20} {r['elements']:>6} el {py['median']:>9.1f} {py['p95']:>9.1f}"
            f"   raw C# {cs['median']:.1f} / {cs['p95']:.1f}"
        )
    if "reliability" in results:
        r = results["reliability"]
        s = r["stats"]
        print(
            f"{combo:<15} reliability {r['ok']}/{r['cycles']} ok ({r['success_rate']:.1%}) "
            f"{s['median']:>9.1f} {s['p95']:>9.1f}"
        )
        for error in r["errors"]:
            print(f"{'':<15}   error: {error}")


def main() -> int:
    """Run every combination, print tables and optionally write JSON.

    :return: Process exit code; 1 when any reliability cycle failed.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-n", "--iterations", type=int, default=10, help="Timed runs per snapshot/capture/scaling op")
    parser.add_argument("--cold-runs", type=int, default=10, help="Fresh processes per cold-start combo")
    parser.add_argument("--cycles", type=int, default=500, help="Find-plus-toggle cycles per combo")
    parser.add_argument("--sections", nargs="+", choices=SECTIONS, default=list(SECTIONS))
    parser.add_argument("--skip-pywinauto", action="store_true", help="Do not run the pywinauto/comtypes comparisons")
    parser.add_argument("--json", type=Path, help="Write raw results to this file")
    args = parser.parse_args()

    print(
        f"Python {platform.python_version()} on {platform.platform()}; {args.iterations} iterations, "
        f"{args.cold_runs} cold runs, {args.cycles} reliability cycles; "
        f"pywinauto {'on' if HAVE_PYWINAUTO and not args.skip_pywinauto else 'off'}, PIL {'on' if HAVE_PIL else 'off'}\n"
    )
    print(f"{'combo':<15} {'workload':<45} {'median':>9} {'p95':>9}   (ms)")
    all_results: dict[str, Any] = {}
    failed = False
    for uia in (UIAutomationTypes.UIA2, UIAutomationTypes.UIA3):
        for app_name in APPS:
            combo = f"{uia.name}_{app_name}"
            results = run_combo(uia, app_name, args)
            all_results[combo] = results
            _print_combo(combo, results)
            if results.get("reliability", {}).get("success_rate", 1.0) < 1.0:
                failed = True
            print()
    for section in args.sections:
        if section in NOTES:
            print(f"Note ({section}): {NOTES[section]}\n")
    if args.json:
        args.json.write_text(json.dumps(all_results, indent=2, default=str))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
