"""Tests for the Checkbox class."""

from typing import Any, Generator

from dirty_equals import HasAttributes
from flaui.core.automation_elements import CheckBox
from flaui.core.definitions import ToggleState
import pytest

from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements
from tests.ui.conftest import WinFormsApplicationElements


class TestCheckBoxElements:
    """Tests for the Checkbox class."""

    @pytest.fixture(name="test_check_box")
    def get_test_checkbox_control(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[CheckBox, Any, None]:
        """Returns the test checkbox element.

        :param test_application: Test application elements.
        :yield: Test checkbox element.
        """
        yield test_application.simple_controls_tab.test_check_box

    @pytest.fixture(name="three_way_check_box")
    def get_three_state_checkbox(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[CheckBox, Any, None]:
        """Returns the three way checkbox element.

        :param test_application: Test application elements.
        :yield: Three way checkbox element.
        """
        yield test_application.simple_controls_tab.three_way_check_box

    def test_toggle_element(
        self,
        test_check_box: CheckBox,
    ) -> None:
        """Tests the toggle method of the Checkbox class."""
        assert test_check_box == HasAttributes(toggle_state=ToggleState.Off), "Checkbox should be off"
        test_check_box.toggle()
        assert test_check_box == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"

    def test_set_state(
        self,
        test_check_box: CheckBox,
    ) -> None:
        """Tests the set_state method of the Checkbox class."""
        test_check_box.toggle_state = ToggleState.On
        assert test_check_box == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"
        test_check_box.toggle_state = ToggleState.Off
        assert test_check_box == HasAttributes(toggle_state=ToggleState.Off), "Checkbox should be off"
        test_check_box.toggle_state = ToggleState.On
        assert test_check_box == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"

    def test_three_way_toggle(self, three_way_check_box: CheckBox) -> None:
        """Tests the three_way_toggle method of the Checkbox class."""
        assert three_way_check_box == HasAttributes(toggle_state=ToggleState.Off), "Checkbox should be off"
        three_way_check_box.toggle()
        assert three_way_check_box == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"
        three_way_check_box.toggle()
        assert three_way_check_box == HasAttributes(toggle_state=ToggleState.Indeterminate), (
            "Checkbox should be indeterminate"
        )

    def test_three_way_set_state(self, three_way_check_box: CheckBox) -> None:
        """Tests the three_way_set_state method of the Checkbox class."""
        three_way_check_box.toggle_state = ToggleState.On
        assert three_way_check_box == HasAttributes(toggle_state=ToggleState.On), "Checkbox should be on"
        three_way_check_box.toggle_state = ToggleState.Off
        assert three_way_check_box == HasAttributes(toggle_state=ToggleState.Off), "Checkbox should be off"
        three_way_check_box.toggle_state = ToggleState.Indeterminate
        assert three_way_check_box == HasAttributes(toggle_state=ToggleState.Indeterminate), (
            "Checkbox should be indeterminate"
        )
