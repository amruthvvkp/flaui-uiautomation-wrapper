"""Wrapper for the UI Automation Text pattern (``ITextPattern``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from flaui.core.definitions import SupportedTextSelection
from flaui.core.patterns.pattern_base import PatternBase
from flaui.core.text_range import TextRange
from flaui.lib.exceptions import handle_csharp_exceptions
from flaui.lib.system.drawing import Point

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement


class TextPattern(PatternBase):
    """Represents the UI Automation Text pattern for controls that expose rich text content."""

    @property
    @handle_csharp_exceptions
    def document_range(self) -> TextRange:
        """Return a text range spanning the entire document.

        :return: A :class:`~flaui.core.text_range.TextRange` over the whole document.
        """
        return TextRange(raw_text_range=self.raw_pattern.DocumentRange)

    @property
    @handle_csharp_exceptions
    def supported_text_selection(self) -> SupportedTextSelection:
        """Return the kind of text selection the control supports.

        :return: The supported text selection mode.
        """
        return SupportedTextSelection(self.raw_pattern.SupportedTextSelection)

    @handle_csharp_exceptions
    def get_selection(self) -> List[TextRange]:
        """Return the currently selected text ranges.

        :return: A list of selected :class:`~flaui.core.text_range.TextRange` objects.
        """
        return [TextRange(raw_text_range=_) for _ in self.raw_pattern.GetSelection()]

    @handle_csharp_exceptions
    def get_visible_ranges(self) -> List[TextRange]:
        """Return the text ranges that are currently visible.

        :return: A list of visible :class:`~flaui.core.text_range.TextRange` objects.
        """
        return [TextRange(raw_text_range=_) for _ in self.raw_pattern.GetVisibleRanges()]

    @handle_csharp_exceptions
    def range_from_child(self, child: "AutomationElement") -> TextRange:
        """Return the text range that encloses a child element.

        :param child: The child element to locate.
        :return: A :class:`~flaui.core.text_range.TextRange` enclosing the child.
        """
        return TextRange(raw_text_range=self.raw_pattern.RangeFromChild(child.raw_element))

    @handle_csharp_exceptions
    def range_from_point(self, point: Point) -> TextRange:
        """Return the degenerate text range nearest to a screen point.

        :param point: The screen point to locate.
        :return: A :class:`~flaui.core.text_range.TextRange` at the point.
        """
        return TextRange(raw_text_range=self.raw_pattern.RangeFromPoint(point.cs_object))
