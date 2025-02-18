"""This tests the Calender element."""

from datetime import datetime
from typing import Any, Generator

import arrow
from dirty_equals import Contains, HasAttributes, HasLen, IsDate, IsList, IsTrueLike
from flaui.core.automation_elements import Calendar
import pytest
from System import DateTime as CSDateTime  # pyright: ignore

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestCalendarElements:
    """This tests the Calender element."""

    @pytest.fixture(name="calendar")
    def get_calendar_element(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, test_application_type: str
    ) -> Generator[Calendar, Any, None]:
        """Returns the calendar element.

        :param test_application: Test application elements.
        :param test_application_type: Test application type.
        :yield: Calendar element.
        """
        if test_application_type != "WPF":
            pytest.skip("Does not support Winforms application type.")
        yield test_application.more_controls_tab.calender

    def test_parse_date(self) -> None:
        """Parses the C# System date object from Python date object."""
        py_date = arrow.now().date()
        csharp_date = CSDateTime.Parse(py_date.strftime("%Y-%m-%d"))
        assert CSDateTime(*arrow.get(py_date).date().timetuple()[:6]).Equals(csharp_date) == IsTrueLike, (
            "Dates should match today's date."
        )
        assert arrow.get(CSDateTime(*arrow.get(py_date).date().timetuple()[:6]).ToString("o")) == arrow.get(py_date)

    def test_select_date(
        self,
        calendar: Calendar,
    ) -> None:
        """Selects the date on the calendar element."""
        _date = arrow.now().shift(days=+1).date()
        calendar.select_date(_date)
        assert calendar == HasAttributes(selected_dates=IsList(positions={0: IsDate(approx=_date)}, length=1)), (
            "Should have the date selected."
        )

    def test_add_to_selection(self, calendar: Calendar) -> None:
        """Adds a date to the calendar element."""
        _dates = [
            arrow.get(datetime(2020, 5, 20)).date(),
            arrow.get(datetime(2020, 5, 23)).date(),
        ]  # We need to use static time values to avoid test failures.

        calendar.select_date(_dates[0])
        calendar.add_to_selection(_dates[1])
        selected_dates = calendar.selected_dates
        assert selected_dates == Contains(*_dates) & HasLen(2), "Should have the same dates selected."

    def test_select_range_test(self, calendar: Calendar) -> None:
        """Selects a range of dates on the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 8)).date(),
            arrow.get(datetime(2021, 3, 9)).date(),
            arrow.get(datetime(2021, 3, 11)).date(),
        ]  # We need to use static time values to avoid test failures.

        calendar.select_range(_dates)
        selected_dates = calendar.selected_dates
        assert selected_dates == Contains(*_dates) & HasLen(3), "Should have the same dates selected."

    def test_add_range_to_selection_test(self, calendar: Calendar) -> None:
        """Adds a range of dates to the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 10)).date(),
            arrow.get(datetime(2021, 3, 15)).date(),
            arrow.get(datetime(2021, 3, 17)).date(),
        ]  # We need to use static time values to avoid test failures.

        calendar.select_date(_dates[0])
        calendar.add_range_to_selection(_dates[1:])
        selected_dates = calendar.selected_dates
        assert selected_dates == Contains(*_dates) & HasLen(3), "Should have the same dates selected."
