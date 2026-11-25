"""This module contains the wrapper for FlaUI's UIAutomation class. This class is a custom class designed to ease the usage of FlaUI's UIAutomation class in Python."""

import logging
from typing import Any, Optional

from flaui.core.application import Application
from flaui.core.automation_base import AutomationBase
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.uia2 import UIA2Automation
from flaui.uia3 import UIA3Automation

logger = logging.getLogger(__name__)


class Automation:
    """UIAutomation constructed wrapper for FlaUI usage.

    FlaUI is written entirely on C# .Net, using it directly inside an IDE within a Python project
    would be painful since intellisense does not pick up the methods/typing hints.

    This class is designed to overcome those challenges by providing Python compatible workstream.

    Attributes:
        ui_automation_type (UIAutomationTypes): The type of UI automation to use (UIA2 or UIA3).
        timeout (Optional[int]): Milliseconds ``application.get_main_window`` waits for the main window;
            ``None`` uses the ``FLAUI_MAIN_WINDOW_TIMEOUT`` setting / built-in default.
        automation_base (AutomationBase): Python facade for the C# automation (preferred for typed APIs).
        cs_automation (Any): Raw C# UIA2Automation or UIA3Automation (interop and backward compatibility).
        cf (ConditionFactory): The condition factory instance.
        tree_walker (RawViewWalker): The tree walker instance.
        application (Application): The application instance.
    """

    def __init__(self, ui_automation_type: UIAutomationTypes, timeout: Optional[int] = None) -> None:
        """Initializes the UIAutomation wrapper.

        :param ui_automation_type: The type of UI automation to use (UIA2 or UIA3).
        :param timeout: Milliseconds ``application.get_main_window`` waits for the main window. ``None``
            (default) uses ``FLAUI_MAIN_WINDOW_TIMEOUT``, else 7000 ms (20000 ms when ``CI`` is set).
        """
        self._ui_automation_types: UIAutomationTypes = ui_automation_type
        self.timeout: Optional[int] = timeout
        self.automation_base: AutomationBase = (
            UIA3Automation() if ui_automation_type == UIAutomationTypes.UIA3 else UIA2Automation()
        )
        self.cs_automation: Any = self.automation_base.raw_automation
        self.cf = ConditionFactory(raw_cf=self.cs_automation.ConditionFactory)
        self.tree_walker: Any = self.cs_automation.TreeWalkerFactory.GetRawViewWalker()
        self.application: Application = Application()

    def __enter__(self) -> "Automation":
        """Enter the runtime context and return the automation instance.

        Enables ``with Automation(UIAutomationTypes.UIA3) as auto:`` usage. The managed application
        is closed and the underlying C# automation is disposed automatically on exit.

        :return: This automation instance.
        """
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Exit the runtime context, closing the application and disposing the automation.

        Never raises — cleanup failures are swallowed so they cannot mask an exception raised inside
        the ``with`` block.

        :param exc_type: The exception type raised in the context, if any.
        :param exc_value: The exception instance raised in the context, if any.
        :param traceback: The traceback for the exception, if any.
        """
        try:
            self.application.__exit__(exc_type, exc_value, traceback)
        except Exception:
            logger.debug("Application cleanup failed during automation context exit", exc_info=True)
        try:
            self.automation_base.dispose()
        except Exception:
            logger.debug("Automation dispose failed during context exit", exc_info=True)
