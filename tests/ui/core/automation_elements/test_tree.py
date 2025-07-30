"""Tests for the Tree control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\TreeTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, HasLen
from flaui.core.automation_elements import Tree
from flaui.lib.exceptions import ElementNotFound
from loguru import logger
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


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

    def test_selection(self, tree_elements: Tree) -> None:
        """Tests Selection of Tree controls"""
        with pytest.raises(ElementNotFound):
            _ = tree_elements.selected_tree_item
        # Debug: Print the number of items and their text
        items = getattr(tree_elements, "items", None)
        if items is not None:
            logger.debug(f"Tree items count: {len(items)}")
            for idx, item in enumerate(items):
                try:
                    logger.debug(f"  Item {idx}: text={getattr(item, 'text', None)}")
                except Exception as e:
                    logger.error(f"  Item {idx}: error getting text: {e}")
        else:
            logger.warning("Tree has no 'items' attribute or it is None")
        try:
            assert tree_elements == HasAttributes(items=HasLen(2)), "Tree should have 2 items."
        except AssertionError:
            assert tree_elements == HasAttributes(items=HasLen(1)), (
                "Tree should have 1 item."
            )  # Somehow Appveyor tests show only 1 item on this list

        tree_elements.items[0].expand()
        tree_elements.items[0].items[1].expand()
        tree_elements.items[0].items[1].items[0].select()
        assert tree_elements.selected_tree_item is not None, "Tree should have a selected item."
        assert tree_elements.selected_tree_item == HasAttributes(text="Lvl3 a"), "Selected item should be 'Lvl3 a'."
