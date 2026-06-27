"""UI integration test for the Value pattern on a TextBox control (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestValuePattern:
    """Tests for the Value pattern on a TextBox control."""

    @pytest.fixture(name="text_box")
    def get_text_box(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the editable TextBox element.

        :param test_application: Test application elements.
        :yield: TextBox automation element.
        """
        yield test_application.simple_controls_tab.test_text_box

    def test_value_pattern(self, text_box: AutomationElement) -> None:
        """Read and set the control value through the Value pattern, restoring the original text."""
        assert_that(text_box, not_none())
        value_pattern = text_box.patterns.value.pattern
        assert_that(value_pattern, not_none())
        assert value_pattern.is_read_only.value is False
        original = value_pattern.value.value
        try:
            value_pattern.set_value("FlaUI value pattern")
            assert value_pattern.value.value == "FlaUI value pattern"
        finally:
            value_pattern.set_value(original or "")
