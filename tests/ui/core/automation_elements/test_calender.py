"""This tests the Calender element."""

from datetime import datetime

import arrow
from dirty_equals import Contains, HasLen, IsTrueLike
import pytest
from System import DateTime as CSDateTime  # pyright: ignore

from tests.test_utilities.elements.winforms_application.base import (
    WinFormsApplicationElements,
)
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


@pytest.mark.xfail(
    condition=lambda request: request.getfixturevalue("test_application_type") == "WinForms",  # type: ignore
    reason="Does not support Winforms application type.",
)
class TestCalendarElements:
    """This tests the Calender element."""

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
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Selects the date on the calendar element."""
        _date = arrow.now().shift(days=+1).date()
        calendar = test_application.more_controls_tab.calender
        calendar.select_date(_date)
        # equal(calendar.selected_dates[0], _date)

    def test_add_to_selection(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Adds a date to the calendar element."""
        _dates = [
            arrow.get(datetime(2020, 5, 20)).date(),
            arrow.get(datetime(2020, 5, 23)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = test_application.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_to_selection(_dates[1])
        selected_dates = calendar.selected_dates
        assert selected_dates == Contains(*_dates) & HasLen(2), "Should have the same dates selected."

    def test_select_range_test(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Selects a range of dates on the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 8)).date(),
            arrow.get(datetime(2021, 3, 9)).date(),
            arrow.get(datetime(2021, 3, 11)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = test_application.more_controls_tab.calender
        calendar.select_range(_dates)
        selected_dates = calendar.selected_dates
        assert selected_dates == Contains(*_dates) & HasLen(3), "Should have the same dates selected."

    def test_add_range_to_selection_test(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Adds a range of dates to the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 10)).date(),
            arrow.get(datetime(2021, 3, 15)).date(),
            arrow.get(datetime(2021, 3, 17)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = test_application.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_range_to_selection(_dates[1:])
        selected_dates = calendar.selected_dates
        assert selected_dates == Contains(*_dates) & HasLen(3), "Should have the same dates selected."
