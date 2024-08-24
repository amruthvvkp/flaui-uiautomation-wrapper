"""Tests for the Slider control."""

from flaui.core.application import Application
from flaui.core.automation_elements import Slider, Window
from flaui.core.automation_type import AutomationType
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
class TestSlider:
    """Tests for Slider control."""

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

    def test_slider_thumb(self):
        """Tests slider thumb control."""
        slider = self.test_elements.simple_controls_tab.slider
        thumb = slider.thumb
        thumb.properties.bounding_rectangle.value.center()  # type: ignore
        # old_position = thumb.properties.bounding_rectangle.value.Center() # TODO: Update this with C# Point class
        thumb.slide_horizontally(50)
        # Complete the assertion when C# Point class is ready

    def test_set_value(self):
        """Tests setting value to the slider control"""
        slider = self.test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        equal(slider.value, self.adjust_number_if_only_value(slider, 5))
        adjusted_value = self.adjust_number_if_only_value(slider, 4)
        slider.value = adjusted_value
        equal(slider.value, adjusted_value)

    def test_small_increment(self):
        """Tests small increments to the slider control value"""
        slider = self.test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.small_increment()
        equal(slider.value, self.adjust_number_if_only_value(slider, 6))

    def test_small_decrement(self):
        """Tests small decrements to the slider control value"""
        slider = self.test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.small_decrement()
        equal(slider.value, self.adjust_number_if_only_value(slider, 4))

    def test_large_increment(self):
        """Tests large increments to the slider control value"""
        slider = self.test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.large_increment()
        equal(slider.value, self.adjust_number_if_only_value(slider, 9))

    def test_large_decrement(self):
        """Tests large decrements to the slider control value"""
        slider = self.test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.large_decrement()
        equal(slider.value, self.adjust_number_if_only_value(slider, 1))

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
