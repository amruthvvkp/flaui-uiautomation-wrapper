"""Tests for the Window control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\WindowTests.cs."""

from dirty_equals import HasAttributes, HasLen
from flaui.core.input import Mouse, MouseButton
from flaui.lib.enums import UIAutomationTypes
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements

# UIA3 WinForms test is Broken in newer .NET Versions
# TODO: Somehow the context menu of Winforms isn't getting captured, fix it and run this test


class TestWindow:
    """Tests for Window control."""

    def test_context_menu(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        ui_automation_type: UIAutomationTypes,
        test_application_type: str,
    ) -> None:
        """Tests Context Menu of Window controls"""
        if ui_automation_type == UIAutomationTypes.UIA3 and test_application_type == "WinForms":
            pytest.skip("Context menu of WinForms is not working with UIA3 on newer .NET versions")

        button = test_application.simple_controls_tab.context_menu_button
        Mouse.click(button.get_clickable_point(), mouse_button=MouseButton.Right, post_wait=True)
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
