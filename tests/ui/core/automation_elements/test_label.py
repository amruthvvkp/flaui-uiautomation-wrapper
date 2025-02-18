"""Tests for the Label control."""

from dirty_equals import HasAttributes

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestLabel:
    """Tests for the Label control."""

    def test_get_text(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Tests the get_text method."""
        assert test_application.simple_controls_tab.test_label == HasAttributes(text="Test Label"), (
            "Label text should be available."
        )
