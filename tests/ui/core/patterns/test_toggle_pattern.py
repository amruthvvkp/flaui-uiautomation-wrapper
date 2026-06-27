"""UI integration test for the Toggle pattern on a CheckBox control (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestTogglePattern:
    """Tests for the Toggle pattern on a CheckBox control."""

    @pytest.fixture(name="check_box")
    def get_check_box(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the two-state CheckBox element.

        :param test_application: Test application elements.
        :yield: CheckBox automation element.
        """
        yield test_application.simple_controls_tab.test_check_box

    def test_toggle_pattern(self, check_box: AutomationElement) -> None:
        """Toggle the checkbox, verify the state flips, then restore the original state."""
        assert_that(check_box, not_none())
        toggle_pattern = check_box.patterns.toggle.pattern
        assert_that(toggle_pattern, not_none())
        original = toggle_pattern.toggle_state.value
        try:
            toggle_pattern.toggle()
            assert toggle_pattern.toggle_state.value != original
        finally:
            # The test application is shared, so leave the checkbox as we found it.
            if toggle_pattern.toggle_state.value != original:
                toggle_pattern.toggle()
            assert toggle_pattern.toggle_state.value == original
