"""Wrapper for the UI Automation Spreadsheet pattern (``ISpreadsheetPattern``)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement


class SpreadsheetPattern(PatternBase):
    """Represents the UI Automation Spreadsheet pattern for accessing cells by name."""

    @handle_csharp_exceptions
    def get_item_by_name(self, name: str) -> AutomationElement:
        """Return the spreadsheet cell with the given name.

        :param name: The name of the cell (e.g. ``"A1"``).
        :return: The matching :class:`~flaui.core.automation_elements.AutomationElement`.
        """
        from flaui.core.automation_elements import AutomationElement

        return AutomationElement(raw_element=self.raw_pattern.GetItemByName(name))
