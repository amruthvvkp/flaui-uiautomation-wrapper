"""UI integration tests for the Table, TableItem and GridItem patterns on a DataGrid (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from flaui.core.definitions import RowOrColumnMajor
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.wpf_only
class TestTablePattern:
    """Tests for the Table, TableItem and GridItem patterns on the WPF DataGrid control."""

    @pytest.fixture(name="data_grid")
    def get_data_grid(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        skip_on_winforms: None,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the DataGrid element from the Complex Controls tab.

        :param test_application: Test application elements.
        :param skip_on_winforms: Fixture that skips WinForms tests.
        :yield: DataGrid automation element.
        """
        yield test_application.complex_controls_tab.data_grid_view

    def test_table_pattern(self, data_grid: AutomationElement, is_pattern_supported: object) -> None:
        """Read the Table pattern row/column-major orientation."""
        assert_that(data_grid, not_none())
        if not is_pattern_supported(data_grid.patterns, "table"):  # type: ignore[operator]
            pytest.skip("Table pattern is not supported on this DataGrid/runtime")
        table_pattern = data_grid.patterns.table.pattern
        assert table_pattern.row_or_column_major.value in (
            RowOrColumnMajor.RowMajor.value,
            RowOrColumnMajor.ColumnMajor.value,
            RowOrColumnMajor.Indeterminate.value,
        )

    def test_grid_item_and_table_item_pattern(
        self,
        data_grid: AutomationElement,
        is_pattern_supported: object,
    ) -> None:
        """Resolve a cell and read its GridItem coordinates and TableItem headers."""
        cell = data_grid.patterns.grid.pattern.get_item(1, 1)
        assert_that(cell, not_none())
        grid_item_pattern = cell.patterns.grid_item.pattern
        assert grid_item_pattern.row.value == 1
        assert grid_item_pattern.column.value == 1
        if is_pattern_supported(cell.patterns, "table_item"):  # type: ignore[operator]
            # Accessing the header items should not raise; the value is an element collection.
            assert cell.patterns.table_item.pattern.column_header_items is not None
