"""Tests for Combobox automation element."""

from flaui.core.automation_elements import ComboBox
from flaui.core.definitions import ExpandCollapseState
import pytest

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestComboBoxElements:
    """Tests for the Combobox class."""

    @pytest.mark.parametrize("element", ("editable_combo_box", "non_editable_combo_box"))
    def test_selected_item(self, test_elements: WPFApplicationElements, element: str):
        """Tests the selected item property.

        :param wpf_elements: The WPF application element map.
        :param element: Element to test.
        """
        combobox: ComboBox = getattr(test_elements.simple_controls_tab, element)
        combobox.items[1].select()
        selected_item = combobox.selected_item
        assert selected_item is not None
        assert selected_item.text == "Item 2"

    @pytest.mark.parametrize("element", ("editable_combo_box", "non_editable_combo_box"))
    def test_select_by_index(self, test_elements: WPFApplicationElements, element: str):
        """Tests the select by index method.

        :param wpf_elements: The WPF application element map.
        :param element: Element to test.
        """
        combobox: ComboBox = getattr(test_elements.simple_controls_tab, element)
        combobox.select(1)
        selected_item = combobox.selected_item
        assert selected_item is not None
        assert selected_item.text == "Item 2"

    @pytest.mark.parametrize("element", ("editable_combo_box", "non_editable_combo_box"))
    def test_select_by_text(self, test_elements: WPFApplicationElements, element: str):
        """Tests the select by text method.

        :param wpf_elements: The WPF application element map.
        :param element: Element to test.
        """
        combobox: ComboBox = getattr(test_elements.simple_controls_tab, element)
        combobox.select("Item 2")
        selected_item = combobox.selected_item
        assert selected_item is not None
        assert selected_item.text == "Item 2"

    @pytest.mark.parametrize("element", ("editable_combo_box", "non_editable_combo_box"))
    def test_expand_collapse(self, test_elements: WPFApplicationElements, element: str):
        """Tests the expand and collapse methods.

        :param wpf_elements: The WPF application element map.
        :param element: Element to test.
        """
        combobox: ComboBox = getattr(test_elements.simple_controls_tab, element)
        combobox.expand()
        assert combobox.expand_collapse_state == ExpandCollapseState.Expanded
        combobox.collapse()
        assert combobox.expand_collapse_state == ExpandCollapseState.Collapsed

    def test_editable_text(self, test_elements: WPFApplicationElements):
        """Tests the editable text property.

        :param wpf_elements: The WPF application element map.
        """
        combobox: ComboBox = test_elements.simple_controls_tab.editable_combo_box
        assert combobox is not None
        combobox.editable_text = "Item 3"
        assert combobox.selected_item is not None
        assert combobox.selected_item.text == "Item 3"

    def test_combo_box_item_is_not_offscreen(self, test_elements: WPFApplicationElements):
        """Tests the combo box item is not offscreen property.

        :param wpf_elements: The WPF application element map.
        """
        combobox: ComboBox = test_elements.simple_controls_tab.non_editable_combo_box
        assert combobox.is_offscreen is False
