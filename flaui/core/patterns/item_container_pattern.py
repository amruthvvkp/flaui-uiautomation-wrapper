"""Wrapper for the UI Automation ItemContainer pattern (``IItemContainerPattern``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement


class ItemContainerPattern(PatternBase):
    """Represents the UI Automation ItemContainer pattern for efficient item lookup in containers."""

    @handle_csharp_exceptions
    def find_item_by_property(
        self, start_after: Optional["AutomationElement"], property_id: Any, value: Any
    ) -> Optional["AutomationElement"]:
        """Find an item by a property value, optionally starting after a given item.

        :param start_after: The item to start searching after, or ``None`` to start at the beginning.
        :param property_id: The C# ``PropertyId`` to match (or ``None`` to find any next item).
        :param value: The property value to match (or ``None``).
        :return: The matching :class:`~flaui.core.automation_elements.AutomationElement`, or ``None``.
        """
        from flaui.core.automation_elements import AutomationElement

        raw_start = None if start_after is None else start_after.raw_element
        result = self.raw_pattern.FindItemByProperty(raw_start, property_id, value)
        return None if result is None else AutomationElement(raw_element=result)
