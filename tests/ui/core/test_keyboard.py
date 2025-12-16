"""Tests for keyboard input functionality, ported from C# KeyboardTests.cs."""

import time

from flaui.core.application import Application
from flaui.core.input import Keyboard
from flaui.core.windows_api import VirtualKeyShort
from flaui.modules.automation import Automation
import pytest


class TestKeyboard:
    """Tests for keyboard input operations."""

    @pytest.mark.skip_notepad_on_win11(reason="Windows 11 Notepad is a Store app; see issue #89")
    def test_keyboard_typing(self, automation: Automation) -> None:
        """Test various keyboard typing operations including special characters and keys.

        Ported from KeyboardTests.cs::KeyboardTest
        """
        app = Application()
        app.launch("notepad.exe")
        try:
            window = app.get_main_window(automation)
            assert window is not None

            # Type various characters including special ones
            Keyboard.type("ééééééööööö aaa | ")

            # Type virtual keys
            Keyboard.type_key(VirtualKeyShort.KEY_Z)
            Keyboard.type_key(VirtualKeyShort.LEFT)
            Keyboard.type_key(VirtualKeyShort.DELETE)
            Keyboard.type_key(VirtualKeyShort.KEY_Y)
            Keyboard.type_key(VirtualKeyShort.BACK)
            Keyboard.type_key(VirtualKeyShort.KEY_X)

            Keyboard.type(" | ")

            # Type non-Latin characters (Bengali script)
            Keyboard.type("ঋ ঌ এ ঐ ও ঔ ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ")

            time.sleep(0.5)

            # Close window - force kill since we have unsaved content
            # Using kill() avoids the "Save changes?" dialog that blocks graceful close
            window.close()
            time.sleep(0.3)

        finally:
            # Force kill to avoid blocking on save dialog
            try:
                app.kill()
            except Exception:
                pass
