import time

from flaui.core.application import Application
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from loguru import logger
from pydantic import FilePath
import pytest

from tests.test_utilities.config import ApplicationType, test_settings


class UITestBase:
    def __init__(self, automation_type: UIAutomationTypes, application_type: ApplicationType):
        self.automation_type = automation_type
        self.application_type = application_type

    def get_automation(self):
        return Automation(self.automation_type)

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

    def start_application(self, automation: Automation):
        try:
            automation.application.launch(str(self.get_test_application_path(self.application_type)))
            automation.application.wait_while_main_handle_is_missing()
        except Exception as e:
            logger.exception(e)
            raise
        else:
            return automation.application

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


@pytest.fixture(scope="class")
def ui_test_base(request, automation_type, application_type):
    base = UITestBase(automation_type, application_type)
    automation = base.get_automation()
    app = base.start_application(automation)
    yield app, automation
    base.close_application(app)


# def pytest_itemcollected(item):
#     # Get the original name
#     name = item.name
#     # Extract parameter values
#     automation_type = item.callspec.params["automation_type"]
#     application_type = item.callspec.params["application_type"]
#     # Create the custom name
#     item.name = f"{name}-{automation_type.name}-{application_type}"
#     item._nodeid = item.name  # Update the nodeid to reflect the new name
