"""Wrapper for the UI Automation Table pattern (``ITablePattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class TablePattern(PatternBase):
    """Represents the UI Automation Table pattern for grids that expose header information."""

    @property
    @handle_csharp_exceptions
    def column_headers(self) -> AutomationProperty:
        """Return the column header elements of the table.

        :return: An :class:`AutomationProperty` wrapping the column header elements.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ColumnHeaders)

    @property
    @handle_csharp_exceptions
    def row_headers(self) -> AutomationProperty:
        """Return the row header elements of the table.

        :return: An :class:`AutomationProperty` wrapping the row header elements.
        """
        return AutomationProperty(raw_property=self.raw_pattern.RowHeaders)

    @property
    @handle_csharp_exceptions
    def row_or_column_major(self) -> AutomationProperty:
        """Return whether the table is row-major or column-major.

        :return: An :class:`AutomationProperty` wrapping the ``RowOrColumnMajor`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.RowOrColumnMajor)
