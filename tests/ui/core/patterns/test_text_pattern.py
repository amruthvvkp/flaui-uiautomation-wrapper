"""UI integration tests for the Text and Text2 patterns on a TextBox control (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from flaui.core.definitions import SupportedTextSelection
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestTextPattern:
    """Tests for the Text pattern (and the UIA3-only Text2 pattern) on a TextBox control."""

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

    def test_text_pattern(self, text_box: AutomationElement, is_pattern_supported: object) -> None:
        """Read the document range text through the Text pattern, restoring the original content."""
        assert_that(text_box, not_none())
        if not is_pattern_supported(text_box.patterns, "text"):  # type: ignore[operator]
            pytest.skip("Text pattern is not supported on this control/runtime")
        text_pattern = text_box.patterns.text.pattern
        assert isinstance(text_pattern.supported_text_selection, SupportedTextSelection)
        value_pattern = text_box.patterns.value.pattern
        original = value_pattern.value.value
        try:
            value_pattern.set_value("text pattern content")
            assert "text pattern content" in text_pattern.document_range.get_text()
        finally:
            value_pattern.set_value(original or "")

    def test_text2_pattern_plumbing(
        self,
        text_box: AutomationElement,
        skip_on_uia2: None,
        is_pattern_supported: object,
    ) -> None:
        """Verify the Text2 accessor (UIA3-only) resolves and reports support as a boolean.

        :param text_box: TextBox automation element.
        :param skip_on_uia2: Fixture that skips the test under UIA2.
        :param is_pattern_supported: Helper that safely reports pattern support.
        """
        assert isinstance(is_pattern_supported(text_box.patterns, "text2"), bool)  # type: ignore[operator]
