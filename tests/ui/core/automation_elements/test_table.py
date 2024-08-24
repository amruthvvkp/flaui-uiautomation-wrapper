"""Tests for the Grid control read as Table."""

from flaui.core.application import Application
from flaui.core.automation_elements import Window
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
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestTable:
    """Tests for the Grid control read as Table."""

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
