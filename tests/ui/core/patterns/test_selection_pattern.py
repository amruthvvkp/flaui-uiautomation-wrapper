"""UI integration tests for the Selection and SelectionItem patterns on a ListBox (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from flaui.core.definitions import ControlType
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestSelectionPattern:
    """Tests for the Selection and SelectionItem patterns on a ListBox control."""

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

    def test_selection_pattern(self, list_box: AutomationElement) -> None:
        """Read the Selection pattern container flags."""
        assert_that(list_box, not_none())
        selection_pattern = list_box.patterns.selection.pattern
        assert_that(selection_pattern, not_none())
        assert isinstance(selection_pattern.can_select_multiple.value, bool)
        assert isinstance(selection_pattern.is_selection_required.value, bool)

    def test_selection_item_pattern(
        self,
        list_box: AutomationElement,
        condition_factory: Any,
    ) -> None:
        """Select the first list item via the SelectionItem pattern and verify it is selected."""
        items = list_box.find_all_descendants(condition=condition_factory.by_control_type(ControlType.ListItem))
        assert len(items) > 0, "ListBox should expose at least one item"
        selection_item_pattern = items[0].patterns.selection_item.pattern
        assert_that(selection_item_pattern, not_none())
        selection_item_pattern.select()
        assert selection_item_pattern.is_selected.value is True
