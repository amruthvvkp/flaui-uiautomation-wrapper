"""Tests for the grid control."""

from typing import Any, Generator, List

from flaui.core.automation_elements import GridRow, Window
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


class TestGrid:
    """Tests for the grid control."""

    def test_grid_pattern(self, wpf_elements: WPFApplicationElements):
        """Tests the grid pattern.

        :param wpf_elements: WPF application element map.
        """
        grid = wpf_elements.complex_controls_tab.list_view_grid
        assert grid.column_count == 2
        assert grid.row_count == 3

    def test_header_and_columns(self, wpf_elements: WPFApplicationElements):
        """Tests the grid header and columns.

        :param wpf_elements: WPF application element map.
        """
        grid = wpf_elements.complex_controls_tab.list_view_grid
        header = grid.header
        columns = header.columns
        assert header is not None
        assert len(columns) == 2
        assert columns[0].name == "Key"
        assert columns[1].name == "Value"

    def test_rows_and_cells(self, wpf_elements: WPFApplicationElements):
        """Tests the grid rows and cells.

        :param wpf_elements: WPF application element map.
        """
        grid = wpf_elements.complex_controls_tab.list_view_grid
        rows = grid.rows
        assert len(rows) == 3
        expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]
        for row_index, row in enumerate(rows):
            self._check_row_content(row, expected_cell_values[row_index])

    @staticmethod
    def _check_row_content(grid_row: GridRow, expected_values: List[str]):
        cells = grid_row.cells
        assert len(cells) == len(expected_values)
        for cell_index, cell in enumerate(cells):
            assert cell.value == expected_values[cell_index]

    def test_select_by_index(self, wpf_elements: WPFApplicationElements):
        """Tests the grid select by index method.

        :param wpf_elements: WPF application element map.
        """
        grid = wpf_elements.complex_controls_tab.list_view_grid
        for k, v in {1: ["2", "20"], 2: ["3", "30"]}.items():
            grid.select(k)
            selected_row = grid.selected_item
            self._check_row_content(selected_row, v)

    def test_select_by_text(self, wpf_elements: WPFApplicationElements):
        """Tests the grid select by text method.

        :param wpf_elements: WPF application element map.
        """
        grid = wpf_elements.complex_controls_tab.list_view_grid
        for _ in [["2", "20"], ["3", "30"]]:
            grid.select(column_index=1, text_to_find=_[1])
            selected_row = grid.selected_item
            self._check_row_content(selected_row, _)
