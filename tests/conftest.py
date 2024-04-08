"""Fixtures for the test suite."""

import os
from typing import Any, Generator, Literal

from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
import psutil
import pytest

from tests.config import test_settings

# isort: off

setup_pythonnet_bridge()

from flaui.core.automation_elements import AutomationElement
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation

# isort: on


def close_test_application_process():
    """Close the test application process."""
    for process in (process for process in psutil.process_iter() if process.name() == "WpfApplication.exe"):
        process.terminate()


@pytest.fixture(scope="package")
def ui_automation_type() -> Generator[Literal[UIAutomationTypes.UIA3, UIAutomationTypes.UIA2], None, None]:
    """Fixture to yield the UI Automation type.

    :yield: UI Automation type
    """
    yield (
        UIAutomationTypes.UIA3 if os.getenv("DEFAULT_UIA_VERSION", "UIA3").upper() == "UIA3" else UIAutomationTypes.UIA2
    )


@pytest.fixture(scope="package")
def automation(ui_automation_type: UIAutomationTypes) -> Generator[Any, None, None]:
    """Fixture to yield the automation object.

    :param ui_automation_type: UI Automation type
    :yield: Automation object
    """
    from FlaUI.UIA2 import UIA2Automation  # pyright: ignore
    from FlaUI.UIA3 import UIA3Automation  # pyright: ignore

    yield UIA3Automation() if ui_automation_type == UIAutomationTypes.UIA3 else UIA2Automation()


@pytest.fixture(scope="package")
def test_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Fixture to yield the test application.

    :param ui_automation_type: UI Automation type
    :yield: Test application
    """
    automation = Automation(ui_automation_type)
    automation.application.launch(str(test_settings.WPF_TEST_APP_EXE))
    yield automation

    automation.application.kill()

    close_test_application_process()


@pytest.fixture(scope="package")
def wordpad(ui_automation_type: UIAutomationTypes):
    """Fixture to yield the wordpad application.

    :param ui_automation_type: UI Automation type
    :yield: Wordpad application
    """
    test_automation = Automation(ui_automation_type)
    test_automation.application.launch("wordpad.exe")
    yield test_automation

    test_automation.application.kill()


@pytest.fixture(scope="package")
def test_app_main_window(test_application: Automation, automation: Any) -> Generator[AutomationElement, None, None]:
    """Fixture to yield the test application main window.

    :param test_application: Test application
    :param automation: Automation object
    :yield: Test application main window
    """
    yield test_application.application.get_main_window(automation)
