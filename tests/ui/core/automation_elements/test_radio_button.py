"""Tests for the Radio Button control."""

from flaui.core.automation_type import AutomationType
import pytest
from pytest_check import is_false, is_true

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
class TestRadioButton(UITestBase):
    """Tests for RadioButton control."""

    def test_select_single_radio_button(self):
        """Tests the select single radio button."""
        element = self.test_elements.simple_controls_tab.radio_button_1
        is_false(element.is_checked)
        element.is_checked = True
        is_true(element.is_checked)

    def test_select_radio_button_group(self):
        """Tests the select radio button group."""
        radio_button_1 = self.test_elements.simple_controls_tab.radio_button_1
        radio_button_2 = self.test_elements.simple_controls_tab.radio_button_2

        is_false(radio_button_2.is_checked)
        radio_button_1.is_checked = True
        is_true(radio_button_1.is_checked)
        is_false(radio_button_2.is_checked)
        radio_button_2.is_checked = True
        is_false(radio_button_1.is_checked)
        is_true(radio_button_2.is_checked)
