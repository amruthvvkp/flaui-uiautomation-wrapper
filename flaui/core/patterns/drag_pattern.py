"""Wrapper for the UI Automation Drag pattern (``IDragPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class DragPattern(PatternBase):
    """Represents the UI Automation Drag pattern for elements that can be dragged."""

    @property
    @handle_csharp_exceptions
    def drop_effect(self) -> AutomationProperty:
        """Return a localized description of the drop effect when dragging.

        :return: An :class:`AutomationProperty` wrapping the drop effect.
        """
        return AutomationProperty(raw_property=self.raw_pattern.DropEffect)

    @property
    @handle_csharp_exceptions
    def drop_effects(self) -> AutomationProperty:
        """Return the full set of localized drop effect descriptions.

        :return: An :class:`AutomationProperty` wrapping the drop effects.
        """
        return AutomationProperty(raw_property=self.raw_pattern.DropEffects)

    @property
    @handle_csharp_exceptions
    def is_grabbed(self) -> AutomationProperty:
        """Return whether the element is currently grabbed for dragging.

        :return: An :class:`AutomationProperty` wrapping the grabbed flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.IsGrabbed)

    @property
    @handle_csharp_exceptions
    def grabbed_items(self) -> AutomationProperty:
        """Return the items being dragged together with this element.

        :return: An :class:`AutomationProperty` wrapping the grabbed items.
        """
        return AutomationProperty(raw_property=self.raw_pattern.GrabbedItems)
