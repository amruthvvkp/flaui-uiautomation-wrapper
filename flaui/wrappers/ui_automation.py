
from typing import Any, Optional

from flaui.lib.enums import UIAutomationTypes
from FlaUI.UIA2 import UIA2Automation  # pyright: ignore
from FlaUI.UIA3 import UIA3Automation  # pyright: ignore


class UIAutomation:
    """UIAutomation constructed wrapper for FlaUI DLL

    FlaUI is written entirely on C# .Net, using it directly inside an IDE within a Python project
    would be painful since intellisense does not pick up the methods/typing hints.
    This class is designed to overcome those challenges by providing Python compatible workstream.
    """

    def __init__(self, ui_automation_types: UIAutomationTypes, timeout: int = 1000) -> None:
        assert isinstance(ui_automation_types, UIAutomationTypes)
        self._ui_automation_types = ui_automation_types
        self.timeout = timeout
        self.automation = UIA3Automation(
        ) if ui_automation_types == UIAutomationTypes.UIA3 else UIA2Automation()
        self.cf = self.automation.ConditionFactory
        self.tree_walker = self.automation.TreeWalkerFactory.GetRawViewWalker()
        self.application: Optional[Any] = None
        self.main_window: Optional['Any'] = None
