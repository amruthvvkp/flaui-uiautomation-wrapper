"""Tests for the ListBox control."""

from flaui.core.automation_elements import ListBoxItem
from flaui.core.automation_type import AutomationType
import pytest
from pytest_check import equal, is_instance, is_none, is_not_none

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
class TestListBox(UITestBase):
    """Tests for the ListBox control."""

    def test_items(self):
        """Tests the items property."""
        element = self.test_elements.simple_controls_tab.list_box
        is_not_none(element)
        equal(len(element.items), 2)

    def test_select_by_index(self):
        """Tests the select_by_index method."""
        element = self.test_elements.simple_controls_tab.list_box
        [is_instance(_, ListBoxItem) for _ in element.items]
        with pytest.raises(ValueError):
            is_none(element.selected_item)
        for index in range(2):
            item = element.select(index)
            equal(item.text, f"ListBox Item #{index + 1}")
            equal(element.selected_item.text, f"ListBox Item #{index + 1}")

    def test_select_by_text(self):
        """Tests the select_by_text method."""
        element = self.test_elements.simple_controls_tab.list_box
        [is_instance(_, ListBoxItem) for _ in element.items]
        for index in range(2):
            item = element.select(f"ListBox Item #{index + 1}")
            equal(item.text, f"ListBox Item #{index + 1}")
            equal(element.selected_item.text, f"ListBox Item #{index + 1}")

    def test_items_property_in_large_list(self):
        """Tests the items property with a large list."""
        if (
            self._application_type == ApplicationType.WinForms
        ):  # test only for WPF, in Windows Forms all list items are loaded at startup
            pytest.skip("test only for WPF, in Windows Forms all list items are loaded at startup")
        element = self.test_elements.more_controls_tab.large_list_box
        equal(len(element.items), 7)
        equal(element.items[6].text, "ListBox Item #7")

    def test_select_by_index_in_large_list(self):
        """Tests the select_by_index method with a large list."""
        if (
            self._application_type == ApplicationType.WinForms
        ):  # test only for WPF, in Windows Forms all list items are loaded at startup
            pytest.skip("test only for WPF, in Windows Forms all list items are loaded at startup")

        element = self.test_elements.more_controls_tab.large_list_box
        item = element.select(6)
        equal(item.text, "ListBox Item #7")
        equal(len(element.selected_items), 1)
        equal(element.selected_item.text, "ListBox Item #7")

        item = element.add_to_selection(5)
        equal(item.text, "ListBox Item #6")
        equal(len(element.selected_items), 2)
        equal(element.selected_items[0].text, "ListBox Item #7")
        equal(element.selected_items[1].text, "ListBox Item #6")
