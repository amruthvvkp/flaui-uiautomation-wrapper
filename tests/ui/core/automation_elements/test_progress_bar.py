"""Tests for ProgressBar control."""

from dirty_equals import HasAttributes

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestProgressBar:
    """Tests for ProgressBar control."""

    def test_minimum_value(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the minimum value property."""
        assert test_application.simple_controls_tab.progress_bar == HasAttributes(minimum=0), "Minimum value is not 0."

    def test_maximum_value(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the maximum value property."""
        assert test_application.simple_controls_tab.progress_bar == HasAttributes(maximum=100), (
            "Maximum value is not 100."
        )

    def test_value(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the value property."""
        assert test_application.simple_controls_tab.progress_bar == HasAttributes(value=50), "Set value is not 50."
