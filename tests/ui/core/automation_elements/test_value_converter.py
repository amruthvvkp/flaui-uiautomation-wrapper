"""
Tests for value conversion and control type, ported from C# ValueConverterTests.cs.
"""

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


# Use fixtures from conftest.py for WinForms/WPF test applications
def test_get_control_type(
    test_application: WinFormsApplicationElements | WPFApplicationElements, ui_automation_type, test_application_type
):
    """Test that the control type of the checkbox is correct (parity with C# ValueConverterTests)."""
    # Find the checkbox by name
    check_box = test_application.main_window.find_first_descendant(
        condition=test_application._cf.by_name("Test Checkbox")
    )
    # The expected control type enum value for CheckBox
    from flaui.core.automation_elements import ControlType

    assert check_box.properties.control_type.to_string == ControlType.CheckBox.name, "ControlType should be CheckBox"
