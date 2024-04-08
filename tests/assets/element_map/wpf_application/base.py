"""This map is used to store the element locators for the WPF application."""

from flaui.core.automation_elements import Window
from flaui.core.condition_factory import ConditionFactory
from flaui.core.definitions import ControlType
from pydantic_settings import BaseSettings

from tests.assets.element_map.wpf_application.complex_controls import ComplexControlsElements
from tests.assets.element_map.wpf_application.menu import MenuElements
from tests.assets.element_map.wpf_application.more_controls import MoreControlsElements
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
    def _condition_factory(self) -> ConditionFactory:
        """Returns the condition factory element.

        :return: The condition factory element.
        """
        return self.main_window.condition_factory

    @property
    def status_bar(self):
        """Returns the status bar element.

        :return: The status bar element.
        """
        return self.main_window.find_first_child(
            condition=self._condition_factory.by_control_type(ControlType.StatusBar)
        )

    @property
    def simple_controls_tab(self) -> SimpleControlsElements:
        """Returns the simple controls tab element and all child controls.

        :return: The simple controls tab element.
        """
        return SimpleControlsElements(main_window=self.main_window)

    @property
    def complex_controls_tab(self) -> ComplexControlsElements:
        """Returns the complex controls tab element and all child controls.

        :return: The complex controls tab element.
        """
        return ComplexControlsElements(main_window=self.main_window)

    @property
    def more_controls_tab(self) -> MoreControlsElements:
        """Returns the more controls tab element and all child controls.

        :return: The more controls tab element.
        """
        return MoreControlsElements(main_window=self.main_window)


def get_wpf_application_elements(main_window: Window):
    """Returns the WPF application element map."""
    return WPFApplicationElements(main_window=main_window)
