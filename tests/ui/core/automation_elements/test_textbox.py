"""Tests for the Textbox control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\TextBoxTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes
from flaui.core.automation_elements import TextBox
from flaui.core.input import Wait
from flaui.lib.system.drawing import Color
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestTextbox:
    """Tests for Textbox control."""

    DEFAULT_TEXT_BOX_TEXT = "Test TextBox"

    @pytest.fixture(name="textbox")
    def get_textbox_element(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[TextBox, Any, None]:
        textbox = test_application.simple_controls_tab.test_text_box
        assert textbox == HasAttributes(text=self.DEFAULT_TEXT_BOX_TEXT), "Text box should have default text"
        yield textbox
        textbox.text = self.DEFAULT_TEXT_BOX_TEXT

    def test_direct_set(self, textbox: TextBox) -> None:
        """Tests direct set of Textbox controls"""
        text_to_set = "Hello World"
        textbox.text = text_to_set
        assert textbox == HasAttributes(text=text_to_set), "Text box should have new text"

    def test_enter(self, textbox: TextBox) -> None:
        """Tests enter method of Textbox controls"""
        text_to_set = "Hello World"
        textbox.enter(text_to_set)
        Wait.until_input_is_processed()
        assert textbox == HasAttributes(text=text_to_set), "Text box should have new text"

    def test_textbox_color(
        self,
        textbox: TextBox,
        test_application_type: str,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Tests color of Textbox controls"""
        if test_application_type == "WinForms":
            pytest.skip("WinForms currently does not report the color on text boxes")

        text_range = textbox.patterns.Text.Pattern  # TODO: Check if we can add a C# wrapper to Python
        color_int = text_range.DocumentRange.GetAttributeValue(
            test_application.main_window.automation.TextAttributeLibrary.ForegroundColor
        )
        color = Color.from_argb(color_int)
        assert color == Color.from_argb(alpha=0, base_color=Color.Green), "Text box should have green text color"
