from flaui.lib.enums import UIAutomationTypes

class TestUIAutomationTypes:
    def test_uiautomation_types(self):
        assert UIAutomationTypes.UIA2.value == "UIA2"
        assert UIAutomationTypes.UIA3.value == "UIA3"
