"""This map is used to store the Menu element locators for the WPF application."""

from flaui.core.automation_elements import Menu, MenuItem, Window
from flaui.core.condition_factory import ConditionFactory
from pydantic_settings import BaseSettings


class MenuElements(BaseSettings):
    """This class is used to store the Menu element locators for the WPF application."""

    main_window: Window

    @property
    def _get_condition_factory(self) -> ConditionFactory:
        """Returns the condition factory for the Menu.

        :return: The condition factory for the Menu.
        """
        return self.main_window.condition_factory

    @property
    def parent_element(self) -> Menu:
        """Returns the Menu element.

        :return: The Menu element.
        """
        return self.main_window.find_first_child(condition=self._get_condition_factory.by_class_name("Menu")).as_menu()

    @property
    def file_menu(self) -> MenuItem:
        """Returns the File Menu element.

        :return: The File Menu element.
        """
        all_menu_items = self.parent_element.find_all_children(
            condition=self._get_condition_factory.by_class_name("MenuItem")
        )
        file_menu_item = [menu_item for menu_item in all_menu_items if menu_item.name == "File"][0]
        return file_menu_item.as_menu_item()

    @property
    def edit_menu(self) -> MenuItem:
        """Returns the Edit Menu element.

        :return: The Edit Menu element.
        """
        all_menu_items = self.parent_element.find_all_children(
            condition=self._get_condition_factory.by_class_name("MenuItem")
        )
        edit_menu_item = [menu_item for menu_item in all_menu_items if menu_item.name == "Edit"][0]
        return edit_menu_item.as_menu_item()
