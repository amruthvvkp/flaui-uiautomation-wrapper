"""Wrapper for the UI Automation VirtualizedItem pattern (``IVirtualizedItemPattern``)."""

from __future__ import annotations

from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class VirtualizedItemPattern(PatternBase):
    """Represents the UI Automation VirtualizedItem pattern for items that can be realized on demand."""

    @handle_csharp_exceptions
    def realize(self) -> None:
        """Realize the virtualized item, making it a full member of the automation tree."""
        self.raw_pattern.Realize()
