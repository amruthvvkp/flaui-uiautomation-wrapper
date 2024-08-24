"""Tests for ProgressBar control."""

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
class TestProgressBar(UITestBase):
    """Tests for ProgressBar control."""

    def test_minimum_value(self):
        """Tests the minimum value property."""
        equal(self.test_elements.simple_controls_tab.progress_bar.minimum, 0)

    def test_maximum_value(self):
        """Tests the maximum value property."""
        equal(self.test_elements.simple_controls_tab.progress_bar.maximum, 100)

    def test_value(self):
        """Tests the value property."""
        equal(self.test_elements.simple_controls_tab.progress_bar.value, 50)
