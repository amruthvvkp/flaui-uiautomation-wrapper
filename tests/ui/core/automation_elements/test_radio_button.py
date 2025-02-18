"""Tests for the Radio Button control."""

from dirty_equals import HasAttributes, IsFalseLike

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestRadioButton:
    """Tests for RadioButton control."""

    def test_select_single_radio_button(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Tests the select single radio button."""
        element = test_application.simple_controls_tab.radio_button_1
        assert element == HasAttributes(is_checked=IsFalseLike), "Radio button should not be checked."
        element.is_checked = True
        assert element == HasAttributes(is_checked=True), "Radio button should be checked."

    def test_select_radio_button_group(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Tests the select radio button group."""
        radio_button_1 = test_application.simple_controls_tab.radio_button_1
        radio_button_2 = test_application.simple_controls_tab.radio_button_2

        assert radio_button_2 == HasAttributes(is_checked=IsFalseLike), "Radio button 2 should not be checked."

        radio_button_1.is_checked = True
        assert radio_button_1 == HasAttributes(is_checked=True), "Radio button 1 should be checked."
        assert radio_button_2 == HasAttributes(is_checked=IsFalseLike), "Radio button 2 should not be checked."

        radio_button_2.is_checked = True
        assert radio_button_1 == HasAttributes(is_checked=IsFalseLike), "Radio button 1 should not be checked."
        assert radio_button_2 == HasAttributes(is_checked=True), "Radio button 2 should be checked."
