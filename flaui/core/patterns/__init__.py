"""Python wrappers for FlaUI C# UI Automation patterns.

This package mirrors ``FlaUI.Core.Patterns``. The :class:`~flaui.core.patterns.patterns.Patterns`
facade (exposed as ``element.patterns``) gives typed, snake_case access to each pattern, matching
the C# ``element.Patterns.<Pattern>.Pattern`` shape. Each pattern wraps a native C# pattern object
reachable via :attr:`~flaui.core.patterns.pattern_base.PatternBase.raw_pattern`.

Patterns are ported incrementally by family; this module re-exports the ones available so far.
"""

from flaui.core.patterns.automation_pattern import AutomationPattern
from flaui.core.patterns.expand_collapse_pattern import ExpandCollapsePattern
from flaui.core.patterns.grid_item_pattern import GridItemPattern
from flaui.core.patterns.grid_pattern import GridPattern
from flaui.core.patterns.invoke_pattern import InvokePattern
from flaui.core.patterns.pattern_base import PatternBase
from flaui.core.patterns.patterns import Patterns
from flaui.core.patterns.range_value_pattern import RangeValuePattern
from flaui.core.patterns.scroll_item_pattern import ScrollItemPattern
from flaui.core.patterns.scroll_pattern import ScrollPattern
from flaui.core.patterns.selection2_pattern import Selection2Pattern
from flaui.core.patterns.selection_item_pattern import SelectionItemPattern
from flaui.core.patterns.selection_pattern import SelectionPattern
from flaui.core.patterns.table_item_pattern import TableItemPattern
from flaui.core.patterns.table_pattern import TablePattern
from flaui.core.patterns.toggle_pattern import TogglePattern
from flaui.core.patterns.value_pattern import ValuePattern

__all__ = [
    "AutomationPattern",
    "ExpandCollapsePattern",
    "GridItemPattern",
    "GridPattern",
    "InvokePattern",
    "PatternBase",
    "Patterns",
    "RangeValuePattern",
    "ScrollItemPattern",
    "ScrollPattern",
    "Selection2Pattern",
    "SelectionItemPattern",
    "SelectionPattern",
    "TableItemPattern",
    "TablePattern",
    "TogglePattern",
    "ValuePattern",
]
