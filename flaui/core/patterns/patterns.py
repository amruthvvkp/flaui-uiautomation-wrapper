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
from flaui.core.patterns.dock_pattern import DockPattern
from flaui.core.patterns.expand_collapse_pattern import ExpandCollapsePattern
from flaui.core.patterns.grid_item_pattern import GridItemPattern
from flaui.core.patterns.grid_pattern import GridPattern
from flaui.core.patterns.invoke_pattern import InvokePattern
from flaui.core.patterns.range_value_pattern import RangeValuePattern
from flaui.core.patterns.scroll_item_pattern import ScrollItemPattern
from flaui.core.patterns.scroll_pattern import ScrollPattern
from flaui.core.patterns.selection2_pattern import Selection2Pattern
from flaui.core.patterns.selection_item_pattern import SelectionItemPattern
from flaui.core.patterns.selection_pattern import SelectionPattern
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
from flaui.core.patterns.window_pattern import WindowPattern


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

    @property
    def grid_item(self) -> AutomationPattern[GridItemPattern]:
        """Access the GridItem pattern.

        :return: The GridItem pattern accessor.
        """
        return AutomationPattern[GridItemPattern](
            raw_automation_pattern=self.raw_patterns.GridItem, pattern_type=GridItemPattern
        )

    @property
    def table(self) -> AutomationPattern[TablePattern]:
        """Access the Table pattern.

        :return: The Table pattern accessor.
        """
        return AutomationPattern[TablePattern](
            raw_automation_pattern=self.raw_patterns.Table, pattern_type=TablePattern
        )

    @property
    def table_item(self) -> AutomationPattern[TableItemPattern]:
        """Access the TableItem pattern.

        :return: The TableItem pattern accessor.
        """
        return AutomationPattern[TableItemPattern](
            raw_automation_pattern=self.raw_patterns.TableItem, pattern_type=TableItemPattern
        )

    @property
    def scroll(self) -> AutomationPattern[ScrollPattern]:
        """Access the Scroll pattern.

        :return: The Scroll pattern accessor.
        """
        return AutomationPattern[ScrollPattern](
            raw_automation_pattern=self.raw_patterns.Scroll, pattern_type=ScrollPattern
        )

    @property
    def scroll_item(self) -> AutomationPattern[ScrollItemPattern]:
        """Access the ScrollItem pattern.

        :return: The ScrollItem pattern accessor.
        """
        return AutomationPattern[ScrollItemPattern](
            raw_automation_pattern=self.raw_patterns.ScrollItem, pattern_type=ScrollItemPattern
        )

    @property
    def selection(self) -> AutomationPattern[SelectionPattern]:
        """Access the Selection pattern.

        :return: The Selection pattern accessor.
        """
        return AutomationPattern[SelectionPattern](
            raw_automation_pattern=self.raw_patterns.Selection, pattern_type=SelectionPattern
        )

    @property
    def selection2(self) -> AutomationPattern[Selection2Pattern]:
        """Access the Selection2 pattern.

        :return: The Selection2 pattern accessor.
        """
        return AutomationPattern[Selection2Pattern](
            raw_automation_pattern=self.raw_patterns.Selection2, pattern_type=Selection2Pattern
        )

    @property
    def selection_item(self) -> AutomationPattern[SelectionItemPattern]:
        """Access the SelectionItem pattern.

        :return: The SelectionItem pattern accessor.
        """
        return AutomationPattern[SelectionItemPattern](
            raw_automation_pattern=self.raw_patterns.SelectionItem, pattern_type=SelectionItemPattern
        )

    @property
    def text(self) -> AutomationPattern[TextPattern]:
        """Access the Text pattern.

        :return: The Text pattern accessor.
        """
        return AutomationPattern[TextPattern](raw_automation_pattern=self.raw_patterns.Text, pattern_type=TextPattern)

    @property
    def text2(self) -> AutomationPattern[Text2Pattern]:
        """Access the Text2 pattern.

        :return: The Text2 pattern accessor.
        """
        return AutomationPattern[Text2Pattern](
            raw_automation_pattern=self.raw_patterns.Text2, pattern_type=Text2Pattern
        )

    @property
    def text_edit(self) -> AutomationPattern[TextEditPattern]:
        """Access the TextEdit pattern.

        :return: The TextEdit pattern accessor.
        """
        return AutomationPattern[TextEditPattern](
            raw_automation_pattern=self.raw_patterns.TextEdit, pattern_type=TextEditPattern
        )

    @property
    def text_child(self) -> AutomationPattern[TextChildPattern]:
        """Access the TextChild pattern.

        :return: The TextChild pattern accessor.
        """
        return AutomationPattern[TextChildPattern](
            raw_automation_pattern=self.raw_patterns.TextChild, pattern_type=TextChildPattern
        )

    @property
    def window(self) -> AutomationPattern[WindowPattern]:
        """Access the Window pattern.

        :return: The Window pattern accessor.
        """
        return AutomationPattern[WindowPattern](
            raw_automation_pattern=self.raw_patterns.Window, pattern_type=WindowPattern
        )

    @property
    def transform(self) -> AutomationPattern[TransformPattern]:
        """Access the Transform pattern.

        :return: The Transform pattern accessor.
        """
        return AutomationPattern[TransformPattern](
            raw_automation_pattern=self.raw_patterns.Transform, pattern_type=TransformPattern
        )

    @property
    def transform2(self) -> AutomationPattern[Transform2Pattern]:
        """Access the Transform2 pattern.

        :return: The Transform2 pattern accessor.
        """
        return AutomationPattern[Transform2Pattern](
            raw_automation_pattern=self.raw_patterns.Transform2, pattern_type=Transform2Pattern
        )

    @property
    def dock(self) -> AutomationPattern[DockPattern]:
        """Access the Dock pattern.

        :return: The Dock pattern accessor.
        """
        return AutomationPattern[DockPattern](raw_automation_pattern=self.raw_patterns.Dock, pattern_type=DockPattern)
