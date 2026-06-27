"""UI integration test for the Window pattern on the application main window (GH-91).

The main window is shared across the session, so the test reads the Window pattern state read-only
rather than mutating the visual state (which would be flaky and could break sibling tests).
"""

from flaui.core.definitions import WindowVisualState
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestWindowPattern:
    """Tests for the Window pattern on the shared application main window."""

    def test_window_pattern(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Read the Window pattern flags and visual state without mutating the shared window."""
        window_pattern = test_application.main_window.patterns.window.pattern
        assert_that(window_pattern, not_none())
        assert isinstance(window_pattern.can_minimize.value, bool)
        assert isinstance(window_pattern.can_maximize.value, bool)
        assert window_pattern.is_modal.value is False
        assert window_pattern.window_visual_state.value in (
            WindowVisualState.Normal.value,
            WindowVisualState.Maximized.value,
            WindowVisualState.Minimized.value,
        )
