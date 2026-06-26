"""Wrapper for the UI Automation Toggle pattern (``ITogglePattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class TogglePattern(PatternBase):
    """Represents the UI Automation Toggle pattern for controls that cycle through states."""

    @property
    @handle_csharp_exceptions
    def toggle_state(self) -> AutomationProperty:
        """Return the current toggle state.

        :return: An :class:`AutomationProperty` wrapping the ``ToggleState`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ToggleState)

    @handle_csharp_exceptions
    def toggle(self) -> None:
        """Cycle the control to its next toggle state."""
        self.raw_pattern.Toggle()
