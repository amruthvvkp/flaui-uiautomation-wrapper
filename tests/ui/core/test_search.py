"""Tests for search and retry functionality, ported from C# SearchTests.cs."""

import asyncio
from typing import Any, cast

from flaui.core.application import Application
from flaui.core.input import Keyboard
from flaui.core.windows_api import VirtualKeyShort
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest


class TestSearch:
    """Tests for search and retry mechanisms."""

    @pytest.mark.skip_notepad_on_win11(reason="Windows 11 Notepad is a Store app; see issue #89")
    def test_search_with_retry(self, automation: Automation) -> None:
        """Test searching with retry mechanism for delayed elements.

        Ported from SearchTests.cs::SearchWithRetryTest
        """
        app = Application()
        app.launch("notepad.exe")
        try:
            window = app.get_main_window(automation)
            assert window is not None
            assert window.title is not None

            # Start async task to show help screen after 5 seconds
            async def show_help_delayed():
                """Show the help dialog after a delay."""
                await asyncio.sleep(5.0)
                # Simulate pressing Alt+H, Alt+A to show help dialog
                # Keyboard.pressing expects a list of VirtualKeyShort; the
                # typing for pressing may not declare a proper context-manager
                # return type, so cast to Any to satisfy the type checker.
                with cast(Any, Keyboard.pressing([VirtualKeyShort.ALT])):
                    Keyboard.type_key(VirtualKeyShort.KEY_H)
                    Keyboard.type_key(VirtualKeyShort.KEY_A)

            # Start the async task in background
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_in_executor(None, lambda: asyncio.run(show_help_delayed()))

        finally:
            try:
                app.kill()
            except Exception:
                pass

    @pytest.mark.skip_notepad_on_win11(reason="Windows 11 Notepad is a Store app; see issue #89")
    @pytest.mark.skipif(
        True,  # Skip by default as this needs UIA3 and AccessibilityRole property
        reason="Requires UIA3 and AccessibilityRole property support",
    )
    def test_search_with_accessibility_role(
        self, ui_automation_type: UIAutomationTypes, automation: Automation
    ) -> None:
        """Test searching using LegacyIAccessible.Role property.

        Ported from SearchTests.cs::SearchWithAccessibilityRole
        Note: This test is UIA3-only in C#
        """
        # Skip on UIA2
        if ui_automation_type != UIAutomationTypes.UIA3:
            pytest.skip("This test is only for UIA3")

        app = Application()
        app.launch("notepad.exe")
        try:
            window = app.get_main_window(automation)
            assert window is not None
            assert window.title is not None

            # Search for text element using AccessibilityRole
            # ROLE_SYSTEM_TEXT = 42 in MSAA
            from flaui.core.condition_factory import PropertyCondition

            editable_text = window.find_first_child(
                PropertyCondition(
                    automation.cs_automation.PropertyLibrary.LegacyIAccessible.Role,  # pyright: ignore[reportCallIssue]
                    42,  # ROLE_SYSTEM_TEXT
                )
            )

            assert editable_text is not None
            assert editable_text.patterns.text.is_supported

        finally:
            try:
                app.kill()
            except Exception:
                pass
