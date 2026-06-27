"""Python wrappers for FlaUI C# UI Automation patterns.

This package mirrors ``FlaUI.Core.Patterns``. The :class:`~flaui.core.patterns.patterns.Patterns`
facade (exposed as ``element.patterns``) gives typed, snake_case access to each pattern, matching
the C# ``element.Patterns.<Pattern>.Pattern`` shape. Each pattern wraps a native C# pattern object
reachable via :attr:`~flaui.core.patterns.pattern_base.PatternBase.raw_pattern`.

All UI Automation patterns from ``FlaUI.Core.Patterns`` are wrapped here.
"""

from flaui.core.patterns.annotation_pattern import AnnotationPattern
from flaui.core.patterns.automation_pattern import AutomationPattern
from flaui.core.patterns.dock_pattern import DockPattern
from flaui.core.patterns.drag_pattern import DragPattern
from flaui.core.patterns.drop_target_pattern import DropTargetPattern
from flaui.core.patterns.expand_collapse_pattern import ExpandCollapsePattern
from flaui.core.patterns.grid_item_pattern import GridItemPattern
from flaui.core.patterns.grid_pattern import GridPattern
from flaui.core.patterns.invoke_pattern import InvokePattern
from flaui.core.patterns.item_container_pattern import ItemContainerPattern
from flaui.core.patterns.legacy_i_accessible_pattern import LegacyIAccessiblePattern
from flaui.core.patterns.multiple_view_pattern import MultipleViewPattern
from flaui.core.patterns.object_model_pattern import ObjectModelPattern
from flaui.core.patterns.pattern_base import PatternBase
from flaui.core.patterns.patterns import Patterns
from flaui.core.patterns.range_value_pattern import RangeValuePattern
from flaui.core.patterns.scroll_item_pattern import ScrollItemPattern
from flaui.core.patterns.scroll_pattern import ScrollPattern
from flaui.core.patterns.selection2_pattern import Selection2Pattern
from flaui.core.patterns.selection_item_pattern import SelectionItemPattern
from flaui.core.patterns.selection_pattern import SelectionPattern
from flaui.core.patterns.spreadsheet_item_pattern import SpreadsheetItemPattern
from flaui.core.patterns.spreadsheet_pattern import SpreadsheetPattern
from flaui.core.patterns.styles_pattern import StylesPattern
from flaui.core.patterns.synchronized_input_pattern import SynchronizedInputPattern
from flaui.core.patterns.table_item_pattern import TableItemPattern
from flaui.core.patterns.table_pattern import TablePattern
from flaui.core.patterns.text2_pattern import Text2Pattern
from flaui.core.patterns.text_child_pattern import TextChildPattern
from flaui.core.patterns.text_edit_pattern import TextEditPattern
from flaui.core.patterns.text_pattern import TextPattern
from flaui.core.patterns.toggle_pattern import TogglePattern
from flaui.core.patterns.transform2_pattern import Transform2Pattern
from flaui.core.patterns.transform_pattern import TransformPattern
from flaui.core.patterns.value_pattern import ValuePattern
from flaui.core.patterns.virtualized_item_pattern import VirtualizedItemPattern
from flaui.core.patterns.window_pattern import WindowPattern

__all__ = [
    "AnnotationPattern",
    "AutomationPattern",
    "DockPattern",
    "DragPattern",
    "DropTargetPattern",
    "ExpandCollapsePattern",
    "GridItemPattern",
    "GridPattern",
    "InvokePattern",
    "ItemContainerPattern",
    "LegacyIAccessiblePattern",
    "MultipleViewPattern",
    "ObjectModelPattern",
    "PatternBase",
    "Patterns",
    "RangeValuePattern",
    "ScrollItemPattern",
    "ScrollPattern",
    "Selection2Pattern",
    "SelectionItemPattern",
    "SelectionPattern",
    "SpreadsheetItemPattern",
    "SpreadsheetPattern",
    "StylesPattern",
    "SynchronizedInputPattern",
    "TableItemPattern",
    "TablePattern",
    "Text2Pattern",
    "TextChildPattern",
    "TextEditPattern",
    "TextPattern",
    "TogglePattern",
    "Transform2Pattern",
    "TransformPattern",
    "ValuePattern",
    "VirtualizedItemPattern",
    "WindowPattern",
]
