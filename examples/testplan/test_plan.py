"""Testplan example driving the bundled WPF test application with FlaUI for Python.

Run it from the project root::

    uv pip install testplan
    uv run python examples/testplan/test_plan.py

The suite launches the application in ``setup``, runs three test cases against the Simple Controls
tab, and disposes the application in ``teardown``.
"""

import sys
from pathlib import Path

# The bridge must be initialised before any C#-backed FlaUI type is used.
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from testplan import test_plan
from testplan.testing.multitest import MultiTest, testcase, testsuite


def _find_test_app() -> Path:
    """Locate the bundled WPF test application by walking up from this file.

    :raises FileNotFoundError: If the bundled executable cannot be found.
    :return: The path to ``WpfApplication.exe``.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "test_applications" / "WPFApplication" / "WpfApplication.exe"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not locate the bundled WPF test application under test_applications/.")


@testsuite
class SimpleControlsSuite:
    """Drive a handful of controls on the WPF Simple Controls tab."""

    def setup(self, env, result) -> None:
        """Launch the application and resolve the main window before the test cases run.

        :param env: The Testplan environment.
        :param result: The Testplan result collector.
        """
        self.automation = Automation(UIAutomationTypes.UIA3)
        self.automation.application.launch(str(_find_test_app()))
        self.automation.application.wait_while_main_handle_is_missing(3000)
        self.window = self.automation.application.get_main_window(self.automation)
        self.cf = self.automation.cf

    def teardown(self, env, result) -> None:
        """Kill and dispose the application after the test cases run.

        :param env: The Testplan environment.
        :param result: The Testplan result collector.
        """
        self.automation.application.kill()
        self.automation.automation_base.dispose()

    @testcase
    def window_title(self, env, result) -> None:
        """The launched application exposes its title.

        :param env: The Testplan environment.
        :param result: The Testplan result collector.
        """
        result.equal(self.window.title, "FlaUI WPF Test App", description="window title")

    @testcase
    def enter_text(self, env, result) -> None:
        """Typing into the text box round-trips through the ``text`` property.

        :param env: The Testplan environment.
        :param result: The Testplan result collector.
        """
        text_box = self.window.find_first_descendant(condition=self.cf.by_automation_id("TextBox")).as_text_box()
        text_box.text = "hello from testplan"
        result.equal(text_box.text, "hello from testplan", description="text entered")

    @testcase
    def toggle_checkbox(self, env, result) -> None:
        """Toggling the checkbox flips its state; the original state is restored.

        :param env: The Testplan environment.
        :param result: The Testplan result collector.
        """
        checkbox = self.window.find_first_descendant(condition=self.cf.by_name("Test Checkbox")).as_check_box()
        original = checkbox.is_checked
        checkbox.toggle()
        result.not_equal(checkbox.is_checked, original, description="checkbox toggled")
        checkbox.toggle()  # leave the shared application as we found it


@test_plan(name="FlaUI for Python TestPlan example")
def main(plan) -> None:
    """Assemble the plan from the single multitest.

    :param plan: The Testplan plan object provided by the ``@test_plan`` decorator.
    """
    plan.add(MultiTest(name="WPF Simple Controls", suites=[SimpleControlsSuite()]))


if __name__ == "__main__":
    sys.exit(not main())
