"""Tests for the Window control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\WindowTests.cs."""

from dirty_equals import HasAttributes, HasLen
from flaui.core.input import Keyboard, Mouse, MouseButton, Wait
from flaui.core.windows_api import VirtualKeyShort
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestWindow:
    """Tests for Window control."""

    def test_modal_windows(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """``modal_windows`` is a property (C# ``ModalWindows``) and is empty while no dialog is open."""
        assert test_application.main_window.modal_windows == []

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
        # The four matrix apps share one desktop; make sure the right-click lands on this app's
        # window and not on another app left in the foreground by an earlier test.
        test_application.main_window.set_foreground()
        Wait.until_input_is_processed()
        Mouse.click(button.get_clickable_point(), mouse_button=MouseButton.Right, post_wait=True)
        try:
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
        finally:
            _dismiss_context_menu(test_application)


def _dismiss_context_menu(test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
    """Close every open level of the context menu so later tests see the app in its default state.

    GH-82: the matrix apps are session-scoped (C# FlaUI restarts the app per test fixture), so a
    context menu left open leaks into later tests. Reading ``items[1].items`` expands the
    "Inner Context" submenu, so a single Escape only closes that level. On WinForms the remaining
    ``DropDown`` popup is an unowned, visible top-level window of the process, which .NET's
    ``Process.MainWindowHandle`` (and therefore ``Application.get_main_window``) then returns
    instead of the real form. Every later fixture got the 195x80 popup as its "main window", so
    the Tab lookup in ``simple_controls_tab`` raised ``ElementNotFound``.

    :param test_application: Test application elements.
    """
    for _ in range(3):
        Keyboard.type_key(VirtualKeyShort.ESCAPE)
        Wait.until_input_is_processed()
        try:
            _ = test_application.main_window.context_menu
        except Exception:
            return  # No context menu is open any more.
