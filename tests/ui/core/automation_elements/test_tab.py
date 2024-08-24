"""Tests for the Tab control."""

from flaui.core.automation_type import AutomationType
from flaui.core.input import Wait
import pytest
from pytest_check import equal

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.constants import (
    ApplicationTabIndex as WinFormsApplicationTabIndex,
)
from tests.test_utilities.elements.wpf_application.constants import ApplicationTabIndex as WpfApplicationTabIndex


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestTab(UITestBase):
    """Tests for Tab control."""

    def test_select_tab(self):
        """Tests selection of Tab controls"""
        tab = self.test_elements.tab

        if self._application_type == ApplicationType.Wpf:
            equal(len(tab.tab_items()), 3)
            tab_index = WpfApplicationTabIndex
        else:
            equal(len(tab.tab_items()), 2)
            tab_index = WinFormsApplicationTabIndex
        for index in tab_index:
            if index != tab_index.SIMPLE_CONTROLS:
                tab.select_tab_item(index.value)
                Wait.until_input_is_processed()

            equal(tab.selected_tab_item_index, index.value)

    def test_exception_on_no_input_value_to_select_tab(self):
        """Tests if ValueError is thrown on no index/value sent to select tab"""
        with pytest.raises(ValueError):
            self.test_elements.tab.select_tab_item()
