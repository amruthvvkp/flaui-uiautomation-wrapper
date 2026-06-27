"""Wrapper for the UI Automation Text2 pattern (``IText2Pattern``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from flaui.core.patterns.text_pattern import TextPattern
from flaui.core.text_range import TextRange
from flaui.lib.exceptions import handle_csharp_exceptions

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement


class Text2Pattern(TextPattern):
    """Extends the Text pattern with caret and annotation range lookups."""

    @handle_csharp_exceptions
    def get_caret_range(self) -> Tuple[TextRange, bool]:
        """Return the text range of the caret and whether the caret is active.

        :return: A tuple ``(caret_range, is_active)``.
        """
        raw_range, is_active = self.raw_pattern.GetCaretRange()
        return TextRange(raw_text_range=raw_range), is_active

    @handle_csharp_exceptions
    def range_from_annotation(self, annotation: "AutomationElement") -> TextRange:
        """Return the text range associated with an annotation element.

        :param annotation: The annotation element.
        :return: A :class:`~flaui.core.text_range.TextRange` for the annotation.
        """
        return TextRange(raw_text_range=self.raw_pattern.RangeFromAnnotation(annotation.raw_element))
