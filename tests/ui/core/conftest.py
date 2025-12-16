"""Fixtures for standalone application tests (non-parametrized)."""

import sys
from typing import Generator

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest


@pytest.fixture(scope="function")
def automation() -> Automation:
    """Provide UIA3 automation for standalone tests.

    These tests use external apps like Notepad, Paint, Calculator
    which aren't part of the parametrized test matrix.

    :return: UIA3 Automation instance
    """
    return Automation(UIAutomationTypes.UIA3)


@pytest.fixture(scope="module")
def notepad_app() -> Generator[Application, None, None]:
    """Launch Notepad for module-scoped tests and ensure teardown.

    Auto-skips on Windows 11 where Notepad is a Store app (see #89).
    """
    try:
        if sys.getwindowsversion().build >= 22000:  # type: ignore[attr-defined]
            pytest.skip("Windows 11 Notepad is a Store app; see issue #89")
    except Exception:
        pass

    app = Application()
    app.launch("notepad.exe")
    try:
        yield app
    finally:
        try:
            app.close()
        except Exception:
            pass


@pytest.fixture(scope="function")
def notepad_window(notepad_app: Application, automation: Automation) -> Window:
    """Return the Notepad main window using shared Application and Automation."""
    return notepad_app.get_main_window(automation)
