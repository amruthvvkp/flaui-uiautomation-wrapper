"""
Test for ScrollItem pattern, ported from C# ScrollItemPatternTests.cs.
"""

# from flaui.core.automation_elements import AutomationElement
# from flaui.core.condition_factory import ConditionFactory
# from flaui.core.tools import ItemRealizer
# from hamcrest import assert_that, not_none
# import pytest

# from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
# from tests.test_utilities.elements.wpf_application import WPFApplicationElements


# @pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
# class TestScrollItemPattern:
#     """Tests for ScrollItem pattern on LargeListView control."""

#     @pytest.fixture(name="large_list_view")
#     def get_large_list_view(
#         self,
#         test_application: WinFormsApplicationElements | WPFApplicationElements,
#         condition_factory: ConditionFactory,
#     ):
#         """Fixture to get the LargeListView element from the Complex Controls tab."""
#         # Select the Complex Controls tab (index may differ by app)
#         if hasattr(test_application, "tab"):
#             tab = test_application.tab
#             # Try to select the Complex Controls tab by index or name
#             if hasattr(tab, "select_tab_item"):
#                 # Try by index first (usually 1)
#                 try:
#                     tab.select_tab_item(1)
#                 except Exception:
#                     # Fallback: try by name
#                     tab.select_tab_item(value="Complex Controls")
#             parent = tab.tab_items[1] if hasattr(tab, "tab_items") else tab
#         else:
#             parent = test_application.main_window
#         # Find the LargeListView
#         large_list_view = parent.find_first_descendant(condition=condition_factory.by_automation_id("LargeListView"))
#         assert_that(large_list_view, not_none())
#         return large_list_view

#     def test_scroll_item_pattern(self, large_list_view: AutomationElement):
#         """Test ScrollItem pattern on LargeListView control."""
#         grid = large_list_view
#         assert_that(grid, not_none())
#         grid_pattern = grid.patterns.Grid.Pattern
#         assert_that(grid_pattern, not_none())
#         assert grid_pattern.ColumnCount.Value == 2
#         assert grid_pattern.RowCount.Value == 7
#         # Realize all items if needed (not implemented, assumed all rows are loaded)
#         ItemRealizer.realize_items(grid)
#         items = grid.as_grid().rows
#         assert len(items) == grid_pattern.RowCount.Value
#         scroll_pattern = grid.patterns.Scroll.Pattern
#         assert_that(scroll_pattern, not_none())
#         assert scroll_pattern.VerticalScrollPercent.Value == 0
#         for item in items:
#             scroll_item_pattern = item.raw_element.Patterns.ScrollItem.Pattern
#             assert_that(scroll_item_pattern, not_none())
#             item.scroll_into_view()
#         assert scroll_pattern.VerticalScrollPercent.Value > 0
