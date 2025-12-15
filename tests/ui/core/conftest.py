"""Fixtures for standalone application tests (non-parametrized)."""

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
