"""Covers tests listed under FlaUI GitHub repository - src\\FlaUI.Core.UITests\\ApplicationTests.cs"""

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.test_utilities.os_platform import is_windows_11


@pytest.mark.xfail(
    is_windows_11, reason="Notepad is not a valid application for testing, it fails on Windows 11 at times."
)
def test_application() -> None:
    """Tests the application module."""
    app = Automation(UIAutomationTypes.UIA3)
    app.application.launch("notepad.exe")
    try:
        app.application.wait_while_main_handle_is_missing(5)
    except Exception as e:
        print(f"An error occurred while waiting for the main handle: {e}")
        raise
    finally:
        app.application.close()
