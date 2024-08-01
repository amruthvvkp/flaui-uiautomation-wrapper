"""Tests for the date time picker control."""

import arrow

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestDateTimePicker:
    """Tests for the date time picker control."""

    def test_select_date(self, test_elements: WPFApplicationElements):
        """Tests the select date method.

        :param wpf_elements: The WPF application element map.
        """

        date = arrow.get(2021, 5, 17).date()
        date_time_picker = test_elements.more_controls_tab.date_picker
        date_time_picker.selected_date = date
        assert date_time_picker.selected_date == date
