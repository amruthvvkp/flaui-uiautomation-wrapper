"""This tests the Calender element."""

from datetime import datetime

import arrow
from flaui.core.automation_type import AutomationType
import pytest
from pytest_check import equal, is_in, is_true
from System import DateTime as CSDateTime  # pyright: ignore

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestCalendarElements(UITestBase):
    """This tests the Calender element."""

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

    def test_add_to_selection(self):
        """Adds a date to the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 8)).date(),
            arrow.get(datetime(2021, 3, 9)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = self.test_elements.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_to_selection(_dates[1])
        selected_dates = calendar.selected_dates
        equal(len(selected_dates), len(_dates))
        for _ in selected_dates:
            is_in(_, _dates)

    def test_select_range_test(self):
        """Selects a range of dates on the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 8)).date(),
            arrow.get(datetime(2021, 3, 9)).date(),
            arrow.get(datetime(2021, 3, 11)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = self.test_elements.more_controls_tab.calender
        calendar.select_range(_dates)
        selected_dates = calendar.selected_dates
        equal(len(selected_dates), len(_dates))
        for _ in selected_dates:
            is_in(_, _dates)

    def test_add_range_to_selection_test(self):
        """Adds a range of dates to the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 10)).date(),
            arrow.get(datetime(2021, 3, 15)).date(),
            arrow.get(datetime(2021, 3, 17)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = self.test_elements.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_range_to_selection(_dates[1:])
        selected_dates = calendar.selected_dates
        equal(len(selected_dates), len(_dates))
        for _ in selected_dates:
            is_in(_, _dates)
