"""Wrapper for the UI Automation Scroll pattern (``IScrollPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.definitions import ScrollAmount
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class ScrollPattern(PatternBase):
    """Represents the UI Automation Scroll pattern for controls that scroll their content."""

    @property
    @handle_csharp_exceptions
    def horizontally_scrollable(self) -> AutomationProperty:
        """Return whether the control can scroll horizontally.

        :return: An :class:`AutomationProperty` wrapping the horizontal-scrollable flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.HorizontallyScrollable)

    @property
    @handle_csharp_exceptions
    def vertically_scrollable(self) -> AutomationProperty:
        """Return whether the control can scroll vertically.

        :return: An :class:`AutomationProperty` wrapping the vertical-scrollable flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.VerticallyScrollable)

    @property
    @handle_csharp_exceptions
    def horizontal_scroll_percent(self) -> AutomationProperty:
        """Return the horizontal scroll position as a percentage.

        :return: An :class:`AutomationProperty` wrapping the horizontal scroll percent.
        """
        return AutomationProperty(raw_property=self.raw_pattern.HorizontalScrollPercent)

    @property
    @handle_csharp_exceptions
    def vertical_scroll_percent(self) -> AutomationProperty:
        """Return the vertical scroll position as a percentage.

        :return: An :class:`AutomationProperty` wrapping the vertical scroll percent.
        """
        return AutomationProperty(raw_property=self.raw_pattern.VerticalScrollPercent)

    @property
    @handle_csharp_exceptions
    def horizontal_view_size(self) -> AutomationProperty:
        """Return the horizontal viewport size as a percentage of the total content.

        :return: An :class:`AutomationProperty` wrapping the horizontal view size.
        """
        return AutomationProperty(raw_property=self.raw_pattern.HorizontalViewSize)

    @property
    @handle_csharp_exceptions
    def vertical_view_size(self) -> AutomationProperty:
        """Return the vertical viewport size as a percentage of the total content.

        :return: An :class:`AutomationProperty` wrapping the vertical view size.
        """
        return AutomationProperty(raw_property=self.raw_pattern.VerticalViewSize)

    @handle_csharp_exceptions
    def scroll(self, horizontal_amount: ScrollAmount, vertical_amount: ScrollAmount) -> None:
        """Scroll the content by the given horizontal and vertical amounts.

        :param horizontal_amount: The horizontal scroll amount.
        :param vertical_amount: The vertical scroll amount.
        """
        self.raw_pattern.Scroll(horizontal_amount.value, vertical_amount.value)

    @handle_csharp_exceptions
    def set_scroll_percent(self, horizontal_percent: float, vertical_percent: float) -> None:
        """Set the scroll position as horizontal and vertical percentages.

        :param horizontal_percent: The horizontal scroll position (0-100), or ``-1`` for no change.
        :param vertical_percent: The vertical scroll position (0-100), or ``-1`` for no change.
        """
        self.raw_pattern.SetScrollPercent(horizontal_percent, vertical_percent)
