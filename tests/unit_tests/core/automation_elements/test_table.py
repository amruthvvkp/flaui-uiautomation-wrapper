"""Tests for the Grid control read as Table."""


from typing import Any, Generator

from flaui.core.automation_elements import Window
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
    """Tests for the Grid control read as Table.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)

class TestTable:
    """Tests for RadioButton control."""

    def test_headers(self, wpf_elements: WPFApplicationElements):
        """Tests the length of table header."""
        table = wpf_elements.complex_controls_tab.list_view_grid
        assert len(table.column_headers) == 2

    def test_header_and_columns(self, wpf_elements: WPFApplicationElements):
        """Tests the table header and columns."""
        table = wpf_elements.complex_controls_tab.list_view_grid
        header = table.header
        columns = header.columns
        assert header is not None
        assert len(columns) == 2
        assert columns[0].text == "Key"
        assert columns[1].text == "Value"

    def test_rows_and_cells(self, wpf_elements: WPFApplicationElements):
        """Tests the table rows and cells."""
        table = wpf_elements.complex_controls_tab.list_view_grid
        rows = table.rows

        assert len(rows) == 3

        expected_row_data = {
            0: ["1", "10"],
            1: ["2", "20"],
            2: ["3", "30"]
        }

        length_of_cells = 2

        for _row, _data in expected_row_data.items():
            cells = rows[_row].cells
            assert len(cells) == length_of_cells
            for _ in range(length_of_cells):
                assert cells[_].as_label().text == _data[_]
