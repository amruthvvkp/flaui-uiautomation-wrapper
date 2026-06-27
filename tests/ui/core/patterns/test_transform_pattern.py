"""UI integration test for the Transform pattern (GH-91).

The pattern is exercised read-only: the main window is shared across the session, so the test does
not actually move or resize it (that would break sibling tests). It validates that the transform
flags are readable when the pattern is supported.
"""

from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestTransformPattern:
    """Tests for the Transform pattern flags on the application main window."""

    def test_transform_pattern(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        is_pattern_supported: object,
    ) -> None:
        """Read the Transform pattern capability flags without mutating the shared window."""
        main_window = test_application.main_window
        if not is_pattern_supported(main_window.patterns, "transform"):  # type: ignore[operator]
            pytest.skip("Transform pattern is not supported on the main window for this runtime")
        transform_pattern = main_window.patterns.transform.pattern
        assert_that(transform_pattern, not_none())
        assert isinstance(transform_pattern.can_move.value, bool)
        assert isinstance(transform_pattern.can_resize.value, bool)
        assert isinstance(transform_pattern.can_rotate.value, bool)
