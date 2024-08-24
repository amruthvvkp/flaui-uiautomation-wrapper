"""Tests for the Checkbox class."""

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.core.definitions import ToggleState
from flaui.modules.automation import Automation
import pytest
from pytest_check import equal

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestCalendarElements:
    """Tests for the Checkbox class."""

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

    # def test_toggle_element(self): # TODO: Looks like a flakey test
    #     """Tests the toggle method of the Checkbox class."""
    #     checkbox = self.test_elements.simple_controls_tab.test_check_box
    #     equal(checkbox.toggle_state, ToggleState.Off)
    #     checkbox.toggle()
    #     equal(checkbox.toggle_state, ToggleState.On)

    # def test_set_state(self): # TODO: Looks like a flakey test
    #     """Tests the set_state method of the Checkbox class."""
    #     checkbox = self.test_elements.simple_controls_tab.test_check_box
    #     checkbox.toggle_state = ToggleState.On
    #     equal(checkbox.toggle_state, ToggleState.On)
    #     checkbox.toggle_state = ToggleState.Off
    #     equal(checkbox.toggle_state, ToggleState.Off)
    #     checkbox.toggle_state = ToggleState.On
    #     equal(checkbox.toggle_state, ToggleState.On)

    def test_three_way_toggle(self):
        """Tests the three_way_toggle method of the Checkbox class."""
        checkbox = self.test_elements.simple_controls_tab.three_way_check_box
        equal(checkbox.toggle_state, ToggleState.Off)
        checkbox.toggle()
        equal(checkbox.toggle_state, ToggleState.On)
        checkbox.toggle()
        equal(checkbox.toggle_state, ToggleState.Indeterminate)

    def test_three_way_set_state(self):
        """Tests the three_way_set_state method of the Checkbox class."""
        checkbox = self.test_elements.simple_controls_tab.three_way_check_box
        checkbox.toggle_state = ToggleState.On
        equal(checkbox.toggle_state, ToggleState.On)
        checkbox.toggle_state = ToggleState.Off
        equal(checkbox.toggle_state, ToggleState.Off)
        checkbox.toggle_state = ToggleState.Indeterminate
        equal(checkbox.toggle_state, ToggleState.Indeterminate)
