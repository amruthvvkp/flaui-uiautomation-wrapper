"""Wrapper for the C# ``IAutomationPattern<T>`` pattern accessor.

Mirrors ``FlaUI.Core.IAutomationPattern<T>``: it lazily materialises a pattern on an element and
reports whether the element supports it.
"""

from __future__ import annotations

from typing import Any, Generic, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from flaui.core.patterns.pattern_base import PatternBase

TPattern = TypeVar("TPattern", bound=PatternBase)


class AutomationPattern(BaseModel, Generic[TPattern]):
    """Provides access to a single pattern on an element, mirroring C# ``IAutomationPattern<T>``."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_automation_pattern: Any = Field(..., description="The underlying C# IAutomationPattern<T> object")
    pattern_type: Type[TPattern] = Field(..., description="Python wrapper class used to wrap the native pattern")

    @property
    def is_supported(self) -> bool:
        """Return whether the element supports this pattern.

        :return: ``True`` if the pattern is supported, else ``False``.
        """
        return self.raw_automation_pattern.IsSupported

    @property
    def pattern(self) -> TPattern:
        """Return the wrapped pattern, raising if the pattern is not supported.

        :return: The wrapped pattern instance.
        :raises PatternNotSupportedException: If the element does not support the pattern.
        """
        return self.pattern_type(raw_pattern=self.raw_automation_pattern.Pattern)

    @property
    def pattern_or_default(self) -> Optional[TPattern]:
        """Return the wrapped pattern, or ``None`` if the pattern is not supported.

        :return: The wrapped pattern instance, or ``None`` when unsupported.
        """
        raw = self.raw_automation_pattern.PatternOrDefault
        return None if raw is None else self.pattern_type(raw_pattern=raw)

    def try_get_pattern(self) -> Tuple[bool, Optional[TPattern]]:
        """Try to get the wrapped pattern.

        :return: A tuple ``(supported, pattern_or_none)``.
        """
        pattern = self.pattern_or_default
        return pattern is not None, pattern
