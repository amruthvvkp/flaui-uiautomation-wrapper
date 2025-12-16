"""
Test for RangeValue pattern, ported from C# RangeValuePatternTests.cs.
"""

# from flaui.core.automation_elements import AutomationElement
# from flaui.core.condition_factory import ConditionFactory
# from hamcrest import assert_that, not_none
# import pytest

# from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
# from tests.test_utilities.elements.wpf_application import WPFApplicationElements


# @pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
# class TestRangeValuePattern:
#     """Tests for RangeValue pattern on Slider control."""

#     @pytest.fixture(name="slider")
#     def get_slider(
#         self,
#         test_application: WinFormsApplicationElements | WPFApplicationElements,
#         condition_factory: ConditionFactory,
#     ):
#         """Fixture to get the Slider element."""
#         slider = test_application.main_window.find_first_descendant(
#             condition=condition_factory.by_automation_id("Slider")
#         )
#         return slider

#     def test_range_value_pattern(self, slider: AutomationElement):
#         """Test RangeValue pattern on Slider control."""
#         assert_that(slider, not_none())
#         rv_pattern = slider.patterns.RangeValue.Pattern  # TODO: Move Patterns to Py-wrapper once it is created
#         assert_that(rv_pattern, not_none())
#         assert not rv_pattern.IsReadOnly.Value
#         assert rv_pattern.Value.Value == 5
#         assert rv_pattern.LargeChange.Value == 4
#         assert rv_pattern.SmallChange.Value == 1
#         assert rv_pattern.Minimum.Value == 0
#         assert rv_pattern.Maximum.Value == 10
#         number1 = 6
#         rv_pattern.SetValue(number1)
#         assert rv_pattern.Value.Value == number1
#         number2 = 3
#         rv_pattern.SetValue(number2)
#         assert rv_pattern.Value.Value == number2
