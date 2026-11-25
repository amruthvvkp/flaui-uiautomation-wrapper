"""Quickstart: a plain Python script (no test framework) that drives the bundled test application.

This is the script the *Basics* guide walks through. It launches the bundled WPF or WinForms test
application, finds a few controls, interacts with them, and shuts everything down cleanly.

Run it from the project root::

    uv run python examples/scripts/quickstart.py                       # WPF app, UIA3
    uv run python examples/scripts/quickstart.py --app winforms --uia 2 # WinForms app, UIA2
"""

import argparse
from pathlib import Path

# --8<-- [start:setup]
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()  # must run before any C#-backed FlaUI import

from flaui.core.definitions import ControlType, ToggleState
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation

# --8<-- [end:setup]

APPS = {
    "wpf": Path("test_applications") / "WPFApplication" / "WpfApplication.exe",
    "winforms": Path("test_applications") / "WinFormsApplication" / "WinFormsApplication.exe",
}


def find_app(kind: str) -> Path:
    """Locate a bundled test application by walking up from this file.

    :param kind: ``"wpf"`` or ``"winforms"``.
    :raises FileNotFoundError: If the executable cannot be found.
    :return: Absolute path to the executable.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / APPS[kind]
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not locate {APPS[kind]} above {Path(__file__).parent}.")


def main(app_kind: str, uia: UIAutomationTypes) -> None:
    """Launch the app, interact with a handful of controls, then close it.

    :param app_kind: Which bundled application to drive (``"wpf"`` or ``"winforms"``).
    :param uia: The UI Automation backend to use.
    """
    executable = str(find_app(app_kind))

    # --8<-- [start:launch]
    # `with` disposes the automation and closes the application on exit.
    with Automation(uia) as automation:
        automation.application.launch(executable)
        automation.application.wait_while_main_handle_is_missing(3000)
        window = automation.application.get_main_window(automation)
        cf = automation.cf
        print(f"Launched: {window.title}")
        # --8<-- [end:launch]

        # --8<-- [start:find]
        text_box = window.find_first_descendant(cf.by_automation_id("TextBox"))  # by AutomationId (preferred)
        checkbox = window.find_first_descendant(cf.by_name("Test Checkbox"))  # by Name (visible text)
        buttons = window.find_all_descendants(cf.by_control_type(ControlType.Button))  # by ControlType
        print(f"Found {len(buttons)} buttons")
        # --8<-- [end:find]

        # --8<-- [start:interact]
        text_box.as_text_box().text = "Hello from FlaUI for Python"
        cb = checkbox.as_check_box()
        cb.toggle()
        print("Checkbox is on:", cb.toggle_state == ToggleState.On)
        cb.toggle()  # put it back
        # --8<-- [end:interact]

        print("Text box now reads:", text_box.as_text_box().text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--app", choices=sorted(APPS), default="wpf", help="bundled app to drive")
    parser.add_argument("--uia", choices=["2", "3"], default="3", help="UI Automation backend")
    args = parser.parse_args()
    main(args.app, UIAutomationTypes.UIA2 if args.uia == "2" else UIAutomationTypes.UIA3)
