"""Tests for the Spinner control, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Elements\\SpinnerTests.cs."""

from typing import Any, Generator

from dirty_equals import HasAttributes
from flaui.core.automation_elements import Spinner
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.platform_limitation
@pytest.mark.uia3_only
@pytest.mark.winforms_only
@pytest.mark.xfail(
    reason="Spinner control element finding is flaky - AutomationID sometimes returns as uuid. "
    "This is a known issue mentioned in element locator comments, particularly noticeable in bulk test runs."
)
class TestSpinner:
    """Tests for Spinner control.

    C# SpinnerTests only runs on UIA3 + WinForms due to platform limitation:
    "The spinner control does not work with UIA2/WinForms anymore due to bugs in Windows / .NET"

    KNOWN ISSUE: Element finding is flaky due to AutomationID instability.
    """

    @pytest.fixture(name="spinner")
    def get_spinner(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        require_uia3_winforms: None,
    ) -> Generator[Spinner, Any, None]:
        """Returns the spinner element.

        :param test_application: Test application elements.
        :param require_uia3_winforms: Fixture that skips if not UIA3+WinForms.
        :return: Test spinner element.
        """
        yield test_application.simple_controls_tab.spinner  # type: ignore

    def test_set_value(self, spinner: Spinner) -> None:
        """Tests the value setting on Spinner control."""
        for value_to_set in [6.0, 4.0]:
            spinner.value = value_to_set
            assert spinner == HasAttributes(value=value_to_set), "Set value is not correct."

    def test_increment(self, spinner: Spinner) -> None:
        """Tests incremental increase of Spinner controls"""
        value_to_set = 5.0
        spinner.value = value_to_set
        assert spinner == HasAttributes(value=value_to_set), "Set value is not correct."
        spinner.increment()
        assert spinner == HasAttributes(value=value_to_set + 1), "Set value is not correct post increment."

    def test_decrement(self, spinner: Spinner) -> None:
        """Tests incremental decrease of Spinner controls"""
        value_to_set = 5.0
        spinner.value = value_to_set
        assert spinner == HasAttributes(value=value_to_set), "Set value is not correct."
        spinner.decrement()
        assert spinner == HasAttributes(value=value_to_set - 1), "Set value is not correct post decrement."
