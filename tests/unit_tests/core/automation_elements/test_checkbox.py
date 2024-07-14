"""Tests for the Checkbox class."""

from typing import Any, Generator

from flaui.core.automation_elements import Window
from flaui.core.definitions import ToggleState
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


class TestCalendarElements:
    """Tests for the Checkbox class."""
    # TODO: Use this Restart application test elsewhere to test the restart functionality
    # def restart_application(
    #     self, wpf_application: Automation, automation: Any, ui_automation_type: UIAutomationTypes
    # ) -> WPFApplicationElements:
    #     """Restarts the test application.

    #     :param wpf_application: Test application to restart.
    #     :param automation: Automation class to use for the tests.
    #     :param ui_automation_type: UIAutomation type to use for the tests.
    #     :return: WPF application element map.
    #     """
    #     wpf_application.application.close()
    #     # TODO: Add Retry.WhileFalse(() => Application.HasExited, TimeSpan.FromSeconds(2), ignoreException: true) method here once the tools namespace is implemented
    #     wpf_application.application.dispose()

    #     wpf_application = Automation(ui_automation_type)
    #     wpf_application.application.launch(
    #         test_settings.WPF_TEST_APP_EXE.as_posix()
    #         if ui_automation_type == UIAutomationTypes.UIA3
    #         else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    #     )
    #     main_window = wpf_application.application.get_main_window(automation)
    #     return WPFApplicationElements(main_window=main_window)

    def test_toggle_element(self, wpf_elements: WPFApplicationElements):
        """Tests the toggle method of the Checkbox class.

        :param wpf_elements: The WPF application element map.
        """
        checkbox = wpf_elements.simple_controls_tab.test_check_box
        assert checkbox.toggle_state == ToggleState.Off
        checkbox.toggle()
        assert checkbox.toggle_state == ToggleState.On

    def test_set_state(self, wpf_elements: WPFApplicationElements):
        """Tests the set_state method of the Checkbox class.

        :param wpf_elements: The WPF application element map.
        """
        checkbox = wpf_elements.simple_controls_tab.test_check_box
        checkbox.toggle_state = ToggleState.On
        assert checkbox.toggle_state == ToggleState.On
        checkbox.toggle_state = ToggleState.Off
        assert checkbox.toggle_state == ToggleState.Off
        checkbox.toggle_state = ToggleState.On
        assert checkbox.toggle_state == ToggleState.On

    def test_three_way_toggle(self, wpf_elements: WPFApplicationElements):
        """Tests the three_way_toggle method of the Checkbox class.

        :param wpf_elements: The WPF application element map.
        """
        checkbox = wpf_elements.simple_controls_tab.three_way_check_box
        assert checkbox.toggle_state == ToggleState.Off
        checkbox.toggle()
        assert checkbox.toggle_state == ToggleState.On
        checkbox.toggle()
        assert checkbox.toggle_state == ToggleState.Indeterminate

    def test_three_way_set_state(self, wpf_elements: WPFApplicationElements):
        """Tests the three_way_set_state method of the Checkbox class.

        :param wpf_elements: The WPF application element map.
        """
        checkbox = wpf_elements.simple_controls_tab.three_way_check_box
        checkbox.toggle_state = ToggleState.On
        assert checkbox.toggle_state == ToggleState.On
        checkbox.toggle_state = ToggleState.Off
        assert checkbox.toggle_state == ToggleState.Off
        checkbox.toggle_state = ToggleState.Indeterminate
        assert checkbox.toggle_state == ToggleState.Indeterminate
