"""This map is used to store the element locators for the WinForms application."""

from flaui.core.automation_elements import AutomationElement, Tab, Window
from flaui.core.condition_factory import ConditionFactory
from flaui.core.definitions import ControlType
from pydantic_settings import BaseSettings

from tests.test_utilities.config import test_settings
from tests.test_utilities.elements.winforms_application.complex_controls import ComplexControlsElements
from tests.test_utilities.elements.winforms_application.menu import MenuElements
from tests.test_utilities.elements.winforms_application.more_controls import MoreControlsElements
from tests.test_utilities.elements.winforms_application.simple_controls import SimpleControlsElements
from tests.test_utilities.elements.winforms_application.title_bar import TitleBarElements


class WinFormsApplicationElements(BaseSettings):
    """This class is used to store the element locators for the WinForms application."""

    process_name: str = test_settings.WPF_TEST_APP_PROCESS
    application_name: str = "FlaUI WinForms Test App"
    main_window: Window

    @property
    def title_bar(self) -> TitleBarElements:
        """Returns the title bar element.

        :return: The title bar element.
        """
        return TitleBarElements(main_window=self.main_window)

    @property
    def menu(self) -> MenuElements:
        """Returns the menu element.

        :return: The menu element.
        """
        return MenuElements(main_window=self.main_window)

    @property
    def _cf(self) -> ConditionFactory:
        """Returns the condition factory element.

        :return: The condition factory element.
        """
        return self.main_window.condition_factory

    @property
    def status_bar(self) -> AutomationElement:
        """Returns the status bar element.

        :return: The status bar element.
        """
        return self.main_window.find_first_child(condition=self._cf.by_control_type(ControlType.StatusBar))

    @property
    def tab(self) -> Tab:
        """Returns the tab on UI

        :return: Tab element
        """
        return self.main_window.find_first_descendant(condition=self._cf.by_control_type(ControlType.Tab)).as_tab()

    @property
    def simple_controls_tab(self) -> SimpleControlsElements:
        """Returns the simple controls tab element and all child controls.

        :return: The simple controls tab element.
        """
        return SimpleControlsElements(main_window=self.main_window, tab=self.tab)

    @property
    def complex_controls_tab(self) -> ComplexControlsElements:
        """Returns the complex controls tab element and all child controls.

        :return: The complex controls tab element.
        """
        return ComplexControlsElements(main_window=self.main_window, tab=self.tab)

    @property
    def more_controls_tab(self) -> MoreControlsElements:
        """Returns the more controls tab element and all child controls.

        :return: The more controls tab element.
        """
        raise ValueError("Winforms application does not have More controls tab")


def get_winforms_application_elements(main_window: Window) -> WinFormsApplicationElements:
    """Returns the WinForms application element map."""
    return WinFormsApplicationElements(main_window=main_window)
