"""Wrapper for the UI Automation RangeValue pattern (``IRangeValuePattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class RangeValuePattern(PatternBase):
    """Represents the UI Automation RangeValue pattern for controls with a numeric range (e.g. sliders)."""

    @property
    @handle_csharp_exceptions
    def is_read_only(self) -> AutomationProperty:
        """Return whether the value is read-only.

        :return: An :class:`AutomationProperty` wrapping the read-only flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.IsReadOnly)

    @property
    @handle_csharp_exceptions
    def large_change(self) -> AutomationProperty:
        """Return the value added or subtracted on a large change.

        :return: An :class:`AutomationProperty` wrapping the large-change amount.
        """
        return AutomationProperty(raw_property=self.raw_pattern.LargeChange)

    @property
    @handle_csharp_exceptions
    def small_change(self) -> AutomationProperty:
        """Return the value added or subtracted on a small change.

        :return: An :class:`AutomationProperty` wrapping the small-change amount.
        """
        return AutomationProperty(raw_property=self.raw_pattern.SmallChange)

    @property
    @handle_csharp_exceptions
    def maximum(self) -> AutomationProperty:
        """Return the maximum value of the range.

        :return: An :class:`AutomationProperty` wrapping the maximum value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Maximum)

    @property
    @handle_csharp_exceptions
    def minimum(self) -> AutomationProperty:
        """Return the minimum value of the range.

        :return: An :class:`AutomationProperty` wrapping the minimum value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Minimum)

    @property
    @handle_csharp_exceptions
    def value(self) -> AutomationProperty:
        """Return the current value.

        :return: An :class:`AutomationProperty` wrapping the current value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Value)

    @handle_csharp_exceptions
    def set_value(self, value: float) -> None:
        """Set the control's value.

        :param value: The numeric value to set.
        """
        self.raw_pattern.SetValue(value)
