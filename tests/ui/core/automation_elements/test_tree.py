"""Tests for the Tree control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\TreeTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, HasLen
from flaui.core.automation_elements import Tree, TreeItem
from flaui.core.tools import Retry
from flaui.lib.exceptions import ElementNotFound
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestTree:
    """Tests for Tree control."""

    @pytest.fixture(name="tree_elements")
    def get_tree_elements(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Tree, Any, None]:
        """Returns the tree elements.

        :param test_application: Test application elements.
        :return: Test tree elements.
        """
        yield test_application.complex_controls_tab.tree_elements

    @staticmethod
    def _wait_for_children(item: Tree | TreeItem, count: int) -> None:
        """Wait until ``item`` exposes at least ``count`` child tree items.

        GH-76: tree items are realised lazily (WPF builds a node's item containers only after it is
        expanded, and the tab content may still be loading right after the tab switch), so on a slow
        CI VM reading ``items`` straight away can return a partial list. Wait for the children
        before indexing into them; the assertions below still check the exact counts.

        :param item: Tree or tree item whose children to wait for.
        :param count: Minimum number of child items to wait for.
        """
        Retry.WhileFalse(lambda: len(item.items) >= count, timeout=5000, interval=100)

    def test_selection(self, tree_elements: Tree) -> None:
        """Tests Selection of Tree controls"""
        with pytest.raises(ElementNotFound):
            _ = tree_elements.selected_tree_item

        self._wait_for_children(tree_elements, 2)
        assert tree_elements == HasAttributes(items=HasLen(2)), "Tree should have 2 items."
        tree_elements.items[0].expand()
        self._wait_for_children(tree_elements.items[0], 2)
        tree_elements.items[0].items[1].expand()
        self._wait_for_children(tree_elements.items[0].items[1], 1)
        tree_elements.items[0].items[1].items[0].select()
        assert tree_elements.selected_tree_item is not None, "Tree should have a selected item."
        assert tree_elements.selected_tree_item == HasAttributes(text="Lvl3 a"), "Selected item should be 'Lvl3 a'."
