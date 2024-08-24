"""Tests for the Menu control."""

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.modules.automation import Automation
import pytest
from pytest_check import equal, is_false, is_not_none, is_true

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestMenu:
    """Tests for the Menu control."""

    @pytest.fixture(autouse=True)
    def setup_method(
        self,
        ui_test_base: tuple[Application, Automation],
        automation_type: AutomationType,
        application_type: ApplicationType,
    ):
        """Sets up essential properties for tests in this class.

        :param ui_test_base: UI Test base fixture
        :param automation_type: Automation Type
        :param application_type: Application Type
        """
        application, automation = ui_test_base
        self.application = application
        self.main_window: Window = application.get_main_window(automation)
        self.automation = automation
        self._automation_type = automation_type
        self._application_type = application_type
        self.test_elements = (
            get_wpf_application_elements(main_window=self.main_window)
            if self._application_type == ApplicationType.Wpf
            else get_winforms_application_elements(main_window=self.main_window)
        )

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
