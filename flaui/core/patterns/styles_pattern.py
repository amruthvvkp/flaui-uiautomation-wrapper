"""Wrapper for the UI Automation Styles pattern (``IStylesPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class StylesPattern(PatternBase):
    """Represents the UI Automation Styles pattern for elements with visual styling (e.g. cells)."""

    @property
    @handle_csharp_exceptions
    def extended_properties(self) -> AutomationProperty:
        """Return extended style properties as a string.

        :return: An :class:`AutomationProperty` wrapping the extended properties.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ExtendedProperties)

    @property
    @handle_csharp_exceptions
    def fill_color(self) -> AutomationProperty:
        """Return the fill color of the element.

        :return: An :class:`AutomationProperty` wrapping the fill color (ARGB int).
        """
        return AutomationProperty(raw_property=self.raw_pattern.FillColor)

    @property
    @handle_csharp_exceptions
    def fill_pattern_color(self) -> AutomationProperty:
        """Return the fill pattern color of the element.

        :return: An :class:`AutomationProperty` wrapping the fill pattern color (ARGB int).
        """
        return AutomationProperty(raw_property=self.raw_pattern.FillPatternColor)

    @property
    @handle_csharp_exceptions
    def fill_pattern_style(self) -> AutomationProperty:
        """Return the fill pattern style name.

        :return: An :class:`AutomationProperty` wrapping the fill pattern style.
        """
        return AutomationProperty(raw_property=self.raw_pattern.FillPatternStyle)

    @property
    @handle_csharp_exceptions
    def shape(self) -> AutomationProperty:
        """Return the shape of the element.

        :return: An :class:`AutomationProperty` wrapping the shape.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Shape)

    @property
    @handle_csharp_exceptions
    def style(self) -> AutomationProperty:
        """Return the style identifier of the element.

        :return: An :class:`AutomationProperty` wrapping the ``StyleType`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Style)

    @property
    @handle_csharp_exceptions
    def style_name(self) -> AutomationProperty:
        """Return the localized style name of the element.

        :return: An :class:`AutomationProperty` wrapping the style name.
        """
        return AutomationProperty(raw_property=self.raw_pattern.StyleName)
