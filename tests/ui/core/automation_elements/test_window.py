"""Tests for the Window control."""

from flaui.core.automation_type import AutomationType
from flaui.core.input import Mouse, MouseButton, Wait
import pytest
from pytest_check import equal

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


# UIA3 WinForms test is Broken in newer .NET Versions
@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        # (AutomationType.UIA2, ApplicationType.WinForms), # TODO: Somehow the context menu of Winforms isn't getting captured, fix it and run this test
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestWindow(UITestBase):
    """Tests for Window control."""

    def test_context_menu(self):
        """Tests Context Menu of Window controls"""
        button = self.test_elements.simple_controls_tab.context_menu_button
        Mouse.click(button.get_clickable_point(), mouse_button=MouseButton.Right)
        Wait.until_input_is_processed()
        try:
            context_menu = self.test_elements.main_window.context_menu
        except Exception:
            pytest.fail("Context menu did not appear as expected")
        else:
            equal(len(context_menu.items), 2)
            equal(len(context_menu.items[1].items), 1)
            equal(context_menu.items[1].items[0].text, "Inner Context")
