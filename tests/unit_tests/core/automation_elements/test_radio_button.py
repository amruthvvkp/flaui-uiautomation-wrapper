"""Tests for the Radio Button control."""


from typing import Any, Generator

from flaui.core.automation_elements import Window
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.assets.element_map.wpf_application.base import WPFApplicationElements
from tests.config import test_settings


@pytest.fixture(scope="class")
def wpf_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    wpf_application = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    wpf_application.application.launch(
        test_settings.WPF_TEST_APP_EXE.as_posix()
        if ui_automation_type == UIAutomationTypes.UIA3
        else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    )
    yield wpf_application

    wpf_application.application.kill()


@pytest.fixture(scope="class")
def main_window(wpf_application: Automation, automation: Any) -> Generator[Window, None, None]:
    """Fetches the main window of the test application.

    :param wpf_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield wpf_application.application.get_main_window(automation)

@pytest.fixture(scope="class")
def wpf_element_map(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)

class TestRadioButton:
    """Tests for RadioButton control."""

    def test_select_single_radio_button(self, wpf_element_map: WPFApplicationElements):
        """Tests the select single radio button."""
        element = wpf_element_map.simple_controls_tab.radio_button_1
        assert element.is_checked is False
        element.is_checked = True
        assert element.is_checked is True

    def test_select_radio_button_group(self, wpf_element_map: WPFApplicationElements):
        """Tests the select radio button group."""
        radio_button_1 = wpf_element_map.simple_controls_tab.radio_button_1
        radio_button_2 = wpf_element_map.simple_controls_tab.radio_button_2

        assert radio_button_2.is_checked is False
        radio_button_1.is_checked = True
        assert radio_button_1.is_checked is True and radio_button_2.is_checked is False
        radio_button_2.is_checked = True
        assert radio_button_1.is_checked is False and radio_button_2.is_checked is True
