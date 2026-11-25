"""Example ``unittest`` suite driving the bundled WPF test application with FlaUI for Python.

Uses only the standard library's ``unittest``. Run it from the project root::

    uv run python -m unittest discover -s examples/unittest -v

``setUpClass`` launches the application once for the class and ``tearDownClass`` disposes it, the
``unittest`` equivalent of the session fixture in the pytest example.
"""

from pathlib import Path
import unittest

# The bridge must be initialised before any C#-backed FlaUI type is used.
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

from flaui.core.automation_elements import Window
from flaui.core.condition_factory import ConditionFactory
from flaui.core.definitions import ToggleState
from flaui.core.tools import Retry
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


def find_test_app() -> Path:
    """Locate the bundled WPF test application by walking up from this file.

    :raises FileNotFoundError: If the bundled executable cannot be found.
    :return: The path to ``WpfApplication.exe``.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "test_applications" / "WPFApplication" / "WpfApplication.exe"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not locate the bundled WPF test application under test_applications/.")


class SimpleControlsTest(unittest.TestCase):
    """Find → wrap → act against the Simple Controls tab."""

    automation: Automation
    window: Window
    cf: ConditionFactory

    @classmethod
    def setUpClass(cls) -> None:
        """Launch the application once for every test in this class."""
        cls.automation = Automation(UIAutomationTypes.UIA3)
        cls.automation.application.launch(str(find_test_app()))
        cls.automation.application.wait_while_main_handle_is_missing(3000)
        cls.window = cls.automation.application.get_main_window(cls.automation)
        cls.cf = cls.automation.cf

    @classmethod
    def tearDownClass(cls) -> None:
        """Kill the application and dispose the automation."""
        cls.automation.application.kill()
        cls.automation.automation_base.dispose()

    def test_window_title(self) -> None:
        """The launched application exposes its title."""
        self.assertEqual(self.window.title, "FlaUI WPF Test App")

    def test_enter_text(self) -> None:
        """Setting the text box's text round-trips through the ``text`` property."""
        text_box = self.window.find_first_descendant(self.cf.by_automation_id("TextBox")).as_text_box()
        text_box.text = "hello from unittest"
        self.assertEqual(text_box.text, "hello from unittest")

    def test_invoke_button(self) -> None:
        """Invoking the button renames it, proving the Invoke pattern fired."""
        button = self.window.find_first_descendant(self.cf.by_automation_id("InvokableButton")).as_button()
        button.invoke()
        self.assertTrue(Retry.WhileFalse(lambda: button.name == "Invoked!", timeout=2000))

    def test_toggle_checkbox(self) -> None:
        """Toggling flips the state; ``addCleanup`` restores it for the next test."""
        checkbox = self.window.find_first_descendant(self.cf.by_name("Test Checkbox")).as_check_box()
        original = checkbox.toggle_state
        checkbox.toggle()
        self.addCleanup(lambda: checkbox.toggle() if checkbox.toggle_state != original else None)
        self.assertNotEqual(checkbox.toggle_state, original)
        self.assertIsInstance(checkbox.toggle_state, ToggleState)


if __name__ == "__main__":
    unittest.main()
