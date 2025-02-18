"""Covers tests listed under FlaUI GitHub repository - src\\FlaUI.Core.UITests\\ApplicationTests.cs"""

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest


@pytest.xfail(reason="Notepad is not a valid application for testing, it fails on Windows 11 at times.")
def test_application() -> None:
    """Tests the application module."""
    app = Automation(UIAutomationTypes.UIA3)
    app.application.launch("notepad.exe")
    app.application.wait_while_main_handle_is_missing()
    app.application.close()
