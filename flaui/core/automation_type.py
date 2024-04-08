"""Enums for handling the automation type."""

from enum import Enum

from FlaUI.Core import AutomationType as CSAutomationType  # pyright: ignore


class AutomationType(Enum):
    """Enums for handling the automation type."""

    UIA2 = CSAutomationType.UIA2
    UIA3 = CSAutomationType.UIA3
