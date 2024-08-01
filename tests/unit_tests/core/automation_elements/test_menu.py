"""Tests for the Menu control."""

from flaui.core.framework_types import FrameworkType
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestMenu:
    """Tests for the Menu control."""

    def test_menu_with_sub_menus(self, test_elements: WPFApplicationElements):
        """Tests the menu with sub menus."""
        element = test_elements.main_window.find_first_child(condition=test_elements._cf.menu()).as_menu()
        assert element is not None
        items = element.items
        assert len(items) == 2
        assert items[0].properties.name.value == "File"
        assert items[1].properties.name.value == "Edit"
        sub_items = items[0].items
        assert len(sub_items) == 1
        assert sub_items[0].properties.name.value == "Exit"
        sub_items = items[1].items
        if element.framework_type == FrameworkType.WinForms:
            # WinForms test application remained unchanged, "Edit" menu has 2 menu items: "Copy" and "Paste"
            assert len(sub_items) == 2
        else:
            # On WPF test application has been added a new menu item "Show Label", under "Edit" menu, so now "Edit" menu has 3 menu items
            assert len(sub_items) == 3

        assert sub_items[0].properties.name.value == "Copy"
        assert sub_items[1].properties.name.value == "Paste"
        if element.framework_type == FrameworkType.WinForms:
            assert sub_items[2].properties.name.value == "Show Label"

        sub_sub_items = sub_items[0].items
        assert len(sub_sub_items) == 2
        assert sub_sub_items[0].properties.name.value == "Plain"
        assert sub_sub_items[1].properties.name.value == "Fancy"

    def test_menu_with_sub_menus_by_name(self, test_elements: WPFApplicationElements):
        """Tests the menu with sub menus by name."""
        element = test_elements.main_window.find_first_child(condition=test_elements._cf.menu()).as_menu()
        edit = element.get_item_by_name("Edit")
        assert edit is not None
        assert edit.properties.name.value == "Edit"
        copy = edit.get_item_by_name("Copy")
        assert copy is not None
        assert copy.properties.name.value == "Copy"
        fancy = copy.get_item_by_name("Fancy")
        assert fancy is not None
        assert fancy.properties.name.value == "Fancy"

    def test_checked_menu_item(self, test_elements: WPFApplicationElements):
        """Tests the checked menu item."""
        if test_elements.main_window.framework_type == FrameworkType.WinForms:
            pytest.skip(
                "UI Automation currently does not support Toggle pattern on menu items in WinForms applications."
            )

        element = test_elements.main_window.find_first_child(condition=test_elements._cf.menu()).as_menu()
        edit = element.get_item_by_name("Edit")
        assert edit is not None
        show_label = edit.get_item_by_name("Show Label")
        assert show_label is not None
        assert show_label.is_checked is True
        show_label.is_checked = False
        assert show_label.is_checked is False
        show_label.is_checked = True
        assert show_label.is_checked is True
