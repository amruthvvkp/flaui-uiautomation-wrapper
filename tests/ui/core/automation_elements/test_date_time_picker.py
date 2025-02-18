"""Tests for the date time picker control."""

import arrow
from dirty_equals import IsDate

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestDateTimePicker:
    """Tests for the datetime picker control."""

    def test_select_date(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, test_application_type: str
    ) -> None:
        """Tests the select date method."""

        date = arrow.get(2021, 5, 17).date()
        if test_application_type == "WPF":
            date_time_picker = test_application.more_controls_tab.date_picker  # type: ignore
        else:
            date_time_picker = test_application.simple_controls_tab.date_picker  # type: ignore
        date_time_picker.selected_date = date
        assert date_time_picker.selected_date == IsDate(approx=date)
