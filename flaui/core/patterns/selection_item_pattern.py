"""Wrapper for the UI Automation SelectionItem pattern (``ISelectionItemPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class SelectionItemPattern(PatternBase):
    """Represents the UI Automation SelectionItem pattern for individually selectable items."""

    @property
    @handle_csharp_exceptions
    def is_selected(self) -> AutomationProperty:
        """Return whether the item is selected.

        :return: An :class:`AutomationProperty` wrapping the selected flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.IsSelected)

    @property
    @handle_csharp_exceptions
    def selection_container(self) -> AutomationProperty:
        """Return the container that holds the item.

        :return: An :class:`AutomationProperty` wrapping the selection container element.
        """
        return AutomationProperty(raw_property=self.raw_pattern.SelectionContainer)

    @handle_csharp_exceptions
    def add_to_selection(self) -> None:
        """Add the item to the current selection."""
        self.raw_pattern.AddToSelection()

    @handle_csharp_exceptions
    def remove_from_selection(self) -> None:
        """Remove the item from the current selection."""
        self.raw_pattern.RemoveFromSelection()

    @handle_csharp_exceptions
    def select(self) -> None:
        """Select the item, deselecting any other selected items."""
        self.raw_pattern.Select()
