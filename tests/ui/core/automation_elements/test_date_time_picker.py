"""Tests for the date time picker control."""

import arrow
from flaui.core.automation_type import AutomationType
import pytest
from pytest_check import equal

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestDateTimePicker(UITestBase):
    """Tests for the datetime picker control."""

    def test_select_date(self):
        """Tests the select date method."""

        date = arrow.get(2021, 5, 17).date()
        if self._application_type == ApplicationType.Wpf:
            date_time_picker = self.test_elements.more_controls_tab.date_picker  # type: ignore
        else:
            date_time_picker = self.test_elements.simple_controls_tab.date_picker  # type: ignore
        date_time_picker.selected_date = date
        equal(date_time_picker.selected_date, date)
