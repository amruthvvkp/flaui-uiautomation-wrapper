"""Tests for Combobox automation element, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\ComboBoxTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes, IsFalseLike
from flaui.core.automation_elements import ComboBox
from flaui.core.definitions import ExpandCollapseState
from flaui.core.tools import Retry
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


# GH-75: the ComboBox is broken on WinForms (UIA2 and UIA3) due to upstream Windows/.NET bugs:
# `Items` is empty, `Select` raises IndexOutOfRangeException and Expand/Collapse does not change
# state. Upstream FlaUI disables its WinForms ComboBoxTests fixtures for the same reason, so the
# WinForms combos are skipped (via `skip_winforms`) and the WPF combos run for real.
#
# The WPF drop-down opens/closes with an animation, so the expand/collapse state and the items'
# IsOffscreen flag can lag the call by a few hundred ms; those checks wait briefly before asserting.
# A WPF drop-down also closes as soon as its window loses activation, and the four matrix apps
# overlap on screen, so the fixtures bring this combo's window to the foreground first.
_ANIMATION_WAIT_MS = 2000
@pytest.mark.platform_limitation
class TestComboBoxElements:
    """Tests for the Combobox class."""

    @pytest.fixture
    def skip_winforms(self, test_application_type: str) -> None:
        """Skip WinForms tests."""
        if test_application_type == "WinForms":
            pytest.skip(
                "GH-75: ComboBox is broken on UIA2/UIA3 + WinForms due to Windows/.NET bugs "
                "(upstream FlaUI disables these fixtures too) - "
                "https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/75"
            )

    @pytest.fixture(name="editable_combo_box")
    def get_editable_combobox_control(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, skip_winforms: None
    ) -> Generator[ComboBox, Any, None]:
        """Returns the editable combobox element.

        :param test_application: Test application elements.
        :yield: Editable combobox element.
        """
        test_application.main_window.set_foreground()
        yield test_application.simple_controls_tab.editable_combo_box

    @pytest.fixture(name="non_editable_combo_box")
    def get_non_editable_combobox_control(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, skip_winforms: None
    ) -> Generator[ComboBox, Any, None]:
        """Returns the non editable combobox element.

        :param test_application: Test application elements.
        :yield: Non editable combobox element.
        """
        test_application.main_window.set_foreground()
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
            Retry.WhileFalse(
                lambda c=combobox: c.expand_collapse_state == ExpandCollapseState.Expanded,
                timeout=_ANIMATION_WAIT_MS,
            )
            assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Expanded), (
                "Combobox not expanded."
            )
            combobox.collapse()
            Retry.WhileFalse(
                lambda c=combobox: c.expand_collapse_state == ExpandCollapseState.Collapsed,
                timeout=_ANIMATION_WAIT_MS,
            )
            assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Collapsed), (
                "Combobox not collapsed."
            )

    def test_editable_text(self, editable_combo_box: ComboBox) -> None:
        """Tests setting the editable text selects the matching item.

        :param editable_combo_box: The editable combobox element.
        """
        editable_combo_box.editable_text = "Item 3"
        assert editable_combo_box.selected_item == HasAttributes(text="Item 3")

    @pytest.mark.parametrize("item_index", [0, 1, 2, 3])
    def test_combo_box_item_is_not_offscreen(self, non_editable_combo_box: ComboBox, item_index: int) -> None:
        """Tests the combo box items are not offscreen.

        :param non_editable_combo_box: The non editable combobox element.
        :param item_index: Index of the combobox item to check.
        """
        try:
            item = non_editable_combo_box.items[item_index]
            Retry.WhileFalse(lambda: not item.is_offscreen, timeout=_ANIMATION_WAIT_MS)
            assert item == HasAttributes(is_offscreen=IsFalseLike), (
                "Combobox item is offscreen."
            )
        finally:
            non_editable_combo_box.collapse()
