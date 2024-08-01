"""Tests for the Grid control read as Table."""

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestTable:
    """Tests for RadioButton control."""

    def test_headers(self, test_elements: WPFApplicationElements):
        """Tests the length of table header."""
        table = test_elements.complex_controls_tab.list_view_grid
        assert len(table.column_headers) == 2

    def test_header_and_columns(self, test_elements: WPFApplicationElements):
        """Tests the table header and columns."""
        table = test_elements.complex_controls_tab.list_view_grid
        header = table.header
        columns = header.columns
        assert header is not None
        assert len(columns) == 2
        assert columns[0].text == "Key"
        assert columns[1].text == "Value"

    def test_rows_and_cells(self, test_elements: WPFApplicationElements):
        """Tests the table rows and cells."""
        table = test_elements.complex_controls_tab.list_view_grid
        rows = table.rows

        assert len(rows) == 3

        expected_row_data = {0: ["1", "10"], 1: ["2", "20"], 2: ["3", "30"]}

        length_of_cells = 2

        for _row, _data in expected_row_data.items():
            cells = rows[_row].cells
            assert len(cells) == length_of_cells
            for _ in range(length_of_cells):
                assert cells[_].as_label().text == _data[_]
