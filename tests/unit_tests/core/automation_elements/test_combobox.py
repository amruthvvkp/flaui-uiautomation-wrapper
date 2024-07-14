"""Tests for Combobox automation element."""
from typing import Any, Generator

from flaui.core.automation_elements import ComboBox, Window
from flaui.core.definitions import ExpandCollapseState
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements
from tests.config import test_settings

@pytest.fixture(scope="class")
def wpf_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    wpf_application = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    wpf_application.application.launch(
        test_settings.WPF_TEST_APP_EXE.as_posix()
        if ui_automation_type == UIAutomationTypes.UIA3
        else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    )
    yield wpf_application

    wpf_application.application.kill()


@pytest.fixture(scope="class")
def main_window(wpf_application: Automation, automation: Any) -> Generator[Window, None, None]:
    """Fetches the main window of the test application.

    :param wpf_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield wpf_application.application.get_main_window(automation)


@pytest.fixture(scope="class")
def wpf_elements(main_window: Window) -> Generator[Any, None, None]:
    """Generates the WPF application element map.

    :param main_window: The main window of the test application.
    :yield: WPF application element map.
    """
    yield WPFApplicationElements(main_window=main_window)


class TestComboBoxElements:
    """Tests for the Combobox class."""

    @pytest.mark.parametrize("element", ("editable_combo_box", "non_editable_combo_box"))
    def test_selected_item(self, wpf_elements: WPFApplicationElements, element: str):
        """Tests the selected item property.

        :param wpf_elements: The WPF application element map.
        :param element: Element to test.
        """
        combobox: ComboBox = getattr(wpf_elements.simple_controls_tab, element)
        combobox.items[1].select()
        selected_item = combobox.selected_item
        assert selected_item is not None
        assert selected_item.text == "Item 2"

    @pytest.mark.parametrize("element", ("editable_combo_box", "non_editable_combo_box"))
    def test_select_by_index(self, wpf_elements: WPFApplicationElements, element: str):
        """Tests the select by index method.

        :param wpf_elements: The WPF application element map.
        :param element: Element to test.
        """
        combobox: ComboBox = getattr(wpf_elements.simple_controls_tab, element)
        combobox.select(1)
        selected_item = combobox.selected_item
        assert selected_item is not None
        assert selected_item.text == "Item 2"

    @pytest.mark.parametrize("element", ("editable_combo_box", "non_editable_combo_box"))
    def test_select_by_text(self, wpf_elements: WPFApplicationElements, element: str):
        """Tests the select by text method.

        :param wpf_elements: The WPF application element map.
        :param element: Element to test.
        """
        combobox: ComboBox = getattr(wpf_elements.simple_controls_tab, element)
        combobox.select("Item 2")
        selected_item = combobox.selected_item
        assert selected_item is not None
        assert selected_item.text == "Item 2"

    @pytest.mark.parametrize("element", ("editable_combo_box", "non_editable_combo_box"))
    def test_expand_collapse(self, wpf_elements: WPFApplicationElements, element: str):
        """Tests the expand and collapse methods.

        :param wpf_elements: The WPF application element map.
        :param element: Element to test.
        """
        combobox: ComboBox = getattr(wpf_elements.simple_controls_tab, element)
        combobox.expand()
        assert combobox.expand_collapse_state == ExpandCollapseState.Expanded
        combobox.collapse()
        assert combobox.expand_collapse_state == ExpandCollapseState.Collapsed

    def test_editable_text(self, wpf_elements: WPFApplicationElements):
        """Tests the editable text property.

        :param wpf_elements: The WPF application element map.
        """
        combobox: ComboBox = wpf_elements.simple_controls_tab.editable_combo_box
        assert combobox is not None
        combobox.editable_text = "Item 3"
        assert combobox.selected_item is not None
        assert combobox.selected_item.text == "Item 3"

    def test_combo_box_item_is_not_offscreen(self, wpf_elements: WPFApplicationElements):
        """Tests the combo box item is not offscreen property.

        :param wpf_elements: The WPF application element map.
        """
        combobox: ComboBox = wpf_elements.simple_controls_tab.non_editable_combo_box
        assert combobox.is_offscreen is False
