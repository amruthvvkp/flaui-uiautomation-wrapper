"""
Test for Grid pattern, ported from C# GridPatternTests.cs.

C# GridPatternTests only runs on WPF (2 fixtures):
[TestFixture(AutomationType.UIA2, TestApplicationType.Wpf)]
[TestFixture(AutomationType.UIA3, TestApplicationType.Wpf)]
"""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from flaui.core.definitions import ControlType
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.wpf_only
class TestGridPattern:
    """Tests for Grid pattern on WPF DataGrid control."""

    @pytest.fixture(name="data_grid")
    def get_data_grid(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        skip_on_winforms: None,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the DataGrid element from the second tab.

        :param test_application: Test application elements.
        :param skip_on_winforms: Fixture that skips WinForms tests.
        :yield: DataGrid automation element.
        """
        tab_control = test_application.main_window.find_first_descendant(
            condition=test_application._cf.by_control_type(ControlType.Tab)
        ).as_tab()
        tab_control.select_tab_item(index=1)
        tab_item = tab_control.tab_items[1]
        data_grid = tab_item.find_first_descendant(condition=test_application._cf.by_automation_id("dataGridView"))
        yield data_grid

    def test_grid_pattern(self, data_grid: AutomationElement) -> None:
        """Test grid pattern on DataGrid control."""
        assert_that(data_grid, not_none())
        grid_pattern = data_grid.patterns.Grid.Pattern  # TODO: Move Patterns to Py-wrapper once it is created
        assert_that(grid_pattern, not_none())
        assert grid_pattern.ColumnCount.Value == 3, "Column count should be 3"
        assert grid_pattern.RowCount.Value == 3, "Row count should be 3"
        item = grid_pattern.GetItem(1, 1)
        assert item.Properties.Name.Value == "24", "Grid cell (1,1) should have value '24'"
