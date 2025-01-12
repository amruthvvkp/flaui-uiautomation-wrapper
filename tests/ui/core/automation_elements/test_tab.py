"""Tests for the Tab control."""

from typing import Dict, Tuple

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.core.input import Wait
from flaui.modules.automation import Automation
from loguru import logger
import pytest
from pytest_check import equal

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.winforms_application.constants import (
    ApplicationTabIndex as WinFormsApplicationTabIndex,
)
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements
from tests.test_utilities.elements.wpf_application.constants import ApplicationTabIndex as WpfApplicationTabIndex


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
class TestTab:
    """Tests for Tab control."""

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

    def test_select_tab(self):
        """Tests selection of Tab controls"""
        tab = self.test_elements.tab

        if self._application_type == ApplicationType.Wpf:
            equal(len(tab.tab_items()), 3)
            tab_index = WpfApplicationTabIndex
        else:
            equal(len(tab.tab_items()), 2)
            tab_index = WinFormsApplicationTabIndex
        for index in tab_index:
            if index != tab_index.SIMPLE_CONTROLS:
                tab.select_tab_item(index.value)
                Wait.until_input_is_processed()

            equal(tab.selected_tab_item_index, index.value)

    def test_exception_on_no_input_value_to_select_tab(self):
        """Tests if ValueError is thrown on no index/value sent to select tab"""
        with pytest.raises(ValueError):
            self.test_elements.tab.select_tab_item()
