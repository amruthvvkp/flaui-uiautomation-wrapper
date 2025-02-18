"""Tests for Combobox automation element."""

from dirty_equals import HasAttributes, IsFalseLike
from flaui.core.automation_elements import ComboBox
from flaui.core.definitions import ExpandCollapseState
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


@pytest.mark.xfail(
    condition=lambda request: request.getfixturevalue("test_application_type") == "WinForms",  # type: ignore
    reason="Combobox got heavily broken with UIA2/UIA3 Winforms due to bugs in Windows/.Net",
)
class TestComboBoxElements:
    """Tests for the Combobox class."""

    def test_selected_item(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the selected item property."""
        for element_type in ["editable_combo_box", "non_editable_combo_box"]:
            combobox: ComboBox = getattr(test_application.simple_controls_tab, element_type)
            combobox.items[1].select()
            assert combobox.selected_item == HasAttributes(text="Item 2"), "Selected item text is not correct."

    def test_select_by_index(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the select by index method."""
        for element_type in ["editable_combo_box", "non_editable_combo_box"]:
            combobox: ComboBox = getattr(test_application.simple_controls_tab, element_type)
            combobox.select(1)
            assert combobox.selected_item == HasAttributes(text="Item 2"), "Selected item text is not correct."

    def test_select_by_text(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the select by text method."""
        for element_type in ["editable_combo_box", "non_editable_combo_box"]:
            combobox: ComboBox = getattr(test_application.simple_controls_tab, element_type)
            combobox.select("Item 2")
            assert combobox.selected_item == HasAttributes(text="Item 2"), "Selected item text is not correct."

    def test_expand_collapse(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the expand and collapse methods."""
        for element_type in ["editable_combo_box", "non_editable_combo_box"]:
            combobox: ComboBox = getattr(test_application.simple_controls_tab, element_type)
            combobox.expand()
            assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Expanded), (
                "Combobox not expanded."
            )
            combobox.collapse()
            assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Collapsed), (
                "Combobox not collapsed."
            )

    def test_editable_text(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the editable text property.

        :param wpf_elements: The WPF application element map.
        """
        combobox: ComboBox = test_application.simple_controls_tab.editable_combo_box
        assert combobox == HasAttributes(editable_text="Item 3")
        assert combobox.selected_item == HasAttributes(text="Item 3")

    def test_combo_box_item_is_not_offscreen(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Tests the combo box item is not offscreen property.

        :param wpf_elements: The WPF application element map.
        """
        combobox: ComboBox = test_application.simple_controls_tab.non_editable_combo_box
        assert combobox == HasAttributes(is_offscreen=IsFalseLike), "Combobox item is offscreen."
