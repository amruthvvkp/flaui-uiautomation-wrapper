"""Wrapper for the UI Automation ExpandCollapse pattern (``IExpandCollapsePattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class ExpandCollapsePattern(PatternBase):
    """Represents the UI Automation ExpandCollapse pattern for controls that expand and collapse."""

    @property
    @handle_csharp_exceptions
    def expand_collapse_state(self) -> AutomationProperty:
        """Return the current expand/collapse state.

        :return: An :class:`AutomationProperty` wrapping the ``ExpandCollapseState`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ExpandCollapseState)

    @handle_csharp_exceptions
    def expand(self) -> None:
        """Expand the control."""
        self.raw_pattern.Expand()

    @handle_csharp_exceptions
    def collapse(self) -> None:
        """Collapse the control."""
        self.raw_pattern.Collapse()
