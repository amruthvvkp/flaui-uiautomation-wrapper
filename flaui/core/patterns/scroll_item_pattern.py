"""Wrapper for the UI Automation ScrollItem pattern (``IScrollItemPattern``)."""

from __future__ import annotations

from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class ScrollItemPattern(PatternBase):
    """Represents the UI Automation ScrollItem pattern for items that can scroll into view."""

    @handle_csharp_exceptions
    def scroll_into_view(self) -> None:
        """Scroll the item into the visible region of its container."""
        self.raw_pattern.ScrollIntoView()
