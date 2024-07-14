"""Tests for the Spinner control."""
# TODO: This is Winforms only tests, update this accordingly

from typing import Any, Generator

from flaui.core.automation_elements import Window
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.config import test_settings

@pytest.fixture(scope="class")
def wpf_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    wpf_application = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    wpf_application.application.launch(
        test_settings.WPF_TEST_APP_EXE.as_posix()
        if ui_automation_type == UIAutomationTypes.UIA3
        else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    )
    yield wpf_application

    wpf_application.application.kill()


@pytest.fixture(scope="class")
def main_window(wpf_application: Automation, automation: Any) -> Generator[Window, None, None]:
    """Fetches the main window of the test application.

    :param wpf_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield wpf_application.application.get_main_window(automation)

@pytest.fixture(scope="class")
def wpf_elements(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)

class TestSpinner:
    """Tests for Spinner control."""

    def test_set_value(self, wpf_elements: WPFApplicationElements):
        """Tests the value setting on Spinner control."""
        spinner = wpf_elements.simple_controls_tab.spinner
        for value_to_set in [6.0, 4.0]:
            spinner.value = value_to_set
            assert spinner.value == value_to_set

    def test_increment(self, wpf_elements: WPFApplicationElements):
        """Tests incremental increase of Spinner controls"""
        spinner = wpf_elements.simple_controls_tab.spinner
        value_to_set = 5.0
        spinner.value = value_to_set
        assert spinner.value == value_to_set
        spinner.increment()
        assert spinner.value == float(value_to_set + 1)

    def test_decrement(self, wpf_elements: WPFApplicationElements):
        """Tests incremental decrease of Spinner controls"""
        spinner = wpf_elements.simple_controls_tab.spinner
        value_to_set = 5.0
        spinner.value = value_to_set
        assert spinner.value == value_to_set
        spinner.decrement()
        assert spinner.value == float(value_to_set - 1)
