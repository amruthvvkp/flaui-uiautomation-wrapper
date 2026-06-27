"""Wrapper for the UI Automation Window pattern (``IWindowPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.definitions import WindowVisualState
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class WindowPattern(PatternBase):
    """Represents the UI Automation Window pattern for top-level and child windows."""

    @property
    @handle_csharp_exceptions
    def can_maximize(self) -> AutomationProperty:
        """Return whether the window can be maximized.

        :return: An :class:`AutomationProperty` wrapping the can-maximize flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CanMaximize)

    @property
    @handle_csharp_exceptions
    def can_minimize(self) -> AutomationProperty:
        """Return whether the window can be minimized.

        :return: An :class:`AutomationProperty` wrapping the can-minimize flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CanMinimize)

    @property
    @handle_csharp_exceptions
    def is_modal(self) -> AutomationProperty:
        """Return whether the window is modal.

        :return: An :class:`AutomationProperty` wrapping the modal flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.IsModal)

    @property
    @handle_csharp_exceptions
    def is_topmost(self) -> AutomationProperty:
        """Return whether the window is top-most.

        :return: An :class:`AutomationProperty` wrapping the top-most flag.
        """
        return AutomationProperty(raw_property=self.raw_pattern.IsTopmost)

    @property
    @handle_csharp_exceptions
    def window_interaction_state(self) -> AutomationProperty:
        """Return the window's current interaction state.

        :return: An :class:`AutomationProperty` wrapping the ``WindowInteractionState`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.WindowInteractionState)

    @property
    @handle_csharp_exceptions
    def window_visual_state(self) -> AutomationProperty:
        """Return the window's current visual state.

        :return: An :class:`AutomationProperty` wrapping the ``WindowVisualState`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.WindowVisualState)

    @handle_csharp_exceptions
    def close(self) -> None:
        """Close the window."""
        self.raw_pattern.Close()

    @handle_csharp_exceptions
    def set_window_visual_state(self, state: WindowVisualState) -> None:
        """Set the window's visual state.

        :param state: The desired visual state (normal, maximized, or minimized).
        """
        self.raw_pattern.SetWindowVisualState(state.value)

    @handle_csharp_exceptions
    def wait_for_input_idle(self, milliseconds: int) -> bool:
        """Wait until the window is ready to accept input, or the timeout elapses.

        :param milliseconds: The maximum time to wait, in milliseconds.
        :return: ``True`` if the window became idle within the timeout, else ``False``.
        """
        return self.raw_pattern.WaitForInputIdle(milliseconds)
