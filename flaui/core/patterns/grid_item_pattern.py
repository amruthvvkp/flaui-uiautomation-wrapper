"""Wrapper for the UI Automation GridItem pattern (``IGridItemPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class GridItemPattern(PatternBase):
    """Represents the UI Automation GridItem pattern for a single cell within a grid."""

    @property
    @handle_csharp_exceptions
    def column(self) -> AutomationProperty:
        """Return the zero-based column index of the cell.

        :return: An :class:`AutomationProperty` wrapping the column index.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Column)

    @property
    @handle_csharp_exceptions
    def column_span(self) -> AutomationProperty:
        """Return the number of columns the cell spans.

        :return: An :class:`AutomationProperty` wrapping the column span.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ColumnSpan)

    @property
    @handle_csharp_exceptions
    def row(self) -> AutomationProperty:
        """Return the zero-based row index of the cell.

        :return: An :class:`AutomationProperty` wrapping the row index.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Row)

    @property
    @handle_csharp_exceptions
    def row_span(self) -> AutomationProperty:
        """Return the number of rows the cell spans.

        :return: An :class:`AutomationProperty` wrapping the row span.
        """
        return AutomationProperty(raw_property=self.raw_pattern.RowSpan)

    @property
    @handle_csharp_exceptions
    def containing_grid(self) -> AutomationProperty:
        """Return the grid that contains the cell.

        :return: An :class:`AutomationProperty` wrapping the containing grid element.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ContainingGrid)
