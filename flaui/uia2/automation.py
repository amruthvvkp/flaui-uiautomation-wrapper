"""Python wrapper for FlaUI.UIA2.UIA2Automation."""

from typing import Any, Optional

from FlaUI.UIA2 import UIA2Automation as CSUIA2Automation  # pyright: ignore

from flaui.core.automation_base import AutomationBase


class UIA2Automation(AutomationBase):
    """UIA2 automation stack; wraps a C# FlaUI.UIA2.UIA2Automation instance."""

    def __init__(self, raw_automation: Optional[Any] = None) -> None:
        """Create a UIA2 wrapper, constructing C# UIA2Automation when raw_automation is omitted.

        :param raw_automation: Existing C# UIA2Automation instance, or None to construct one
        """
        raw = CSUIA2Automation() if raw_automation is None else raw_automation
        super().__init__(raw_automation=raw)
