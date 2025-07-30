"""Value converter tests, equivalent to C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\Converters\\ValueConverterTests.cs."""

from dirty_equals import HasAttributes
from flaui.core.automation_elements import ControlType

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestValueConverter:
    def test_get_control_type(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Tests the get_control_type method."""
        assert test_application.simple_controls_tab.test_check_box == HasAttributes(control_type=ControlType.CheckBox)
