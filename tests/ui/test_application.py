"""Covers tests listed under FlaUI GitHub repository - src\\FlaUI.Core.UITests\\ApplicationTests.cs"""

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from loguru import logger
import pytest

from tests.test_utilities.os_platform import is_windows_11


@pytest.mark.windows11
@pytest.mark.xfail(
    is_windows_11,
    reason="Notepad has moved to Windows Store framework on Windows 11. "
    "The Win32 notepad.exe may not launch reliably or have different automation properties. "
    "Consider using test applications (WinForms/WPF) instead of Notepad for stable testing.",
)
def test_application() -> None:
    """Tests the application module.

    NOTE: This test uses notepad.exe which is unreliable on Windows 11.
    """
    app = Automation(UIAutomationTypes.UIA3)
    app.application.launch("notepad.exe")
    try:
        app.application.wait_while_main_handle_is_missing(5)
    except Exception as e:
        logger.error(f"An error occurred while waiting for the main handle: {e}")
        raise
    finally:
        app.application.close()
