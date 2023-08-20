"""This map is used to store the element locators for the WPF application."""

from pydantic_settings import BaseSettings

from flaui.core.automation_elements import Window
from flaui.core.definitions import ControlType
from tests.assets.element_map.wpf_application.menu import MenuElements
from tests.assets.element_map.wpf_application.simple_controls import SimpleControlsElements
from tests.assets.element_map.wpf_application.title_bar import TitleBarElements


class WPFApplicationElements(BaseSettings):
    """This class is used to store the element locators for the WPF application."""
    process_name: str = "WpfApplication.exe"
    application_name: str = "FlaUI WPF Test App"
    main_window: Window

    @property
    def title_bar(self):
        """Returns the title bar element.

        :return: The title bar element.
        """
        return TitleBarElements(main_window=self.main_window)

    @property
    def menu(self):
        """Returns the menu element.

        :return: The menu element.
        """
        return MenuElements(main_window=self.main_window)

    @property
    def status_bar(self):
        """Returns the status bar element.

        :return: The status bar element.
        """
        return self.main_window.find_first_child(condition=self.main_window.condition_factory.by_control_type(ControlType.StatusBar))

    @property
    def simple_controls_tab(self):
        """Returns the simple controls tab element and all child controls.

        :return: The simple controls tab element.
        """
        return SimpleControlsElements(main_window=self.main_window)

def get_wpf_application_elements(main_window: Window):
    """Returns the WPF application element map."""
    return WPFApplicationElements(main_window=main_window)
