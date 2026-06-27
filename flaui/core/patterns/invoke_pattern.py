"""Wrapper for the UI Automation Invoke pattern (``IInvokePattern``)."""

from __future__ import annotations

from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class InvokePattern(PatternBase):
    """Represents the UI Automation Invoke pattern for controls that perform a single action."""

    @handle_csharp_exceptions
    def invoke(self) -> None:
        """Invoke the control (perform its primary action)."""
        self.raw_pattern.Invoke()
