"""This contains common abstracts of element map classes for all the control pages of the WPF test application."""

from abc import ABC

from flaui.core.automation_elements import Window
from pydantic_settings import BaseSettings

class AbtstractControlCollection(BaseSettings, ABC):
    """This abstract class is used to store the element locators for the WPF application."""

    main_window: Window

    @property
    def _condition_factory(self):
        """Returns the condition factory for the Simple Controls.

        :return: The condition factory for the Simple Controls.
        """
        return self.main_window.condition_factory
