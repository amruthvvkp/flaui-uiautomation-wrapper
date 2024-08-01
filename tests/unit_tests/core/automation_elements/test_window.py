"""Tests for the Window control."""

from flaui.core.input import Mouse, MouseButton, Wait
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestWindow:
    """Tests for Window control."""

    def test_context_menu(self, test_elements: WPFApplicationElements):
        """Tests Context Menu of Window controls"""
        button = test_elements.simple_controls_tab.context_menu_button
        Mouse.click(button.get_clickable_point(), mouse_button=MouseButton.Right)
        Wait.until_input_is_processed()
        try:
            context_menu = test_elements.main_window.context_menu
        except ValueError:
            pytest.fail("Context menu did not appear as expected")
        else:
            assert len(context_menu.items) == 2
            assert len(context_menu.items[1].items) == 1
            assert context_menu.items[1].items[0].text == "Inner Context"
