"""Tests for the Tree control."""

import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestTree:
    """Tests for Tree control."""

    def test_selection(self, test_elements: WPFApplicationElements):
        """Tests Selection of Tree controls"""
        tree = test_elements.complex_controls_tab.tree_elements
        with pytest.raises(ValueError):
            assert tree.selected_tree_item is None
        assert len(tree.items) == 2
        tree.items[0].expand()
        tree.items[0].items[1].expand()
        tree.items[0].items[1].items[0].select()
        assert tree.selected_tree_item is not None
        assert tree.selected_tree_item.text == "Lvl3 a"
