"""Measure what element name maps (page objects) add over a direct wrapper find.

Compares, for the "TextBox" control on the Simple Controls tab of both bundled test apps:

* **direct**: ``window.find_first_descendant(cf.by_automation_id("TextBox"))``, the plain wrapper call;
* **suite path inlined**: the exact lookups the test-suite map performs (find the tab, resolve the
  tab item, check it is selected, find the child), written out without any map classes;
* **suite map**: ``elements.simple_controls_tab.test_text_box`` from ``tests/test_utilities/elements``;
* **docs map**: ``app.simple.name_box`` from ``examples/pytest/app_map.py`` (the documented recipe);
* the cost of constructing each map's page class alone, which is pure Python.

``inlined - direct`` is the cost of the extra UIA lookups the map path does; ``map - inlined`` is the
cost of the map classes themselves.

Usage::

    uv run python scripts/benchmark_name_map.py -n 100
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "examples" / "pytest")]

from benchmark import APPS, _time  # noqa: E402  (also sets up the PythonNet bridge)

# isort: off
from flaui.core.definitions import ControlType  # noqa: E402
from flaui.lib.enums import UIAutomationTypes  # noqa: E402
from flaui.modules.automation import Automation  # noqa: E402
from app_map import SimpleControlsPage, TestAppMap  # noqa: E402
from tests.test_utilities.elements.winforms_application import get_winforms_application_elements  # noqa: E402
from tests.test_utilities.elements.winforms_application.simple_controls import (  # noqa: E402
    SimpleControlsElements as WinFormsSimpleControls,
)
from tests.test_utilities.elements.wpf_application import get_wpf_application_elements  # noqa: E402
from tests.test_utilities.elements.wpf_application.simple_controls import (  # noqa: E402
    SimpleControlsElements as WPFSimpleControls,
)

# isort: on


def run_combo(uia: UIAutomationTypes, app_name: str, iterations: int) -> dict[str, dict[str, float] | None]:
    """Time every lookup style against one UIA type and test app.

    :param uia: UIA2 or UIA3.
    :param app_name: Key of ``benchmark.APPS``.
    :param iterations: Timed runs per operation.
    :return: ``{operation: stats}``; ``None`` when that style does not work on this app.
    """
    automation = Automation(uia)
    automation.application.launch(str(APPS[app_name].resolve()))
    try:
        automation.application.wait_while_main_handle_is_missing(5000)
        window = automation.application.get_main_window(automation)
        deadline = time.monotonic() + 15
        while window.raw_element.FindFirstDescendant(window.condition_factory.raw_cf.ByAutomationId("TextBox")) is None:
            if time.monotonic() > deadline:
                raise RuntimeError(f"{uia.name}_{app_name}: TextBox never appeared")
            time.sleep(0.25)

        if app_name == "WPF":
            suite = get_wpf_application_elements(window)
            page_cls: Any = WPFSimpleControls

            def suite_inlined() -> Any:
                """Do the WPF suite map's lookups without its classes."""
                cf = window.condition_factory
                tab = window.find_first_descendant(cf.by_control_type(ControlType.Tab)).as_tab()
                item = tab.find_first_child(cf.by_name("Simple Controls")).as_tab_item()
                _ = item.is_selected
                return item.find_first_child(cf.by_automation_id("TextBox")).as_text_box()

        else:
            suite = get_winforms_application_elements(window)
            page_cls = WinFormsSimpleControls

            def suite_inlined() -> Any:
                """Do the WinForms suite map's lookups without its classes."""
                cf = window.condition_factory
                tab = window.find_first_descendant(cf.by_control_type(ControlType.Tab)).as_tab()
                _ = tab.selected_tab_item_index
                item = tab.tab_items[0]
                return item.find_first_child(cf.by_automation_id("TextBox")).as_text_box()

        tab = suite.tab
        docs = TestAppMap(window=window)
        ops: dict[str, Callable[[], Any]] = {
            "direct wrapper find": lambda: window.find_first_descendant(
                window.condition_factory.by_automation_id("TextBox")
            ).as_text_box(),
            "suite path inlined (no map classes)": suite_inlined,
            "suite map: simple_controls_tab.test_text_box": lambda: suite.simple_controls_tab.test_text_box,
            "suite map: build page class only": lambda: page_cls(main_window=window, tab=tab),
            "docs map: app.simple.name_box": lambda: docs.simple.name_box,
            "docs map: build page class only": lambda: SimpleControlsPage(window=window),
        }
        results: dict[str, dict[str, float] | None] = {}
        for label, fn in ops.items():
            try:
                assert label.endswith("only") or fn().automation_id == "TextBox"
                results[label] = _time(fn, iterations)
            except Exception as error:  # a map written for one app may not fit the other
                print(f"  {uia.name}_{app_name}: {label} unavailable: {type(error).__name__}: {error}")
                results[label] = None
        return results
    finally:
        automation.application.kill()
        automation.application.dispose()
        time.sleep(0.5)


def main() -> int:
    """Run every combination and print mean/p95 per lookup style plus the derived overheads.

    :return: Process exit code (always 0; this script reports, it does not gate).
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-n", "--iterations", type=int, default=50)
    args = parser.parse_args()
    print(f"{args.iterations} iterations, times in ms\n")
    for uia in (UIAutomationTypes.UIA2, UIAutomationTypes.UIA3):
        for app_name in APPS:
            combo = f"{uia.name}_{app_name}"
            results = run_combo(uia, app_name, args.iterations)
            print(f"{combo}")
            for label, stats in results.items():
                text = "n/a" if stats is None else f"mean {stats['mean']:>8.2f}   p95 {stats['p95']:>8.2f}"
                print(f"  {label:<46} {text}")
            mean = {k: v["mean"] for k, v in results.items() if v is not None}
            direct = mean["direct wrapper find"]
            inlined = mean["suite path inlined (no map classes)"]
            suite = mean.get("suite map: simple_controls_tab.test_text_box")
            docs = mean.get("docs map: app.simple.name_box")
            print(
                f"  -> suite map vs direct {suite - direct:+.2f}  (lookups {inlined - direct:+.2f}, "
                f"classes {suite - inlined:+.2f})"
                if suite is not None
                else ""
            )
            if docs is not None:
                print(f"  -> docs map vs direct  {docs - direct:+.2f}")
            print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
