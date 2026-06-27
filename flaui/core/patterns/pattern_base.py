"""Base Pydantic model for FlaUI UI Automation pattern wrappers.

Mirrors the C# ``FlaUI.Core.Patterns.Infrastructure.PatternBase`` shape: every pattern wraps a
native C# pattern object and exposes its properties (as :class:`~flaui.core.automation_elements.AutomationProperty`)
and methods. The wrapped C# object is always reachable via :attr:`PatternBase.raw_pattern` as an
escape hatch for members that are not yet ported.
"""

from __future__ import annotations

import abc
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from flaui.lib.exceptions import PatternNotSupportedException


class PatternBase(BaseModel, abc.ABC):  # pragma: no cover
    """Base model wrapping a native C# FlaUI pattern object."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_pattern: Any = Field(..., description="The underlying C# FlaUI pattern object")

    @field_validator("raw_pattern")
    def validate_pattern_exists(cls, v: Any, info: ValidationInfo) -> Any:
        """Validate the native pattern object exists.

        :param v: Raw C# pattern object.
        :param info: Pydantic validation info.
        :raises PatternNotSupportedException: If the pattern object is ``None``.
        :return: The validated raw pattern object.
        """
        if v is None:
            raise PatternNotSupportedException("Pattern is not supported by this element")
        return v
