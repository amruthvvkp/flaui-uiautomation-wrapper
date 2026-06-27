"""Facade over a FlaUI element's patterns, mirroring C# ``IFrameworkPatterns``.

This is the Python equivalent of ``element.Patterns`` in C#. Each accessor returns an
:class:`~flaui.core.patterns.automation_pattern.AutomationPattern`, so usage mirrors the C# API
one-to-one::

    element.patterns.value.pattern.value.value      # C#: element.Patterns.Value.Pattern.Value.Value
    element.patterns.toggle.is_supported             # C#: element.Patterns.Toggle.IsSupported

The underlying C# ``IFrameworkPatterns`` object remains reachable via :attr:`Patterns.raw_patterns`
as an escape hatch for patterns that are not yet wrapped.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from flaui.core.patterns.automation_pattern import AutomationPattern
from flaui.core.patterns.expand_collapse_pattern import ExpandCollapsePattern
from flaui.core.patterns.grid_pattern import GridPattern
from flaui.core.patterns.invoke_pattern import InvokePattern
from flaui.core.patterns.range_value_pattern import RangeValuePattern
from flaui.core.patterns.toggle_pattern import TogglePattern
from flaui.core.patterns.value_pattern import ValuePattern


class Patterns(BaseModel):
    """Provides typed access to the UI Automation patterns of an element."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_patterns: Any = Field(..., description="The underlying C# IFrameworkPatterns object")

    @property
    def invoke(self) -> AutomationPattern[InvokePattern]:
        """Access the Invoke pattern.

        :return: The Invoke pattern accessor.
        """
        return AutomationPattern[InvokePattern](
            raw_automation_pattern=self.raw_patterns.Invoke, pattern_type=InvokePattern
        )

    @property
    def toggle(self) -> AutomationPattern[TogglePattern]:
        """Access the Toggle pattern.

        :return: The Toggle pattern accessor.
        """
        return AutomationPattern[TogglePattern](
            raw_automation_pattern=self.raw_patterns.Toggle, pattern_type=TogglePattern
        )

    @property
    def value(self) -> AutomationPattern[ValuePattern]:
        """Access the Value pattern.

        :return: The Value pattern accessor.
        """
        return AutomationPattern[ValuePattern](
            raw_automation_pattern=self.raw_patterns.Value, pattern_type=ValuePattern
        )

    @property
    def range_value(self) -> AutomationPattern[RangeValuePattern]:
        """Access the RangeValue pattern.

        :return: The RangeValue pattern accessor.
        """
        return AutomationPattern[RangeValuePattern](
            raw_automation_pattern=self.raw_patterns.RangeValue, pattern_type=RangeValuePattern
        )

    @property
    def expand_collapse(self) -> AutomationPattern[ExpandCollapsePattern]:
        """Access the ExpandCollapse pattern.

        :return: The ExpandCollapse pattern accessor.
        """
        return AutomationPattern[ExpandCollapsePattern](
            raw_automation_pattern=self.raw_patterns.ExpandCollapse, pattern_type=ExpandCollapsePattern
        )

    @property
    def grid(self) -> AutomationPattern[GridPattern]:
        """Access the Grid pattern.

        :return: The Grid pattern accessor.
        """
        return AutomationPattern[GridPattern](raw_automation_pattern=self.raw_patterns.Grid, pattern_type=GridPattern)
