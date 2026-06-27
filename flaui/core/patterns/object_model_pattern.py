"""Wrapper for the UI Automation ObjectModel pattern (``IObjectModelPattern``)."""

from __future__ import annotations

from typing import Any

from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class ObjectModelPattern(PatternBase):
    """Represents the UI Automation ObjectModel pattern, exposing a control's underlying object model."""

    @handle_csharp_exceptions
    def get_underlying_object_model(self) -> Any:
        """Return the control's underlying object model.

        :return: The native object model (a COM/.NET object specific to the control).
        """
        return self.raw_pattern.GetUnderlyingObjectModel()
