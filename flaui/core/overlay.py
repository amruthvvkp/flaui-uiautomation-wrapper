"""Python wrapper for ``FlaUI.Core.Overlay`` — visual-debugging overlays.

An overlay draws a colored border around a screen rectangle for a short duration, which is handy
when debugging where an element actually is. Each :class:`~flaui.core.automation_base.AutomationBase`
exposes one via ``overlay_manager``; :meth:`~flaui.core.automation_elements.AutomationElement.draw_highlight`
uses it under the hood.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from flaui.lib.exceptions import handle_csharp_exceptions
from flaui.lib.system.drawing import ColorData, Rectangle


class OverlayManager(BaseModel):
    """Wraps a C# ``IOverlayManager`` (``WinFormsOverlayManager`` or ``NullOverlayManager``)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_overlay_manager: Any = Field(..., description="Underlying C# IOverlayManager instance")

    @property
    @handle_csharp_exceptions
    def size(self) -> int:
        """Get the overlay border size."""
        return self.raw_overlay_manager.Size

    @size.setter
    @handle_csharp_exceptions
    def size(self, value: int) -> None:
        """Set the overlay border size.

        :param value: Border size in pixels.
        """
        self.raw_overlay_manager.Size = value

    @property
    @handle_csharp_exceptions
    def margin(self) -> int:
        """Get the overlay margin (use a negative value to move it inside the rectangle)."""
        return self.raw_overlay_manager.Margin

    @margin.setter
    @handle_csharp_exceptions
    def margin(self, value: int) -> None:
        """Set the overlay margin.

        :param value: Margin in pixels (negative moves the overlay inside the rectangle).
        """
        self.raw_overlay_manager.Margin = value

    @handle_csharp_exceptions
    def show(self, rectangle: Rectangle, color: ColorData, duration_in_ms: int) -> None:
        """Show the overlay for a duration asynchronously (non-blocking).

        :param rectangle: The screen rectangle to outline.
        :param color: The border color.
        :param duration_in_ms: How long to show the overlay, in milliseconds.
        """
        self.raw_overlay_manager.Show(rectangle.raw_value, color.cs_object, duration_in_ms)

    @handle_csharp_exceptions
    def show_blocking(self, rectangle: Rectangle, color: ColorData, duration_in_ms: int) -> None:
        """Show the overlay and block execution until it is hidden again.

        :param rectangle: The screen rectangle to outline.
        :param color: The border color.
        :param duration_in_ms: How long to show the overlay, in milliseconds.
        """
        self.raw_overlay_manager.ShowBlocking(rectangle.raw_value, color.cs_object, duration_in_ms)

    @handle_csharp_exceptions
    def dispose(self) -> None:
        """Dispose the overlay manager and release its resources."""
        self.raw_overlay_manager.Dispose()
