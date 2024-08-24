"""This tests the Calender element."""

from datetime import datetime

import arrow
from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.modules.automation import Automation
import pytest
from pytest_check import equal, is_in, is_true
from System import DateTime as CSDateTime  # pyright: ignore

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
class TestCalendarElements:
    """This tests the Calender element."""

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

    def test_parse_date(self):
        """Parses the C# System date object from Python date object."""
        py_date = arrow.now().date()
        csharp_date = CSDateTime.Parse(py_date.strftime("%Y-%m-%d"))
        is_true(CSDateTime(*arrow.get(py_date).date().timetuple()[:6]).Equals(csharp_date))
        equal(arrow.get(CSDateTime(*arrow.get(py_date).date().timetuple()[:6]).ToString("o")), arrow.get(py_date))

    def test_select_date(self):
        """Selects the date on the calendar element."""
        _date = arrow.now().shift(days=+1).date()
        calendar = self.test_elements.more_controls_tab.calender
        calendar.select_date(_date)
        equal(calendar.selected_dates[0], _date)

    def test_add_to_selection(self):  # TODO: Looks like a flakey test
        """Adds a date to the calendar element."""
        _dates = [
            arrow.get(datetime(2020, 5, 20)).date(),
            arrow.get(datetime(2020, 5, 23)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = self.test_elements.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_to_selection(_dates[1])
        selected_dates = calendar.selected_dates
        equal(len(selected_dates), 2)
        for _ in selected_dates:
            is_in(_, _dates)

    # def test_select_range_test(self): # TODO: Looks like a flakey test
    #     """Selects a range of dates on the calendar element."""
    #     _dates = [
    #         arrow.get(datetime(2021, 3, 8)).date(),
    #         arrow.get(datetime(2021, 3, 9)).date(),
    #         arrow.get(datetime(2021, 3, 11)).date(),
    #     ]  # We need to use static time values to avoid test failures.
    #     calendar = self.test_elements.more_controls_tab.calender
    #     calendar.select_range(_dates)
    #     selected_dates = calendar.selected_dates
    #     equal(len(selected_dates), len(_dates))
    #     for _ in selected_dates:
    #         is_in(_, _dates)

    # def test_add_range_to_selection_test(self): # TODO: Looks like a flakey test
    #     """Adds a range of dates to the calendar element."""
    #     _dates = [
    #         arrow.get(datetime(2021, 3, 10)).date(),
    #         arrow.get(datetime(2021, 3, 15)).date(),
    #         arrow.get(datetime(2021, 3, 17)).date(),
    #     ]  # We need to use static time values to avoid test failures.
    #     calendar = self.test_elements.more_controls_tab.calender
    #     calendar.select_date(_dates[0])
    #     calendar.add_range_to_selection(_dates[1:])
    #     selected_dates = calendar.selected_dates
    #     equal(len(selected_dates), len(_dates))
    #     for _ in selected_dates:
    #         is_in(_, _dates)
