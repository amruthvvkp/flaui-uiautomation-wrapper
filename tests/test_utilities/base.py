# Utilities for unit or example tests


import time
from typing import Dict, Tuple, Union

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from loguru import logger
import psutil
from pydantic import FilePath
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed

from tests.test_utilities.config import ApplicationType, test_settings
from tests.test_utilities.elements.winforms_application.base import (
    WinFormsApplicationElements,
    get_winforms_application_elements,
)
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements, get_wpf_application_elements


def force_close_test_application_process():
    """Close the test application process."""
    for process in (
        process
        for process in psutil.process_iter()
        if process.name() == test_settings.WPF_TEST_APP_PROCESS
        or process.name() == test_settings.WINFORMS_TEST_APP_PROCESS
    ):
        process.terminate()


class FlaUITestBase:
    """Base class for ui tests with some helper methods."""

    def get_automation(self, automation_type: UIAutomationTypes) -> Automation:
        """
        Get the automation instance that should be used.

        :return: The automation instance
        """
        return Automation(automation_type)

    @pytest.fixture(autouse=True)
    def setup_environment(self, automation_type: UIAutomationTypes, application_type: ApplicationType):
        """Fixture to setup the environment for the test

        :param automation_type: Automation Type
        :param application_type: Application Type
        """
        pass

    def start_application(self):
        """Start the application.

        :return: Application instance
        """
        pass

    def restart_application(self):
        """Close and restart the application."""
        self.close_application()
        self.start_application()

    @staticmethod
    def close_application():
        """Close the application."""
        pass


class UITestBase(FlaUITestBase):
    """Base class for UI Tests with FlaUI test applications"""

    _application_cache: Dict[Tuple[UIAutomationTypes, ApplicationType], Application] = {}

    @staticmethod
    def get_test_application_path(application_type: ApplicationType) -> FilePath:
        """Fetches the path of the Test Application

        :param application_type: Test Application Type
        """
        if application_type == ApplicationType.Wpf:
            return test_settings.WPF_TEST_APP_EXE
        elif application_type == ApplicationType.WinForms:
            return test_settings.WINFORMS_TEST_APP_EXE

    @staticmethod
    def get_test_application_process(application_type: ApplicationType) -> str:
        if application_type == ApplicationType.Wpf:
            return test_settings.WPF_TEST_APP_PROCESS
        elif application_type == ApplicationType.WinForms:
            return test_settings.WINFORMS_TEST_APP_PROCESS

    @pytest.fixture(scope="class", autouse=True)
    def application_lifecycle(self, request):
        def fin():
            for app in self._application_cache.values():
                self.close_application(app)
            self._application_cache.clear()

        request.addfinalizer(fin)

    @pytest.fixture(autouse=True)
    def setup_environment(
        self, application_lifecycle, automation_type: UIAutomationTypes, application_type: ApplicationType
    ):
        """Fixture to setup the environment for the test

        :param automation_type: Automation Type
        :param application_type: Application Type
        """
        self._automation_type: UIAutomationTypes = automation_type
        self._application_type: ApplicationType = application_type

        self.automation: Automation = Automation(automation_type)
        self.start_application()
        yield

    @property
    def application(self) -> Application:
        """Fetches Application object

        :return: Application
        """
        if not hasattr(self.automation, "application"):
            raise ValueError("Automation object does not have `application` attribute, cannot fetch `application`")

        return self.automation.application

    @property
    def main_window(self) -> Window:
        """Fetches Main Window object

        :return: Main Window parsed as Window control
        """
        if not hasattr(self.automation, "application"):
            raise ValueError("Automation object does not have `application` attribute, cannot fetch `main_window`")
        main_window = self.application.get_main_window(self.automation)
        if main_window:
            main_window.focus()
        return main_window

    @property
    def condition_factory(self) -> ConditionFactory:
        """Fetches Condition Factory object from the running application

        :return: Condition Factory
        """
        if not hasattr(self.automation, "application"):
            raise ValueError(
                "Automation object does not have `application` attribute, cannot fetch `condition_factory`"
            )
        return self.main_window.condition_factory

    @property
    def test_elements(self) -> Union[WPFApplicationElements, WinFormsApplicationElements]:
        """Generates an instance of test elements

        :return: Application Element map
        """
        if not hasattr(self.automation, "application"):
            raise ValueError("Automation object does not have `application` attribute, cannot fetch `test_elements`")
        if self._application_type == ApplicationType.Wpf:
            return get_wpf_application_elements(main_window=self.main_window)
        else:
            return get_winforms_application_elements(main_window=self.main_window)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def start_application(self):
        """Start the application.

        :return: Application instance
        """
        key = self._parse_app_cache_key
        if key not in self._application_cache:
            try:
                self.automation.application.launch(str(self.get_test_application_path(self._application_type)))
                self.automation.application.wait_while_main_handle_is_missing()
            except Exception as e:
                logger.exception(e)
                raise
            else:
                self._application_cache[key] = self.automation.application
        else:
            self.automation.application = self._application_cache[key]

    @property
    def _parse_app_cache_key(self):
        """Parses Key for the Application in Application Cache

        :return: Parsed key
        """
        key = (self._automation_type, self._application_type)
        return key

    def restart_application(self):
        """Close and restart the application."""
        key = self._parse_app_cache_key
        if key in self._application_cache:
            application = self._application_cache[key]
            self.close_application(application)
            self._application_cache.pop(key, None)

        self.start_application()

    @staticmethod
    def close_application(application: Application):
        """Close the application."""
        if application:
            while application.has_exited is False:
                try:
                    application.close()
                except Exception as e:
                    logger.exception(e)
                finally:
                    time.sleep(2)
            application.dispose()
