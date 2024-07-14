"""Tests for the Slider control."""


from typing import Any, Generator

from flaui.core.automation_elements import Slider, Window
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
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

class TestSlider:
    """Tests for Slider control."""

    def test_slider_thumb(self, wpf_elements: WPFApplicationElements):
        """Tests slider thumb control."""
        slider = wpf_elements.simple_controls_tab.slider
        thumb = slider.thumb
        # old_position = thumb.properties.bounding_rectangle.value.Center() # TODO: Update this with C# Point class
        thumb.slide_horizontally(50)
        # Complete the assertion when C# Point class is ready

    def test_set_value(self, wpf_elements: WPFApplicationElements):
        """Tests setting value to the slider control"""
        slider = wpf_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        assert slider.value == self.adjust_number_if_only_value(slider, 5)
        adjusted_value = self.adjust_number_if_only_value(slider, 4)
        slider.value = adjusted_value
        assert slider.value == adjusted_value

    def test_small_increment(self, wpf_elements: WPFApplicationElements):
        """Tests small increments to the slider control value"""
        slider = wpf_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.small_increment()
        assert slider.value == self.adjust_number_if_only_value(slider, 6)

    def test_small_decrement(self, wpf_elements: WPFApplicationElements):
        """Tests small decrements to the slider control value"""
        slider = wpf_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.small_decrement()
        assert slider.value == self.adjust_number_if_only_value(slider, 4)

    def test_large_increment(self, wpf_elements: WPFApplicationElements):
        """Tests large increments to the slider control value"""
        slider = wpf_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.large_increment()
        assert slider.value == self.adjust_number_if_only_value(slider, 9)

    def test_large_decrement(self, wpf_elements: WPFApplicationElements):
        """Tests large decrements to the slider control value"""
        slider = wpf_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.large_decrement()
        assert slider.value == self.adjust_number_if_only_value(slider, 1)

    @staticmethod
    def adjust_number_if_only_value(slider: Slider, number: float) -> float:
        """Adjusts the range of slider control.
        The range of test slider is set to 0-10, but in UIA3 Winforms the range is always 0-100, this functions sets the appropriate value.

        :param slider: Slider control
        :param number: Number to set
        :return: Set number
        """
        return float(number * 10) if slider.is_only_value else float(number)

    def reset_to_center(self, slider: Slider) -> None:
        """Resets slider to center

        :param slider: Slider control
        """
        slider.value = self.adjust_number_if_only_value(slider, 5)
