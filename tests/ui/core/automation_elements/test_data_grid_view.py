"""Tests the data grid view element."""

from dirty_equals import HasAttributes, HasLen, IsList
from flaui.lib.enums import UIAutomationTypes
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


@pytest.mark.xfail(
    condition=lambda request: request.getfixturevalue("ui_automation_type") == UIAutomationTypes.UIA2
    and request.getfixturevalue("test_application_type") == "WPF",  # type: ignore
    reason="Fails on UIA2 WPF applications.",
)
class TestDataGridView:
    """Tests for the Data Grid View element."""

    def test_header_and_columns(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the header and columns property."""
        data_grid_view = test_application.complex_controls_tab.data_grid_view
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

    def test_rows_and_cells(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the rows and cells property."""
        grid = test_application.complex_controls_tab.data_grid_view
        rows = grid.rows
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
