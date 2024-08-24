"""Tests for the Tree control."""

from flaui.core.automation_type import AutomationType
import pytest
from pytest_check import equal, is_none, is_not_none

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestTree(UITestBase):
    """Tests for Tree control."""

    def test_selection(self):
        """Tests Selection of Tree controls"""
        tree = self.test_elements.complex_controls_tab.tree_elements
        with pytest.raises(ValueError):
            is_none(tree.selected_tree_item)
        equal(len(tree.items), 2)
        tree.items[0].expand()
        tree.items[0].items[1].expand()
        tree.items[0].items[1].items[0].select()
        is_not_none(tree.selected_tree_item)
        equal(tree.selected_tree_item.text, "Lvl3 a")
