"""Tests for the Checkbox class."""

from flaui.core.automation_type import AutomationType
from flaui.core.definitions import ToggleState
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
class TestCalendarElements(UITestBase):
    """Tests for the Checkbox class."""

    def test_toggle_element(self):
        """Tests the toggle method of the Checkbox class."""
        checkbox = self.test_elements.simple_controls_tab.test_check_box
        equal(checkbox.toggle_state, ToggleState.Off)
        checkbox.toggle()
        equal(checkbox.toggle_state, ToggleState.On)

    def test_set_state(self):
        """Tests the set_state method of the Checkbox class."""
        checkbox = self.test_elements.simple_controls_tab.test_check_box
        checkbox.toggle_state = ToggleState.On
        equal(checkbox.toggle_state, ToggleState.On)
        checkbox.toggle_state = ToggleState.Off
        equal(checkbox.toggle_state, ToggleState.Off)
        checkbox.toggle_state = ToggleState.On
        equal(checkbox.toggle_state, ToggleState.On)

    def test_three_way_toggle(self):
        """Tests the three_way_toggle method of the Checkbox class."""
        checkbox = self.test_elements.simple_controls_tab.three_way_check_box
        equal(checkbox.toggle_state, ToggleState.Off)
        checkbox.toggle()
        equal(checkbox.toggle_state, ToggleState.On)
        checkbox.toggle()
        equal(checkbox.toggle_state, ToggleState.Indeterminate)

    def test_three_way_set_state(self):
        """Tests the three_way_set_state method of the Checkbox class."""
        checkbox = self.test_elements.simple_controls_tab.three_way_check_box
        checkbox.toggle_state = ToggleState.On
        equal(checkbox.toggle_state, ToggleState.On)
        checkbox.toggle_state = ToggleState.Off
        equal(checkbox.toggle_state, ToggleState.Off)
        checkbox.toggle_state = ToggleState.Indeterminate
        equal(checkbox.toggle_state, ToggleState.Indeterminate)
