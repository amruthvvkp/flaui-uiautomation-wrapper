"""Covers tests listed under FlaUI GitHub repository - src\\FlaUI.Core.UITests\\ApplicationTests.cs"""

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


def test_dispose_when_closed(ui_automation_type: UIAutomationTypes):
    """Tests that the application is disposed when closed.

    params: ui_automation_type (UIAutomationTypes): The UIAutomationType to use.
    """
    automation = Automation(ui_automation_type)
    application = automation.application
    application.launch("notepad.exe")
    # application.wait_while_main_handle_is_missing(10) # TODO: uncomment this after including System.TimeSpan in FlaUI
    application.close()
