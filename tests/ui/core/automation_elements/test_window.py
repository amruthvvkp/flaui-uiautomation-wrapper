"""Tests for the Window control."""

from typing import Dict, Tuple

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.core.input import Mouse, MouseButton, Wait
from flaui.modules.automation import Automation
from loguru import logger
import pytest
from pytest_check import equal

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements


# UIA3 WinForms test is Broken in newer .NET Versions
@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        # (AutomationType.UIA2, ApplicationType.WinForms), # TODO: Somehow the context menu of Winforms isn't getting captured, fix it and run this test
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestWindow:
    """Tests for Window control."""

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(
        self,
        request: pytest.FixtureRequest,
        setup_application_cache: Dict[Tuple[AutomationType, ApplicationType], Tuple[Automation, Application]],
        automation_type: AutomationType,
        application_type: ApplicationType,
    ):
        """Sets up essential properties for tests in this class.

        :param ui_test_base: UI Test base fixture
        :param automation_type: Automation Type
        :param application_type: Application Type
        """
        logger.info(f"Starting test: {request.node.name}")
        automation, application = setup_application_cache[(automation_type, application_type)]
        self.application = application
        self.main_window: Window = application.get_main_window(automation)
        self.automation = automation
        self._automation_type = automation_type
        self._application_type = application_type
        self.test_elements = (
            get_wpf_application_elements(main_window=self.main_window)
            if self._application_type == ApplicationType.Wpf
            else get_winforms_application_elements(main_window=self.main_window)
        )
        yield
        logger.info(f"Finished test: {request.node.name}")

    def test_context_menu(self):
        """Tests Context Menu of Window controls"""
        button = self.test_elements.simple_controls_tab.context_menu_button
        Mouse.click(button.get_clickable_point(), mouse_button=MouseButton.Right)
        Wait.until_input_is_processed()
        try:
            context_menu = self.test_elements.main_window.context_menu
        except Exception:
            pytest.fail("Context menu did not appear as expected")
        else:
            equal(len(context_menu.items), 2)
            equal(len(context_menu.items[1].items), 1)
            equal(context_menu.items[1].items[0].text, "Inner Context")
