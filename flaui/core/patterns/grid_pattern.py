"""Wrapper for the UI Automation Grid pattern (``IGridPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationElement, AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class GridPattern(PatternBase):
    """Represents the UI Automation Grid pattern for controls arranged in a grid of cells."""

    @property
    @handle_csharp_exceptions
    def column_count(self) -> AutomationProperty:
        """Return the number of columns in the grid.

        :return: An :class:`AutomationProperty` wrapping the column count.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ColumnCount)

    @property
    @handle_csharp_exceptions
    def row_count(self) -> AutomationProperty:
        """Return the number of rows in the grid.

        :return: An :class:`AutomationProperty` wrapping the row count.
        """
        return AutomationProperty(raw_property=self.raw_pattern.RowCount)

    @handle_csharp_exceptions
    def get_item(self, row: int, column: int) -> AutomationElement:
        """Return the cell at the given zero-based row and column.

        :param row: Zero-based row index.
        :param column: Zero-based column index.
        :return: The :class:`AutomationElement` at the requested cell.
        """
        return AutomationElement(raw_element=self.raw_pattern.GetItem(row, column))
