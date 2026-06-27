"""Wrapper for the UI Automation TextEdit pattern (``ITextEditPattern``)."""

from __future__ import annotations

from typing import Optional

from flaui.core.patterns.text_pattern import TextPattern
from flaui.core.text_range import TextRange
from flaui.lib.exceptions import handle_csharp_exceptions


class TextEditPattern(TextPattern):
    """Extends the Text pattern with access to in-progress text composition (IME) ranges."""

    @handle_csharp_exceptions
    def get_active_composition(self) -> Optional[TextRange]:
        """Return the text range of the active text composition, if any.

        :return: The active composition :class:`~flaui.core.text_range.TextRange`, or ``None``.
        """
        result = self.raw_pattern.GetActiveComposition()
        return None if result is None else TextRange(raw_text_range=result)

    @handle_csharp_exceptions
    def get_conversion_target(self) -> Optional[TextRange]:
        """Return the text range of the current conversion target, if any.

        :return: The conversion target :class:`~flaui.core.text_range.TextRange`, or ``None``.
        """
        result = self.raw_pattern.GetConversionTarget()
        return None if result is None else TextRange(raw_text_range=result)
