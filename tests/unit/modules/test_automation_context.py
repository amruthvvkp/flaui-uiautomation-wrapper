"""Unit tests for the Automation context-manager lifecycle."""

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


def test_enter_returns_self() -> None:
    """__enter__ returns the automation instance for use in a with-block."""
    auto = Automation(UIAutomationTypes.UIA3)
    with auto as entered:
        assert entered is auto


def test_exit_disposes_without_error() -> None:
    """__exit__ disposes the automation base and closes the app without raising."""
    auto = Automation(UIAutomationTypes.UIA3)
    # Nothing was launched, so this should clean up the automation base quietly.
    assert auto.__exit__(None, None, None) is None
