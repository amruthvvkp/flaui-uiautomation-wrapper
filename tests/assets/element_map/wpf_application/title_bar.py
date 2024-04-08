from flaui.core.automation_elements import AutomationElement, Button, TitleBar, Window
from pydantic_settings import BaseSettings


class TitleBarElements(BaseSettings):
    """This class is used to store the element locators for the title bar."""

    main_window: Window

    def _condition_factory(self):
        """Returns the condition factory for the title bar.

        :return: The condition factory for the title bar.
        """
        return self.main_window.condition_factory

    @property
    def parent_element(self) -> TitleBar:
        """Returns the title bar element.

        :return: The title bar element.
        """
        return self.main_window.find_first_child(
            condition=self._condition_factory.by_automation_id("TitleBar")
        ).as_title_bar()

    @property
    def minimize_button(self) -> Button:
        """Returns the minimize button element.

        :return: The minimize button element.
        """
        return self.parent_element.find_first_child(
            condition=self._condition_factory.by_automation_id("Minimize-Restore")
        ).as_button()

    @property
    def maximize_button(self) -> Button:
        """Returns the maximize button element.

        :return: The maximize button element.
        """
        return self.parent_element.find_first_child(
            condition=self._condition_factory.by_automation_id("Maximize-Restore")
        ).as_button()

    @property
    def close_button(self) -> Button:
        """Returns the close button element.

        :return: The close button element.
        """
        return self.parent_element.find_first_child(
            condition=self._condition_factory.by_automation_id("Close")
        ).as_button()

    @property
    def menu_bar(self) -> AutomationElement:
        """Returns the menu bar element.

        :return: The menu bar element.
        """
        return self.parent_element.find_first_child(condition=self._condition_factory.by_automation_id("SystemMenuBar"))
