"""Tests for the grid control."""

from typing import List

from flaui.core.automation_elements import GridRow
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
class TestGrid(UITestBase):
    """Tests for the grid control."""

    def test_grid_pattern(self):
        """Tests the grid pattern."""
        grid = self.test_elements.complex_controls_tab.list_view_grid
        equal(grid.column_count, 2)
        equal(grid.row_count, 3)

    def test_header_and_columns(self):
        """Tests the grid header and columns."""
        grid = self.test_elements.complex_controls_tab.list_view_grid
        header = grid.header
        columns = header.columns
        is_not_none(header)
        equal(len(columns), 2)
        equal(columns[0].name, "Key")
        equal(columns[1].name, "Value")

    def test_rows_and_cells(self):
        """Tests the grid rows and cells."""
        grid = self.test_elements.complex_controls_tab.list_view_grid
        rows = grid.rows
        equal(len(rows), 3)
        expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]
        for row_index, row in enumerate(rows):
            self._check_row_content(row, expected_cell_values[row_index])

    @staticmethod
    def _check_row_content(grid_row: GridRow, expected_values: List[str]):
        """Checks Grid row content

        :param grid_row: Grid row element
        :param expected_values: Expected values
        """
        cells = grid_row.cells
        equal(len(cells), len(expected_values))
        for cell_index, cell in enumerate(cells):
            equal(cell.value, expected_values[cell_index])

    def test_select_by_index(self):
        """Tests the grid select by index method."""
        grid = self.test_elements.complex_controls_tab.list_view_grid
        for k, v in {1: ["2", "20"], 2: ["3", "30"]}.items():
            grid.select(k)
            selected_row = grid.selected_item
            self._check_row_content(selected_row, v)

    def test_select_by_text(self):
        """Tests the grid select by text method."""
        grid = self.test_elements.complex_controls_tab.list_view_grid
        for _ in [["2", "20"], ["3", "30"]]:
            grid.select(column_index=1, text_to_find=_[1])
            selected_row = grid.selected_item
            self._check_row_content(selected_row, _)
