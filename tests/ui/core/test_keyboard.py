"""Tests for keyboard input functionality, ported from C# KeyboardTests.cs."""

import time

from flaui.core.application import Application
from flaui.lib.keyboard import Keyboard, VirtualKeyShort
from flaui.modules.automation import Automation


class TestKeyboard:
    """Tests for keyboard input operations."""

    def test_keyboard_typing(self, automation: Automation) -> None:
        """Test various keyboard typing operations including special characters and keys.

        Ported from KeyboardTests.cs::KeyboardTest
        """
        app = Application.launch("notepad.exe")
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

            # Close window without saving
            window.close()
            time.sleep(0.5)
            
            # Handle "Don't Save" dialog if it appears
            try:
                dialog = window.find_first_child(
                    window.condition_factory.by_control_type_and_name(
                        from flaui.core.definitions import ControlType
                        ControlType.Window,
                        "Notepad"
                    )
                )
                if dialog is not None:
                    dont_save_button = dialog.find_first_child(
                        dialog.condition_factory.by_name("Don't Save")
                    )
                    if dont_save_button is not None:
                        dont_save_button.click()
            except Exception:
                pass

        finally:
            try:
                app.dispose()
            except Exception:
                pass
