"""UIAutomation test fixtures."""

import gc
import time
from typing import Any, Generator

from flaui.lib.enums import UIAutomationTypes
from flaui.lib.exceptions import ElementNotFound
from loguru import logger
import pytest

from tests.test_utilities.base import FlaUITestBase
from tests.test_utilities.elements.winforms_application.base import (
    WinFormsApplicationElements,
    get_winforms_application_elements,
)
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements, get_wpf_application_elements


@pytest.fixture(scope="session")
def launch_all_test_applications() -> Generator[dict[UIAutomationTypes, dict[str, FlaUITestBase]], Any, None]:
    """Fixture to launch all test applications for the UIAutomation tests."""
    result = {UIAutomationTypes.UIA2: {}, UIAutomationTypes.UIA3: {}}

    for app_type in ["WinForms", "WPF"]:
        for ui_automation_type in [UIAutomationTypes.UIA2, UIAutomationTypes.UIA3]:
            test_base = FlaUITestBase(ui_automation_type, app_type)
            try:
                logger.debug(f"Launching test application: {app_type} with {ui_automation_type}")
                test_base.launch_test_app()
                time.sleep(1)  # Give time for UI to initialize
                assert test_base.automation.application, "Application did not start correctly!"
            except Exception as e:
                logger.error(f"Error launching test app: {e}")
                pytest.exit("Test application failed to launch!")
            else:
                result[ui_automation_type][app_type] = test_base
    yield result
    for ui_automation_type in [UIAutomationTypes.UIA2, UIAutomationTypes.UIA3]:
        for app_type in ["WinForms", "WPF"]:
            test_base = result[ui_automation_type][app_type]
            test_base.close_test_app()
            gc.collect()


@pytest.fixture(
    scope="session",
    params=[
        pytest.param((UIAutomationTypes.UIA2, "WinForms"), id="UIA2_WinForms"),
        pytest.param((UIAutomationTypes.UIA2, "WPF"), id="UIA2_WPF"),
        pytest.param((UIAutomationTypes.UIA3, "WinForms"), id="UIA3_WinForms"),
        pytest.param((UIAutomationTypes.UIA3, "WPF"), id="UIA3_WPF"),
    ],
)
def setup_ui_testing_environment(
    request: pytest.FixtureRequest, launch_all_test_applications: dict[UIAutomationTypes, dict[str, FlaUITestBase]]
) -> Generator[FlaUITestBase, Any, None]:
    """Fixture to launch the test application for the UIAutomation tests."""
    ui_automation_type, test_application_type = request.param

    yield launch_all_test_applications[ui_automation_type][test_application_type]


@pytest.fixture(scope="class", name="test_application")
def get_ui_test_application(
    setup_ui_testing_environment: FlaUITestBase,
) -> Generator[WinFormsApplicationElements | WPFApplicationElements, Any, None]:
    """Fixture to get the test application for the UIAutomation tests.

    :param setup_ui_testing_environment: Application object.
    :yield: Application object.
    """
    application = setup_ui_testing_environment.automation.application
    automation = setup_ui_testing_environment.automation.cs_automation
    test_application_type = setup_ui_testing_environment.app_type
    elements = (
        get_winforms_application_elements(application.get_main_window(automation))
        if test_application_type == "WinForms"
        else get_wpf_application_elements(application.get_main_window(automation))
    )
    try:
        elements.main_window.find_first_descendant(
            condition=elements._cf.by_name("Simple Controls")
        ).as_tab_item().click()
    except ElementNotFound as e:
        print(f"Error: {e}")
    yield elements


@pytest.fixture()
def ui_automation_type(setup_ui_testing_environment: FlaUITestBase) -> Generator[UIAutomationTypes, None, None]:
    """Fixture to get the UIAutomation type for the UIAutomation tests.

    :param setup_ui_testing_environment: Application object.
    :yield: UIAutomation type.
    """
    yield setup_ui_testing_environment.ui_automation_type


@pytest.fixture()
def test_application_type(setup_ui_testing_environment: FlaUITestBase) -> Generator[str, None, None]:
    """Fixture to get the test application type for the UIAutomation tests.

    :param setup_ui_testing_environment: Application object.
    :yield: Test application type.
    """
    yield setup_ui_testing_environment.app_type


@pytest.fixture()
def condition_factory(test_application: WinFormsApplicationElements | WPFApplicationElements) -> Generator:
    """Fixture to get the condition factory for the UIAutomation tests.

    :param test_application: Application object.
    :yield: Condition factory.
    """
    yield test_application._cf


# @pytest.fixture(scope="function")
# def restart_test_app(request: pytest.FixtureRequest, test_app: Automation) -> Generator[Automation, Any, None]:
#     """Fixture to restart the test application for the UIAutomation tests.

#     :param test_app: Application object.
#     :yield: Application object.
#     """
#     ui_automation_type, test_application_type = request.param
#     test_base = FlaUITestBase(ui_automation_type, test_application_type)
#     test_base.restart_test_app()
#     yield test_base.automation
#     # tes
