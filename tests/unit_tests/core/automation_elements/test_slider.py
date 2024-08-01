"""Tests for the Slider control."""

from flaui.core.automation_elements import Slider

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestSlider:
    """Tests for Slider control."""

    def test_slider_thumb(self, test_elements: WPFApplicationElements):
        """Tests slider thumb control."""
        slider = test_elements.simple_controls_tab.slider
        thumb = slider.thumb
        thumb.properties.bounding_rectangle.value.center()  # type: ignore
        # old_position = thumb.properties.bounding_rectangle.value.Center() # TODO: Update this with C# Point class
        thumb.slide_horizontally(50)
        # Complete the assertion when C# Point class is ready

    def test_set_value(self, test_elements: WPFApplicationElements):
        """Tests setting value to the slider control"""
        slider = test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        assert slider.value == self.adjust_number_if_only_value(slider, 5)
        adjusted_value = self.adjust_number_if_only_value(slider, 4)
        slider.value = adjusted_value
        assert slider.value == adjusted_value

    def test_small_increment(self, test_elements: WPFApplicationElements):
        """Tests small increments to the slider control value"""
        slider = test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.small_increment()
        assert slider.value == self.adjust_number_if_only_value(slider, 6)

    def test_small_decrement(self, test_elements: WPFApplicationElements):
        """Tests small decrements to the slider control value"""
        slider = test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.small_decrement()
        assert slider.value == self.adjust_number_if_only_value(slider, 4)

    def test_large_increment(self, test_elements: WPFApplicationElements):
        """Tests large increments to the slider control value"""
        slider = test_elements.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.large_increment()
        assert slider.value == self.adjust_number_if_only_value(slider, 9)

    def test_large_decrement(self, test_elements: WPFApplicationElements):
        """Tests large decrements to the slider control value"""
        slider = test_elements.simple_controls_tab.slider
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
