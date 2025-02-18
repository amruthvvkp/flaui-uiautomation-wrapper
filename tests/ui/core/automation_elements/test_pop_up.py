"""Tests for the PopUp control."""

from dirty_equals import HasAttributes, HasLen, IsList
from flaui.core.input import Wait
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


@pytest.mark.xfail(
    condition=lambda request: request.getfixturevalue("test_application_type") == "WinForms",  # type: ignore
    reason="UI Automation currently does not support Toggle pattern on menu items in WinForms applications.",
)
class TestPopUp:
    """Tests for the PopUp control."""

    def test_check_box_in_popup(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the check box in the pop up."""
        element = test_application.simple_controls_tab.popup_toggle_button1
        element.click()
        Wait.until_input_is_processed()
        popup = test_application.main_window.popup
        assert popup is not None, "Popup should be visible"
        popup_children = popup.find_all_children()
        assert popup_children == HasLen(1), "Popup should have one child"
        assert popup_children[0].as_check_box() == HasAttributes(text="This is a popup"), (
            "Popup should have a check box"
        )

    def test_menu_in_popup(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the menu in the pop up."""
        element = test_application.simple_controls_tab.popup_toggle_button2
        element.click()
        Wait.until_input_is_processed()
        popup = test_application.main_window.popup
        assert popup is not None, "Popup should be visible"
        popup_children = popup.find_all_children()
        assert popup_children == HasLen(1), "Popup should have one child"
        menu = popup_children[0].as_menu()
        assert menu.items == IsList(positions={0: HasAttributes(text="Some MenuItem")}, length=1), (
            "Popup should have a menu"
        )
