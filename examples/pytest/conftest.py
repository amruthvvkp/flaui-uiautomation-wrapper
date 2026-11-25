"""Pytest fixtures for the FlaUI for Python example suite.

Launches the bundled WPF test application once per session and hands each test a ready-to-use main
window and condition factory. This mirrors the structure of the project's own ``tests/`` suite, but
is trimmed down to a single self-contained example.
"""

from pathlib import Path
from typing import Generator

# --8<-- [start:bridge]
# isort: off  -- the bridge must be initialised before any C#-backed import is used.
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

from flaui.core.automation_elements import Window
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

# isort: on
# --8<-- [end:bridge]


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


# --8<-- [start:session_fixture]
@pytest.fixture(scope="session")
def automation() -> Generator[Automation, None, None]:
    """Launch the WPF test application for the whole session and dispose it afterwards.

    :yield: A ready ``Automation`` instance with the application launched.
    """
    auto = Automation(UIAutomationTypes.UIA3)
    auto.application.launch(str(find_test_app()))
    auto.application.wait_while_main_handle_is_missing(3000)
    try:
        yield auto
    finally:
        auto.application.kill()
        auto.automation_base.dispose()


# --8<-- [end:session_fixture]


@pytest.fixture
def main_window(automation: Automation) -> Window:
    """Return the application's main window.

    :param automation: The session automation instance.
    :return: The main ``Window`` of the test application.
    """
    return automation.application.get_main_window(automation)


@pytest.fixture
def condition_factory(automation: Automation) -> ConditionFactory:
    """Return the automation's condition factory for building search conditions.

    :param automation: The session automation instance.
    :return: The shared ``ConditionFactory``.
    """
    return automation.cf


# --8<-- [start:screenshot_on_failure]
@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]) -> Generator[None, object, object]:
    """Save a screenshot of the whole screen when a test body fails.

    The file lands in ``artifacts/<test name>.png`` (git-ignored), ready to upload from CI. Only the
    ``call`` phase is captured, so failing fixtures and teardowns don't produce extra images.

    :param item: The test item being reported.
    :param call: Information about the phase that just ran.
    :yield: Control to pytest, which builds the report.
    :return: The test report.
    """
    report = yield
    if call.when == "call" and getattr(report, "failed", False):
        from flaui.core.capturing import Capture

        artifacts = Path("artifacts")
        artifacts.mkdir(exist_ok=True)
        safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in item.name)
        try:
            with Capture.main_screen() as image:
                image.to_file(str(artifacts / f"{safe_name}.png"))
        except Exception as error:  # a broken screenshot must never hide the real failure
            item.add_report_section("call", "screenshot", f"could not capture screen: {error}")
    return report


# --8<-- [end:screenshot_on_failure]
