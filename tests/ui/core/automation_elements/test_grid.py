"""Tests for the grid control."""

from dirty_equals import HasAttributes, IsList

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestGrid:
    """Tests for the grid control."""

    def test_grid_pattern(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the grid pattern."""
        assert test_application.complex_controls_tab.list_view_grid == HasAttributes(column_count=2, row_count=3), (
            "Grid pattern should be available."
        )

    def test_header_and_columns(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the grid header and columns."""
        grid = test_application.complex_controls_tab.list_view_grid
        assert grid.header.columns == IsList(
            positions={0: HasAttributes(name="Key"), 1: HasAttributes(name="Value")}, length=2
        ), "Grid columns should be available."

    def test_rows_and_cells(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the grid rows and cells."""
        grid = test_application.complex_controls_tab.list_view_grid
        expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]
        for row_index, row in enumerate(grid.rows):
            assert row.cells == IsList(
                positions={
                    0: HasAttributes(value=expected_cell_values[row_index][0]),
                    1: HasAttributes(value=expected_cell_values[row_index][1]),
                },
                length=2,
            )

    def test_select_by_index(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the grid select by index method."""
        grid = test_application.complex_controls_tab.list_view_grid
        for index, expected_cell_values in {1: ["2", "20"], 2: ["3", "30"]}.items():
            grid.select(index)
            assert grid.selected_item.cells == IsList(
                positions={
                    0: HasAttributes(value=expected_cell_values[0]),
                    1: HasAttributes(value=expected_cell_values[1]),
                },
                length=2,
            )

    def test_select_by_text(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the grid select by text method."""
        grid = test_application.complex_controls_tab.list_view_grid
        for expected_cell_values in [["2", "20"], ["3", "30"]]:
            grid.select(column_index=1, text_to_find=expected_cell_values[1])
            assert grid.selected_item.cells == IsList(
                positions={
                    0: HasAttributes(value=expected_cell_values[0]),
                    1: HasAttributes(value=expected_cell_values[1]),
                },
                length=2,
            )
