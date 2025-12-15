"""Value converter tests, equivalent to C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Converters\\ValueConverterTests.cs."""

from dirty_equals import HasAttributes
from flaui.core.automation_elements import ControlType
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestValueConverter:
    @pytest.mark.bug(
        "GH-82",
        "test_get_control_type fails intermittently on UIA2+WinForms - Tab element not found during setup",
        run=True,
    )
    def test_get_control_type(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Tests the get_control_type method."""
        assert test_application.simple_controls_tab.test_check_box == HasAttributes(control_type=ControlType.CheckBox)
