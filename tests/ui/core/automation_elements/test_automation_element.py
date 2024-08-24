"""UI tests for the module automation_elements.py"""

import time

from flaui.core.automation_type import AutomationType
from flaui.core.definitions import ControlType
from flaui.core.tools import Retry
import pytest
from pytest_check import equal, is_false, is_true

from tests.test_utilities.base import UITestBase
from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
)
class TestAutomationElementEssentials(UITestBase):
    """Mirrors essential UI tests from TestAutomation element in FlaUI"""

    def test_parent(self):
        """Tests if parent is Window"""
        self.restart_application()
        window = self.application.get_main_window(self.automation)
        child = window.find_first_child()
        equal(child.parent.control_type, ControlType.Window)

    def test_is_available(self):
        """Tests if parent window is available"""
        self.restart_application()
        window = self.application.get_main_window(self.automation)
        is_true(window.is_available)
        window.close()
        Retry.WhileTrue(lambda: window.is_available, timeout=5)
        time.sleep(2)  # Adding a 2 second delay for Window to close properly
        is_false(window.is_available, "Window should be closed")


# @pytest.mark.parametrize(
#     "automation_type,application_type",
#     [
#         (AutomationType.UIA2, ApplicationType.WinForms),
#         (AutomationType.UIA2, ApplicationType.Wpf),
#         (AutomationType.UIA3, ApplicationType.WinForms),
#         (AutomationType.UIA3, ApplicationType.Wpf),
#     ],
# )
# class TestAutomationElementAdditional(UITestBase):
#     """Additional UI tests for all other properties in Python class"""

#     def test_class_properties(self):
#         """Test the class properties of the AutomationElement class."""
#         element = self.main_window

#         greater(element.actual_height, 0)
#         greater(element.actual_width, 0)
#         is_instance(element.automation_type, AutomationType)
#         is_not_none(element.bounding_rectangle)
#         is_not_none(element.class_name)
#         is_instance(element.condition_factory, ConditionFactory)
#         is_not_none(element.control_type)
#         is_not_none(element.framework_type)
#         if self._application_type == ApplicationType.Wpf:
#             is_(element.help_text, "")
#         is_true(element.is_available)
#         is_true(element.is_enabled)
#         is_false(element.is_offscreen)
#         equal(
#             element.name,
#             "FlaUI WPF Test App" if self._application_type == ApplicationType.Wpf else "FlaUI WinForms Test App",
#         )
#         is_not_none(element.parent)
#         is_not_none(element.patterns)
#         is_not_none(element.properties)

#     def test_no_element_exists(self):
#         """Test the no_element_exists method of the AutomationElement class."""
#         with pytest.raises(ValidationError):
#             self.main_window.find_first_child(self.condition_factory.by_class_name(class_name="NoSuchClass"))

#     def test_capture(self):
#         """Test the capture method of the AutomationElement class."""
#         from System.Drawing import Bitmap  # pyright: ignore

#         is_instance(self.main_window.capture(), Bitmap)

#     def test_capture_to_file(self):
#         """Test the capture_to_file method of the AutomationElement class."""
#         file_path = Path(os.path.join(Path(test_settings.WPF_TEST_APP_EXE).parent.resolve(), "test_capture.png"))

#         self.main_window.capture_to_file(str(file_path))

#         is_true(file_path.exists())
#         file_path.unlink()

#     def test_click(self):
#         """Test the click method of the AutomationElement class."""
#         for move_mouse in [False, True]:
#             try:
#                 self.main_window.click(move_mouse)
#             except Exception:
#                 pytest.fail("Unable to click on the test element")

#     def test_double_click(self):
#         """Test the double_click method of the AutomationElement class."""
#         for move_mouse in [False, True]:
#             try:
#                 self.main_window.double_click(move_mouse)
#             except Exception:
#                 pytest.fail("Unable to double click on the test element")

#     def test_find_all(self):
#         """Test the find_all method of the AutomationElement class."""
#         elements = self.main_window.find_all(
#             TreeScope.Descendants, self.condition_factory.by_control_type(ControlType.TabItem)
#         )
#         for _ in elements:
#             equal(_.control_type, ControlType.TabItem)

#     def test_find_all_by_x_path(self):
#         """Test the find_all_by_x_path method of the AutomationElement class."""
#         elements = self.main_window.find_all_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
#         for _ in elements:
#             equal(_.control_type, ControlType.TabItem)

#     def test_find_all_children(self):
#         """Test the find_all_children method of the AutomationElement class."""
#         elements = self.main_window.find_all_children(self.condition_factory.by_control_type(ControlType.Tab))
#         equal(len(elements), 1)

#     def test_find_all_descendants(self):
#         """Test the find_all_descendants method of the AutomationElement class."""
#         elements = self.main_window.find_all_descendants(self.condition_factory.by_control_type(ControlType.Tab))
#         equal(len(elements), 1)

#     def test_find_all_nested(self):
#         """Test the find_all_nested method of the AutomationElement class."""
#         elements = self.main_window.find_all_nested(self.condition_factory.by_control_type(ControlType.Tab))
#         equal(len(elements), 1)

#     # TODO: Check why this test case fails
#     # def test_find_all_with_options(self):
#     #     """Test the find_all_with_options method of the AutomationElement class."""
#     #     elements = self.main_window.find_all_with_options(
#     #         TreeScope.Descendants,
#     #         self.condition_factory.by_class_name("TabControl"),
#     #         TreeTraversalOptions.Default,
#     #         self.main_window.raw_element,
#     #     )
#     #     equal(len(elements), 1)

#     def test_find_at(self):
#         """Test the find_at method of the AutomationElement class."""
#         element = self.main_window.find_at(
#             TreeScope.Descendants, 0, self.condition_factory.by_control_type(ControlType.Tab)
#         )
#         equal(element.control_type, ControlType.Tab)

#     def test_find_child_at(self):
#         """Test the find_child_at method of the AutomationElement class."""
#         element = self.main_window.find_child_at(0, self.condition_factory.by_control_type(ControlType.Tab))
#         equal(element.control_type, ControlType.Tab)

#     def test_find_first(self):
#         """Test the find_first method of the AutomationElement class."""
#         element = self.main_window.find_first(
#             TreeScope.Descendants, self.condition_factory.by_control_type(ControlType.Tab)
#         )
#         equal(element.control_type, ControlType.Tab)

#     def test_find_first_by_x_path(self):
#         """Test the find_first_by_x_path method of the AutomationElement class."""
#         element = self.main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
#         equal(element.control_type, ControlType.TabItem)

#     def test_find_first_child(self):
#         """Test the find_first_child method of the AutomationElement class."""
#         element = self.main_window.find_first_child(self.condition_factory.by_control_type(ControlType.Tab))
#         equal(element.control_type, ControlType.Tab)

#     def test_find_first_descendant(self):
#         """Test the find_first_descendant method of the AutomationElement class."""
#         element = self.main_window.find_first_descendant(self.condition_factory.by_control_type(ControlType.Tab))
#         equal(element.control_type, ControlType.Tab)

#     def test_find_first_nested(self):
#         """Test the find_first_nested method of the AutomationElement class."""
#         element = self.main_window.find_first_nested(self.condition_factory.by_control_type(ControlType.Tab))
#         equal(element.control_type, ControlType.Tab)

#     # TODO: Check why this test case fails
#     # def test_find_first_with_options(self):
#     #     """Test the find_first_with_options method of the AutomationElement class."""
#     #     element = self.main_window.find_first_with_options(
#     #         TreeScope.Descendants,
#     #         self.condition_factory.by_control_type(ControlType.Tab),
#     #         TreeTraversalOptions.Default,
#     #         self.main_window.raw_element,
#     #     )
#     #     equal(element.control_type, ControlType.Tab)

#     def test_focus(self):
#         """Test the focus method of the AutomationElement class."""
#         try:
#             self.main_window.focus()
#         except Exception:
#             pytest.fail("Unable to focus on the test element")

#     def test_focus_native(self):
#         """Test the focus_native method of the AutomationElement class."""
#         try:
#             self.main_window.focus_native()
#         except Exception:
#             pytest.fail("Unable to use native focus on the test element")

#     def test_get_clickable_point(self):
#         """Test the get_clickable_point method of the AutomationElement class."""
#         point = self.main_window.get_clickable_point()
#         is_not_none(point)

#     def test_get_current_metadata_value(self):
#         """Test the get_current_metadata_value method of the AutomationElement class."""
#         pass  # TODO: Build this test

#     def test_get_supported_patterns(self):
#         """Test the get_supported_patterns method of the AutomationElement class."""
#         patterns = self.main_window.get_supported_patterns()
#         not_equal(patterns, [])

#     def test_get_supported_patterns_direct(self):
#         """Test the get_supported_patterns_direct method of the AutomationElement class."""
#         patterns = self.main_window.get_supported_patterns_direct()
#         not_equal(patterns, [])

#     def test_get_supported_properties_direct(self):
#         """Test the get_supported_properties_direct method of the AutomationElement class."""
#         properties = self.main_window.get_supported_properties_direct()
#         not_equal(properties, [])

#     def test_right_click(self):
#         """Test the right_click method of the AutomationElement class."""
#         for move_mouse in [False, True]:
#             try:
#                 self.main_window.right_click(move_mouse)
#             except Exception:
#                 pytest.fail("Unable to right click on the test element")

#     def test_right_double_click(self):
#         """Test the right_double_click method of the AutomationElement class."""
#         for move_mouse in [False, True]:
#             try:
#                 self.main_window.right_double_click(move_mouse)
#             except Exception:
#                 pytest.fail("Unable to right double click on the test element")

#     def test_set_focus(self):
#         """Test the set_focus method of the AutomationElement class."""
#         try:
#             self.main_window.set_focus()
#         except Exception:
#             pytest.fail("Unable to use set focus on the test element")

#     def test_set_foreground(self):
#         """Test the set_foreground method of the AutomationElement class."""
#         try:
#             self.main_window.set_foreground()
#         except Exception:
#             pytest.fail("Unable to use set foreground on the test element")

#     def test_to_string(self):
#         """Test the to_string method of the AutomationElement class."""
#         actual_string = self.main_window.to_string()
#         if self._application_type == ApplicationType.Wpf:
#             equal(actual_string, "AutomationId:, Name:FlaUI WPF Test App, ControlType:window, FrameworkId:WPF")
#         elif self._application_type == ApplicationType.WinForms:
#             equal(
#                 actual_string,
#                 "AutomationId:Form1, Name:FlaUI WinForms Test App, ControlType:window, FrameworkId:WinForm",
#             )

#     def test_try_get_clickable_point(self):
#         """Test the try_get_clickable_point method of the AutomationElement class."""
#         found, point = self.main_window.try_get_clickable_point()
#         is_true(found)
#         is_not_none(point)

#     def test_as_calendar(self):
#         """Test the as_calendar method of the AutomationElement class."""
#         calendar = self.main_window.as_calendar()
#         is_not_none(calendar)
#         is_instance(calendar, Calendar)

#     def test_as_check_box(self):
#         """Test the as_check_box method of the AutomationElement class."""
#         check_box = self.main_window.as_check_box()
#         is_not_none(check_box)
#         is_instance(check_box, CheckBox)

#     def test_as_combo_box(self):
#         """Test the as_combo_box method of the AutomationElement class."""
#         combo_box = self.main_window.as_combo_box()
#         is_not_none(combo_box)
#         is_instance(combo_box, ComboBox)

#     def test_as_data_grid_view(self):
#         """Test the as_data_grid_view method of the AutomationElement class."""
#         data_grid_view = self.main_window.as_data_grid_view()
#         is_not_none(data_grid_view)
#         is_instance(data_grid_view, DataGridView)

#     def test_as_date_time_picker(self):
#         """Test the as_date_time_picker method of the AutomationElement class."""
#         date_time_picker = self.main_window.as_date_time_picker()
#         is_not_none(date_time_picker)
#         is_instance(date_time_picker, DateTimePicker)

#     def test_as_label(self):
#         """Test the as_label method of the AutomationElement class."""
#         label = self.main_window.as_label()
#         is_not_none(label)
#         is_instance(label, Label)

#     def test_as_grid(self):
#         """Test the as_grid method of the AutomationElement class."""
#         grid = self.main_window.as_grid()
#         is_not_none(grid)
#         is_instance(grid, Grid)

#     def test_as_grid_row(self):
#         """Test the as_grid_row method of the AutomationElement class."""
#         grid_row = self.main_window.as_grid_row()
#         is_not_none(grid_row)
#         is_instance(grid_row, GridRow)

#     def test_as_grid_cell(self):
#         """Test the as_grid_cell method of the AutomationElement class."""
#         grid_cell = self.main_window.as_grid_cell()
#         is_not_none(grid_cell)
#         is_instance(grid_cell, GridCell)

#     def test_as_grid_header_item(self):
#         """Test the as_grid_header_item method of the AutomationElement class."""
#         grid_header_item = self.main_window.as_grid_header_item()
#         is_not_none(grid_header_item)
#         is_instance(grid_header_item, GridHeaderItem)

#     def test_as_list_box(self):
#         """Test the as_list_box method of the AutomationElement class."""
#         list_box = self.main_window.as_list_box()
#         is_not_none(list_box)
#         is_instance(list_box, ListBox)

#     def test_as_list_box_item(self):
#         """Test the as_list_box_item method of the AutomationElement class."""
#         list_box_item = self.main_window.as_list_box_item()
#         is_not_none(list_box_item)
#         is_instance(list_box_item, ListBoxItem)

#     def test_as_menu(self):
#         """Test the as_menu method of the AutomationElement class."""
#         menu = self.main_window.as_menu()
#         is_not_none(menu)
#         is_instance(menu, Menu)

#     def test_as_menu_item(self):
#         """Test the as_menu_item method of the AutomationElement class."""
#         menu_item = self.main_window.as_menu_item()
#         is_not_none(menu_item)
#         is_instance(menu_item, MenuItem)

#     def test_as_progress_bar(self):
#         """Test the as_progress_bar method of the AutomationElement class."""
#         progress_bar = self.main_window.as_progress_bar()
#         is_not_none(progress_bar)
#         is_instance(progress_bar, ProgressBar)

#     def test_as_radio_button(self):
#         """Test the as_radio_button method of the AutomationElement class."""
#         radio_button = self.main_window.as_radio_button()
#         is_not_none(radio_button)
#         is_instance(radio_button, RadioButton)

#     def test_as_slider(self):
#         """Test the as_slider method of the AutomationElement class."""
#         slider = self.main_window.as_slider()
#         is_not_none(slider)
#         is_instance(slider, Slider)

#     def test_as_spinner(self):
#         """Test the as_spinner method of the AutomationElement class."""
#         spinner = self.main_window.as_spinner()
#         is_not_none(spinner)
#         is_instance(spinner, Spinner)

#     def test_as_tab(self):
#         """Test the as_tab method of the AutomationElement class."""
#         tab = self.main_window.as_tab()
#         is_not_none(tab)
#         is_instance(tab, Tab)

#     def test_as_tab_item(self):
#         """Test the as_tab_item method of the AutomationElement class."""
#         tab_item = self.main_window.as_tab_item()
#         is_not_none(tab_item)
#         is_instance(tab_item, TabItem)

#     def test_as_text_box(self):
#         """Test the as_text_box method of the AutomationElement class."""
#         text_box = self.main_window.as_text_box()
#         is_not_none(text_box)
#         is_instance(text_box, TextBox)

#     def test_as_thumb(self):
#         """Test the as_thumb method of the AutomationElement class."""
#         thumb = self.main_window.as_thumb()
#         is_not_none(thumb)
#         is_instance(thumb, Thumb)

#     def test_as_title_bar(self):
#         """Test the as_title_bar method of the AutomationElement class."""
#         title_bar = self.main_window.as_title_bar()
#         is_not_none(title_bar)
#         is_instance(title_bar, TitleBar)

#     def test_as_toggle_button(self):
#         """Test the as_toggle_button method of the AutomationElement class."""
#         toggle_button = self.main_window.as_toggle_button()
#         is_not_none(toggle_button)
#         is_instance(toggle_button, ToggleButton)

#     def test_as_tree(self):
#         """Test the as_tree method of the AutomationElement class."""
#         tree = self.main_window.as_tree()
#         is_not_none(tree)
#         is_instance(tree, Tree)

#     def test_as_tree_item(self):
#         """Test the as_tree_item method of the AutomationElement class."""
#         tree_item = self.main_window.as_tree_item()
#         is_not_none(tree_item)
#         is_instance(tree_item, TreeItem)

#     def test_as_window(self):
#         """Test the as_window method of the AutomationElement class."""
#         window = self.main_window.as_window()
#         is_not_none(window)
#         is_instance(window, Window)
