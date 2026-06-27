"""Wrapper for the UI Automation Dock pattern (``IDockPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.definitions import DockPosition
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class DockPattern(PatternBase):
    """Represents the UI Automation Dock pattern for controls docked within a docking container."""

    @property
    @handle_csharp_exceptions
    def dock_position(self) -> AutomationProperty:
        """Return the control's current dock position.

        :return: An :class:`AutomationProperty` wrapping the ``DockPosition`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.DockPosition)

    @handle_csharp_exceptions
    def set_dock_position(self, dock_position: DockPosition) -> None:
        """Set the control's dock position.

        :param dock_position: The desired dock position.
        """
        self.raw_pattern.SetDockPosition(dock_position.value)
