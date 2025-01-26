from typing import Any, Generator

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.test_utilities.base import FlaUITestBase


@pytest.fixture(
    scope="function",
    params=[
        (UIAutomationTypes.UIA2, "WinForms"),
        (UIAutomationTypes.UIA2, "WPF"),
        (UIAutomationTypes.UIA3, "WinForms"),
        (UIAutomationTypes.UIA3, "WPF"),
    ],
)
def ui_automation_test_app(request: pytest.FixtureRequest) -> Generator[Automation, Any, None]:
    """Fixture to launch the test application for the UIAutomation tests.

    :param request: Pytest request object.
    :yield: Application object.
    """
    ui_automation_type, app_type = request.param
    test_base = FlaUITestBase(ui_automation_type, app_type)
    yield test_base.automation
    test_base.close_test_app()


@pytest.fixture(scope="function")
def restart_test_app(
    request: pytest.FixtureRequest, ui_automation_test_app: Automation
) -> Generator[Automation, Any, None]:
    """Fixture to restart the test application for the UIAutomation tests.

    :param ui_automation_test_app: Application object.
    :yield: Application object.
    """
    ui_automation_type, app_type = request.param
    test_base = FlaUITestBase(ui_automation_type, app_type)
    test_base.restart_test_app()
    yield test_base.automation
    # tes
