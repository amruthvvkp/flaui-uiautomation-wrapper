"""Tests for the Menu control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\MenuTests.cs."""

from typing import Any, Dict, Generator, List

from dirty_equals import DirtyEquals, HasAttributes, IsFalseLike, IsTrueLike
from flaui.core.automation_elements import ConditionFactory, Menu
from loguru import logger
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class IsMenuStructure(DirtyEquals[List[Any]]):
    """
    Custom validator for menu and sub-menu structures.

    Example Usage:
        assert menu_items == IsMenuStructure([
            {"name": "File", "sub_items": [{"name": "Exit"}]},
            {"name": "Edit", "sub_items": [
                {"name": "Copy", "sub_items": ["Plain", "Fancy"]},
                {"name": "Paste"}
            ]}
        ])
    """

    def __init__(self, expected_structure: List[Dict[str, Any]]):
        """
        Args:
            expected_structure (List[Dict[str, Any]]): Expected menu structure.
        """
        self.expected_structure = expected_structure
        super().__init__(expected_structure)

    def equals(self, other: Any) -> bool:
        """
        Compares actual menu structure against expected.

        Args:
            other (Any): The actual menu structure.

        Returns:
            bool: True if the structures match, False otherwise.
        """
        if not isinstance(other, list):
            return False

        if len(other) != len(self.expected_structure):
            return False

        for actual_menu, expected_menu in zip(other, self.expected_structure, strict=False):
            # Ensure top-level menu names match
            if actual_menu.properties.name.value != expected_menu["name"]:
                return False

            # Check if sub-items exist
            actual_sub_items = getattr(actual_menu, "items", [])
            expected_sub_items = expected_menu.get("sub_items", [])

            if not self._validate_sub_items(actual_sub_items, expected_sub_items):
                return False

        return True

    def _validate_sub_items(self, actual_sub_items, expected_sub_items) -> bool:
        """
        Validates sub-items recursively.

        Args:
            actual_sub_items (List[Any]): Actual sub-menu items.
            expected_sub_items (List[Dict[str, Any]]): Expected sub-menu items.

        Returns:
            bool: True if they match, False otherwise.
        """
        if len(actual_sub_items) != len(expected_sub_items):
            return False

        for actual_item, expected_item in zip(actual_sub_items, expected_sub_items, strict=False):
            if isinstance(expected_item, str):
                # If expected_item is just a name, compare it directly
                if actual_item.properties.name.value != expected_item:
                    return False
            else:
                # If expected_item is a dict, check name and nested sub-items
                if actual_item.properties.name.value != expected_item["name"]:
                    return False
                if not self._validate_sub_items(actual_item.items, expected_item.get("sub_items", [])):
                    return False

        return True


class TestMenu:
    """Tests for the Menu control."""

    def test_menu_with_sub_menus(
        self,
        menu: Menu,
        test_application_type: str,
    ) -> None:
        """Tests the menu with sub menus."""

        expected_structure = [
            {"name": "File", "sub_items": [{"name": "Exit"}]},
            {"name": "Edit", "sub_items": [{"name": "Copy", "sub_items": ["Plain", "Fancy"]}, {"name": "Paste"}]},
        ]

        if test_application_type == "WPF":
            expected_structure[1]["sub_items"].append({"name": "Show Label"})

        assert menu.items == IsMenuStructure(expected_structure), "Menu structure does not match expected structure"

    def test_menu_with_sub_menus_by_name(
        self,
        menu: Menu,
    ) -> None:
        """Tests the menu with sub menus by name."""
        edit = menu.get_item_by_name("Edit")
        assert edit is not None, "Edit menu item not found"
        logger.debug(edit.properties.name.value)
        assert edit.properties.name.value == "Edit", "Edit menu item name does not match"
        copy = edit.get_item_by_name("Copy")
        assert copy is not None, "Copy menu item not found"
        assert copy.properties.name.value == "Copy", "Copy menu item name does not match"
        fancy = copy.get_item_by_name("Fancy")
        assert fancy is not None, "Fancy menu item not found"
        assert fancy.properties.name.value == "Fancy", "Fancy menu item name does not match"

    def test_checked_menu_item(self, menu: Menu, test_application_type: str) -> None:
        """Tests the checked menu item."""
        if test_application_type == "WinForms":
            pytest.skip(
                "UI Automation currently does not support Toggle pattern on menu items in WinForms applications."
            )
        edit = menu.get_item_by_name("Edit")
        assert edit is not None, "Edit menu item not found"
        show_label = edit.get_item_by_name("Show Label")
        assert show_label is not None, "Show Label menu item not found"
        assert show_label == HasAttributes(is_checked=IsTrueLike), "Show Label menu item is checked"
        show_label.is_checked = False
        assert show_label == HasAttributes(is_checked=IsFalseLike), "Show Label menu item is not checked"
        show_label.is_checked = True
        assert show_label == HasAttributes(is_checked=IsTrueLike), "Show Label menu item is checked"

    @pytest.fixture(name="menu")
    def get_application_menu(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> Generator[Menu, Any, None]:
        yield test_application.main_window.find_first_child(condition=condition_factory.menu()).as_menu()
        test_application.status_bar.click()
