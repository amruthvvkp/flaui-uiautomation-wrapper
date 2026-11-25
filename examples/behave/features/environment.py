"""Behave environment hooks for the FlaUI for Python example suite.

``before_all`` initialises the PythonNet bridge, launches the bundled WPF test application, and
stores the automation/window on the behave ``context``. ``after_all`` disposes everything.
"""

from pathlib import Path

# The bridge must be initialised before any C#-backed FlaUI type is used.
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


def _find_test_app() -> Path:
    """Locate the bundled WPF test application by walking up from this file.

    :raises FileNotFoundError: If the bundled executable cannot be found.
    :return: The path to ``WpfApplication.exe``.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "test_applications" / "WPFApplication" / "WpfApplication.exe"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not locate the bundled WPF test application under test_applications/.")


# --8<-- [start:before_all]
def before_all(context) -> None:
    """Launch the application once for the whole behave run.

    :param context: The behave run context.
    """
    context.automation = Automation(UIAutomationTypes.UIA3)
    context.automation.application.launch(str(_find_test_app()))
    context.automation.application.wait_while_main_handle_is_missing(3000)
    context.window = context.automation.application.get_main_window(context.automation)
    context.cf = context.automation.cf


# --8<-- [end:before_all]


# --8<-- [start:after_step]
def after_step(context, step) -> None:
    """Save a screenshot when a step fails, named after the scenario and step.

    :param context: The behave run context.
    :param step: The step that just ran.
    """
    if step.status == "failed":
        from flaui.core.capturing import Capture

        artifacts = Path("artifacts")
        artifacts.mkdir(exist_ok=True)
        name = "".join(c if c.isalnum() else "_" for c in f"{context.scenario.name}-{step.name}")
        with Capture.main_screen() as image:
            image.to_file(str(artifacts / f"{name}.png"))


# --8<-- [end:after_step]


def after_all(context) -> None:
    """Kill and dispose the application after the run.

    :param context: The behave run context.
    """
    context.automation.application.kill()
    context.automation.automation_base.dispose()
