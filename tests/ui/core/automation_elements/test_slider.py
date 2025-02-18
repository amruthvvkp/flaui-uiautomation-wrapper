"""Tests for the Slider control."""

from dirty_equals import IsApprox, IsInt
from flaui.core.automation_elements import Slider
from flaui.lib.system.drawing import Point

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestSlider:
    """Tests for Slider control."""

    def test_slider_thumb(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests slider thumb control."""
        slider = test_application.simple_controls_tab.slider
        thumb = slider.thumb
        old_position: Point = thumb.properties.bounding_rectangle.value.center()  # type: ignore
        thumb.slide_horizontally(50)
        new_position: Point = thumb.properties.bounding_rectangle.value.center()  # type: ignore

        # Extract x and y explicitly
        old_x, old_y = old_position.raw_value.X, old_position.raw_value.Y  # type: ignore
        new_x, new_y = new_position.raw_value.X, new_position.raw_value.Y  # type: ignore

        # Validate the movement using IsApprox
        assert new_x == IsApprox((old_x + 50), delta=1), "Thumb did not move horizontally by 50 pixels."
        assert new_y == IsInt(exactly=old_y), "Thumb moved vertically."

    def test_set_value(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests setting value to the slider control"""
        slider = test_application.simple_controls_tab.slider
        self.reset_to_center(slider)
        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 5), delta=0.1), (
            "Slider value is not 5."
        )
        adjusted_value = self.adjust_number_if_only_value(slider, 4)
        slider.value = adjusted_value
        assert slider.value == IsApprox(adjusted_value, delta=0.1), "Slider value is not 4."

    def test_small_increment(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests small increments to the slider control value"""
        slider = test_application.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.small_increment()
        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 6), delta=0.1), (
            "Slider value is not 6."
        )

    def test_small_decrement(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests small decrements to the slider control value"""
        slider = test_application.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.small_decrement()
        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 4), delta=0.1), (
            "Slider value is not 4."
        )

    def test_large_increment(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests large increments to the slider control value"""
        slider = test_application.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.large_increment()
        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 9), delta=0.1), (
            "Slider value is not 9."
        )

    def test_large_decrement(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests large decrements to the slider control value"""
        slider = test_application.simple_controls_tab.slider
        self.reset_to_center(slider)
        slider.large_decrement()
        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 1), delta=0.1), (
            "Slider value is not 1."
        )

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
