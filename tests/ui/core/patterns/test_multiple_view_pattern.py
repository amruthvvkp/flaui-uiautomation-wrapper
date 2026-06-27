"""UI integration test for the MultipleView pattern (GH-91)."""

from flaui.core.definitions import ControlType
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestMultipleViewPattern:
    """Tests for the MultipleView pattern on a control that exposes several presentations."""

    def test_multiple_view_pattern(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        is_pattern_supported: object,
    ) -> None:
        """Read the current and supported views when the pattern is available, else skip."""
        tab = test_application.main_window.find_first_descendant(
            condition=test_application._cf.by_control_type(ControlType.Tab)
        )
        assert_that(tab, not_none())
        if not is_pattern_supported(tab.patterns, "multiple_view"):  # type: ignore[operator]
            pytest.skip("MultipleView pattern is not supported by the available controls")
        view_pattern = tab.patterns.multiple_view.pattern
        assert view_pattern.supported_views.value is not None
        assert view_pattern.current_view.value is not None
