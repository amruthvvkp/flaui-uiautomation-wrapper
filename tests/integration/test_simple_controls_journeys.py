"""Journeys across the Simple Controls page: filling the form, touring the tabs, keyboard-only use."""

from dirty_equals import IsApprox
from flaui.core.automation_elements import Slider
from flaui.core.definitions import ExpandCollapseState, ToggleState
from flaui.core.expectations import expect
from flaui.core.input import Keyboard, Wait
from flaui.core.tools import Retry
from flaui.core.windows_api import VirtualKeyShort
import pytest

from tests.integration.conftest import JourneyApp

pytestmark = pytest.mark.integration

#: Tab captions in display order. The WinForms app has no "More Controls" tab.
EXPECTED_TABS = {
    "WinForms": ["Simple Controls", "Complex Controls"],
    "WPF": ["Simple Controls", "Complex Controls", "More Controls"],
}


def _slider_units(slider: Slider, value: float) -> float:
    """Convert a 0-10 slider position into the units the provider reports.

    The slider's range is 0-10, but UIA3 on WinForms only exposes the Value pattern, scaled 0-100.

    :param slider: The slider control.
    :param value: Position on the 0-10 scale.
    :return: ``value`` in the provider's units.
    """
    return float(value * 10) if slider.is_only_value else float(value)


class TestSimpleControlsJourneys:
    """End-to-end journeys over the Simple Controls page."""

    def test_fill_form_and_read_back_after_tab_round_trip(self, journey_app: JourneyApp) -> None:
        """Fill every input, leave the page through another tab, come back and read each value."""
        page = journey_app.elements.simple_controls_tab

        page.test_text_box.enter("Integration journey", post_wait=True)
        page.test_check_box.toggle_state = ToggleState.On
        page.three_way_check_box.toggle_state = ToggleState.Indeterminate
        page.radio_button_2.is_checked = True
        page.radio_button_1.is_checked = True  # Selecting RadioButton1 must clear RadioButton2.
        slider = page.slider
        slider.value = _slider_units(slider, 7)

        # Leave the page; its controls are re-found from scratch when we come back.
        journey_app.elements.tab.select_tab_item(1, post_wait=True)
        assert journey_app.elements.complex_controls_tab.tree_elements.items, "Complex Controls did not load"
        journey_app.elements.tab.select_tab_item(0, post_wait=True)

        page = journey_app.refresh().simple_controls_tab
        assert page.test_text_box.text == "Integration journey"
        assert page.test_check_box.toggle_state == ToggleState.On
        assert page.three_way_check_box.toggle_state == ToggleState.Indeterminate
        assert page.radio_button_1.is_checked is True
        assert page.radio_button_2.is_checked is False
        assert page.slider.value == IsApprox(_slider_units(page.slider, 7), delta=0.1)

    def test_tour_every_tab_and_refind_elements(self, journey_app: JourneyApp) -> None:
        """Visit every tab, check each page loads, and confirm elements are re-found rather than stale."""
        tab = journey_app.elements.tab
        assert [item.name for item in tab.tab_items] == EXPECTED_TABS[journey_app.app_type]

        text_box_before = journey_app.elements.simple_controls_tab.test_text_box
        for index, caption in enumerate(EXPECTED_TABS[journey_app.app_type]):
            tab.select_tab_item(index, post_wait=True)
            assert tab.selected_tab_item_index == index
            assert tab.selected_tab_item.name == caption

            if caption == "Complex Controls":
                assert len(journey_app.elements.complex_controls_tab.tree_elements.items) == 2
            elif caption == "More Controls":
                assert len(journey_app.elements.more_controls_tab.large_list_box.items) > 0

        tab.select_tab_item(0, post_wait=True)
        text_box_after = journey_app.refresh().simple_controls_tab.test_text_box
        # The fresh lookup resolves to the same UI element, and the old reference still works.
        assert journey_app.automation.automation_base.compare(text_box_before, text_box_after)
        text_box_after.text = "Still the same control"
        assert text_box_before.text == "Still the same control"

    # GH-75: ComboBox is broken on WinForms with both UIA2 and UIA3 (upstream Windows/.NET issue),
    # so this journey runs on the two WPF combinations only.
    @pytest.mark.platform_limitation
    def test_pick_combo_box_items(self, journey_app: JourneyApp, skip_on_winforms: None) -> None:
        """Open the editable combo box, pick items by index and by text, then type a custom value."""
        combo = journey_app.elements.simple_controls_tab.editable_combo_box

        combo.expand()
        expect(combo).to_be_visible()
        assert Retry.WhileFalse(lambda: combo.expand_collapse_state == ExpandCollapseState.Expanded, timeout=2000)
        assert [item.text for item in combo.items] == ["Item 1", "Item 2", "Item 3"]

        assert combo.select(1).text == "Item 2"
        assert combo.selected_item.text == "Item 2"
        assert combo.select("Item 3").text == "Item 3"
        combo.collapse()
        assert Retry.WhileFalse(lambda: combo.expand_collapse_state == ExpandCollapseState.Collapsed, timeout=2000)
        assert combo.value == "Item 3"

        combo.editable_text = "Custom entry"
        assert combo.editable_text == "Custom entry"

    def test_keyboard_only_navigation(self, journey_app: JourneyApp) -> None:
        """Type, move focus, toggle a check box and switch tabs using only the keyboard."""
        page = journey_app.elements.simple_controls_tab
        automation = journey_app.automation.automation_base

        text_box = page.test_text_box
        text_box.focus()
        with Keyboard.pressing([VirtualKeyShort.CONTROL]):
            Keyboard.type_key(VirtualKeyShort.KEY_A)
        Keyboard.type("Typed by keyboard")
        Wait.until_input_is_processed()
        expect(text_box).to_have_text("Typed by keyboard")

        # Tab moves focus off the text box.
        Keyboard.type_key(VirtualKeyShort.TAB)
        Wait.until_input_is_processed()
        assert Retry.WhileFalse(lambda: not automation.compare(automation.focused_element(), text_box), timeout=2000)

        # Space toggles the focused check box.
        check_box = page.test_check_box
        check_box.focus()
        Keyboard.type_key(VirtualKeyShort.SPACE)
        assert Retry.WhileFalse(lambda: check_box.toggle_state == ToggleState.On, timeout=2000)
        Keyboard.type_key(VirtualKeyShort.SPACE)
        assert Retry.WhileFalse(lambda: check_box.toggle_state == ToggleState.Off, timeout=2000)

        # Ctrl+Tab / Ctrl+Shift+Tab cycle the tab control.
        tab = journey_app.elements.tab
        with Keyboard.pressing([VirtualKeyShort.CONTROL]):
            Keyboard.type_key(VirtualKeyShort.TAB)
        assert Retry.WhileFalse(lambda: tab.selected_tab_item_index == 1, timeout=2000)
        with Keyboard.pressing([VirtualKeyShort.CONTROL, VirtualKeyShort.SHIFT]):
            Keyboard.type_key(VirtualKeyShort.TAB)
        assert Retry.WhileFalse(lambda: tab.selected_tab_item_index == 0, timeout=2000)
