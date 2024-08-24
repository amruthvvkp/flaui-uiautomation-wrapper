"""Tests for the PopUp control."""

from flaui.core.automation_type import AutomationType
from flaui.core.input import Wait
import pytest
from pytest_check import equal, is_not_none

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestPopUp(UITestBase):
    """Tests for the PopUp control."""

    def test_check_box_in_popup(self):
        """Tests the check box in the pop up."""
        element = self.test_elements.simple_controls_tab.popup_toggle_button1
        element.click()
        Wait.until_input_is_processed()
        popup = self.test_elements.main_window.popup
        is_not_none(popup)
        popup_children = popup.find_all_children()
        equal(len(popup_children), 1)
        check = popup_children[0].as_check_box()
        equal(check.text, "This is a popup")

    def test_menu_in_popup(self):
        """Tests the menu in the pop up."""
        element = self.test_elements.simple_controls_tab.popup_toggle_button2
        element.click()
        Wait.until_input_is_processed()
        popup = self.test_elements.main_window.popup
        is_not_none(popup)
        popup_children = popup.find_all_children()
        equal(len(popup_children), 1)
        menu = popup_children[0].as_menu()
        equal(len(menu.items), 1)
        equal(menu.items[0].text, "Some MenuItem")
