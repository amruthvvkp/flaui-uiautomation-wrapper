"""Journeys across the Complex Controls page: walking the tree and working with the list grid."""

from dirty_equals import IsList
from flaui.core.definitions import ExpandCollapseState
from flaui.core.tools import Retry
import pytest

from tests.integration.conftest import JourneyApp

pytestmark = pytest.mark.integration


class TestComplexControlsJourneys:
    """End-to-end journeys over the Complex Controls page."""

    @pytest.mark.bug(
        id="GH-76",
        url="https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/76",
        reason="Tree intermittently exposes only 1 item on AppVeyor CI; passes locally on all combos. "
        "run=True keeps the journey running so a fix is detected.",
        run=True,
    )
    def test_expand_tree_select_leaf_and_collapse(self, journey_app: JourneyApp) -> None:
        """Expand two tree levels, select a leaf, confirm the selection, then collapse back."""
        tree = journey_app.elements.complex_controls_tab.tree_elements
        assert [item.text for item in tree.items] == ["Lvl1 a", "Lvl1 b"]

        root = tree.items[0]
        root.expand()
        assert Retry.WhileFalse(lambda: root.expand_collapse_state == ExpandCollapseState.Expanded, timeout=2000)
        branch = Retry.WhileEmpty(lambda: root.items, timeout=2000)[1]
        branch.expand()
        leaf = Retry.WhileEmpty(lambda: branch.items, timeout=2000)[0]
        leaf.select()

        assert Retry.WhileFalse(lambda: leaf.is_selected, timeout=2000)
        assert tree.selected_tree_item.text == "Lvl3 a"

        root.collapse()
        assert Retry.WhileFalse(lambda: root.expand_collapse_state == ExpandCollapseState.Collapsed, timeout=2000)

    def test_select_grid_rows_by_index_and_by_text(self, journey_app: JourneyApp) -> None:
        """Read the list grid, select a row by index, then find and select another by cell text."""
        grid = journey_app.elements.complex_controls_tab.list_view_grid
        assert [column.name for column in grid.header.columns] == ["Key", "Value"]
        assert (grid.row_count, grid.column_count) == (3, 2)
        assert [[cell.value for cell in row.cells] for row in grid.rows] == [["1", "10"], ["2", "20"], ["3", "30"]]

        grid.select(1)
        assert [cell.value for cell in grid.selected_item.cells] == ["2", "20"]

        row = grid.select(column_index=1, text_to_find="30")
        assert [cell.value for cell in row.cells] == ["3", "30"]
        assert grid.selected_item.cells == IsList(length=2)
        assert grid.selected_item.cells[0].value == "3"
