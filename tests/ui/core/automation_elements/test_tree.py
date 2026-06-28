"""Tests for the Tree control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\TreeTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, HasLen
from flaui.core.automation_elements import Tree
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

    @pytest.mark.bug(
        id="GH-76",
        url="https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/76",
        reason="Tree selection flaky on AppVeyor CI - the tree intermittently exposes only 1 item "
        "instead of the expected 2. Passes locally on all combos. run=True so the test still "
        "executes (BUG-PASS locally, BUG-FAIL on CI) and an eventual fix is detected.",
        run=True,
    )
    def test_selection(self, tree_elements: Tree) -> None:
        """Tests Selection of Tree controls"""
        with pytest.raises(ElementNotFound):
            _ = tree_elements.selected_tree_item

        assert tree_elements == HasAttributes(items=HasLen(2)), "Tree should have 2 items."
        tree_elements.items[0].expand()
        tree_elements.items[0].items[1].expand()
        tree_elements.items[0].items[1].items[0].select()
        assert tree_elements.selected_tree_item is not None, "Tree should have a selected item."
        assert tree_elements.selected_tree_item == HasAttributes(text="Lvl3 a"), "Selected item should be 'Lvl3 a'."
