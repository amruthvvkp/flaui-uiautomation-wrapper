"""Tests for the PopUp control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\PopupTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, HasLen, IsList
from flaui.core.automation_elements import Button
from flaui.core.input import Wait
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestPopUp:
    """Tests for the PopUp control."""

    @pytest.fixture
    def skip_winforms(self, test_application_type: str) -> None:
        """Skip WinForms tests."""
        if test_application_type == "WinForms":
            pytest.skip("Combobox got heavily broken with UIA2/UIA3 Winforms due to bugs in Windows/.Net")

    @pytest.fixture(name="popup_toggle_button1")
    def get_popup_toggle_button1(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, skip_winforms: None
    ) -> Generator[Button, Any, None]:
        """Returns the first pop up toggle button element."""
        yield test_application.simple_controls_tab.popup_toggle_button1

    @pytest.fixture(name="popup_toggle_button2")
    def get_popup_toggle_button2(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, skip_winforms: None
    ) -> Generator[Button, Any, None]:
        """Returns the second pop up toggle button element."""
        yield test_application.simple_controls_tab.popup_toggle_button2

    def test_check_box_in_popup(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, popup_toggle_button1: Button
    ) -> None:
        """Tests the check box in the pop up."""
        popup_toggle_button1.click()
        Wait.until_input_is_processed()
        popup = test_application.main_window.popup
        assert popup is not None, "Popup should be visible"
        popup_children = popup.find_all_children()
        assert popup_children == HasLen(1), "Popup should have one child"
        assert popup_children[0].as_check_box() == HasAttributes(text="This is a popup"), (
            "Popup should have a check box"
        )

    def test_menu_in_popup(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, popup_toggle_button2: Button
    ) -> None:
        """Tests the menu in the pop up."""
        popup_toggle_button2.click()
        Wait.until_input_is_processed()
        popup = test_application.main_window.popup
        assert popup is not None, "Popup should be visible"
        popup_children = popup.find_all_children()
        assert popup_children == HasLen(1), "Popup should have one child"
        menu = popup_children[0].as_menu()
        assert menu.items == IsList(positions={0: HasAttributes(text="Some MenuItem")}, length=1), (
            "Popup should have a menu"
        )
