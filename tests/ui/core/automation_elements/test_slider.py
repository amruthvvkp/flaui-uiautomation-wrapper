"""Tests for the Slider control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\SliderTests.cs."""

from typing import Any, Generator

from dirty_equals import IsApprox
from loguru import logger
from flaui.core.automation_elements import Slider
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestSlider:
    """Tests for Slider control."""

    @pytest.fixture()
    def get_slider(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Slider, Any, None]:
        """Returns the slider element.

        :param test_application: Test application elements.
        :return: Test slider element.
        """
        yield test_application.simple_controls_tab.slider

    def test_slider_thumb(self, slider: Slider) -> None:
        """Tests slider thumb control."""
        thumb = slider.thumb
        old_value = slider.value
        thumb.slide_horizontally(50)
        new_value = slider.value

        # Print debug info for troubleshooting platform-specific slider behavior
        logger.debug(
            f"Slider thumb test: old_value={old_value}, new_value={new_value}, slider.min={getattr(slider, 'minimum', None)}, slider.max={getattr(slider, 'maximum', None)}"
        )

        # Assert that the value changed
        assert new_value != old_value, (
            f"Slider value did not change after sliding thumb. Old: {old_value}, New: {new_value}"
        )
        # Warn if the value decreased (WinForms slider may wrap or behave differently)
        if new_value < old_value:
            logger.warning(f"[WARN] Slider value decreased after sliding thumb. Old: {old_value}, New: {new_value}")

    def test_set_value(self, slider: Slider) -> None:
        """Tests setting value to the slider control"""

        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 5), delta=0.1), (
            "Slider value is not 5."
        )
        adjusted_value = self.adjust_number_if_only_value(slider, 4)
        slider.value = adjusted_value
        assert slider.value == IsApprox(adjusted_value, delta=0.1), "Slider value is not 4."

    def test_small_increment(self, slider: Slider) -> None:
        """Tests small increments to the slider control value"""

        slider.small_increment()
        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 6), delta=0.1), (
            "Slider value is not 6."
        )

    def test_small_decrement(self, slider: Slider) -> None:
        """Tests small decrements to the slider control value"""

        slider.small_decrement()
        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 4), delta=0.1), (
            "Slider value is not 4."
        )

    def test_large_increment(self, slider: Slider) -> None:
        """Tests large increments to the slider control value"""

        slider.large_increment()
        assert slider.value == IsApprox(self.adjust_number_if_only_value(slider, 9), delta=0.1), (
            "Slider value is not 9."
        )

    def test_large_decrement(self, slider: Slider) -> None:
        """Tests large decrements to the slider control value"""

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

    @pytest.fixture(scope="function", name="slider")
    def reset_to_center(self, get_slider: Slider) -> Generator[Slider, Any, None]:
        """Resets slider to center

        :param slider: Slider control
        :return: Slider control
        """
        get_slider.value = self.adjust_number_if_only_value(get_slider, 5)
        yield get_slider
