"""Pytest fixtures for the FlaUI for Python example suite.

Launches the bundled WPF test application once per session and hands each test a ready-to-use main
window and condition factory. This mirrors the structure of the project's own ``tests/`` suite, but
is trimmed down to a single self-contained example.
"""

from pathlib import Path
from typing import Generator

# isort: off  -- the bridge must be initialised before any C#-backed import is used.
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

from flaui.core.automation_elements import Window
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

# isort: on


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


@pytest.fixture(scope="session")
def automation() -> Generator[Automation, None, None]:
    """Launch the WPF test application for the whole session and dispose it afterwards.

    :yield: A ready ``Automation`` instance with the application launched.
    """
    auto = Automation(UIAutomationTypes.UIA3)
    auto.application.launch(str(find_test_app()))
    auto.application.wait_while_main_handle_is_missing(3000)
    try:
        yield auto
    finally:
        auto.application.kill()
        auto.automation_base.dispose()


@pytest.fixture
def main_window(automation: Automation) -> Window:
    """Return the application's main window.

    :param automation: The session automation instance.
    :return: The main ``Window`` of the test application.
    """
    return automation.application.get_main_window(automation)


@pytest.fixture
def condition_factory(automation: Automation) -> ConditionFactory:
    """Return the automation's condition factory for building search conditions.

    :param automation: The session automation instance.
    :return: The shared ``ConditionFactory``.
    """
    return automation.cf
