"""UI integration test for the LegacyIAccessible pattern on a Button control (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestLegacyIAccessiblePattern:
    """Tests for the LegacyIAccessible (MSAA bridge) pattern on a standard control."""

    @pytest.fixture(name="element")
    def get_element(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get a control that resolves on both WinForms and WPF.

        :param test_application: Test application elements.
        :yield: CheckBox automation element.
        """
        yield test_application.simple_controls_tab.test_check_box

    def test_legacy_i_accessible_pattern(
        self,
        element: AutomationElement,
        is_pattern_supported: object,
    ) -> None:
        """Read MSAA name and role through the LegacyIAccessible pattern when supported."""
        assert_that(element, not_none())
        if not is_pattern_supported(element.patterns, "legacy_i_accessible"):  # type: ignore[operator]
            pytest.skip("LegacyIAccessible pattern is not supported on this control/runtime")
        legacy_pattern = element.patterns.legacy_i_accessible.pattern
        name = legacy_pattern.name.value_or_default
        assert name is None or isinstance(name, str)
        assert legacy_pattern.role.value is not None
