"""Tests for the cache request and caching, ported from C# CacheTests.cs."""

from typing import Any, Generator

from dirty_equals import HasLen
from flaui.core.automation_elements import AutomationElement, Grid
from flaui.core.cache_request import CacheRequest
from flaui.core.definitions import TreeScope
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestCache:
    """Tests for the cache request and caching behavior."""

    @pytest.fixture(name="list_view_grid")
    def get_list_view_grid(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Grid, Any, None]:
        """Returns the list view grid element.

        :param test_application: Test application elements.
        :yield: List view grid element.
        """
        yield test_application.complex_controls_tab.list_view_grid

    @pytest.mark.skip_if_matrix(
        {"ui_automation_type": [UIAutomationTypes.UIA2], "test_app_type": ["WinForms"]},
        reason="Tab element not exposed in UIA2_WinForms",
    )
    def test_rows_and_cells_cached(self, ui_automation_type: UIAutomationTypes, list_view_grid: Grid) -> None:
        """Tests that rows and cells are cached and have correct values using CacheRequest wrapper.

        Ported from CacheTests.cs::RowsAndCellsTest
        """
        expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]

        # Create cache request and configure it
        automation = Automation(ui_automation_type)
        cache_request = CacheRequest(automation)
        cache_request.tree_scope = TreeScope.Descendants
        cache_request.add_property(automation.cs_automation.PropertyLibrary.Element.Name)

        with cache_request.activate():
            rows = list_view_grid.rows
            assert rows == HasLen(3), "Grid should have 3 rows."

            for row_index, row in enumerate(rows):
                # Use cached_children property
                cells = row.cached_children
                assert cells == HasLen(2), "Each row should have 2 cells."

                for cell_index, cell in enumerate(cells):
                    # Convert to AutomationElement and get label
                    cell_element = AutomationElement(raw_element=cell)
                    cell_text = cell_element.as_label().text
                    assert cell_text == expected_cell_values[row_index][cell_index], (
                        f"Cell value mismatch at row {row_index}, cell {cell_index}."
                    )
