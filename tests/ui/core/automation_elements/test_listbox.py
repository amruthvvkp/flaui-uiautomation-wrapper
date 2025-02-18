"""Tests for the ListBox control."""

from dirty_equals import HasAttributes, HasLen, IsList
from flaui.core.automation_elements import ListBoxItem
from flaui.lib.exceptions import ElementNotFound
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestListBox:
    """Tests for the ListBox control."""

    def test_items(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the items property."""
        element = test_application.simple_controls_tab.list_box
        assert element == HasAttributes(items=HasLen(2)), "List box should have 2 items."

    def test_select_by_index(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the select_by_index method."""
        element = test_application.simple_controls_tab.list_box
        assert element.items == HasLen(2), "List box should have 2 items."
        assert all([isinstance(_, ListBoxItem) for _ in element.items]), "All items should be ListBoxItem instances."
        assert element.selected_items == IsList(length=0), "No item should be selected."
        with pytest.raises(
            ElementNotFound
        ):  # This is needed since Python layer explicitly validates if element is found or not
            assert element.selected_item
        for index in range(2):
            item = element.select(index)
            assert item == HasAttributes(text=f"ListBox Item #{index + 1}")
            assert element.selected_item == HasAttributes(text=f"ListBox Item #{index + 1}")

    def test_select_by_text(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the select_by_text method."""
        element = test_application.simple_controls_tab.list_box
        for index in range(2):
            item = element.select(f"ListBox Item #{index + 1}")
            assert item == HasAttributes(text=f"ListBox Item #{index + 1}")
            assert element.selected_item == HasAttributes(text=f"ListBox Item #{index + 1}")

    @pytest.mark.xfail(
        condition=lambda request: request.getfixturevalue("test_application_type") == "WinForms",  # type: ignore
        reason="Combobox got heavily broken with UIA2/UIA3 Winforms due to bugs in Windows/.Net",
    )
    def test_items_property_in_large_list(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Tests the items property with a large list."""
        assert test_application.more_controls_tab.large_list_box.items == IsList(
            positions={6: HasAttributes(text="ListBox Item #7")}, length=7
        ), "List box should have 7 items."

    @pytest.mark.xfail(
        condition=lambda request: request.getfixturevalue("test_application_type") == "WinForms",  # type: ignore
        reason="Combobox got heavily broken with UIA2/UIA3 Winforms due to bugs in Windows/.Net",
    )
    def test_select_by_text_in_large_list(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Tests the select_by_index method with a large list."""
        element = test_application.more_controls_tab.large_list_box
        item = element.select("ListBox Item #7")
        assert item == HasAttributes(text="ListBox Item #7"), "Selected item text is not correct."
        assert element.selected_items == IsList(positions={0: HasAttributes(text="ListBox Item #7")}, length=1), (
            "Selected item text is not correct."
        )

        item = element.add_to_selection("ListBox Item #6")
        assert item == HasAttributes(text="ListBox Item #6"), "Selected item text is not correct."
        assert element.selected_items == IsList(
            positions={0: HasAttributes(text="ListBox Item #7"), 1: HasAttributes(text="ListBox Item #6")}, length=2
        ), "Selected items are not correct."

    @pytest.mark.xfail(
        condition=lambda request: request.getfixturevalue("test_application_type") == "WinForms",  # type: ignore
        reason="Combobox got heavily broken with UIA2/UIA3 Winforms due to bugs in Windows/.Net",
    )
    def test_select_by_index_in_large_list(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Tests the select_by_index method with a large list."""
        element = test_application.more_controls_tab.large_list_box
        item = element.select(6)
        assert item == HasAttributes(text="ListBox Item #7"), "Selected item text is not correct."
        assert element.selected_items == IsList(positions={0: HasAttributes(text="ListBox Item #7")}, length=1), (
            "Selected item text is not correct."
        )

        item = element.add_to_selection(5)
        assert item == HasAttributes(text="ListBox Item #6"), "Selected item text is not correct."
        assert element.selected_items == IsList(
            positions={0: HasAttributes(text="ListBox Item #7"), 1: HasAttributes(text="ListBox Item #6")}, length=2
        ), "Selected items are not correct."
