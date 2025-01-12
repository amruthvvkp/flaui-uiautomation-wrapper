"""Tests for the Radio Button control."""

from typing import Dict, Tuple

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.modules.automation import Automation
from loguru import logger
import pytest
from pytest_check import is_false, is_true

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestRadioButton:
    """Tests for RadioButton control."""

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

    def test_select_single_radio_button(self):
        """Tests the select single radio button."""
        element = self.test_elements.simple_controls_tab.radio_button_1
        is_false(element.is_checked)
        element.is_checked = True
        is_true(element.is_checked)

    def test_select_radio_button_group(self):
        """Tests the select radio button group."""
        radio_button_1 = self.test_elements.simple_controls_tab.radio_button_1
        radio_button_2 = self.test_elements.simple_controls_tab.radio_button_2

        is_false(radio_button_2.is_checked)
        radio_button_1.is_checked = True
        is_true(radio_button_1.is_checked)
        is_false(radio_button_2.is_checked)
        radio_button_2.is_checked = True
        is_false(radio_button_1.is_checked)
        is_true(radio_button_2.is_checked)
