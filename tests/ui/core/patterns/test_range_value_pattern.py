"""
Test for RangeValue pattern, ported from C# RangeValuePatternTests.cs.
"""

from typing import Any, Generator

from dirty_equals import IsApprox
from flaui.core.automation_elements import AutomationElement
from flaui.core.condition_factory import ConditionFactory
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestRangeValuePattern:
    """Tests for RangeValue pattern on Slider control."""

    @pytest.fixture(name="slider")
    def get_slider(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the Slider element.

        :param test_application: Test application elements.
        :param condition_factory: Condition factory for building search conditions.
        :yield: Slider automation element.
        """
        slider = test_application.main_window.find_first_descendant(
            condition=condition_factory.by_automation_id("Slider")
        )
        yield slider

    def test_range_value_pattern(self, slider: AutomationElement) -> None:
        """Test RangeValue pattern on Slider control."""
        assert_that(slider, not_none())
        # UIA3 + WinForms normalizes the slider range to 0-100 (``is_only_value``); every
        # other combination uses the configured 0-10 range. Scale expected values to match,
        # mirroring ``TestSlider.adjust_number_if_only_value``.
        scale = 10 if slider.as_slider().is_only_value else 1
        rv_pattern = slider.patterns.range_value.pattern
        assert_that(rv_pattern, not_none())
        assert not rv_pattern.is_read_only.value
        assert rv_pattern.large_change.value == IsApprox(4 * scale, delta=0.1)
        assert rv_pattern.small_change.value == IsApprox(1 * scale, delta=0.1)
        assert rv_pattern.minimum.value == 0
        assert rv_pattern.maximum.value == IsApprox(10 * scale, delta=0.1)
        # The test application is shared across the session, so an earlier Slider test may
        # have moved the thumb. Set a known baseline instead of assuming the default value.
        rv_pattern.set_value(5 * scale)
        assert rv_pattern.value.value == IsApprox(5 * scale, delta=0.1)
        number1 = 6 * scale
        rv_pattern.set_value(number1)
        assert rv_pattern.value.value == IsApprox(number1, delta=0.1)
        number2 = 3 * scale
        rv_pattern.set_value(number2)
        assert rv_pattern.value.value == IsApprox(number2, delta=0.1)
