"""Wrapper for the UI Automation Transform2 pattern (``ITransform2Pattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.definitions import ZoomUnit
from flaui.core.patterns.transform_pattern import TransformPattern
from flaui.lib.exceptions import handle_csharp_exceptions


class Transform2Pattern(TransformPattern):
    """Extends the Transform pattern with zoom capabilities."""

    @property
    @handle_csharp_exceptions
    def can_zoom(self) -> AutomationProperty:
        """Return whether the control can be zoomed.

        :return: An :class:`AutomationProperty` wrapping the can-zoom flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CanZoom)

    @property
    @handle_csharp_exceptions
    def zoom_level(self) -> AutomationProperty:
        """Return the current zoom level.

        :return: An :class:`AutomationProperty` wrapping the zoom level.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ZoomLevel)

    @property
    @handle_csharp_exceptions
    def zoom_maximum(self) -> AutomationProperty:
        """Return the maximum zoom level.

        :return: An :class:`AutomationProperty` wrapping the maximum zoom level.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ZoomMaximum)

    @property
    @handle_csharp_exceptions
    def zoom_minimum(self) -> AutomationProperty:
        """Return the minimum zoom level.

        :return: An :class:`AutomationProperty` wrapping the minimum zoom level.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ZoomMinimum)

    @handle_csharp_exceptions
    def zoom(self, zoom: float) -> None:
        """Zoom the control to the given level.

        :param zoom: The target zoom level.
        """
        self.raw_pattern.Zoom(zoom)

    @handle_csharp_exceptions
    def zoom_by_unit(self, zoom_unit: ZoomUnit) -> None:
        """Zoom the control by a discrete unit.

        :param zoom_unit: The zoom unit (increment/decrement amount).
        """
        self.raw_pattern.ZoomByUnit(zoom_unit.value)
