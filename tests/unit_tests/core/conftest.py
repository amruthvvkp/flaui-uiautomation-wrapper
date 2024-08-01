# Conftest for flaui_core unit tests

from typing import Any, Generator

from flaui.core.automation_elements import Window
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.assets.config import test_settings
from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.assets.utils import force_close_test_application_process


@pytest.fixture(scope="class")
def test_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    test_application = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    test_application.application.launch(
        test_settings.WPF_TEST_APP_EXE.as_posix()
        if ui_automation_type == UIAutomationTypes.UIA3
        else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    )
    yield test_application

    test_application.application.kill()

    force_close_test_application_process()


@pytest.fixture(scope="class")
def main_window(test_application: Automation, automation: Any) -> Generator[Window, None, None]:
    """Fetches the main window of the test application.

    :param wpf_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield test_application.application.get_main_window(automation)


@pytest.fixture(scope="class")
def condition_factory(main_window: Window):
    """Fixture for the ConditionFactory class.

    :param main_window: The main window of the test application.
    :return: The ConditionFactory class.
    """
    return main_window.condition_factory


@pytest.fixture(scope="class")
def test_elements(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)


@pytest.fixture(scope="class")
def more_controls_tab(test_elements: WPFApplicationElements):
    """Fixture for the More Controls tab.

    :param wpf_elements: The WPF application element map.
    :return: The More Controls tab.
    """
    return main_window.find_first_child(condition=main_window.condition_factory.by_name("More Controls"))
