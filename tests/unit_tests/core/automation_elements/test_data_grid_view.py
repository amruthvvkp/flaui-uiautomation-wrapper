"""Tests the data grid view element."""

from typing import List

from flaui.core.automation_elements import DataGridViewRow

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestDataGridView:
    """Tests for the Data Grid View element."""

    def test_header_and_columns(self, test_elements: WPFApplicationElements):
        """Tests the header and columns property."""
        data_grid_view = test_elements.complex_controls_tab.data_grid_view
        header = data_grid_view.header
        columns = header.columns
        assert header is not None
        assert len(columns) == 3
        assert columns[0].name == "Name"
        assert columns[1].name == "Number"
        assert columns[2].name == "IsChecked"

    @staticmethod
    def _check_row(data_grid_view_row: DataGridViewRow, expected_cell_values: List[str]):
        """Checks the row and its cells.

        :param data_grid_view_row: Data Grid View row to check.
        :param expected_cell_values: Expected cell values.
        """
        cells = data_grid_view_row.cells
        assert len(cells) == len(expected_cell_values)
        for cell_index, cell in enumerate(cells):
            assert cell.value == expected_cell_values[cell_index]

    def test_rows_and_cells(self, test_elements: WPFApplicationElements):
        """Tests the rows and cells property."""
        data_grid_view = test_elements.complex_controls_tab.data_grid_view
        rows = data_grid_view.rows
        assert len(rows) == 3

        # There is an empty row on the application which we need to remove for the test to work through
        rows.pop(-1)
        expected_cell_values = [["John", "12", "False"], ["Doe", "24", "True"]]
        for row_index, row in enumerate(rows):
            self._check_row(row, expected_cell_values[row_index])
