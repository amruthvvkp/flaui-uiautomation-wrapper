# This file consists of fixtures that are used in the unit tests.
import os
from typing import Any
from typing import Generator
from typing import Literal

from config import test_settings
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
from loguru import logger
import psutil
from pydantic import FilePath
import pytest

# # isort: off

setup_pythonnet_bridge()

from flaui.core.automation_elements import AutomationElement
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation

# # isort: on


def close_test_application_process():
    """This closes the test application process if it is still running."""
    for process in (process for process in psutil.process_iter() if process.name() == "WpfApplication.exe"):
        process.terminate()


@pytest.fixture(scope="package")
def ui_automation_type() -> Generator[Literal[UIAutomationTypes.UIA3, UIAutomationTypes.UIA2], None, None]:
    """Sets the UIAutomation type to use for the tests.

    :yield: UIAutomation type to use for the tests.
    """
    yield UIAutomationTypes.UIA3 if os.getenv(
        "DEFAULT_UIA_VERSION", "UIA3"
    ).upper() == "UIA3" else UIAutomationTypes.UIA2


@pytest.fixture(scope="package")
def automation(ui_automation_type: UIAutomationTypes) -> Generator[Any, None, None]:
    """Sets the Automation class to use for the tests.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: Automation class to use for the tests.
    """
    from FlaUI.UIA2 import UIA2Automation  # pyright: ignore
    from FlaUI.UIA3 import UIA3Automation  # pyright: ignore

    yield UIA3Automation() if ui_automation_type == UIAutomationTypes.UIA3 else UIA2Automation()


@pytest.fixture(scope="package")
def test_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    automation = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    if not test_settings.WPF_TEST_APP.exists():
        download_test_application_from_github(test_settings.WPF_TEST_APP)
    automation.application.launch(test_settings.WPF_TEST_APP.as_posix())
    yield automation

    automation.application.kill()

    close_test_application_process()


@pytest.fixture(scope="package")
def wordpad(ui_automation_type: UIAutomationTypes):
    """Generates FlaUI Automation class with the wordpad application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the wordpad application.
    """
    test_automation = Automation(ui_automation_type)
    test_automation.application.launch("wordpad.exe")
    yield test_automation

    test_automation.application.kill()


@pytest.fixture(scope="package")
def test_app_main_window(test_application: Automation, automation: Any) -> Generator[AutomationElement, None, None]:
    """Fetches the main window of the test application.

    :param test_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield test_application.application.get_main_window(automation)

@pytest.fixture(scope="package")
def condition_factory(automation: Any) -> Generator[ConditionFactory, None, None]:
    """Generates FlaUI ConditionFactory class.

    :param automation: Automation class to use for the tests.
    :yield: FlaUI ConditionFactory class.
    """
    yield ConditionFactory(raw_cf=automation.condition_factory)


def download_test_application_from_github(application_path: FilePath):
    """This downloads a test application .exe file from github to run the unit tests against.

    :param application_path: Local application path to download the test application to.
    """
    import urllib.request

    mapped_application_url = {
        "WpfApplication.exe": "https://raw.githubusercontent.com/GDATASoftwareAG/robotframework-flaui/main/atests/apps/WpfApplication.exe",
    }

    if application_path.name not in mapped_application_url:
        raise ValueError(f"Application {application_path.name} is not mapped to a URL.")

    url = mapped_application_url[application_path.name]
    urllib.request.urlretrieve(url, application_path)
    logger.debug(f"Downloaded test application from {url} to {application_path}")
