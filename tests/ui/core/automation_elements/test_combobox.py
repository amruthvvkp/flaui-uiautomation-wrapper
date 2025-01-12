"""Tests for Combobox automation element."""

from typing import Dict, Tuple

from flaui.core.application import Application
from flaui.core.automation_elements import ComboBox, Window
from flaui.core.automation_type import AutomationType
from flaui.core.definitions import ExpandCollapseState
from flaui.modules.automation import Automation
from loguru import logger
import pytest
from pytest_check import equal, is_not_none

from tests.test_utilities.config import ApplicationType
from tests.test_utilities.elements.winforms_application.base import get_winforms_application_elements
from tests.test_utilities.elements.wpf_application.base import get_wpf_application_elements


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="session",
)
class TestComboBoxElements:
    """Tests for the Combobox class."""

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

    def test_selected_item(self):
        """Tests the selected item property."""
        for element_type in ["editable_combo_box", "non_editable_combo_box"]:
            combobox: ComboBox = getattr(self.test_elements.simple_controls_tab, element_type)
            combobox.items[1].select()
            selected_item = combobox.selected_item
            is_not_none(selected_item)
            equal(selected_item.text, "Item 2")

    def test_select_by_index(self):
        """Tests the select by index method."""
        for element_type in ["editable_combo_box", "non_editable_combo_box"]:
            combobox: ComboBox = getattr(self.test_elements.simple_controls_tab, element_type)
            combobox.select(1)
            selected_item = combobox.selected_item
            is_not_none(selected_item)
            equal(selected_item.text, "Item 2")

    def test_select_by_text(self):
        """Tests the select by text method."""
        for element_type in ["editable_combo_box", "non_editable_combo_box"]:
            combobox: ComboBox = getattr(self.test_elements.simple_controls_tab, element_type)
            combobox.select("Item 2")
            selected_item = combobox.selected_item
            is_not_none(selected_item)
            equal(selected_item.text, "Item 2")

    def test_expand_collapse(self):
        """Tests the expand and collapse methods."""
        for element_type in ["editable_combo_box", "non_editable_combo_box"]:
            combobox: ComboBox = getattr(self.test_elements.simple_controls_tab, element_type)
            combobox.expand()
            equal(combobox.expand_collapse_state, ExpandCollapseState.Expanded)
            combobox.collapse()
            equal(combobox.expand_collapse_state, ExpandCollapseState.Collapsed)

    def test_editable_text(self):
        """Tests the editable text property.

        :param wpf_elements: The WPF application element map.
        """
        combobox: ComboBox = self.test_elements.simple_controls_tab.editable_combo_box
        assert combobox is not None
        combobox.editable_text = "Item 3"
        assert combobox.selected_item is not None
        assert combobox.selected_item.text == "Item 3"

    def test_combo_box_item_is_not_offscreen(self):
        """Tests the combo box item is not offscreen property.

        :param wpf_elements: The WPF application element map.
        """
        combobox: ComboBox = self.test_elements.simple_controls_tab.non_editable_combo_box
        assert combobox.is_offscreen is False
