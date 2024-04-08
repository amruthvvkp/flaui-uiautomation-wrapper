"""This module contains tests for the enums module."""

from flaui.lib.enums import UIAutomationTypes


class TestUIAutomationTypes:
    """Test cases for the UIAutomationTypes enum."""

    def test_uiautomation_types(self):
        """Test the UIAutomationTypes enum."""
        assert UIAutomationTypes.UIA2.value == "UIA2"
        assert UIAutomationTypes.UIA3.value == "UIA3"
