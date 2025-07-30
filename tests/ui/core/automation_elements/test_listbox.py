"""Tests for the ListBox control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\ListBoxTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, HasLen, IsList
from flaui.core.automation_elements import ListBox, ListBoxItem
from flaui.lib.exceptions import ElementNotFound
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestListBox:
    """Tests for the ListBox control."""

    @pytest.fixture(name="list_box")
    def get_list_box(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[ListBox, Any, None]:
        """Returns the list box element.

        :param test_application: Test application elements.
        :return: Test list box element.
        """
        yield test_application.simple_controls_tab.list_box

    @pytest.fixture(name="large_list_box")
    def get_large_list_box(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, test_application_type: str
    ) -> Generator[ListBox, Any, None]:
        """Returns the list box element with a large list.

        :param test_application: Test application elements.
        :return: Test list box element with a large list.
        """
        if test_application_type == "WinForms":
            pytest.skip("Combobox got heavily broken with UIA2/UIA3 Winforms due to bugs in Windows/.Net")
        yield test_application.more_controls_tab.large_list_box

    def test_items(self, list_box: ListBox) -> None:
        """Tests the items property."""
        assert list_box == HasAttributes(items=HasLen(2)), "List box should have 2 items."

    def test_select_by_index(self, list_box: ListBox) -> None:
        """Tests the select_by_index method."""
        assert list_box.items == HasLen(2), "List box should have 2 items."
        assert all([isinstance(_, ListBoxItem) for _ in list_box.items]), "All items should be ListBoxItem instances."
        assert list_box.selected_items == IsList(length=0), "No item should be selected."
        with pytest.raises(
            ElementNotFound
        ):  # This is needed since Python layer explicitly validates if element is found or not
            assert list_box.selected_item
        for index in range(2):
            item = list_box.select(index)
            assert item == HasAttributes(text=f"ListBox Item #{index + 1}")
            assert list_box.selected_item == HasAttributes(text=f"ListBox Item #{index + 1}")

    def test_select_by_text(self, list_box: ListBox) -> None:
        """Tests the select_by_text method."""
        for index in range(2):
            item = list_box.select(f"ListBox Item #{index + 1}")
            assert item == HasAttributes(text=f"ListBox Item #{index + 1}")
            assert list_box.selected_item == HasAttributes(text=f"ListBox Item #{index + 1}")

    def test_items_property_in_large_list(self, large_list_box: ListBox) -> None:
        """Tests the items property with a large list."""
        assert large_list_box.items == IsList(positions={6: HasAttributes(text="ListBox Item #7")}, length=7), (
            "List box should have 7 items."
        )

    def test_select_by_text_in_large_list(self, large_list_box: ListBox) -> None:
        """Tests the select_by_index method with a large list."""
        item = large_list_box.select("ListBox Item #7")
        assert item == HasAttributes(text="ListBox Item #7"), "Selected item text is not correct."
        assert large_list_box.selected_items == IsList(
            positions={0: HasAttributes(text="ListBox Item #7")}, length=1
        ), "Selected item text is not correct."

        item = large_list_box.add_to_selection("ListBox Item #6")
        assert item == HasAttributes(text="ListBox Item #6"), "Selected item text is not correct."
        assert large_list_box.selected_items == IsList(
            positions={0: HasAttributes(text="ListBox Item #7"), 1: HasAttributes(text="ListBox Item #6")}, length=2
        ), "Selected items are not correct."

    def test_select_by_index_in_large_list(self, large_list_box: ListBox) -> None:
        """Tests the select_by_index method with a large list."""
        item = large_list_box.select(6)
        assert item == HasAttributes(text="ListBox Item #7"), "Selected item text is not correct."
        assert large_list_box.selected_items == IsList(
            positions={0: HasAttributes(text="ListBox Item #7")}, length=1
        ), "Selected item text is not correct."

        item = large_list_box.add_to_selection(5)
        assert item == HasAttributes(text="ListBox Item #6"), "Selected item text is not correct."
        assert large_list_box.selected_items == IsList(
            positions={0: HasAttributes(text="ListBox Item #7"), 1: HasAttributes(text="ListBox Item #6")}, length=2
        ), "Selected items are not correct."
