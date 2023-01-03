import os
from typing import Any, Generator, Literal

import psutil, pytest

from config import settings
from flaui.lib.enums import UIAutomationTypes
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from flaui.wrappers.core.automation_elements import AutomationElement


def close_test_application_process():
    for process in (process for process in psutil.process_iter() if process.name() == "WpfApplication.exe"):
        process.terminate()


@pytest.fixture(scope="package")
def ui_automation_type() -> Generator[Literal[UIAutomationTypes.UIA3, UIAutomationTypes.UIA2], None, None]:
    yield UIAutomationTypes.UIA3 if os.getenv(
        "DEFAULT_UIA_VERSION", "UIA3"
    ).upper() == "UIA3" else UIAutomationTypes.UIA2


@pytest.fixture(scope="package")
def automation(ui_automation_type: UIAutomationTypes) -> Generator[Any, None, None]:
    from FlaUI.UIA2 import UIA2Automation  # pyright: ignore
    from FlaUI.UIA3 import UIA3Automation  # pyright: ignore

    yield UIA3Automation() if ui_automation_type == UIAutomationTypes.UIA3 else UIA2Automation()


@pytest.fixture(scope="package")
def test_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    automation = Automation(ui_automation_type)
    automation.application.launch(settings.WPF_TEST_APP)
    yield automation

    automation.application.kill()

    close_test_application_process()


@pytest.fixture(scope="package")
def wordpad(ui_automation_type: UIAutomationTypes):
    test_automation = Automation(ui_automation_type)
    test_automation.application.launch("wordpad.exe")
    yield test_automation

    test_automation.application.kill()


@pytest.fixture(scope="package")
def test_app_main_window(test_application: Automation, automation: Any) -> Generator[AutomationElement, None, None]:
    yield test_application.application.get_main_window(automation)
