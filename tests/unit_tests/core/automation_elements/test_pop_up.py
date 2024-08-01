"""Tests for the PopUp control."""

from typing import Any, Generator

from flaui.core.automation_elements import Window
from flaui.core.input import Wait
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.assets.config import test_settings


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
def wpf_elements(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)


class TestPopUp:
    """Tests for the PopUp control."""

    def test_check_box_in_popup(self, wpf_elements: WPFApplicationElements):
        """Tests the check box in the pop up."""
        element = wpf_elements.simple_controls_tab.popup_toggle_button1
        element.click()
        Wait.until_input_is_processed()
        popup = wpf_elements.main_window.popup
        assert popup is not None
        popup_children = popup.find_all_children()
        assert len(popup_children) == 1
        check = popup_children[0].as_check_box()
        assert check.text == "This is a popup"

    def test_menu_in_popup(self, wpf_elements: WPFApplicationElements):
        """Tests the menu in the pop up."""
        element = wpf_elements.simple_controls_tab.popup_toggle_button2
        element.click()
        Wait.until_input_is_processed()
        popup = wpf_elements.main_window.popup
        assert popup is not None
        popup_children = popup.find_all_children()
        assert len(popup_children) == 1
        menu = popup_children[0].as_menu()
        assert len(menu.items) == 1
        assert menu.items[0].text == "Some MenuItem"
