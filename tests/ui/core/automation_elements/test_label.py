"""Tests for the Label control."""

from flaui.core.automation_type import AutomationType
import pytest
from pytest_check import equal

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestLabel(UITestBase):
    """Tests for the Label control."""

    def test_get_text(self):
        """Tests the get_text method."""
        label_element = self.test_elements.simple_controls_tab.test_label
        equal(label_element.text, "Test Label")
