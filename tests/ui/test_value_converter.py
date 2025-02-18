# from flaui.core.automation_elements import ControlType
# from flaui.lib.enums import UIAutomationTypes
# from flaui.modules.automation import Automation
# import pytest


# def test_get_control_type(test_app: Automation) -> None:
#     window = test_app.application.get_main_window(test_app.cs_automation)
#     checkbox = window.find_first_descendant(condition=test_app.cf.by_name("Test CheckBox"))
#     assert checkbox.control_type == ControlType.CheckBox
