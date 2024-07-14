"""Tests for the Textbox control."""


from typing import Any, Generator

from flaui.core.automation_elements import Window
from flaui.core.input import Wait
from flaui.lib.enums import UIAutomationTypes
from flaui.lib.system.drawing import Color
from flaui.modules.automation import Automation
from loguru import logger
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.config import test_settings

@pytest.fixture(scope="class")
def wpf_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    wpf_application = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    wpf_application.application.launch(
        test_settings.WPF_TEST_APP_EXE.as_posix()
        if ui_automation_type == UIAutomationTypes.UIA3
        else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    )
    yield wpf_application

    wpf_application.application.kill()


@pytest.fixture(scope="class")
def main_window(wpf_application: Automation, automation: Any) -> Generator[Window, None, None]:
    """Fetches the main window of the test application.

    :param wpf_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield wpf_application.application.get_main_window(automation)

@pytest.fixture(scope="class")
def wpf_elements(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)

class TestTextbox:
    """Tests for Textbox control."""

    DEFAULT_TEXT_BOX_TEXT = "Test TextBox"

    def test_direct_set(self, wpf_elements: WPFApplicationElements):
        """Tests direct set of Textbox controls"""
        textbox = wpf_elements.simple_controls_tab.test_text_box
        assert textbox.text == self.DEFAULT_TEXT_BOX_TEXT

        text_to_set = "Hello World"
        textbox.text = text_to_set
        assert textbox.text == text_to_set

        textbox.text = self.DEFAULT_TEXT_BOX_TEXT

    def test_enter(self, wpf_elements: WPFApplicationElements):
        """Tests enter method of Textbox controls"""
        textbox = wpf_elements.simple_controls_tab.test_text_box
        assert textbox.text == self.DEFAULT_TEXT_BOX_TEXT

        text_to_set = "Hello World"
        textbox.enter(text_to_set)
        Wait.until_input_is_processed()
        assert textbox.text == text_to_set

        textbox.text = self.DEFAULT_TEXT_BOX_TEXT

    def test_textbox_color(self, wpf_elements: WPFApplicationElements):
        """Tests color of Textbox controls"""
        if wpf_elements.process_name != "WpfApplication.exe":
            logger.warning("WinForms currently does not report the color on text boxes")
            return

        textbox = wpf_elements.simple_controls_tab.test_text_box
        text_range = textbox.patterns.Text.Pattern # TODO: Check if we can add a C# wrapper to Python
        color_int = text_range.DocumentRange.GetAttributeValue(wpf_elements.main_window.automation.TextAttributeLibrary.ForegroundColor)
        color = Color.from_argb(color_int)
        assert color == Color.from_argb(alpha=0, base_color=Color.Green)
