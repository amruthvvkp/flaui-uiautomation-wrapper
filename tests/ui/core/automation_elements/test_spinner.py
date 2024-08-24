# """Tests for the Spinner control."""

# from flaui.core.automation_type import AutomationType
# import pytest

#
# from tests.test_utilities.config import ApplicationType
# from pytest_check import equal


# @pytest.mark.parametrize(
#     "automation_type,application_type",
#     [
#         (AutomationType.UIA3, ApplicationType.WinForms),
#     ],
# )
# @pytest.xfail(
#     "Somehow Spinner control is not visible from the descendants, need to verify"
# )  # TODO: Find spinner control and fix this test case
# class TestSpinner:
#     """Tests for Spinner control."""

#     def test_set_value(self):
#         """Tests the value setting on Spinner control."""

#         spinner = self.test_elements.simple_controls_tab.spinner
#         for value_to_set in [6.0, 4.0]:
#             spinner.value = value_to_set
#             equal(spinner.value, value_to_set)

#     def test_increment(self):
#         """Tests incremental increase of Spinner controls"""

#         spinner = self.test_elements.simple_controls_tab.spinner
#         value_to_set = 5.0
#         spinner.value = value_to_set
#         equal(spinner.value, value_to_set)
#         spinner.increment()
#         equal(spinner.value, float(value_to_set + 1))

#     def test_decrement(self):
#         """Tests incremental decrease of Spinner controls"""

#         spinner = self.test_elements.simple_controls_tab.spinner
#         value_to_set = 5.0
#         spinner.value = value_to_set
#         equal(spinner.value, value_to_set)
#         spinner.decrement()
#         equal(spinner.value, float(value_to_set - 1))
