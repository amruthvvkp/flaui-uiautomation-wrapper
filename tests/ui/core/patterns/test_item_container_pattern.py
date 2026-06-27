"""UI integration test for the ItemContainer pattern on a ListBox control (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestItemContainerPattern:
    """Tests for the ItemContainer pattern on a ListBox control."""

    @pytest.fixture(name="list_box")
    def get_list_box(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the ListBox element.

        :param test_application: Test application elements.
        :yield: ListBox automation element.
        """
        yield test_application.simple_controls_tab.list_box

    def test_item_container_pattern(self, list_box: AutomationElement, is_pattern_supported: object) -> None:
        """Find the first contained item through the ItemContainer pattern when supported."""
        assert_that(list_box, not_none())
        if not is_pattern_supported(list_box.patterns, "item_container"):  # type: ignore[operator]
            pytest.skip("ItemContainer pattern is not supported on this control/runtime")
        # ``find_item_by_property(None, None, None)`` returns the first contained item.
        first_item = list_box.patterns.item_container.pattern.find_item_by_property(None, None, None)
        assert_that(first_item, not_none())
