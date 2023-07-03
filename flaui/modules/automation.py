from FlaUI.UIA2 import UIA2Automation  # pyright: ignore
from FlaUI.UIA3 import UIA3Automation  # pyright: ignore

from flaui.core.application import Application
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes

class Automation:
    """UIAutomation constructed wrapper for FlaUI usage.

    FlaUI is written entirely on C# .Net, using it directly inside an IDE within a Python project
    would be painful since intellisense does not pick up the methods/typing hints.

    This class is designed to overcome those challenges by providing Python compatible workstream.
    """

    def __init__(self, ui_automation_type: UIAutomationTypes, timeout: int = 1000) -> None:
        self._ui_automation_types = ui_automation_type
        self.timeout = timeout
        self.automation = UIA3Automation() if ui_automation_type == UIAutomationTypes.UIA3 else UIA2Automation()
        self.cf = ConditionFactory(raw_cf=self.automation.ConditionFactory)
        self.tree_walker = self.automation.TreeWalkerFactory.GetRawViewWalker()
        self.application: Application = Application()
