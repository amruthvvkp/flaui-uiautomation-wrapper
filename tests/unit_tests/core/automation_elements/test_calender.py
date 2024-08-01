"""This tests the Calender element."""

from datetime import datetime

import arrow
from System import DateTime as CSDateTime  # pyright: ignore

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestCalendarElements:
    """This tests the Calender element."""

    def test_parse_date(self):
        """Parses the C# System date object from Python date object."""
        py_date = arrow.now().date()
        csharp_date = CSDateTime.Parse(py_date.strftime("%Y-%m-%d"))
        assert CSDateTime(*arrow.get(py_date).date().timetuple()[:6]).Equals(csharp_date)
        assert arrow.get(CSDateTime(*arrow.get(py_date).date().timetuple()[:6]).ToString("o")) == arrow.get(py_date)

    def test_select_date(self, test_elements: WPFApplicationElements):
        """Selects the date on the calendar element."""
        _date = arrow.now().shift(days=+1).date()
        calendar = test_elements.more_controls_tab.calender
        calendar.select_date(_date)
        assert calendar.selected_dates[0] == _date

    def test_add_to_selection(self, test_elements: WPFApplicationElements):
        """Adds a date to the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 8)).date(),
            arrow.get(datetime(2021, 3, 9)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = test_elements.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_to_selection(_dates[1])
        selected_dates = calendar.selected_dates
        assert len(selected_dates) == len(_dates)
        for _ in selected_dates:
            assert _ in _dates

    def test_select_range_test(self, test_elements: WPFApplicationElements):
        """Selects a range of dates on the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 8)).date(),
            arrow.get(datetime(2021, 3, 9)).date(),
            arrow.get(datetime(2021, 3, 11)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = test_elements.more_controls_tab.calender
        calendar.select_range(_dates)
        selected_dates = calendar.selected_dates
        assert len(selected_dates) == len(_dates)
        for _ in selected_dates:
            assert _ in _dates

    def test_add_range_to_selection_test(self, test_elements: WPFApplicationElements):
        """Adds a range of dates to the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 10)).date(),
            arrow.get(datetime(2021, 3, 15)).date(),
            arrow.get(datetime(2021, 3, 17)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = test_elements.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_range_to_selection(_dates[1:])
        selected_dates = calendar.selected_dates
        assert len(selected_dates) == len(_dates)
        for _ in selected_dates:
            assert _ in _dates
