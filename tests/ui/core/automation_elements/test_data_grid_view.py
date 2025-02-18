"""Tests the data grid view element."""

from typing import Any, Generator

from dirty_equals import HasAttributes, HasLen, IsList
from flaui.core.automation_elements import DataGridView
from flaui.lib.enums import UIAutomationTypes
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestDataGridView:
    """Tests for the Data Grid View element."""

    @pytest.fixture(name="data_grid_view")
    def get_data_grid_view(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        ui_automation_type: UIAutomationTypes,
        test_application_type: str,
    ) -> Generator[DataGridView, Any, None]:
        """Returns the data grid view element.

        :param test_application: Test application elements.
        :param ui_automation_type: UI automation type.
        :param test_application_type: Test application type.
        :yield: Data grid view element.
        """
        if test_application_type == "WPF" and ui_automation_type == UIAutomationTypes.UIA2:
            pytest.skip("Fails on UIA2 WPF applications.")
        yield test_application.complex_controls_tab.data_grid_view

    def test_header_and_columns(self, data_grid_view: DataGridView) -> None:
        """Tests the header and columns property."""
        header = data_grid_view.header
        columns = header.columns
        assert header is not None, "Header should not be None."
        assert columns == IsList(
            positions={
                0: HasAttributes(name="Name"),
                1: HasAttributes(name="Number"),
                2: HasAttributes(name="IsChecked"),
            },
            length=3,
        )

    def test_rows_and_cells(self, data_grid_view: DataGridView) -> None:
        """Tests the rows and cells property."""
        rows = data_grid_view.rows
        assert rows == HasLen(3), "Rows should have a length of 3."

        # There is an empty row on the application which we need to remove for the test to work through
        rows.pop(-1)
        expected_cell_values = [["John", "12", "False"], ["Doe", "24", "True"]]
        for row_index, row in enumerate(rows):
            assert row.cells == IsList(
                positions={
                    0: HasAttributes(value=expected_cell_values[row_index][0]),
                    1: HasAttributes(value=expected_cell_values[row_index][1]),
                    2: HasAttributes(value=expected_cell_values[row_index][2]),
                },
                length=3,
            )
