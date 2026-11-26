"""Measure element-finding and action latency against the bundled test applications.

Backs the "Element finding" and "Action execution" rows of the v1.0 success metrics in
``ROADMAP.md`` (GH-85). Each operation runs on all four UIA2/UIA3 x WinForms/WPF combinations and
is timed through the Python wrapper and, for comparison, through the raw C# object it wraps, so the
PythonNet/Pydantic overhead is visible on its own.

Usage::

    uv run python scripts/benchmark.py              # 50 iterations per operation
    uv run python scripts/benchmark.py -n 200 --json results.json

The script needs an interactive desktop: it launches the test apps and clicks a checkbox.
"""

from __future__ import annotations

import argparse
import gc
import itertools
import json
from pathlib import Path
import platform
import statistics
import sys
import time
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge  # noqa: E402

# isort: off
setup_pythonnet_bridge()

from flaui.lib.enums import UIAutomationTypes  # noqa: E402
from flaui.modules.automation import Automation  # noqa: E402

# isort: on

APPS = {
    "WinForms": Path("test_applications/WinFormsApplication/WinFormsApplication.exe"),
    "WPF": Path("test_applications/WPFApplication/WpfApplication.exe"),
}
# Absolute latency is dominated by Windows UIA and the target app's provider, so it is reported for
# reference only. The gate is what this wrapper adds on top of calling FlaUI C# directly.
FIND_TARGET_MS = 100.0
ACTION_TARGET_MS = 50.0
OVERHEAD_TARGET_MS = 5.0


def _time(fn: Callable[[], Any], iterations: int, warmup: int = 3) -> dict[str, float]:
    """Run ``fn`` repeatedly and return latency statistics in milliseconds.

    :param fn: Zero-argument callable to time.
    :param iterations: Number of timed runs.
    :param warmup: Untimed runs first, so JIT and COM proxy setup are not counted.
    :return: Mean, median, p95, min and max in milliseconds.
    """
    for _ in range(warmup):
        fn()
    samples = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - start) * 1000)
    samples.sort()
    return {
        "mean": statistics.fmean(samples),
        "median": statistics.median(samples),
        "p95": samples[min(len(samples) - 1, int(len(samples) * 0.95))],
        "min": samples[0],
        "max": samples[-1],
    }


def run_combo(uia: UIAutomationTypes, app_name: str, iterations: int) -> dict[str, dict[str, dict[str, float]]]:
    """Benchmark one UIA type against one test application.

    :param uia: UIA2 or UIA3.
    :param app_name: Key of :data:`APPS`.
    :param iterations: Timed runs per operation.
    :return: ``{operation: {"python": stats, "csharp": stats}}``.
    """
    automation = Automation(uia)
    automation.application.launch(str(APPS[app_name].resolve()))
    try:
        automation.application.wait_while_main_handle_is_missing(5000)
        window = automation.application.get_main_window(automation)
        cf = automation.cf
        cs_window = window.raw_element
        cs_cf = cf.raw_cf if hasattr(cf, "raw_cf") else automation.cs_automation.ConditionFactory

        # Simple Controls is the default tab in both apps, so these controls are on screen.
        # Both controls exist in both apps (WinForms has no "InvokableButton").
        by_id = cf.by_automation_id("SimpleCheckBox")
        by_name = cf.by_name("BigButton")
        cs_by_id = cs_cf.ByAutomationId("SimpleCheckBox")
        cs_by_name = cs_cf.ByName("BigButton")

        # The window handle appears before the controls finish loading; wait for them untimed.
        deadline = time.monotonic() + 15
        while cs_window.FindFirstDescendant(cs_by_id) is None or cs_window.FindFirstDescendant(cs_by_name) is None:
            if time.monotonic() > deadline:
                raise RuntimeError(f"{uia.name}_{app_name}: benchmark controls never appeared")
            time.sleep(0.25)
        checkbox = window.find_first_descendant(by_id).as_check_box()
        button = window.find_first_descendant(by_name).as_button()
        radio = window.find_first_descendant(cf.by_automation_id("RadioButton1")).as_radio_button()
        cs_button = button.raw_element
        cs_radio = radio.raw_element
        cs_checkbox = checkbox.raw_element

        ops: dict[str, tuple[Callable[[], Any], Callable[[], Any]]] = {
            "find: descendant by automation id": (
                lambda: window.find_first_descendant(by_id),
                lambda: cs_window.FindFirstDescendant(cs_by_id),
            ),
            "find: descendant by name": (
                lambda: window.find_first_descendant(by_name),
                lambda: cs_window.FindFirstDescendant(cs_by_name),
            ),
            "find: all children": (
                lambda: window.find_all_children(),
                lambda: list(cs_window.FindAllChildren()),
            ),
            "action: read name property": (lambda: button.name, lambda: cs_button.Name),
            "action: select radio button": (
                lambda: setattr(radio, "is_checked", True),
                lambda: setattr(cs_radio, "IsChecked", True),
            ),
            "action: toggle checkbox": (lambda: checkbox.toggle(), lambda: cs_checkbox.Toggle()),
            # Alternate targets: FlaUI's Mouse.Click sleeps out the system double-click time when a click
            # lands on the same spot as the previous one, so clicking one control in a loop measures that guard.
            "action: mouse click (alternating)": (
                lambda py=itertools.cycle((checkbox, radio)): next(py).click(),
                lambda cs=itertools.cycle((cs_checkbox, cs_radio)): next(cs).Click(False),
            ),
        }
        results = {}
        for label, (py_fn, cs_fn) in ops.items():
            gc.collect()
            results[label] = {"python": _time(py_fn, iterations), "csharp": _time(cs_fn, iterations)}
        return results
    finally:
        automation.application.kill()
        automation.application.dispose()
        time.sleep(0.5)


def main() -> int:
    """Run every combination, print a table and optionally write JSON.

    :return: Process exit code; 1 when the wrapper's overhead on any operation misses its target.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-n", "--iterations", type=int, default=50)
    parser.add_argument("--json", type=Path, help="Write raw results to this file")
    args = parser.parse_args()

    all_results: dict[str, Any] = {}
    failed = False
    print(f"Python {platform.python_version()} on {platform.platform()}, {args.iterations} iterations\n")
    header = f"{'combo':<15} {'operation':<36} {'py mean':>8} {'py p95':>8} {'cs mean':>8} {'overhead':>9}"
    print(header)
    print("-" * len(header))
    for uia in (UIAutomationTypes.UIA2, UIAutomationTypes.UIA3):
        for app_name in APPS:
            combo = f"{uia.name}_{app_name}"
            results = run_combo(uia, app_name, args.iterations)
            all_results[combo] = results
            for label, stats in results.items():
                py, cs = stats["python"], stats["csharp"]
                target = FIND_TARGET_MS if label.startswith("find") else ACTION_TARGET_MS
                overhead = py["mean"] - cs["mean"]
                note = ""
                if overhead >= OVERHEAD_TARGET_MS:
                    note, failed = "  OVERHEAD MISS", True
                elif py["mean"] >= target:
                    note = "  slow in FlaUI/UIA"
                print(
                    f"{combo:<15} {label:<36} {py['mean']:>8.2f} {py['p95']:>8.2f} "
                    f"{cs['mean']:>8.2f} {overhead:>+9.2f}{note}"
                )
    print(
        f"\nGate: wrapper overhead < {OVERHEAD_TARGET_MS:.0f} ms mean per operation. Reference: find < "
        f"{FIND_TARGET_MS:.0f} ms, action < {ACTION_TARGET_MS:.0f} ms mean (all times ms)"
    )
    if args.json:
        args.json.write_text(json.dumps(all_results, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
