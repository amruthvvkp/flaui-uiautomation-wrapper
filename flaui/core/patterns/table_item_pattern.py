"""Wrapper for the UI Automation TableItem pattern (``ITableItemPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class TableItemPattern(PatternBase):
    """Represents the UI Automation TableItem pattern for a cell that knows its header items."""

    @property
    @handle_csharp_exceptions
    def column_header_items(self) -> AutomationProperty:
        """Return the column header items associated with the cell.

        :return: An :class:`AutomationProperty` wrapping the column header items.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ColumnHeaderItems)

    @property
    @handle_csharp_exceptions
    def row_header_items(self) -> AutomationProperty:
        """Return the row header items associated with the cell.

        :return: An :class:`AutomationProperty` wrapping the row header items.
        """
        return AutomationProperty(raw_property=self.raw_pattern.RowHeaderItems)
