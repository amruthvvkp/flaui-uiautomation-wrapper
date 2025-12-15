"""Tests for Combobox automation element, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\ComboBoxTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, IsFalseLike
from flaui.core.automation_elements import ComboBox
from flaui.core.definitions import ExpandCollapseState
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.bug(
    id="GH-75",
    url="https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/75",
    reason="Combobox heavily broken on WinForms due to Windows/.NET bugs",
)
@pytest.mark.xfail(reason="Combobox heavily broken on WinForms due to Windows/.NET bugs")
class TestComboBoxElements:
    """Tests for the Combobox class."""

    @pytest.fixture
    def skip_winforms(self, test_application_type: str) -> None:
        """Skip WinForms tests."""
        if test_application_type == "WinForms":
            pytest.skip("Combobox got heavily broken with UIA2/UIA3 Winforms due to bugs in Windows/.Net")

    @pytest.fixture(name="editable_combo_box")
    def get_editable_combobox_control(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, skip_winforms: None
    ) -> Generator[ComboBox, Any, None]:
        """Returns the editable combobox element.

        :param test_application: Test application elements.
        :yield: Editable combobox element.
        """
        yield test_application.simple_controls_tab.editable_combo_box

    @pytest.fixture(name="non_editable_combo_box")
    def get_non_editable_combobox_control(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, skip_winforms: None
    ) -> Generator[ComboBox, Any, None]:
        """Returns the non editable combobox element.

        :param test_application: Test application elements.
        :yield: Non editable combobox element.
        """
        yield test_application.simple_controls_tab.non_editable_combo_box

    def test_selected_item(self, editable_combo_box: ComboBox, non_editable_combo_box: ComboBox) -> None:
        """Tests the selected item property."""
        for combobox in [editable_combo_box, non_editable_combo_box]:
            combobox.items[1].select()
            assert combobox.selected_item == HasAttributes(text="Item 2"), "Selected item text is not correct."

    def test_select_by_index(self, editable_combo_box: ComboBox, non_editable_combo_box: ComboBox) -> None:
        """Tests the select by index method."""
        for combobox in [editable_combo_box, non_editable_combo_box]:
            combobox.select(1)
            assert combobox.selected_item == HasAttributes(text="Item 2"), "Selected item text is not correct."

    def test_select_by_text(self, editable_combo_box: ComboBox, non_editable_combo_box: ComboBox) -> None:
        """Tests the select by text method."""
        for combobox in [editable_combo_box, non_editable_combo_box]:
            combobox.select("Item 2")
            assert combobox.selected_item == HasAttributes(text="Item 2"), "Selected item text is not correct."

    def test_expand_collapse(self, editable_combo_box: ComboBox, non_editable_combo_box: ComboBox) -> None:
        """Tests the expand and collapse methods."""
        for combobox in [editable_combo_box, non_editable_combo_box]:
            combobox.expand()
            assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Expanded), (
                "Combobox not expanded."
            )
            combobox.collapse()
            assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Collapsed), (
                "Combobox not collapsed."
            )

    def test_editable_text(self, editable_combo_box: ComboBox) -> None:
        """Tests the editable text property.

        :param wpf_elements: The WPF application element map.
        """
        assert editable_combo_box == HasAttributes(editable_text="Item 3")
        assert editable_combo_box.selected_item == HasAttributes(text="Item 3")

    def test_combo_box_item_is_not_offscreen(self, non_editable_combo_box: ComboBox) -> None:
        """Tests the combo box item is not offscreen property.

        :param wpf_elements: The WPF application element map.
        """
        assert non_editable_combo_box == HasAttributes(is_offscreen=IsFalseLike), "Combobox item is offscreen."
