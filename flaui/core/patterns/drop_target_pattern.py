"""Wrapper for the UI Automation DropTarget pattern (``IDropTargetPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class DropTargetPattern(PatternBase):
    """Represents the UI Automation DropTarget pattern for elements that accept drops."""

    @property
    @handle_csharp_exceptions
    def drop_target_effect(self) -> AutomationProperty:
        """Return a localized description of the effect when dropping onto this target.

        :return: An :class:`AutomationProperty` wrapping the drop target effect.
        """
        return AutomationProperty(raw_property=self.raw_pattern.DropTargetEffect)

    @property
    @handle_csharp_exceptions
    def drop_target_effects(self) -> AutomationProperty:
        """Return the full set of localized drop target effect descriptions.

        :return: An :class:`AutomationProperty` wrapping the drop target effects.
        """
        return AutomationProperty(raw_property=self.raw_pattern.DropTargetEffects)
