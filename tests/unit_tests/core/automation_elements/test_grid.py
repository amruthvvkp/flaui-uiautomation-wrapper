"""Tests for the grid control."""

from typing import List

from flaui.core.automation_elements import GridRow

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestGrid:
    """Tests for the grid control."""

    def test_grid_pattern(self, test_elements: WPFApplicationElements):
        """Tests the grid pattern.

        :param wpf_elements: WPF application element map.
        """
        grid = test_elements.complex_controls_tab.list_view_grid
        assert grid.column_count == 2
        assert grid.row_count == 3

    def test_header_and_columns(self, test_elements: WPFApplicationElements):
        """Tests the grid header and columns.

        :param wpf_elements: WPF application element map.
        """
        grid = test_elements.complex_controls_tab.list_view_grid
        header = grid.header
        columns = header.columns
        assert header is not None
        assert len(columns) == 2
        assert columns[0].name == "Key"
        assert columns[1].name == "Value"

    def test_rows_and_cells(self, test_elements: WPFApplicationElements):
        """Tests the grid rows and cells.

        :param wpf_elements: WPF application element map.
        """
        grid = test_elements.complex_controls_tab.list_view_grid
        rows = grid.rows
        assert len(rows) == 3
        expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]
        for row_index, row in enumerate(rows):
            self._check_row_content(row, expected_cell_values[row_index])

    @staticmethod
    def _check_row_content(grid_row: GridRow, expected_values: List[str]):
        cells = grid_row.cells
        assert len(cells) == len(expected_values)
        for cell_index, cell in enumerate(cells):
            assert cell.value == expected_values[cell_index]

    def test_select_by_index(self, test_elements: WPFApplicationElements):
        """Tests the grid select by index method.

        :param wpf_elements: WPF application element map.
        """
        grid = test_elements.complex_controls_tab.list_view_grid
        for k, v in {1: ["2", "20"], 2: ["3", "30"]}.items():
            grid.select(k)
            selected_row = grid.selected_item
            self._check_row_content(selected_row, v)

    def test_select_by_text(self, test_elements: WPFApplicationElements):
        """Tests the grid select by text method.

        :param wpf_elements: WPF application element map.
        """
        grid = test_elements.complex_controls_tab.list_view_grid
        for _ in [["2", "20"], ["3", "30"]]:
            grid.select(column_index=1, text_to_find=_[1])
            selected_row = grid.selected_item
            self._check_row_content(selected_row, _)
