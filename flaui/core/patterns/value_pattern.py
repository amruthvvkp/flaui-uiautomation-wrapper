"""Wrapper for the UI Automation Value pattern (``IValuePattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class ValuePattern(PatternBase):
    """Represents the UI Automation Value pattern for reading and setting a control's text value."""

    @property
    @handle_csharp_exceptions
    def is_read_only(self) -> AutomationProperty:
        """Return whether the value is read-only.

        :return: An :class:`AutomationProperty` wrapping the read-only flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.IsReadOnly)

    @property
    @handle_csharp_exceptions
    def value(self) -> AutomationProperty:
        """Return the current value.

        :return: An :class:`AutomationProperty` wrapping the value string.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Value)

    @handle_csharp_exceptions
    def set_value(self, value: str) -> None:
        """Set the control's value.

        :param value: The value to set.
        """
        self.raw_pattern.SetValue(value)
