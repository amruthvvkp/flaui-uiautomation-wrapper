"""Tests for the date time picker control."""

import arrow
from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
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
class TestDateTimePicker:
    """Tests for the datetime picker control."""

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

    def test_select_date(self):
        """Tests the select date method."""

        date = arrow.get(2021, 5, 17).date()
        if self._application_type == ApplicationType.Wpf:
            date_time_picker = self.test_elements.more_controls_tab.date_picker  # type: ignore
        else:
            date_time_picker = self.test_elements.simple_controls_tab.date_picker  # type: ignore
        date_time_picker.selected_date = date
        equal(date_time_picker.selected_date, date)
