"""Tests for the date time picker control."""

from typing import Any, Generator

import arrow
from dirty_equals import IsDate
from flaui.core.automation_elements import DateTimePicker
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestDateTimePicker:
    """Tests for the datetime picker control."""

    @pytest.fixture(name="date_time_picker")
    def get_date_time_picker(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, test_application_type: str
    ) -> Generator[DateTimePicker, Any, None]:
        """Returns the date time picker element.

        :param test_application: Test application elements.
        :yield: Date time picker element.
        """
        if test_application_type == "WPF":
            yield test_application.more_controls_tab.date_picker  # type: ignore
        else:
            yield test_application.simple_controls_tab.date_picker  # type: ignore

    def test_select_date(self, date_time_picker: DateTimePicker) -> None:
        """Tests the select date method."""

        date = arrow.get(2021, 5, 17).date()
        date_time_picker.selected_date = date
        assert date_time_picker.selected_date == IsDate(approx=date)
