"""Tests for ProgressBar control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\ProgressBarTests.cs."""

import math
from typing import Any, Generator

from dirty_equals import HasAttributes
from flaui.core.automation_elements import ProgressBar
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


def _same_float(actual: float, expected: float) -> bool:
    """Compare two floats, treating NaN as equal to NaN.

    :param actual: The value under test.
    :param expected: The expected value.
    :return: True when both are NaN or they are equal.
    """
    return isinstance(actual, float) and (actual == expected or (math.isnan(actual) and math.isnan(expected)))


class TestProgressBar:
    """Tests for ProgressBar control."""

    @pytest.fixture(name="progress_bar")
    def get_progress_bar(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[ProgressBar, Any, None]:
        """Returns the progress bar element.

        :param test_application: Test application elements.
        :yield: Test progress bar element.
        """
        yield test_application.simple_controls_tab.progress_bar

    def test_minimum_value(self, progress_bar: ProgressBar) -> None:
        """Tests the minimum value property."""
        assert progress_bar == HasAttributes(minimum=0), "Minimum value is not 0."

    def test_maximum_value(self, progress_bar: ProgressBar) -> None:
        """Tests the maximum value property."""
        assert progress_bar == HasAttributes(maximum=100), "Maximum value is not 100."

    def test_value(self, progress_bar: ProgressBar) -> None:
        """Tests the value property."""
        assert progress_bar == HasAttributes(value=50), "Set value is not 50."

    def test_range_value_pattern(self, progress_bar: ProgressBar) -> None:
        """The RangeValue pattern (C# ``ProgressBar.RangeValuePattern``) reports the same range as the shortcuts."""
        pattern = progress_bar.range_value_pattern
        assert pattern.minimum.value == progress_bar.minimum
        assert pattern.maximum.value == progress_bar.maximum
        assert pattern.value.value == progress_bar.value

    def test_range_value_accessors(self, progress_bar: ProgressBar) -> None:
        """The Slider-style range accessors read through the RangeValue pattern."""
        pattern = progress_bar.range_value_pattern
        # Progress bars commonly report NaN for the step sizes (they have no user-driven steps),
        # so compare with NaN-aware equality.
        assert _same_float(progress_bar.small_change, float(pattern.small_change.value))
        assert _same_float(progress_bar.large_change, float(pattern.large_change.value))
        assert progress_bar.is_read_only is True, "A progress bar value should be read-only."
