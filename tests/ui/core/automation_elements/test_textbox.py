"""Tests for the Textbox control."""

from flaui.core.automation_type import AutomationType
from flaui.core.input import Wait
from flaui.lib.system.drawing import Color
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
class TestTextbox(UITestBase):
    """Tests for Textbox control."""

    DEFAULT_TEXT_BOX_TEXT = "Test TextBox"

    def test_direct_set(self):
        """Tests direct set of Textbox controls"""
        textbox = self.test_elements.simple_controls_tab.test_text_box
        equal(textbox.text, self.DEFAULT_TEXT_BOX_TEXT)

        text_to_set = "Hello World"
        textbox.text = text_to_set
        equal(textbox.text, text_to_set)

        textbox.text = self.DEFAULT_TEXT_BOX_TEXT

    def test_enter(self):
        """Tests enter method of Textbox controls"""
        textbox = self.test_elements.simple_controls_tab.test_text_box
        equal(textbox.text, self.DEFAULT_TEXT_BOX_TEXT)

        text_to_set = "Hello World"
        textbox.enter(text_to_set)
        Wait.until_input_is_processed()
        equal(textbox.text, text_to_set)

        textbox.text = self.DEFAULT_TEXT_BOX_TEXT

    def test_textbox_color(self):
        """Tests color of Textbox controls"""
        if self._application_type == ApplicationType.WinForms:
            pytest.skip("WinForms currently does not report the color on text boxes")

        textbox = self.test_elements.simple_controls_tab.test_text_box
        text_range = textbox.patterns.Text.Pattern  # TODO: Check if we can add a C# wrapper to Python
        color_int = text_range.DocumentRange.GetAttributeValue(
            self.test_elements.main_window.automation.TextAttributeLibrary.ForegroundColor
        )
        color = Color.from_argb(color_int)
        equal(color, Color.from_argb(alpha=0, base_color=Color.Green))
