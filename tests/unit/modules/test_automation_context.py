"""Unit tests for the Automation context-manager lifecycle."""

from unittest.mock import MagicMock

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


def test_exit_swallows_application_cleanup_failure() -> None:
    """A failing application cleanup is logged and swallowed so it never masks an inner error."""
    auto = Automation(UIAutomationTypes.UIA3)
    auto.application = MagicMock()
    auto.application.__exit__.side_effect = RuntimeError("app cleanup failed")
    auto.automation_base = MagicMock()

    assert auto.__exit__(None, None, None) is None
    auto.application.__exit__.assert_called_once()
    auto.automation_base.dispose.assert_called_once_with()


def test_exit_swallows_automation_dispose_failure() -> None:
    """A failing automation dispose is logged and swallowed without raising."""
    auto = Automation(UIAutomationTypes.UIA3)
    auto.application = MagicMock()
    auto.automation_base = MagicMock()
    auto.automation_base.dispose.side_effect = RuntimeError("dispose failed")

    assert auto.__exit__(None, None, None) is None
    auto.automation_base.dispose.assert_called_once_with()
