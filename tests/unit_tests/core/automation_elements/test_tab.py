"""Tests for the Tab control."""


from typing import Any, Generator

from flaui.core.automation_elements import Window
from flaui.core.input import Wait
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.assets.elements.wpf_application.constants import ApplicationTabIndex
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

class TestTab:
    """Tests for Tab control."""

    def test_select_tab(self, wpf_elements: WPFApplicationElements):
        """Tests selection of Tab controls"""
        tab = wpf_elements.tab

        assert len(tab.tab_items()) == 3 if wpf_elements.process_name == "WpfApplication.exe" else 2 # TODO: Set Winforms elements to this test case
        for index in ApplicationTabIndex:
            if index != ApplicationTabIndex.SIMPLE_CONTROLS:
                tab.select_tab_item(index.value)
                Wait.until_input_is_processed()

            assert tab.selected_tab_item_index == index.value

    def test_exception_on_no_input_value_to_select_tab(self, wpf_elements: WPFApplicationElements):
        """Tests if ValueError is thrown on no index/value sent to select tab"""
        with pytest.raises(ValueError):
            wpf_elements.tab.select_tab_item()
