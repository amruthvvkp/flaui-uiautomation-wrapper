"""Wrapper for the UI Automation Transform pattern (``ITransformPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class TransformPattern(PatternBase):
    """Represents the UI Automation Transform pattern for movable, resizable, rotatable controls."""

    @property
    @handle_csharp_exceptions
    def can_move(self) -> AutomationProperty:
        """Return whether the control can be moved.

        :return: An :class:`AutomationProperty` wrapping the can-move flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CanMove)

    @property
    @handle_csharp_exceptions
    def can_resize(self) -> AutomationProperty:
        """Return whether the control can be resized.

        :return: An :class:`AutomationProperty` wrapping the can-resize flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CanResize)

    @property
    @handle_csharp_exceptions
    def can_rotate(self) -> AutomationProperty:
        """Return whether the control can be rotated.

        :return: An :class:`AutomationProperty` wrapping the can-rotate flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CanRotate)

    @handle_csharp_exceptions
    def move(self, x: float, y: float) -> None:
        """Move the control to the given screen coordinates.

        :param x: The target x-coordinate.
        :param y: The target y-coordinate.
        """
        self.raw_pattern.Move(x, y)

    @handle_csharp_exceptions
    def resize(self, width: float, height: float) -> None:
        """Resize the control to the given dimensions.

        :param width: The target width.
        :param height: The target height.
        """
        self.raw_pattern.Resize(width, height)

    @handle_csharp_exceptions
    def rotate(self, degrees: float) -> None:
        """Rotate the control by the given number of degrees.

        :param degrees: The rotation in degrees.
        """
        self.raw_pattern.Rotate(degrees)
