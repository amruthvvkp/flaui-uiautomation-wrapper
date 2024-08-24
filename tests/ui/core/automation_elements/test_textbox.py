"""Tests for the Textbox control."""

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.core.input import Wait
from flaui.lib.system.drawing import Color
from flaui.modules.automation import Automation
import pytest
from pytest_check import equal

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestTextbox:
    """Tests for Textbox control."""

    DEFAULT_TEXT_BOX_TEXT = "Test TextBox"

    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        ui_test_base: tuple[Application, Automation],
        automation_type: AutomationType,
        application_type: ApplicationType,
    ):
        """Sets up essential properties for tests in this class.

        :param ui_test_base: UI Test base fixture
        :param automation_type: Automation Type
        :param application_type: Application Type
        """
        application, automation = ui_test_base
        self.application = application
        self.main_window: Window = application.get_main_window(automation)
        self.automation = automation
        self._automation_type = automation_type
        self._application_type = application_type
        self.test_elements = (
            get_wpf_application_elements(main_window=self.main_window)
            if self._application_type == ApplicationType.Wpf
            else get_winforms_application_elements(main_window=self.main_window)
        )

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
