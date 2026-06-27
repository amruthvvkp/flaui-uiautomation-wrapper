"""Wrapper for the UI Automation Selection pattern (``ISelectionPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class SelectionPattern(PatternBase):
    """Represents the UI Automation Selection pattern for containers of selectable items."""

    @property
    @handle_csharp_exceptions
    def can_select_multiple(self) -> AutomationProperty:
        """Return whether the container allows multiple items to be selected.

        :return: An :class:`AutomationProperty` wrapping the multi-select flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CanSelectMultiple)

    @property
    @handle_csharp_exceptions
    def is_selection_required(self) -> AutomationProperty:
        """Return whether the container requires at least one item to be selected.

        :return: An :class:`AutomationProperty` wrapping the selection-required flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.IsSelectionRequired)

    @property
    @handle_csharp_exceptions
    def selection(self) -> AutomationProperty:
        """Return the currently selected items.

        :return: An :class:`AutomationProperty` wrapping the selected elements.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Selection)
