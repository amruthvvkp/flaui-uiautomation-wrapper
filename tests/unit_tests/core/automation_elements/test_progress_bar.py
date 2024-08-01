"""Tests for ProgressBar control."""

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestProgressBar:
    """Tests for ProgressBar control."""

    def test_minimum_value(self, test_elements: WPFApplicationElements):
        """Tests the minimum value property."""
        assert test_elements.simple_controls_tab.progress_bar.minimum == 0

    def test_maximum_value(self, test_elements: WPFApplicationElements):
        """Tests the maximum value property."""
        assert test_elements.simple_controls_tab.progress_bar.maximum == 100

    def test_value(self, test_elements: WPFApplicationElements):
        """Tests the value property."""
        assert test_elements.simple_controls_tab.progress_bar.value == 50
