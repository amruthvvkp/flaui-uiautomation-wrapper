"""Tests for ProgressBar control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\ProgressBarTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes
from flaui.core.automation_elements import ProgressBar
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


class TestProgressBar:
    """Tests for ProgressBar control."""

    @pytest.fixture(name="progress_bar")
    def get_progress_bar(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[ProgressBar, Any, None]:
        """Returns the progress bar element.

        :param test_application: Test application elements.
        :yield: Test progress bar element.
        """
        yield test_application.simple_controls_tab.progress_bar

    def test_minimum_value(self, progress_bar: ProgressBar) -> None:
        """Tests the minimum value property."""
        assert progress_bar == HasAttributes(minimum=0), "Minimum value is not 0."

    def test_maximum_value(self, progress_bar: ProgressBar) -> None:
        """Tests the maximum value property."""
        assert progress_bar == HasAttributes(maximum=100), "Maximum value is not 100."

    def test_value(self, progress_bar: ProgressBar) -> None:
        """Tests the value property."""
        assert progress_bar == HasAttributes(value=50), "Set value is not 50."
