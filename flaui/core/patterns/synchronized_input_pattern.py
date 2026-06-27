"""Wrapper for the UI Automation SynchronizedInput pattern (``ISynchronizedInputPattern``)."""

from __future__ import annotations

from flaui.core.definitions import SynchronizedInputType
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class SynchronizedInputPattern(PatternBase):
    """Represents the UI Automation SynchronizedInput pattern for coordinating input events."""

    @handle_csharp_exceptions
    def cancel(self) -> None:
        """Cancel listening for synchronized input."""
        self.raw_pattern.Cancel()

    @handle_csharp_exceptions
    def start_listening(self, input_type: SynchronizedInputType) -> None:
        """Begin listening for the given type of synchronized input.

        :param input_type: The type of input event to listen for.
        """
        self.raw_pattern.StartListening(input_type.value)
