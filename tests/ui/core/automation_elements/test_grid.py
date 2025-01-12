"""Tests for the grid control."""

from typing import Dict, List, Tuple

from flaui.core.application import Application
from flaui.core.automation_elements import GridRow, Window
from flaui.core.automation_type import AutomationType
from flaui.modules.automation import Automation
from loguru import logger
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
class TestGrid:
    """Tests for the grid control."""

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(
        self,
        request: pytest.FixtureRequest,
        setup_application_cache: Dict[Tuple[AutomationType, ApplicationType], Tuple[Automation, Application]],
        automation_type: AutomationType,
        application_type: ApplicationType,
    ):
        """Sets up essential properties for tests in this class.

        :param ui_test_base: UI Test base fixture
        :param automation_type: Automation Type
        :param application_type: Application Type
        """
        logger.info(f"Starting test: {request.node.name}")
        automation, application = setup_application_cache[(automation_type, application_type)]
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
        yield
        logger.info(f"Finished test: {request.node.name}")

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

    # def test_rows_and_cells(self):# TODO: Looks like a flakey test
    #     """Tests the grid rows and cells."""
    #     grid = self.test_elements.complex_controls_tab.list_view_grid
    #     rows = grid.rows
    #     equal(len(rows), 3)
    #     expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]
    #     for row_index, row in enumerate(rows):
    #         self._check_row_content(row, expected_cell_values[row_index])

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

    # def test_select_by_index(self):# TODO: Looks like a flakey test
    #     """Tests the grid select by index method."""
    #     grid = self.test_elements.complex_controls_tab.list_view_grid
    #     for k, v in {1: ["2", "20"], 2: ["3", "30"]}.items():
    #         grid.select(k)
    #         selected_row = grid.selected_item
    #         self._check_row_content(selected_row, v)

    def test_select_by_text(self):
        """Tests the grid select by text method."""
        grid = self.test_elements.complex_controls_tab.list_view_grid
        for _ in [["2", "20"], ["3", "30"]]:
            grid.select(column_index=1, text_to_find=_[1])
            selected_row = grid.selected_item
            self._check_row_content(selected_row, _)
