"""Tests for the Checkbox class."""

from dirty_equals import HasAttributes
from flaui.core.definitions import ToggleState

from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements
from tests.ui.conftest import WinFormsApplicationElements


class TestCheckBoxElements:
    """Tests for the Checkbox class."""

    def test_toggle_element(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Tests the toggle method of the Checkbox class."""
        checkbox = test_application.simple_controls_tab.test_check_box
        assert checkbox == HasAttributes(toggle_state=ToggleState.Off), "Checkbox should be off"
        checkbox.toggle()
        assert checkbox == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"

    def test_set_state(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Tests the set_state method of the Checkbox class."""
        checkbox = test_application.simple_controls_tab.test_check_box
        checkbox.toggle_state = ToggleState.On
        assert checkbox == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"
        checkbox.toggle_state = ToggleState.Off
        assert checkbox == HasAttributes(toggle_state=ToggleState.Off), "Checkbox should be off"
        checkbox.toggle_state = ToggleState.On
        assert checkbox == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"

    def test_three_way_toggle(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Tests the three_way_toggle method of the Checkbox class."""
        checkbox = test_application.simple_controls_tab.three_way_check_box
        assert checkbox == HasAttributes(toggle_state=ToggleState.Off), "Checkbox should be off"
        checkbox.toggle()
        assert checkbox == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"
        checkbox.toggle()
        assert checkbox == HasAttributes(toggle_state=ToggleState.Indeterminate), "Checkbox should be indeterminate"

    def test_three_way_set_state(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Tests the three_way_set_state method of the Checkbox class."""
        checkbox = test_application.simple_controls_tab.three_way_check_box
        checkbox.toggle_state = ToggleState.On
        assert checkbox == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"
        checkbox.toggle_state = ToggleState.Off
        assert checkbox == HasAttributes(toggle_state=ToggleState.Off), "Checkbox should be off"
        checkbox.toggle_state = ToggleState.Indeterminate
        assert checkbox == HasAttributes(toggle_state=ToggleState.Indeterminate), "Checkbox should be indeterminate"
