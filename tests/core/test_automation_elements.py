# Unit tests for the module automation_elements.py
import os
from pathlib import Path

from config import test_settings
from flaui.core.automation_elements import AutomationElement
from flaui.core.automation_elements import Calendar
from flaui.core.automation_elements import CheckBox
from flaui.core.automation_elements import ComboBox
from flaui.core.automation_elements import DataGridView
from flaui.core.automation_elements import DateTimePicker
from flaui.core.automation_elements import Grid
from flaui.core.automation_elements import GridCell
from flaui.core.automation_elements import GridHeaderItem
from flaui.core.automation_elements import GridRow
from flaui.core.automation_elements import Label
from flaui.core.automation_elements import ListBox
from flaui.core.automation_elements import ListBoxItem
from flaui.core.automation_elements import Menu
from flaui.core.automation_elements import MenuItem
from flaui.core.automation_elements import ProgressBar
from flaui.core.automation_elements import RadioButton
from flaui.core.automation_elements import Slider
from flaui.core.automation_elements import Spinner
from flaui.core.automation_elements import Tab
from flaui.core.automation_elements import TabItem
from flaui.core.automation_elements import TextBox
from flaui.core.automation_elements import Thumb
from flaui.core.automation_elements import TitleBar
from flaui.core.automation_elements import ToggleButton
from flaui.core.automation_elements import Tree
from flaui.core.automation_elements import TreeItem
from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.core.condition_factory import ConditionFactory
from FlaUI.Core.Definitions import TreeScope  # pyright: ignore
from FlaUI.Core.Definitions import TreeTraversalOptions  # pyright: ignore
from flaui.core.definitions import ControlType
from flaui.lib.enums import KnownClassNames
from pydantic import ValidationError
import pytest

@pytest.fixture(scope="module")
def condition_factory(test_app_main_window: AutomationElement):
    return test_app_main_window.condition_factory


@pytest.fixture(scope="module")
def generic_element(test_app_main_window: AutomationElement):
    return test_app_main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")

# @pytest.fixture(scope="module")
# def


class TestAutomationElement:
    def test_class_properties(self, test_app_main_window: AutomationElement, automation):
        element = test_app_main_window

        assert element.actual_height != 0
        assert element.actual_width != 0
        assert isinstance(element.automation_type, AutomationType)
        assert element.bounding_rectangle is not None
        assert element.cached_children is not None
        assert element.cached_parent is None
        assert element.class_name is not None
        assert isinstance(element.condition_factory, ConditionFactory)
        assert element.control_type is not None
        isinstance(element.framework_automation_element, type(automation))
        assert element.framework_type is not None
        assert element.help_text == ""
        assert element.is_available
        assert element.is_enabled
        assert element.is_offscreen is False
        assert element.name == "FlaUI WPF Test App"
        assert element.parent is not None
        assert element.patterns is not None
        assert element.properties is not None

    def test_no_element_exists(self, test_app_main_window: Window, condition_factory: ConditionFactory):
        """Raise exception if no element exists"""
        with pytest.raises(ValidationError):
            test_app_main_window.find_first_child(condition_factory.by_class_name(class_name="NoSuchClass"))


    def test_capture(self, generic_element: AutomationElement):
        from System.Drawing import Bitmap  # pyright: ignore

        isinstance(generic_element.capture(), Bitmap)

    def test_capture_to_file(self, generic_element: AutomationElement):
        file_path = Path(os.path.join(Path(test_settings.WPF_TEST_APP).parent.resolve(), "test_capture.png"))

        generic_element.capture_to_file(str(file_path))

        assert file_path.exists()
        file_path.unlink()

    def test_click(self, generic_element: AutomationElement):
        for _ in [False, True]:
            try:
                generic_element.click(_)
            except Exception:
                pytest.fail("Unable to click on the test element")

    def test_double_click(self, generic_element: AutomationElement):
        for _ in [False, True]:
            try:
                generic_element.double_click(_)
            except Exception:
                pytest.fail("Unable to click on the test element")

    def test_find_all(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        elements = test_app_main_window.find_all(
            TreeScope.Descendants, condition_factory.by_control_type(ControlType.TabItem)
        )
        for _ in elements:
            assert _.class_name == "TabItem"

    def test_find_all_by_x_path(self, test_app_main_window: AutomationElement):
        elements = test_app_main_window.find_all_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        for _ in elements:
            assert _.class_name == "TabItem"

    def test_find_all_children(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        elements = test_app_main_window.find_all_children(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert len(elements) == 1
        assert elements[0].class_name == KnownClassNames.TabControl.value

    def test_find_all_descendants(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        elements = test_app_main_window.find_all_descendants(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert len(elements) == 1
        assert elements[0].class_name == KnownClassNames.TabControl.value

    def test_find_all_nested(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        elements = test_app_main_window.find_all_nested(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert len(elements) == 1
        assert elements[0].class_name == KnownClassNames.TabControl.value

    def test_find_all_with_options(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        elements = test_app_main_window.find_all_with_options(
            TreeScope.Descendants,
            condition_factory.by_class_name(class_name=KnownClassNames.TabControl),
            TreeTraversalOptions.Default,
            test_app_main_window.raw_element,
        )
        assert len(elements) == 1
        assert elements[0].class_name == KnownClassNames.TabControl.value

    def test_find_at(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        element = test_app_main_window.find_at(TreeScope.Descendants, 0, condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_child_at(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        element = test_app_main_window.find_child_at(0, condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        element = test_app_main_window.find_first(TreeScope.Descendants, condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first_by_x_path(self, test_app_main_window: AutomationElement):
        element = test_app_main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        assert element.class_name == KnownClassNames.TabItem.value

    def test_find_first_child(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        element = test_app_main_window.find_first_child(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first_descendant(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        element = test_app_main_window.find_first_descendant(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first_nested(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        element = test_app_main_window.find_first_nested(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first_with_options(
        self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory
    ):
        element = test_app_main_window.find_first_with_options(
            TreeScope.Descendants,
            condition_factory.by_class_name(class_name=KnownClassNames.TabControl),
            TreeTraversalOptions.Default,
            test_app_main_window.raw_element,
        )
        assert element.class_name == KnownClassNames.TabControl.value

    def test_focus(self, generic_element: AutomationElement):
        generic_element.focus()

    def test_focus_native(self, generic_element: AutomationElement):
        generic_element.focus_native()

    def test_get_clickable_point(self, generic_element: AutomationElement):
        point = generic_element.get_clickable_point()
        assert point is not None

    def test_get_current_metadata_value(self):
        pass

    def test_get_supported_patterns(self, generic_element: AutomationElement):
        patterns = generic_element.get_supported_patterns()
        assert patterns != []

    def test_get_supported_patterns_direct(self, generic_element: AutomationElement):
        patterns = generic_element.get_supported_patterns_direct()
        assert patterns != []

    def test_get_supported_properties_direct(self, generic_element: AutomationElement):
        properties = generic_element.get_supported_properties_direct()
        assert properties != []

    def test_right_click(self, generic_element: AutomationElement):
        for _ in [False, True]:
            generic_element.right_click(_)

    def test_right_double_click(self, generic_element: AutomationElement):
        for _ in [False, True]:
            generic_element.right_double_click(_)

    def test_set_focus(self, generic_element: AutomationElement):
        generic_element.set_focus()

    def test_set_foreground(self, generic_element: AutomationElement):
        generic_element.set_foreground()

    def test_to_string(self, generic_element: AutomationElement):
        test_string = generic_element.to_string()
        assert test_string == "AutomationId:, Name:Simple Controls, ControlType:tab item, FrameworkId:WPF"

    def test_try_get_clickable_point(self, generic_element: AutomationElement):
        found, point = generic_element.try_get_clickable_point()
        assert found
        assert point is not None

    def test_as_calendar(self, generic_element: AutomationElement):
        calendar = generic_element.as_calendar()
        assert calendar is not None
        assert isinstance(calendar, Calendar)

    def test_as_check_box(self, generic_element: AutomationElement):
        check_box = generic_element.as_check_box()
        assert check_box is not None
        assert isinstance(check_box, CheckBox)

    def test_as_combo_box(self, generic_element: AutomationElement):
        combo_box = generic_element.as_combo_box()
        assert combo_box is not None
        assert isinstance(combo_box, ComboBox)

    def test_as_data_grid_view(self, generic_element: AutomationElement):
        data_grid_view = generic_element.as_data_grid_view()
        assert data_grid_view is not None
        assert isinstance(data_grid_view, DataGridView)

    def test_as_date_time_picker(self, generic_element: AutomationElement):
        date_time_picker = generic_element.as_date_time_picker()
        assert date_time_picker is not None
        assert isinstance(date_time_picker, DateTimePicker)

    def test_as_label(self, generic_element: AutomationElement):
        label = generic_element.as_label()
        assert label is not None
        assert isinstance(label, Label)

    def test_as_grid(self, generic_element: AutomationElement):
        grid = generic_element.as_grid()
        assert grid is not None
        assert isinstance(grid, Grid)

    def test_as_grid_row(self, generic_element: AutomationElement):
        grid_row = generic_element.as_grid_row()
        assert grid_row is not None
        assert isinstance(grid_row, GridRow)

    def test_as_grid_cell(self, generic_element: AutomationElement):
        grid_cell = generic_element.as_grid_cell()
        assert grid_cell is not None
        assert isinstance(grid_cell, GridCell)

    def test_as_grid_header_item(self, generic_element: AutomationElement):
        grid_header_item = generic_element.as_grid_header_item()
        assert grid_header_item is not None
        assert isinstance(grid_header_item, GridHeaderItem)

    def test_as_list_box(self, generic_element: AutomationElement):
        list_box = generic_element.as_list_box()
        assert list_box is not None
        assert isinstance(list_box, ListBox)

    def test_as_list_box_item(self, generic_element: AutomationElement):
        list_box_item = generic_element.as_list_box_item()
        assert list_box_item is not None
        assert isinstance(list_box_item, ListBoxItem)

    def test_as_menu(self, generic_element: AutomationElement):
        menu = generic_element.as_menu()
        assert menu is not None
        assert isinstance(menu, Menu)

    def test_as_menu_item(self, generic_element: AutomationElement):
        menu_item = generic_element.as_menu_item()
        assert menu_item is not None
        assert isinstance(menu_item, MenuItem)

    def test_as_progress_bar(self, generic_element: AutomationElement):
        progress_bar = generic_element.as_progress_bar()
        assert progress_bar is not None
        assert isinstance(progress_bar, ProgressBar)

    def test_as_radio_button(self, generic_element: AutomationElement):
        radio_button = generic_element.as_radio_button()
        assert radio_button is not None
        assert isinstance(radio_button, RadioButton)

    def test_as_slider(self, generic_element: AutomationElement):
        slider = generic_element.as_slider()
        assert slider is not None
        assert isinstance(slider, Slider)

    def test_as_spinner(self, generic_element: AutomationElement):
        spinner = generic_element.as_spinner()
        assert spinner is not None
        assert isinstance(spinner, Spinner)

    def test_as_tab(self, generic_element: AutomationElement):
        tab = generic_element.as_tab()
        assert tab is not None
        assert isinstance(tab, Tab)

    def test_as_tab_item(self, generic_element: AutomationElement):
        tab_item = generic_element.as_tab_item()
        assert tab_item is not None
        assert isinstance(tab_item, TabItem)

    def test_as_text_box(self, generic_element: AutomationElement):
        text_box = generic_element.as_text_box()
        assert text_box is not None
        assert isinstance(text_box, TextBox)

    def test_as_thumb(self, generic_element: AutomationElement):
        thumb = generic_element.as_thumb()
        assert thumb is not None
        assert isinstance(thumb, Thumb)

    def test_as_title_bar(self, generic_element: AutomationElement):
        title_bar = generic_element.as_title_bar()
        assert title_bar is not None
        assert isinstance(title_bar, TitleBar)

    def test_as_toggle_button(self, generic_element: AutomationElement):
        toggle_button = generic_element.as_toggle_button()
        assert toggle_button is not None
        assert isinstance(toggle_button, ToggleButton)

    def test_as_tree(self, generic_element: AutomationElement):
        tree = generic_element.as_tree()
        assert tree is not None
        assert isinstance(tree, Tree)

    def test_as_tree_item(self, generic_element: AutomationElement):
        tree_item = generic_element.as_tree_item()
        assert tree_item is not None
        assert isinstance(tree_item, TreeItem)

    def test_as_window(self, generic_element: AutomationElement):
        window = generic_element.as_window()
        assert window is not None
        assert isinstance(window, Window)
