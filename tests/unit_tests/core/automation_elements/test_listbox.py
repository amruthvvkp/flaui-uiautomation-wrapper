"""Tests for the ListBox control."""

from flaui.core.automation_elements import ListBoxItem
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestListBox:
    """Tests for the ListBox control."""

    def test_items(self, test_elements: WPFApplicationElements):
        """Tests the items property.

        :param wpf_elements: WPF application element map.
        """
        element = test_elements.simple_controls_tab.list_box
        assert element is not None
        assert len(element.items) == 2

    def test_select_by_index(self, test_elements: WPFApplicationElements):
        """Tests the select_by_index method.

        :param wpf_elements: WPF application element map.
        """
        element = test_elements.simple_controls_tab.list_box
        assert all([isinstance(_, ListBoxItem) for _ in element.items])
        with pytest.raises(ValueError):
            assert element.selected_item is None
        for index in range(2):
            item = element.select(index)
            assert item.text == f"ListBox Item #{index + 1}"
            assert element.selected_item.text == f"ListBox Item #{index + 1}"

    def test_select_by_text(self, test_elements: WPFApplicationElements):
        """Tests the select_by_text method.

        :param wpf_elements: WPF application element map.
        """
        element = test_elements.simple_controls_tab.list_box
        assert all([isinstance(_, ListBoxItem) for _ in element.items])
        for index in range(2):
            item = element.select(f"ListBox Item #{index + 1}")
            assert item.text == f"ListBox Item #{index + 1}"
            assert element.selected_item.text == f"ListBox Item #{index + 1}"

    def test_items_property_in_large_list(self, test_elements: WPFApplicationElements):
        """Tests the items property with a large list.

        :param wpf_elements: WPF application element map.
        """
        element = test_elements.more_controls_tab.large_list_box
        assert len(element.items) == 7
        assert element.items[6].text == "ListBox Item #7"

    def test_select_by_index_in_large_list(self, test_elements: WPFApplicationElements):
        """Tests the select_by_index method with a large list.

        :param wpf_elements: WPF application element map.
        """
        element = test_elements.more_controls_tab.large_list_box
        item = element.select(6)
        assert item.text == "ListBox Item #7"
        assert len(element.selected_items) == 1
        assert element.selected_item.text == "ListBox Item #7"

        item = element.add_to_selection(5)
        assert item.text == "ListBox Item #6"
        assert len(element.selected_items) == 2
        assert element.selected_items[0].text == "ListBox Item #7"
        assert element.selected_items[1].text == "ListBox Item #6"
