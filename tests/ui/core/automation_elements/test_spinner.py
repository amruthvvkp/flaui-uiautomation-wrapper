"""Tests for the Spinner control."""

from dirty_equals import HasAttributes
from flaui.lib.enums import UIAutomationTypes
import pytest

from tests.test_utilities.elements.winforms_application.base import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application.base import WPFApplicationElements


@pytest.mark.xfail(reason="Spinner control on WinForms is sometimes unavailable while running bulk tests")
class TestSpinner:
    """Tests for Spinner control."""

    def test_set_value(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        ui_automation_type: UIAutomationTypes,
        test_application_type: str,
    ) -> None:
        """Tests the value setting on Spinner control."""
        if not (ui_automation_type == UIAutomationTypes.UIA3 and test_application_type == "WinForms"):
            pytest.skip("Only runs for UIA3 + WinForms")

        spinner = test_application.simple_controls_tab.spinner
        for value_to_set in [6.0, 4.0]:
            spinner.value = value_to_set
            assert spinner == HasAttributes(value=value_to_set), "Set value is not correct."

    @pytest.fixture()
    def skip_if_non_compliant(self, ui_automation_type: UIAutomationTypes, test_application_type: str) -> None:
        if not (ui_automation_type == UIAutomationTypes.UIA3 and test_application_type == "WinForms"):
            pytest.skip("Only runs for UIA3 + WinForms")

    def test_increment(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        ui_automation_type: UIAutomationTypes,
        test_application_type: str,
    ) -> None:
        """Tests incremental increase of Spinner controls"""
        if not (ui_automation_type == UIAutomationTypes.UIA3 and test_application_type == "WinForms"):
            pytest.skip("Only runs for UIA3 + WinForms")

        spinner = test_application.simple_controls_tab.spinner
        value_to_set = 5.0
        spinner.value = value_to_set
        assert spinner == HasAttributes(value=value_to_set), "Set value is not correct."
        spinner.increment()
        assert spinner == HasAttributes(value=value_to_set + 1), "Set value is not correct post increment."

    def test_decrement(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        ui_automation_type: UIAutomationTypes,
        test_application_type: str,
    ) -> None:
        """Tests incremental decrease of Spinner controls"""
        if not (ui_automation_type == UIAutomationTypes.UIA3 and test_application_type == "WinForms"):
            pytest.skip("Only runs for UIA3 + WinForms")

        spinner = test_application.simple_controls_tab.spinner
        value_to_set = 5.0
        spinner.value = value_to_set
        assert spinner == HasAttributes(value=value_to_set), "Set value is not correct."
        spinner.decrement()
        assert spinner == HasAttributes(value=value_to_set - 1), "Set value is not correct post decrement."
