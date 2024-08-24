"""Tests for the Grid control read as Table."""

from flaui.core.automation_type import AutomationType
import pytest
from pytest_check import equal, is_not_none

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestTable(UITestBase):
    """Tests for the Grid control read as Table."""

    def test_headers(self):
        """Tests the length of table header."""
        table = self.test_elements.complex_controls_tab.list_view_grid
        equal(len(table.column_headers), 2)

    def test_header_and_columns(self):
        """Tests the table header and columns."""
        table = self.test_elements.complex_controls_tab.list_view_grid
        header = table.header
        columns = header.columns
        is_not_none(header)
        equal(len(columns), 2)
        equal(columns[0].text, "Key")
        equal(columns[1].text, "Value")

    def test_rows_and_cells(self):
        """Tests the table rows and cells."""
        table = self.test_elements.complex_controls_tab.list_view_grid
        rows = table.rows

        equal(len(rows), 3)

        expected_row_data = {0: ["1", "10"], 1: ["2", "20"], 2: ["3", "30"]}

        length_of_cells = 2

        for _row, _data in expected_row_data.items():
            cells = rows[_row].cells
            equal(len(cells), length_of_cells)
            for _ in range(length_of_cells):
                equal(cells[_].as_label().text, _data[_])
