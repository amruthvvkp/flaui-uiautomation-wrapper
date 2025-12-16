"""Test for focus changed event handling, ported from C# FocusChangedTests.cs."""
# TODO: Implement this test when RegisterFocusChangedEvent is created in UIA3
# """
# Test for focus changed event handling, ported from C# FocusChangedTests.cs.
# """

# import os
# import time

# from flaui.lib.enums import UIAutomationTypes
# from flaui.modules.automation import Automation
# import pytest


# # Only run this test on Windows with mspaint available
# @pytest.mark.skipif(os.name != "nt", reason="Requires Windows and mspaint.exe")
# def test_focus_changed_with_paint():
#     """Test focus changed event handling in mspaint (parity with C#)."""
#     automation = Automation(UIAutomationTypes.UIA3)
#     app = automation.application.launch("mspaint")
#     try:
#         app.wait_while_main_handle_is_missing(5)
#         focus_changed_elements = []
#         main_window = app.get_main_window(automation)
#         # Register focus changed event
#         x = automation.register_focus_changed_event(lambda element: focus_changed_elements.append(str(element)))
#         time.sleep(0.1)
#         # Find and click the Resize button
#         resize_text = "Resize"
#         button1 = main_window.find_first_descendant(
#             lambda cf: cf.by_control_type("Button").and_(cf.by_text(resize_text))
#         )
#         button1.as_button().invoke()
#         time.sleep(0.1)
#         # Find and click the Pixels radio button
#         pixels_text = "Pixels"
#         radio2 = main_window.find_first_descendant(
#             lambda cf: cf.by_control_type("RadioButton").and_(cf.by_text(pixels_text))
#         )
#         radio2.get_clickable_point().click()
#         time.sleep(0.1)
#         # Press Escape to close dialog
#         from flaui.core.input import Keyboard, VirtualKeyShort

#         Keyboard.press(VirtualKeyShort.ESCAPE)
#         time.sleep(0.1)
#         x.dispose()
#         main_window.close()
#         assert len(focus_changed_elements) > 0, "Should have received focus changed events."
#     finally:
#         app.close()
