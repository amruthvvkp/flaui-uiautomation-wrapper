"""Gallery: automate Notepad - write text, read it back, then discard it.

Works with both the classic Win32 Notepad (Windows 10) and the Store Notepad (Windows 11). On
Windows 11 ``notepad.exe`` is only a stub that hands off to the Store app and exits, so instead of
trusting the launched process we look the window up on the desktop by its class name.

Run it from the project root::

    uv run python examples/scripts/notepad.py
"""

from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()  # must run before any C#-backed FlaUI import

from flaui.core.definitions import ControlType
from flaui.core.tools import Retry
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


def main() -> None:
    """Open Notepad, write into it, verify the text, and close it without saving."""
    with Automation(UIAutomationTypes.UIA3) as automation:
        cf = automation.cf
        desktop = automation.automation_base.get_desktop()
        automation.application.launch("notepad.exe")

        # Classic and Store Notepad both use the top-level window class "Notepad".
        # `find_first_child` raises ElementNotFound until the window exists, so retry while it raises.
        window = Retry.WhileException(
            lambda: desktop.find_first_child(cf.by_class_name("Notepad")),
            timeout=10000,
            throw_on_timeout=True,
            timeout_message="Notepad window did not appear",
        ).as_window()
        window.focus()

        # Classic Notepad exposes an Edit control; Store Notepad a Document. Take whichever exists.
        editor = window.find_first_descendant(
            cf.by_control_type(ControlType.Document) | cf.by_control_type(ControlType.Edit)
        )
        # Set the text through the Value pattern: no keystrokes, so nothing else on the desktop can
        # interleave with it. Use `Keyboard.type(...)` instead when you need real key events.
        text_box = editor.as_text_box()
        text_box.text = "Hello from FlaUI for Python"
        print("Notepad says:", text_box.text)
        assert text_box.text == "Hello from FlaUI for Python", text_box.text

        # Empty the document again so closing neither prompts to save nor restores the text next time.
        text_box.text = ""
        window.close()


if __name__ == "__main__":
    main()
