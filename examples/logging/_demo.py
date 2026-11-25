"""Shared demo workload for the logging examples: launch the bundled WPF app and touch a control.

Each ``*_sink.py`` script configures logging its own way, then calls :func:`run` so you can compare
what the different sinks record for exactly the same FlaUI activity.
"""

from pathlib import Path


def find_test_app() -> Path:
    """Locate the bundled WPF test application by walking up from this file.

    :raises FileNotFoundError: If the bundled executable cannot be found.
    :return: The path to ``WpfApplication.exe``.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "test_applications" / "WPFApplication" / "WpfApplication.exe"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not locate the bundled WPF test application under test_applications/.")


def run() -> None:
    """Initialise the bridge, launch the app, read a control, and close the app (all logged)."""
    from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

    setup_pythonnet_bridge()

    from flaui.core.logging import enable_csharp_logging
    from flaui.lib.enums import UIAutomationTypes
    from flaui.modules.automation import Automation

    enable_csharp_logging()  # C# FlaUI messages -> the "flaui.csharp" Python logger

    with Automation(UIAutomationTypes.UIA3) as automation:
        automation.application.launch(str(find_test_app()))
        window = automation.application.get_main_window(automation)
        text_box = window.find_first_descendant(automation.cf.by_automation_id("TextBox")).as_text_box()
        text_box.text = "logged"
