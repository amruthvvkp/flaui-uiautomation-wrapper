"""Tests for the Tree control."""

from typing import Dict, Tuple

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.modules.automation import Automation
from loguru import logger
import pytest
from pytest_check import equal, is_none, is_not_none

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
class TestTree:
    """Tests for Tree control."""

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

    def test_selection(self):
        """Tests Selection of Tree controls"""
        tree = self.test_elements.complex_controls_tab.tree_elements
        with pytest.raises(ValueError):
            is_none(tree.selected_tree_item)
        equal(len(tree.items), 2)
        tree.items[0].expand()
        tree.items[0].items[1].expand()
        tree.items[0].items[1].items[0].select()
        is_not_none(tree.selected_tree_item)
        equal(tree.selected_tree_item.text, "Lvl3 a")
