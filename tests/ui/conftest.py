from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.test_utilities.base import force_close_test_application_process
from tests.test_utilities.config import test_settings


@pytest.fixture(scope="package")
def test_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Fixture to yield the test application.

    :param ui_automation_type: UI Automation type
    :yield: Test application
    """
    automation = Automation(ui_automation_type)
    automation.application.launch(
        str(
            test_settings.WPF_TEST_APP_EXE
            if ui_automation_type == UIAutomationTypes.UIA3
            else test_settings.WINFORMS_TEST_APP_EXE
        )
    )
    yield automation

    automation.application.kill()

    force_close_test_application_process()


@pytest.fixture(scope="package")
def test_app_main_window(test_application: Automation, _automation: Any) -> Generator[AutomationElement, None, None]:
    """Fixture to yield the test application main window.

    :param test_application: Test application
    :param automation: Automation object
    :yield: Test application main window
    """
    yield test_application.application.get_main_window(_automation)
