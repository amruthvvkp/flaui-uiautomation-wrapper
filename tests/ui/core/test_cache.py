# """Tests for the cache request and caching, ported from C# CacheTests.cs."""

# from typing import Any, Generator

# from dirty_equals import HasLen
# from flaui.core.automation_elements import Grid
# from flaui.core.cache_request import CacheRequest
# from flaui.core.definitions import TreeScope
# from flaui.lib.enums import UIAutomationTypes
# from flaui.modules.automation import Automation
# import pytest

# from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
# from tests.test_utilities.elements.wpf_application import WPFApplicationElements


# class TestCache:
#     """Tests for the cache request and caching behavior."""

#     @pytest.fixture(name="list_view_grid")
#     def get_list_view_grid(
#         self, test_application: WinFormsApplicationElements | WPFApplicationElements
#     ) -> Generator[Grid, Any, None]:
#         """Returns the list view grid element.

#         :param test_application: Test application elements.
#         :yield: List view grid element.
#         """
#         yield test_application.complex_controls_tab.list_view_grid

#     def test_rows_and_cells_cached(self, ui_automation_type: UIAutomationTypes, list_view_grid: Grid) -> None:
#         """Tests that rows and cells are cached and have correct values using CacheRequest wrapper."""

#         expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]
#         cache_request = CacheRequest()
#         cache_request.tree_scope = TreeScope.Descendants
#         # Add the Name property to cache (mirroring C#)
#         # This assumes Automation.PropertyLibrary.Element.Name is available as in C#

#         automation = Automation(ui_automation_type)
#         cache_request.add_property(automation.cs_automation.PropertyLibrary.Element.Name)
#         with cache_request.activate():
#             rows = list_view_grid.rows
#             assert rows == HasLen(3), "Grid should have 3 rows."
#             for row_index, row in enumerate(rows):
#                 # Prefer .cached_children if available, else .cells
#                 cells = getattr(row, "cached_children", None) or row.cells
#                 assert cells == HasLen(2), "Each row should have 2 cells."
#                 for cell_index, cell in enumerate(cells):
#                     cell_text = cell.as_label().text if hasattr(cell, "as_label") else cell.value
#                     assert cell_text == expected_cell_values[row_index][cell_index], (
#                         f"Cell value mismatch at row {row_index}, cell {cell_index}."
#                     )
