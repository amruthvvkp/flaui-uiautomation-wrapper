"""Tests for the Menu control."""

from flaui.core.automation_type import AutomationType
import pytest
from pytest_check import equal, is_false, is_not_none, is_true

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
class TestMenu(UITestBase):
    """Tests for the Menu control."""

    def test_menu_with_sub_menus(self):
        """Tests the menu with sub menus."""
        element = self.test_elements.main_window.find_first_child(condition=self.test_elements._cf.menu()).as_menu()
        is_not_none(element)
        items = element.items
        equal(len(items), 2)
        equal(items[0].properties.name.value, "File")
        equal(items[1].properties.name.value, "Edit")
        sub_items = items[0].items
        equal(len(sub_items), 1)
        equal(sub_items[0].properties.name.value, "Exit")
        sub_items = items[1].items
        if self._application_type == ApplicationType.WinForms:
            # WinForms test application remained unchanged, "Edit" menu has 2 menu items: "Copy" and "Paste"
            equal(len(sub_items), 2)
        else:
            # On WPF test application has been added a new menu item "Show Label", under "Edit" menu, so now "Edit" menu has 3 menu items
            equal(len(sub_items), 3)

        equal(sub_items[0].properties.name.value, "Copy")
        equal(sub_items[1].properties.name.value, "Paste")
        if self._application_type == ApplicationType.Wpf:
            equal(sub_items[2].properties.name.value, "Show Label")

        sub_sub_items = sub_items[0].items
        equal(len(sub_sub_items), 2)
        equal(sub_sub_items[0].properties.name.value, "Plain")
        equal(sub_sub_items[1].properties.name.value, "Fancy")

    def test_menu_with_sub_menus_by_name(self):
        """Tests the menu with sub menus by name."""
        element = self.test_elements.main_window.find_first_child(condition=self.test_elements._cf.menu()).as_menu()
        edit = element.get_item_by_name("Edit")
        is_not_none(edit)
        equal(edit.properties.name.value, "Edit")
        copy = edit.get_item_by_name("Copy")
        is_not_none(copy)
        equal(copy.properties.name.value, "Copy")
        fancy = copy.get_item_by_name("Fancy")
        is_not_none(fancy)
        equal(fancy.properties.name.value, "Fancy")

    def test_checked_menu_item(self):
        """Tests the checked menu item."""
        if self._application_type == ApplicationType.WinForms:
            pytest.skip(
                "UI Automation currently does not support Toggle pattern on menu items in WinForms applications."
            )

        element = self.test_elements.main_window.find_first_child(condition=self.test_elements._cf.menu()).as_menu()
        edit = element.get_item_by_name("Edit")
        is_not_none(edit)
        show_label = edit.get_item_by_name("Show Label")
        is_not_none(show_label)
        is_true(show_label.is_checked)
        show_label.is_checked = False
        is_false(show_label.is_checked)
        show_label.is_checked = True
        is_true(show_label.is_checked)
