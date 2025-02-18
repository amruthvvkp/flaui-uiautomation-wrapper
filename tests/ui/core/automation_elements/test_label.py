"""Tests for the Label control."""

from typing import Any, Generator

from dirty_equals import HasAttributes
from flaui.core.automation_elements import Label
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestLabel:
    """Tests for the Label control."""

    @pytest.fixture(name="test_label")
    def get_test_label(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Label, Any, None]:
        """Returns the test label element.

        :param test_application: Test application elements.
        :return: Test label element.
        """
        yield test_application.simple_controls_tab.test_label

    def test_get_text(self, test_label: Label) -> None:
        """Tests the get_text method."""
        assert test_label == HasAttributes(text="Test Label"), "Label text should be available."
