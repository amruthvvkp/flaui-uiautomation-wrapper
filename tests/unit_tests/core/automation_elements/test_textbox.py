"""Tests for the Textbox control."""

from flaui.core.input import Wait
from flaui.lib.system.drawing import Color
from loguru import logger

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestTextbox:
    """Tests for Textbox control."""

    DEFAULT_TEXT_BOX_TEXT = "Test TextBox"

    def test_direct_set(self, test_elements: WPFApplicationElements):
        """Tests direct set of Textbox controls"""
        textbox = test_elements.simple_controls_tab.test_text_box
        assert textbox.text == self.DEFAULT_TEXT_BOX_TEXT

        text_to_set = "Hello World"
        textbox.text = text_to_set
        assert textbox.text == text_to_set

        textbox.text = self.DEFAULT_TEXT_BOX_TEXT

    def test_enter(self, test_elements: WPFApplicationElements):
        """Tests enter method of Textbox controls"""
        textbox = test_elements.simple_controls_tab.test_text_box
        assert textbox.text == self.DEFAULT_TEXT_BOX_TEXT

        text_to_set = "Hello World"
        textbox.enter(text_to_set)
        Wait.until_input_is_processed()
        assert textbox.text == text_to_set

        textbox.text = self.DEFAULT_TEXT_BOX_TEXT

    def test_textbox_color(self, test_elements: WPFApplicationElements):
        """Tests color of Textbox controls"""
        if test_elements.process_name != "WpfApplication.exe":
            logger.warning("WinForms currently does not report the color on text boxes")
            return

        textbox = test_elements.simple_controls_tab.test_text_box
        text_range = textbox.patterns.Text.Pattern  # TODO: Check if we can add a C# wrapper to Python
        color_int = text_range.DocumentRange.GetAttributeValue(
            test_elements.main_window.automation.TextAttributeLibrary.ForegroundColor
        )
        color = Color.from_argb(color_int)
        assert color == Color.from_argb(alpha=0, base_color=Color.Green)
