"""Tests for the Window control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\WindowTests.cs."""

from dirty_equals import HasAttributes, HasLen
from flaui.core.input import Mouse, MouseButton
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestWindow:
    """Tests for Window control."""

    # GH-79: Context menu of WinForms is not captured with UIA3 on newer .NET versions (upstream
    # limitation). Skipped on UIA3 + WinForms via skip_on_uia3_winforms; runs on the other three
    # matrix combinations. Tagged platform_limitation (queryable via `-m platform_limitation`)
    # rather than `bug`, because the bug marker is whole-test and would skip the healthy combos too.
    @pytest.mark.platform_limitation
    def test_context_menu(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        skip_on_uia3_winforms: None,
    ) -> None:
        """Tests Context Menu of Window controls"""
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
