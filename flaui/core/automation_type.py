"""This module provides a wrapper for the AutomationType class from the object <class 'FlaUI.Core.AutomationType'> from the module - FlaUI.Core."""
from enum import Enum

from FlaUI.Core import AutomationType as CSAutomationType  # pyright: ignore

class AutomationType(Enum):
    """
    An enumeration of the supported automation types.

    Attributes:
        UIA2: The UI Automation 2 automation type.
        UIA3: The UI Automation 3 automation type.
    """
    UIA2 = CSAutomationType.UIA2
    UIA3 = CSAutomationType.UIA3
