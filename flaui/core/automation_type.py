from enum import Enum

from FlaUI.Core import AutomationType as CSAutomationType  # pyright: ignore


class AutomationType(Enum):
    UIA2 = CSAutomationType.UIA2
    UIA3 = CSAutomationType.UIA3
