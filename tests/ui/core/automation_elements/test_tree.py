"""Tests for the Tree control."""

from dirty_equals import HasAttributes, HasLen
from flaui.lib.exceptions import ElementNotFound
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestTree:
    """Tests for Tree control."""

    def test_selection(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests Selection of Tree controls"""
        tree = test_application.complex_controls_tab.tree_elements
        with pytest.raises(ElementNotFound):
            _ = tree.selected_tree_item
        assert tree == HasAttributes(items=HasLen(2)), "Tree should have 2 items."
        tree.items[0].expand()
        tree.items[0].items[1].expand()
        tree.items[0].items[1].items[0].select()
        assert tree.selected_tree_item is not None, "Tree should have a selected item."
        assert tree.selected_tree_item == HasAttributes(text="Lvl3 a"), "Selected item should be 'Lvl3 a'."
