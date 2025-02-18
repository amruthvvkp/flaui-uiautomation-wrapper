"""Tests for the Grid control read as Table, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\TableTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, HasLen, IsDict, IsList
from flaui.core.automation_elements import Grid
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestTable:
    """Tests for the Grid control read as Table."""

    @pytest.fixture(name="list_view_grid")
    def get_list_view_grid(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Grid, Any, None]:
        """Returns the table element.

        :param test_application: Test application elements.
        :return: Test table element.
        """
        yield test_application.complex_controls_tab.list_view_grid

    def test_headers(self, list_view_grid: Grid) -> None:
        """Tests the length of table header."""
        assert list_view_grid == HasAttributes(column_headers=HasLen(2)), "Table should have 2 headers."

    def test_header_and_columns(self, list_view_grid: Grid) -> None:
        """Tests the table header and columns."""
        header = list_view_grid.header
        columns = header.columns
        assert header is not None, "Header should not be None."
        assert columns == IsList(positions={0: HasAttributes(text="Key"), 1: HasAttributes(text="Value")}, length=2), (
            "Table should have 2 columns."
        )

    def test_rows_and_cells(self, list_view_grid: Grid) -> None:
        """Tests the table rows and cells."""
        rows = list_view_grid.rows

        assert rows == HasLen(3), "Table should have 3 rows."

        actual_row_data = {index: [cell.as_label().text for cell in row.cells] for index, row in enumerate(rows)}
        assert actual_row_data == IsDict({0: ["1", "10"], 1: ["2", "20"], 2: ["3", "30"]})
