"""Tests for the Radio Button control."""

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestRadioButton:
    """Tests for RadioButton control."""

    def test_select_single_radio_button(self, test_elements: WPFApplicationElements):
        """Tests the select single radio button."""
        element = test_elements.simple_controls_tab.radio_button_1
        assert element.is_checked is False
        element.is_checked = True
        assert element.is_checked is True

    def test_select_radio_button_group(self, test_elements: WPFApplicationElements):
        """Tests the select radio button group."""
        radio_button_1 = test_elements.simple_controls_tab.radio_button_1
        radio_button_2 = test_elements.simple_controls_tab.radio_button_2

        assert radio_button_2.is_checked is False
        radio_button_1.is_checked = True
        assert radio_button_1.is_checked is True and radio_button_2.is_checked is False
        radio_button_2.is_checked = True
        assert radio_button_1.is_checked is False and radio_button_2.is_checked is True
