import time
from typing import Generator

from flaui.core.application import Application
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from loguru import logger
from pydantic import FilePath
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed

from tests.test_utilities.base import force_close_test_application_process
from tests.test_utilities.config import ApplicationType, test_settings


@pytest.fixture(scope="package")
def test_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Fixture to yield the test application.

    :param ui_automation_type: UI Automation type
    :yield: Test application
    """
    automation = Automation(ui_automation_type)
    automation.application.launch(
        str(
            test_settings.WPF_TEST_APP_EXE
            if ui_automation_type == UIAutomationTypes.UIA3
            else test_settings.WINFORMS_TEST_APP_EXE
        )
    )
    yield automation

    automation.application.kill()

    force_close_test_application_process()


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

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def start_application(
        self, automation: Automation, automation_type: UIAutomationTypes, application_type: ApplicationType
    ):
        logger.debug(f"Launching {automation_type}-{application_type} application")
        try:
            automation.application.launch(str(self.get_test_application_path(self.application_type)))
            time.sleep(0.5)
            automation.application.wait_while_main_handle_is_missing(2000)
        except Exception as e:
            logger.exception(e)
            raise
        else:
            return automation.application

    @staticmethod
    def close_application(
        application: Application, automation_type: UIAutomationTypes, application_type: ApplicationType
    ):
        logger.debug(f"Closing {automation_type}-{application_type} application")
        if application:
            try:
                application.close(True)
            except Exception as e:
                logger.exception(f"Error while killing application: {e}")

            timeout = 10
            start_time = time.time()
            while not application.has_exited and time.time() - start_time < timeout:
                time.sleep(0.5)

            if not application.has_exited:
                logger.warning("Application did not exit within the timeout period")

            force_close_test_application_process()

            application.dispose()
        logger.debug("Application closed")


@pytest.fixture(scope="session")
def ui_test_base(request, automation_type, application_type):
    logger.info(f"Starting test: {request.node.name}")
    base = UITestBase(automation_type, application_type)
    automation = base.get_automation()
    try:
        application = base.start_application(automation, automation_type, application_type)
    except Exception as e:
        logger.exception(e)
        raise
    else:
        yield application, automation
    finally:
        if application:
            base.close_application(application, automation_type, application_type)
        logger.info(f"Finished test: {request.node.name}")
