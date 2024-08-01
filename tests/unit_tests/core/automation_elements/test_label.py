"""Tests for the Label control."""

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestLabel:
    """Tests for the Label control."""

    def test_get_text(self, test_elements: WPFApplicationElements):
        """Tests the get_text method.

        :param wpf_elements: WPF application element map.
        """
        label_element = test_elements.simple_controls_tab.test_label
        assert label_element.text == "Test Label"
