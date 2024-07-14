"""Tests for the Menu control."""

from typing import Any, Generator

from flaui.core.automation_elements import Window
from flaui.core.framework_types import FrameworkType
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.config import test_settings

@pytest.fixture(scope="class")
def wpf_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    wpf_application = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    wpf_application.application.launch(
        test_settings.WPF_TEST_APP_EXE.as_posix()
        if ui_automation_type == UIAutomationTypes.UIA3
        else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    )
    yield wpf_application

    wpf_application.application.kill()


@pytest.fixture(scope="class")
def main_window(wpf_application: Automation, automation: Any) -> Generator[Window, None, None]:
    """Fetches the main window of the test application.

    :param wpf_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield wpf_application.application.get_main_window(automation)


@pytest.fixture(scope="class")
def wpf_elements(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)


class TestMenu:
    """Tests for the Menu control."""

    def test_menu_with_sub_menus(self, wpf_elements: WPFApplicationElements):
        """Tests the menu with sub menus."""
        element = wpf_elements.main_window.find_first_child(condition=wpf_elements._cf.menu()).as_menu()
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

    def test_menu_with_sub_menus_by_name(self, wpf_elements: WPFApplicationElements):
        """Tests the menu with sub menus by name."""
        element = wpf_elements.main_window.find_first_child(condition=wpf_elements._cf.menu()).as_menu()
        edit = element.get_item_by_name("Edit")
        assert edit is not None
        assert edit.properties.name.value == "Edit"
        copy = edit.get_item_by_name("Copy")
        assert copy is not None
        assert copy.properties.name.value == "Copy"
        fancy = copy.get_item_by_name("Fancy")
        assert fancy is not None
        assert fancy.properties.name.value == "Fancy"

    def test_checked_menu_item(self, wpf_elements: WPFApplicationElements):
        """Tests the checked menu item."""
        if wpf_elements.main_window.framework_type == FrameworkType.WinForms:
            pytest.skip("UI Automation currently does not support Toggle pattern on menu items in WinForms applications.")

        element = wpf_elements.main_window.find_first_child(condition=wpf_elements._cf.menu()).as_menu()
        edit = element.get_item_by_name("Edit")
        assert edit is not None
        show_label = edit.get_item_by_name("Show Label")
        assert show_label is not None
        assert show_label.is_checked is True
        show_label.is_checked = False
        assert show_label.is_checked is False
        show_label.is_checked = True
        assert show_label.is_checked is True
