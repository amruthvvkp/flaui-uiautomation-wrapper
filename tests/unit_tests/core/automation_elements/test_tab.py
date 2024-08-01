"""Tests for the Tab control."""

from flaui.core.input import Wait
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.assets.elements.wpf_application.constants import ApplicationTabIndex


class TestTab:
    """Tests for Tab control."""

    def test_select_tab(self, test_elements: WPFApplicationElements):
        """Tests selection of Tab controls"""
        tab = test_elements.tab

        assert (
            len(tab.tab_items()) == 3 if test_elements.process_name == "WpfApplication.exe" else 2
        )  # TODO: Set Winforms elements to this test case
        for index in ApplicationTabIndex:
            if index != ApplicationTabIndex.SIMPLE_CONTROLS:
                tab.select_tab_item(index.value)
                Wait.until_input_is_processed()

            assert tab.selected_tab_item_index == index.value

    def test_exception_on_no_input_value_to_select_tab(self, test_elements: WPFApplicationElements):
        """Tests if ValueError is thrown on no index/value sent to select tab"""
        with pytest.raises(ValueError):
            test_elements.tab.select_tab_item()
