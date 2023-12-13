"""This tests the Calender element."""


from datetime import datetime
from typing import Any, Generator

import arrow
from flaui.core.automation_elements import Window
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest
from System import DateTime as CSDateTime  # pyright: ignore

from tests.assets.element_map.wpf_application.base import WPFApplicationElements
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
def wpf_element_map(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)


@pytest.fixture(scope="class")
def more_controls_tab(wpf_element_map: WPFApplicationElements):
    """Fixture for the More Controls tab.

    :param wpf_element_map: The WPF application element map.
    :return: The More Controls tab.
    """
    return main_window.find_first_child(condition=main_window.condition_factory.by_name("More Controls"))


class TestCalendarElements:
    """This tests the Calender element."""

    def test_parse_date(self):
        """Parses the C# System date object from Python date object."""
        py_date = arrow.now().date()
        csharp_date = CSDateTime.Parse(py_date.strftime("%Y-%m-%d"))
        assert CSDateTime(*arrow.get(py_date).date().timetuple()[:6]).Equals(csharp_date)
        assert arrow.get(CSDateTime(*arrow.get(py_date).date().timetuple()[:6]).ToString("o")) == arrow.get(py_date)

    def test_select_date(self, wpf_element_map: WPFApplicationElements):
        """Selects the date on the calendar element."""
        _date = arrow.now().shift(days=+1).date()
        calendar = wpf_element_map.more_controls_tab.calender
        calendar.select_date(_date)
        assert calendar.selected_dates[0] == _date

    def test_add_to_selection(self, wpf_element_map: WPFApplicationElements):
        """Adds a date to the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 8)).date(),
            arrow.get(datetime(2021, 3, 9)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = wpf_element_map.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_to_selection(_dates[1])
        selected_dates = calendar.selected_dates
        assert len(selected_dates) == len(_dates)
        for _ in selected_dates:
            assert _ in _dates

    def test_select_range_test(self, wpf_element_map: WPFApplicationElements):
        """Selects a range of dates on the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 8)).date(),
            arrow.get(datetime(2021, 3, 9)).date(),
            arrow.get(datetime(2021, 3, 11)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = wpf_element_map.more_controls_tab.calender
        calendar.select_range(_dates)
        selected_dates = calendar.selected_dates
        assert len(selected_dates) == len(_dates)
        for _ in selected_dates:
            assert _ in _dates

    def test_add_range_to_selection_test(self, wpf_element_map: WPFApplicationElements):
        """Adds a range of dates to the calendar element."""
        _dates = [
            arrow.get(datetime(2021, 3, 10)).date(),
            arrow.get(datetime(2021, 3, 15)).date(),
            arrow.get(datetime(2021, 3, 17)).date(),
        ]  # We need to use static time values to avoid test failures.
        calendar = wpf_element_map.more_controls_tab.calender
        calendar.select_date(_dates[0])
        calendar.add_range_to_selection(_dates[1:])
        selected_dates = calendar.selected_dates
        assert len(selected_dates) == len(_dates)
        for _ in selected_dates:
            assert _ in _dates
