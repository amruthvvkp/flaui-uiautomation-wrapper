"""Tests for Combobox automation element."""

from flaui.core.automation_elements import ComboBox
from flaui.core.automation_type import AutomationType
from flaui.core.definitions import ExpandCollapseState
import pytest
from pytest_check import equal, is_not_none

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestComboBoxElements(UITestBase):
    """Tests for the Combobox class."""

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
