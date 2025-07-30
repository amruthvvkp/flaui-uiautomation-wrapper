"""Tests for the Tab control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\TabTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, HasLen
from flaui.core.automation_elements import Tab
from flaui.core.input import Wait
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.winforms_application.constants import (
    ApplicationTabIndex as WinFormsApplicationTabIndex,
)
from tests.test_utilities.elements.wpf_application import WPFApplicationElements
from tests.test_utilities.elements.wpf_application.constants import ApplicationTabIndex as WpfApplicationTabIndex


class TestTab:
    """Tests for Tab control."""

    @pytest.fixture(name="tab")
    def get_tab(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Tab, Any, None]:
        """Returns the tab element.

        :param test_application: Test application elements.
        :return: Test tab element.
        """
        yield test_application.tab

    def test_select_tab(self, tab: Tab, test_application_type: str) -> None:
        """Tests selection of Tab controls"""
        if test_application_type == "WPF":
            assert tab == HasAttributes(tab_items=HasLen(3)), "Tab for WPF application should have 3 items."
            tab_index = WpfApplicationTabIndex
        else:
            assert tab == HasAttributes(tab_items=HasLen(2)), "Tab for WinForms application should have 2 items."
            tab_index = WinFormsApplicationTabIndex
        for index in tab_index:
            if index != tab_index.SIMPLE_CONTROLS:
                tab.select_tab_item(index.value)
                Wait.until_input_is_processed()

            assert tab == HasAttributes(selected_tab_item_index=index.value), f"Tab item {index.value} not selected."

    def test_exception_on_no_input_value_to_select_tab(self, tab: Tab) -> None:
        """Tests if ValueError is thrown on no index/value sent to select tab"""
        with pytest.raises(ValueError):
            tab.select_tab_item()
