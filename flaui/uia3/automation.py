"""Python wrapper for FlaUI.UIA3.UIA3Automation."""

from typing import Any, Optional

from FlaUI.UIA3 import UIA3Automation as CSUIA3Automation  # pyright: ignore

from flaui.core.automation_base import AutomationBase


class UIA3Automation(AutomationBase):
    """UIA3 automation stack; wraps a C# FlaUI.UIA3.UIA3Automation instance."""

    def __init__(self, raw_automation: Optional[Any] = None) -> None:
        """Create a UIA3 wrapper, constructing C# UIA3Automation when raw_automation is omitted.

        :param raw_automation: Existing C# UIA3Automation instance, or None to construct one
        """
        raw = CSUIA3Automation() if raw_automation is None else raw_automation
        super().__init__(raw_automation=raw)
