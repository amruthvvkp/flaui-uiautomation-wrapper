"""Tests for the ListBox control."""


from typing import Any, Generator

from flaui.core.automation_elements import ListBoxItem, Window
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


class TestListBox:
    """Tests for the ListBox control."""

    def test_items(self, wpf_elements: WPFApplicationElements):
        """Tests the items property.

        :param wpf_elements: WPF application element map.
        """
        element = wpf_elements.simple_controls_tab.list_box
        assert element is not None
        assert len(element.items) == 2

    def test_select_by_index(self, wpf_elements: WPFApplicationElements):
        """Tests the select_by_index method.

        :param wpf_elements: WPF application element map.
        """
        element = wpf_elements.simple_controls_tab.list_box
        assert all([isinstance(_, ListBoxItem) for _ in element.items])
        with pytest.raises(ValueError):
            assert element.selected_item is None
        for index in range(2):
            item = element.select(index)
            assert item.text == f"ListBox Item #{index + 1}"
            assert element.selected_item.text == f"ListBox Item #{index + 1}"

    def test_select_by_text(self, wpf_elements: WPFApplicationElements):
        """Tests the select_by_text method.

        :param wpf_elements: WPF application element map.
        """
        element = wpf_elements.simple_controls_tab.list_box
        assert all([isinstance(_, ListBoxItem) for _ in element.items])
        for index in range(2):
            item = element.select(f"ListBox Item #{index + 1}")
            assert item.text == f"ListBox Item #{index + 1}"
            assert element.selected_item.text == f"ListBox Item #{index + 1}"

    def test_items_property_in_large_list(self, wpf_elements: WPFApplicationElements):
        """Tests the items property with a large list.

        :param wpf_elements: WPF application element map.
        """
        element = wpf_elements.more_controls_tab.large_list_box
        assert len(element.items) == 7
        assert element.items[6].text == "ListBox Item #7"

    def test_select_by_index_in_large_list(self, wpf_elements: WPFApplicationElements):
        """Tests the select_by_index method with a large list.

        :param wpf_elements: WPF application element map.
        """
        element = wpf_elements.more_controls_tab.large_list_box
        item = element.select(6)
        assert item.text == "ListBox Item #7"
        assert len(element.selected_items) == 1
        assert element.selected_item.text == "ListBox Item #7"

        item = element.add_to_selection(5)
        assert item.text == "ListBox Item #6"
        assert len(element.selected_items) == 2
        assert element.selected_items[0].text == "ListBox Item #7"
        assert element.selected_items[1].text == "ListBox Item #6"
