"""This module contains unit tests for the enums module."""
from flaui.lib.enums import UIAutomationTypes

class TestUIAutomationTypes:
    """
    This class contains unit tests for the UIAutomationTypes enum.
    """
    def test_uiautomation_types(self):
        """
        This method tests the values of the UIAutomationTypes enum.
        """
        assert UIAutomationTypes.UIA2.value == "UIA2"
        assert UIAutomationTypes.UIA3.value == "UIA3"
