"""Tests for the grid control."""

from typing import Any, Generator

from dirty_equals import HasAttributes, IsList
from flaui.core.automation_elements import Grid
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestGrid:
    """Tests for the grid control."""

    @pytest.fixture(name="list_view_grid")
    def get_list_view_grid(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Grid, Any, None]:
        """Returns the list view grid element.

        :param test_application: Test application elements.
        :yield: List view grid element.
        """
        yield test_application.complex_controls_tab.list_view_grid

    def test_grid_pattern(self, list_view_grid: Grid) -> None:
        """Tests the grid pattern."""
        assert list_view_grid == HasAttributes(column_count=2, row_count=3), "Grid pattern should be available."

    def test_header_and_columns(self, list_view_grid: Grid) -> None:
        """Tests the grid header and columns."""
        assert list_view_grid.header.columns == IsList(
            positions={0: HasAttributes(name="Key"), 1: HasAttributes(name="Value")}, length=2
        ), "Grid columns should be available."

    def test_rows_and_cells(self, list_view_grid: Grid) -> None:
        """Tests the grid rows and cells."""
        expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]
        for row_index, row in enumerate(list_view_grid.rows):
            assert row.cells == IsList(
                positions={
                    0: HasAttributes(value=expected_cell_values[row_index][0]),
                    1: HasAttributes(value=expected_cell_values[row_index][1]),
                },
                length=2,
            )

    def test_select_by_index(self, list_view_grid: Grid) -> None:
        """Tests the grid select by index method."""
        for index, expected_cell_values in {1: ["2", "20"], 2: ["3", "30"]}.items():
            list_view_grid.select(index)
            assert list_view_grid.selected_item.cells == IsList(
                positions={
                    0: HasAttributes(value=expected_cell_values[0]),
                    1: HasAttributes(value=expected_cell_values[1]),
                },
                length=2,
            )

    def test_select_by_text(self, list_view_grid: Grid) -> None:
        """Tests the grid select by text method."""
        for expected_cell_values in [["2", "20"], ["3", "30"]]:
            list_view_grid.select(column_index=1, text_to_find=expected_cell_values[1])
            assert list_view_grid.selected_item.cells == IsList(
                positions={
                    0: HasAttributes(value=expected_cell_values[0]),
                    1: HasAttributes(value=expected_cell_values[1]),
                },
                length=2,
            )
