"""This module contains the wrapper for FlaUI's UIAutomation class. This class is a custom class designed to ease the usage of FlaUI's UIAutomation class in Python."""

from typing import Any

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

    Attributes:
        ui_automation_type (UIAutomationTypes): The type of UI automation to use (UIA2 or UIA3).
        timeout (int): The timeout value in milliseconds.
        automation (UIA2Automation or UIA3Automation): The UI automation instance.
        cf (ConditionFactory): The condition factory instance.
        tree_walker (RawViewWalker): The tree walker instance.
        application (Application): The application instance.
    """

    def __init__(self, ui_automation_type: UIAutomationTypes, timeout: int = 1000) -> None:
        """Initializes the UIAutomation wrapper.

        :param ui_automation_type: The type of UI automation to use (UIA2 or UIA3).
        :param timeout: The timeout value in milliseconds.
        :param element_map: The element map instance, map of the entire application elements for reference.
        """
        self._ui_automation_types: UIAutomationTypes = ui_automation_type
        self.timeout: int = timeout
        self.cs_automation: Any = UIA3Automation() if ui_automation_type == UIAutomationTypes.UIA3 else UIA2Automation()
        self.cf = ConditionFactory(raw_cf=self.cs_automation.ConditionFactory)
        self.tree_walker: Any = self.cs_automation.TreeWalkerFactory.GetRawViewWalker()
        self.application: Application = Application()
