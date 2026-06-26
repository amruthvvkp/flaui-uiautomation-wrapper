"""Wrapper for the UI Automation SpreadsheetItem pattern (``ISpreadsheetItemPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class SpreadsheetItemPattern(PatternBase):
    """Represents the UI Automation SpreadsheetItem pattern for a single spreadsheet cell."""

    @property
    @handle_csharp_exceptions
    def formula(self) -> AutomationProperty:
        """Return the formula of the cell.

        :return: An :class:`AutomationProperty` wrapping the formula string.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Formula)

    @property
    @handle_csharp_exceptions
    def annotation_objects(self) -> AutomationProperty:
        """Return the annotation elements associated with the cell.

        :return: An :class:`AutomationProperty` wrapping the annotation elements.
        """
        return AutomationProperty(raw_property=self.raw_pattern.AnnotationObjects)

    @property
    @handle_csharp_exceptions
    def annotation_types(self) -> AutomationProperty:
        """Return the annotation type identifiers associated with the cell.

        :return: An :class:`AutomationProperty` wrapping the annotation types.
        """
        return AutomationProperty(raw_property=self.raw_pattern.AnnotationTypes)
