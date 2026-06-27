"""Wrapper for the UI Automation Selection2 pattern (``ISelection2Pattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.selection_pattern import SelectionPattern
from flaui.lib.exceptions import handle_csharp_exceptions


class Selection2Pattern(SelectionPattern):
    """Extends the Selection pattern with current/first/last selected item and item-count info."""

    @property
    @handle_csharp_exceptions
    def current_selected_item(self) -> AutomationProperty:
        """Return the currently selected item.

        :return: An :class:`AutomationProperty` wrapping the current selected element.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CurrentSelectedItem)

    @property
    @handle_csharp_exceptions
    def first_selected_item(self) -> AutomationProperty:
        """Return the first selected item.

        :return: An :class:`AutomationProperty` wrapping the first selected element.
        """
        return AutomationProperty(raw_property=self.raw_pattern.FirstSelectedItem)

    @property
    @handle_csharp_exceptions
    def last_selected_item(self) -> AutomationProperty:
        """Return the last selected item.

        :return: An :class:`AutomationProperty` wrapping the last selected element.
        """
        return AutomationProperty(raw_property=self.raw_pattern.LastSelectedItem)

    @property
    @handle_csharp_exceptions
    def item_count(self) -> AutomationProperty:
        """Return the number of selected items.

        :return: An :class:`AutomationProperty` wrapping the selected-item count.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ItemCount)
