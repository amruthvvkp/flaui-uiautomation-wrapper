"""Tests for the Radio Button control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\RadioButtonTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, IsFalseLike
from flaui.core.automation_elements import RadioButton
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestRadioButton:
    """Tests for RadioButton control."""

    @pytest.fixture(name="radio_button_1")
    def get_radio_button_1(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[RadioButton, Any, None]:
        """Returns the radio button 1 element.

        :param test_application: Test application elements.
        :yield: Test radio button 1 element.
        """
        yield test_application.simple_controls_tab.radio_button_1

    @pytest.fixture(name="radio_button_2")
    def get_radio_button_2(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[RadioButton, Any, None]:
        """Returns the radio button 2 element.

        :param test_application: Test application elements.
        :yield: Test radio button 2 element.
        """
        yield test_application.simple_controls_tab.radio_button_2

    def test_select_single_radio_button(self, radio_button_1: RadioButton) -> None:
        """Tests the select single radio button."""
        assert radio_button_1 == HasAttributes(is_checked=IsFalseLike), "Radio button should not be checked."
        radio_button_1.is_checked = True
        assert radio_button_1 == HasAttributes(is_checked=True), "Radio button should be checked."

    def test_select_radio_button_group(self, radio_button_1: RadioButton, radio_button_2: RadioButton) -> None:
        """Tests the select radio button group."""
        assert radio_button_2 == HasAttributes(is_checked=IsFalseLike), "Radio button 2 should not be checked."

        radio_button_1.is_checked = True
        assert radio_button_1 == HasAttributes(is_checked=True), "Radio button 1 should be checked."
        assert radio_button_2 == HasAttributes(is_checked=IsFalseLike), "Radio button 2 should not be checked."

        radio_button_2.is_checked = True
        assert radio_button_1 == HasAttributes(is_checked=IsFalseLike), "Radio button 1 should not be checked."
        assert radio_button_2 == HasAttributes(is_checked=True), "Radio button 2 should be checked."
