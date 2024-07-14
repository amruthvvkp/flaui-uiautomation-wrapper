"""Tests the data grid view element."""

from typing import Any, Generator, List

from flaui.core.automation_elements import DataGridViewRow, Window
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.config import test_settings

@pytest.fixture(scope="class")
def wpf_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    wpf_application = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    wpf_application.application.launch(
        test_settings.WPF_TEST_APP_EXE.as_posix()
        if ui_automation_type == UIAutomationTypes.UIA3
        else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    )
    yield wpf_application

    wpf_application.application.kill()


@pytest.fixture(scope="class")
def main_window(wpf_application: Automation, automation: Any) -> Generator[Window, None, None]:
    """Fetches the main window of the test application.

    :param wpf_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield wpf_application.application.get_main_window(automation)


@pytest.fixture(scope="class")
def wpf_elements(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)


class TestDataGridView:
    """Tests for the Data Grid View element."""

    def test_header_and_columns(self, wpf_elements: WPFApplicationElements):
        """Tests the header and columns property."""
        data_grid_view = wpf_elements.complex_controls_tab.data_grid_view
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

    def test_rows_and_cells(self, wpf_elements: WPFApplicationElements):
        """Tests the rows and cells property."""
        data_grid_view = wpf_elements.complex_controls_tab.data_grid_view
        rows = data_grid_view.rows
        assert len(rows) == 3

        # There is an empty row on the application which we need to remove for the test to work through
        rows.pop(-1)
        expected_cell_values = [["John", "12", "False"], ["Doe", "24", "True"]]
        for row_index, row in enumerate(rows):
            self._check_row(row, expected_cell_values[row_index])
