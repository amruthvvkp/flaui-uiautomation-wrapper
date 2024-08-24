"""Tests the data grid view element."""

from typing import List

from flaui.core.application import Application
from flaui.core.automation_elements import DataGridViewRow, Window
from flaui.core.automation_type import AutomationType
from flaui.modules.automation import Automation
import pytest
from pytest_check import equal, is_not_none

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestDataGridView:
    """Tests for the Data Grid View element."""

    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        ui_test_base: tuple[Application, Automation],
        automation_type: AutomationType,
        application_type: ApplicationType,
    ):
        """Sets up essential properties for tests in this class.

        :param ui_test_base: UI Test base fixture
        :param automation_type: Automation Type
        :param application_type: Application Type
        """
        application, automation = ui_test_base
        self.application = application
        self.main_window: Window = application.get_main_window(automation)
        self.automation = automation
        self._automation_type = automation_type
        self._application_type = application_type
        self.test_elements = (
            get_wpf_application_elements(main_window=self.main_window)
            if self._application_type == ApplicationType.Wpf
            else get_winforms_application_elements(main_window=self.main_window)
        )

    def test_header_and_columns(self):
        """Tests the header and columns property."""
        data_grid_view = self.test_elements.complex_controls_tab.data_grid_view
        header = data_grid_view.header
        columns = header.columns
        is_not_none(header)
        equal(len(columns), 3)
        equal(columns[0].name, "Name")
        equal(columns[1].name, "Number")
        equal(columns[2].name, "IsChecked")

    @staticmethod
    def _check_row(data_grid_view_row: DataGridViewRow, expected_cell_values: List[str]):
        """Checks the row and its cells.

        :param data_grid_view_row: Data Grid View row to check.
        :param expected_cell_values: Expected cell values.
        """
        cells = data_grid_view_row.cells
        equal(len(cells), len(expected_cell_values))
        for cell_index, cell in enumerate(cells):
            equal(cell.value, expected_cell_values[cell_index])

    def test_rows_and_cells(self):
        """Tests the rows and cells property."""
        data_grid_view = self.test_elements.complex_controls_tab.data_grid_view
        rows = data_grid_view.rows
        equal(len(rows), 3)

        # There is an empty row on the application which we need to remove for the test to work through
        rows.pop(-1)
        expected_cell_values = [["John", "12", "False"], ["Doe", "24", "True"]]
        for row_index, row in enumerate(rows):
            self._check_row(row, expected_cell_values[row_index])
