"""Covers tests listed under FlaUI GitHub repository - src\\FlaUI.Core.UITests\\ApplicationTests.cs"""

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import logging

logger = logging.getLogger(__name__)
import pytest


@pytest.mark.windows11
@pytest.mark.skip_notepad_on_win11(
    reason="Notepad has moved to the Windows Store framework on Windows 11; the Win32 notepad.exe "
    "may not launch reliably. Skipped on Windows 11 (see issue #89); use WinForms/WPF test "
    "applications for stable coverage."
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
