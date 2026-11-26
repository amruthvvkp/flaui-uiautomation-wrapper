"""Compare the wrapper's find and action latency with pywinauto on the bundled test applications.

Backs the "Compare with pywinauto" item of GH-85. Runs the operations from ``scripts/benchmark.py``
on the same WinForms and WPF test apps through:

- the FlaUI wrapper on UIA2 and UIA3 (``benchmark.run_combo``, wrapper side only);
- pywinauto's ``uia`` backend, written the way pywinauto documents it
  (``window.child_window(...).wrapper_object()``, wrapper methods);
- raw UIA ``FindFirst`` through pywinauto's own comtypes ``IUIAutomation`` object, for the two
  descendant searches only, to separate pywinauto's search strategy from the cost of COM itself;
- pywinauto's ``win32`` backend, on WinForms only (WPF controls have no window handles).

The operations are equivalent in intent, not identical in mechanism. Where they differ, the label
says so and ``NOTES`` explains it; the notes are printed under the table.

pywinauto is an optional benchmark dependency (``bench`` group)::

    uv run --group bench python scripts/benchmark_pywinauto.py              # 50 iterations
    uv run --group bench python scripts/benchmark_pywinauto.py -n 200 --json pywinauto.json
    uv run --group bench python scripts/benchmark_pywinauto.py --skip-flaui # pywinauto only

The script needs an interactive desktop: it launches the test apps and clicks controls.
"""

from __future__ import annotations

import argparse
import gc
import itertools
import json
from pathlib import Path
import platform
import sys
import time
from typing import Any, Callable

# pywinauto picks its COM apartment at import time, so import it before the CLR starts.
try:
    import pywinauto
    from pywinauto import Application
    from pywinauto.uia_defines import IUIA
except ImportError:  # pragma: no cover - depends on the optional bench group
    raise SystemExit(
        "pywinauto is not installed. Run: uv run --group bench python scripts/benchmark_pywinauto.py"
    ) from None

sys.path.insert(0, str(Path(__file__).resolve().parent))

# isort: off
# Importing benchmark also sets up the PythonNet bridge.
from benchmark import APPS, _time, run_combo  # noqa: E402  # pylint: disable=wrong-import-position
from flaui.lib.enums import UIAutomationTypes  # noqa: E402  # pylint: disable=wrong-import-position

# isort: on

Stats = dict[str, float]

# On WPF the button's text child is also named "BigButton". FlaUI's FindFirst returns the first match
# (the button); pywinauto insists on a unique match, so it is also given the control type.
BY_NAME = {"title": "BigButton", "control_type": "Button"}

NOTES = {
    "find": (
        "pywinauto child_window(...).wrapper_object() re-resolves the window spec, fetches every "
        "descendant with one cached FindAll, then filters in Python (auto_id is always filtered in "
        "Python) and checks the match is unique. FlaUI find_first_descendant sends one FindFirst with "
        "the condition to UIA, which stops at the first match. 'uia FindFirst' is that same FindFirst "
        "call made through pywinauto's comtypes IUIAutomation. The by-name search also passes "
        "control_type='Button' to pywinauto, which goes into its FindAll condition, because on WPF the "
        "button's text child has the same name and pywinauto rejects ambiguous matches."
    ),
    "win32": (
        "win32 backend: WinForms only. It has no AutomationId (control ids are assigned at runtime), so "
        "the by-id search is skipped; 'select radio' and 'toggle checkbox' send BM_SETCHECK and wait "
        "for the GUI thread to go idle instead of calling a UIA pattern."
    ),
    "click": (
        "Mouse clicks: both libraries move the real cursor and send input. Before every click, pywinauto "
        "click_input() waits until the system double-click time (500 ms by default) has passed since the "
        "last input of any kind, then sleeps Timings.after_clickinput_wait (90 ms) after it. FlaUI click() "
        "waits for input to be processed and only waits out the double-click time when the same spot is "
        "clicked twice in a row. Back-to-back clicks therefore show pywinauto's full guard; in a test with "
        "other work between clicks it costs less."
    ),
}


def _wait_for(find: Callable[[], Any], what: str, timeout: float = 15.0) -> Any:
    """Call ``find`` until it returns without raising, untimed.

    :param find: Zero-argument lookup that raises (or returns ``None``) until the control exists.
    :param what: Description used in the timeout error.
    :param timeout: Seconds to keep trying.
    :return: Whatever ``find`` returned.
    :raises RuntimeError: When the control does not appear in time.
    """
    deadline = time.monotonic() + timeout
    error: Exception | None = None
    while True:
        try:
            found = find()
            if found is not None:
                return found
        except Exception as exc:  # pylint: disable=broad-exception-caught  # pywinauto raises several types
            error = exc
        if time.monotonic() > deadline:
            raise RuntimeError(f"{what} never appeared (last error: {error!r})")
        time.sleep(0.25)


def _uia_find_first(element_info: Any, property_name: str, value: str) -> Callable[[], Any]:
    """Build a raw UIA ``FindFirst(TreeScope_Descendants, ...)`` call through pywinauto's comtypes.

    :param element_info: pywinauto ``UIAElementInfo`` of the search root.
    :param property_name: ``"AutomationId"`` or ``"Name"``.
    :param value: Property value to match.
    :return: Zero-argument callable that runs the search and returns the raw COM element.
    """
    iuia = IUIA()
    prop_id = getattr(iuia.UIA_dll, f"UIA_{property_name}PropertyId")
    condition = iuia.iuia.CreatePropertyCondition(prop_id, value)
    scope = iuia.tree_scope["descendants"]
    root = element_info.element
    return lambda: root.FindFirst(scope, condition)


def run_pywinauto(app_name: str, iterations: int) -> dict[str, dict[str, Stats]]:  # pylint: disable=too-many-locals
    """Benchmark pywinauto against one test application.

    :param app_name: Key of :data:`benchmark.APPS`.
    :param iterations: Timed runs per operation.
    :return: ``{operation: {tool: stats}}``; tools are ``pywinauto uia``, ``uia FindFirst`` and
        ``pywinauto win32``.
    """
    app = Application(backend="uia").start(f'"{APPS[app_name].resolve()}"')
    try:
        spec = _wait_for(app.top_window, "main window")
        win = spec.wrapper_object()
        # The window appears before its controls are ready; wait for every control untimed.
        checkbox = _wait_for(lambda: spec.child_window(auto_id="SimpleCheckBox").wrapper_object(), "SimpleCheckBox")
        radio = _wait_for(lambda: spec.child_window(auto_id="RadioButton1").wrapper_object(), "RadioButton1")
        button = _wait_for(lambda: spec.child_window(**BY_NAME).wrapper_object(), "BigButton")

        uia_targets = itertools.cycle((checkbox, radio))
        ops: dict[str, dict[str, Callable[[], Any]]] = {
            "find: descendant by automation id": {
                "pywinauto uia": lambda: spec.child_window(auto_id="SimpleCheckBox").wrapper_object(),
                "uia FindFirst": _uia_find_first(win.element_info, "AutomationId", "SimpleCheckBox"),
            },
            "find: descendant by name": {
                "pywinauto uia": lambda: spec.child_window(**BY_NAME).wrapper_object(),
                "uia FindFirst": _uia_find_first(win.element_info, "Name", "BigButton"),
            },
            "find: all children": {"pywinauto uia": win.children},
            "action: read name property": {"pywinauto uia": button.window_text},
            "action: select radio button": {"pywinauto uia": radio.select},
            "action: toggle checkbox": {"pywinauto uia": checkbox.toggle},
            "action: mouse click (alternating)": {
                "pywinauto uia": lambda: next(uia_targets).click_input(),
            },
        }

        if app_name == "WinForms":
            w32 = Application(backend="win32").connect(process=app.process)
            w32_spec = w32.window(handle=win.handle)
            w32_win = w32_spec.wrapper_object()
            w32_checkbox = w32_spec.child_window(handle=checkbox.handle).wrapper_object()
            w32_radio = w32_spec.child_window(handle=radio.handle).wrapper_object()
            w32_button = w32_spec.child_window(title="BigButton").wrapper_object()
            checks = itertools.cycle((w32_checkbox.uncheck, w32_checkbox.check))
            w32_targets = itertools.cycle((w32_checkbox, w32_radio))
            w32_ops = {
                "find: descendant by name": lambda: w32_spec.child_window(title="BigButton").wrapper_object(),
                "find: all children": w32_win.children,
                "action: read name property": w32_button.window_text,
                "action: select radio button": w32_radio.check,
                "action: toggle checkbox": lambda: next(checks)(),  # pylint: disable=unnecessary-lambda
                "action: mouse click (alternating)": lambda: next(w32_targets).click_input(),
            }
            for label, fn in w32_ops.items():
                ops[label]["pywinauto win32"] = fn

        results: dict[str, dict[str, Stats]] = {}
        for label, tools in ops.items():
            results[label] = {}
            for tool, fn in tools.items():
                gc.collect()
                results[label][tool] = _time(fn, iterations)
        return results
    finally:
        app.kill()
        time.sleep(0.5)


def main() -> int:
    """Run FlaUI and pywinauto on both apps, print median and p95 per tool and optionally write JSON.

    :return: Process exit code; always 0, as this script only reports.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-n", "--iterations", type=int, default=50)
    parser.add_argument("--json", type=Path, help="Write raw results to this file")
    parser.add_argument("--skip-flaui", action="store_true", help="Only run pywinauto")
    args = parser.parse_args()

    print(
        f"Python {platform.python_version()} on {platform.platform()}, pywinauto {pywinauto.__version__}, "
        f"{args.iterations} iterations\n"
    )
    all_results: dict[str, dict[str, dict[str, Stats]]] = {}
    for app_name in APPS:
        per_op: dict[str, dict[str, Stats]] = {}
        if not args.skip_flaui:
            for uia in (UIAutomationTypes.UIA2, UIAutomationTypes.UIA3):
                for label, stats in run_combo(uia, app_name, args.iterations).items():
                    per_op.setdefault(label, {})[f"FlaUI {uia.name}"] = stats["python"]
        for label, tools in run_pywinauto(app_name, args.iterations).items():
            per_op.setdefault(label, {}).update(tools)
        all_results[app_name] = per_op

    header = f"{'app':<9} {'operation':<36} {'tool':<16} {'median':>8} {'p95':>8}"
    print(header)
    print("-" * len(header))
    for app_name, per_op in all_results.items():
        for label, tools in per_op.items():
            for tool, stats in tools.items():
                print(f"{app_name:<9} {label:<36} {tool:<16} {stats['median']:>8.2f} {stats['p95']:>8.2f}")
        print()
    print("All times in ms. Where the operations differ:")
    for note in NOTES.values():
        print(f"- {note}")
    if args.json:
        args.json.write_text(json.dumps(all_results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
