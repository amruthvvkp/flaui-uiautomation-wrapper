"""Tests for the PopUp control."""

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.core.input import Wait
from flaui.modules.automation import Automation
import pytest
from pytest_check import equal, is_not_none

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestPopUp:
    """Tests for the PopUp control."""

    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        ui_test_base: tuple[Application, Automation],
        automation_type: AutomationType,
        application_type: ApplicationType,
    ):
        """Sets up essential properties for tests in this class.

        :param ui_test_base: UI Test base fixture
        :param automation_type: Automation Type
        :param application_type: Application Type
        """
        application, automation = ui_test_base
        self.application = application
        self.main_window: Window = application.get_main_window(automation)
        self.automation = automation
        self._automation_type = automation_type
        self._application_type = application_type
        self.test_elements = (
            get_wpf_application_elements(main_window=self.main_window)
            if self._application_type == ApplicationType.Wpf
            else get_winforms_application_elements(main_window=self.main_window)
        )

    def test_check_box_in_popup(self):
        """Tests the check box in the pop up."""
        element = self.test_elements.simple_controls_tab.popup_toggle_button1
        element.click()
        Wait.until_input_is_processed()
        popup = self.test_elements.main_window.popup
        is_not_none(popup)
        popup_children = popup.find_all_children()
        equal(len(popup_children), 1)
        check = popup_children[0].as_check_box()
        equal(check.text, "This is a popup")

    def test_menu_in_popup(self):
        """Tests the menu in the pop up."""
        element = self.test_elements.simple_controls_tab.popup_toggle_button2
        element.click()
        Wait.until_input_is_processed()
        popup = self.test_elements.main_window.popup
        is_not_none(popup)
        popup_children = popup.find_all_children()
        equal(len(popup_children), 1)
        menu = popup_children[0].as_menu()
        equal(len(menu.items), 1)
        equal(menu.items[0].text, "Some MenuItem")
