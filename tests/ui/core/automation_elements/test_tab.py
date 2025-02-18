"""Tests for the Tab control."""

from dirty_equals import HasAttributes, HasLen
from flaui.core.input import Wait
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.winforms_application.constants import (
    ApplicationTabIndex as WinFormsApplicationTabIndex,
)
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements
from tests.test_utilities.elements.wpf_application.constants import ApplicationTabIndex as WpfApplicationTabIndex


class TestTab:
    """Tests for Tab control."""

    def test_select_tab(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, test_application_type: str
    ) -> None:
        """Tests selection of Tab controls"""
        tab = test_application.tab

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

    def test_exception_on_no_input_value_to_select_tab(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Tests if ValueError is thrown on no index/value sent to select tab"""
        with pytest.raises(ValueError):
            test_application.tab.select_tab_item()
