"""Wrapper for the UI Automation TextChild pattern (``ITextChildPattern``)."""

from __future__ import annotations

from typing import Any

from flaui.core.patterns.pattern_base import PatternBase
from flaui.core.text_range import TextRange
from flaui.lib.exceptions import handle_csharp_exceptions


class TextChildPattern(PatternBase):
    """Represents the UI Automation TextChild pattern for elements embedded inside text content."""

    @property
    @handle_csharp_exceptions
    def text_container(self) -> Any:
        """Return the nearest ancestor that supports the Text pattern.

        :return: The containing :class:`~flaui.core.automation_elements.AutomationElement`.
        """
        from flaui.core.automation_elements import AutomationElement

        return AutomationElement(raw_element=self.raw_pattern.TextContainer)

    @property
    @handle_csharp_exceptions
    def text_range(self) -> TextRange:
        """Return the text range that encloses this child element.

        :return: A :class:`~flaui.core.text_range.TextRange` for the element.
        """
        return TextRange(raw_text_range=self.raw_pattern.TextRange)
