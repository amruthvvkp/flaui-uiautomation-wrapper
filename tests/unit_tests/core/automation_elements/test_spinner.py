"""Tests for the Spinner control."""
# TODO: This is Winforms only tests, update this accordingly

import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestSpinner:
    """Tests for Spinner control."""

    def test_set_value(self, request, test_elements: WPFApplicationElements):
        """Tests the value setting on Spinner control."""
        if str(request.config.getoption("--test-app-uia-version")).upper() == "UIA3":
            pytest.skip("Test cannot run on WPF Test Application, skipping this one.")
        spinner = test_elements.simple_controls_tab.spinner
        for value_to_set in [6.0, 4.0]:
            spinner.value = value_to_set
            assert spinner.value == value_to_set

    def test_increment(self, request, test_elements: WPFApplicationElements):
        """Tests incremental increase of Spinner controls"""
        if str(request.config.getoption("--test-app-uia-version")).upper() == "UIA3":
            pytest.skip("Test cannot run on WPF Test Application, skipping this one.")
        spinner = test_elements.simple_controls_tab.spinner
        value_to_set = 5.0
        spinner.value = value_to_set
        assert spinner.value == value_to_set
        spinner.increment()
        assert spinner.value == float(value_to_set + 1)

    def test_decrement(self, request, test_elements: WPFApplicationElements):
        """Tests incremental decrease of Spinner controls"""
        if str(request.config.getoption("--test-app-uia-version")).upper() == "UIA3":
            pytest.skip("Test cannot run on WPF Test Application, skipping this one.")
        spinner = test_elements.simple_controls_tab.spinner
        value_to_set = 5.0
        spinner.value = value_to_set
        assert spinner.value == value_to_set
        spinner.decrement()
        assert spinner.value == float(value_to_set - 1)
