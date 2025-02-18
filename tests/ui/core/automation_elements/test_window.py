"""Tests for the Window control."""

from dirty_equals import HasAttributes, HasLen
from flaui.core.input import Mouse, MouseButton, Wait
from flaui.lib.enums import UIAutomationTypes
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


# UIA3 WinForms test is Broken in newer .NET Versions
# TODO: Somehow the context menu of Winforms isn't getting captured, fix it and run this test
@pytest.mark.xfail(
    condition=lambda request: request.getfixturevalue("ui_automation_type") == UIAutomationTypes.UIA3
    and request.getfixturevalue("test_application_type") == "WinForms",  # type: ignore
    reason="Fails on UIA2 WinForms/WPF and UIA3 WinForms",
)
class TestWindow:
    """Tests for Window control."""

    def test_context_menu(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests Context Menu of Window controls"""
        button = test_application.simple_controls_tab.context_menu_button
        Mouse.click(button.get_clickable_point(), mouse_button=MouseButton.Right)
        Wait.until_input_is_processed()
        try:
            context_menu = test_application.main_window.context_menu
        except Exception:
            pytest.fail("Context menu did not appear as expected")
        else:
            assert context_menu == HasAttributes(items=HasLen(2)), "Context menu should have 2 items."
            assert context_menu.items[1] == HasAttributes(items=HasLen(1)), "Inner Context menu should have 1 item."
            assert context_menu.items[1].items[0] == HasAttributes(text="Inner Context"), (
                "Inner Context menu should have 1 item."
            )
