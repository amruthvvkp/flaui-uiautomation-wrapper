"""
Unit tests for the module automation_elements.py

This module contains unit tests for the automation_elements.py module. The tests cover the following classes:
- AutomationElement
- Calendar
- CheckBox
- ComboBox
- DataGridView
- DateTimePicker
- Grid
- GridCell
- GridHeaderItem
- GridRow
- Label
- ListBox
- ListBoxItem
- Menu
- MenuItem
- ProgressBar
- RadioButton
- Slider
- Spinner
- Tab
- TabItem
- TextBox
- Thumb
- TitleBar
- ToggleButton
- Tree
- TreeItem
- Window

The tests cover the following methods:
- test_class_properties
- test_no_element_exists
- test_capture
- test_capture_to_file
- test_click
- test_double_click
- test_find_all
- test_find_all_by_x_path
- test_find_all_children
"""

import os
from pathlib import Path
from typing import Any, Generator

from config import test_settings
from flaui.core.automation_elements import (
    AutomationElement,
    Calendar,
    CheckBox,
    ComboBox,
    DataGridView,
    DateTimePicker,
    Grid,
    GridCell,
    GridHeaderItem,
    GridRow,
    Label,
    ListBox,
    ListBoxItem,
    Menu,
    MenuItem,
    ProgressBar,
    RadioButton,
    Slider,
    Spinner,
    Tab,
    TabItem,
    TextBox,
    Thumb,
    TitleBar,
    ToggleButton,
    Tree,
    TreeItem,
    Window,
)
from flaui.core.automation_type import AutomationType
from flaui.core.condition_factory import ConditionFactory
from flaui.core.definitions import ControlType
from FlaUI.Core.Definitions import TreeScope, TreeTraversalOptions  # pyright: ignore
from flaui.lib.enums import KnownClassNames, UIAutomationTypes
from flaui.modules.automation import Automation
from pydantic import ValidationError
import pytest

@pytest.fixture(scope="class")
def wpf_application(ui_automation_type: UIAutomationTypes) -> Generator[Automation, None, None]:
    """Generates FlaUI Automation class with the test application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the test application.
    """
    wpf_application = Automation(ui_automation_type)

    # We want to download the test application only once per test run if the downloaded executable does not exist on local folder.
    wpf_application.application.launch(test_settings.WPF_TEST_APP_EXE.as_posix() if ui_automation_type == UIAutomationTypes.UIA3 else test_settings.WINFORMS_TEST_APP_EXE.as_posix())
    yield wpf_application

    wpf_application.application.kill()


@pytest.fixture(scope="class")
def main_window(wpf_application: Automation, automation: Any) -> Generator[Window, None, None]:
    """Fetches the main window of the test application.

    :param wpf_application: Test application to fetch the main window from.
    :param automation: Automation class to use for the tests.
    :yield: Main window element of the test application.
    """
    yield wpf_application.application.get_main_window(automation)


@pytest.fixture(scope="class")
def condition_factory(main_window: Window):
    """Fixture for the ConditionFactory class.

    :param main_window: The main window of the test application.
    :return: The ConditionFactory class.
    """
    return main_window.condition_factory


@pytest.fixture(scope="class")
def generic_element(main_window: Window):
    """Fixture for the generic element.

    :param main_window: The main window of the test application.
    :return: The generic element.
    """
    return main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")


class TestAutomationElement:
    """Unit tests for the AutomationElement class."""
    def test_class_properties(self, main_window: Window, automation):
        """Test the class properties of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param automation: The automation object.
        """
        element = main_window

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

    def test_no_element_exists(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the no_element_exists method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        with pytest.raises(ValidationError):
            main_window.find_first_child(condition_factory.by_class_name(class_name="NoSuchClass"))


    def test_capture(self, generic_element: AutomationElement):
        """Test the capture method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        from System.Drawing import Bitmap  # pyright: ignore

        isinstance(generic_element.capture(), Bitmap)

    def test_capture_to_file(self, generic_element: AutomationElement):
        """Test the capture_to_file method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        file_path = Path(os.path.join(Path(test_settings.WPF_TEST_APP_EXE).parent.resolve(), "test_capture.png"))

        generic_element.capture_to_file(str(file_path))

        assert file_path.exists()
        file_path.unlink()

    def test_click(self, generic_element: AutomationElement):
        """Test the click method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        for _ in [False, True]:
            try:
                generic_element.click(_)
            except Exception:
                pytest.fail("Unable to click on the test element")

    def test_double_click(self, generic_element: AutomationElement):
        """Test the double_click method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        for _ in [False, True]:
            try:
                generic_element.double_click(_)
            except Exception:
                pytest.fail("Unable to click on the test element")

    def test_find_all(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_all method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        elements = main_window.find_all(
            TreeScope.Descendants, condition_factory.by_control_type(ControlType.TabItem)
        )
        for _ in elements:
            assert _.class_name == "TabItem"

    def test_find_all_by_x_path(self, main_window: Window):
        """Test the find_all_by_x_path method of the AutomationElement class.

        :param main_window: The main window of the test application.
        """
        elements = main_window.find_all_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        for _ in elements:
            assert _.class_name == "TabItem"

    def test_find_all_children(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_all_children method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        elements = main_window.find_all_children(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert len(elements) == 1
        assert elements[0].class_name == KnownClassNames.TabControl.value

    def test_find_all_descendants(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_all_descendants method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        elements = main_window.find_all_descendants(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert len(elements) == 1
        assert elements[0].class_name == KnownClassNames.TabControl.value

    def test_find_all_nested(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_all_nested method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        elements = main_window.find_all_nested(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert len(elements) == 1
        assert elements[0].class_name == KnownClassNames.TabControl.value

    def test_find_all_with_options(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_all_with_options method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        elements = main_window.find_all_with_options(
            TreeScope.Descendants,
            condition_factory.by_class_name(class_name=KnownClassNames.TabControl),
            TreeTraversalOptions.Default,
            main_window.raw_element,
        )
        assert len(elements) == 1
        assert elements[0].class_name == KnownClassNames.TabControl.value

    def test_find_at(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_at method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        element = main_window.find_at(TreeScope.Descendants, 0, condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_child_at(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_child_at method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        element = main_window.find_child_at(0, condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_first method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        element = main_window.find_first(TreeScope.Descendants, condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first_by_x_path(self, main_window: Window):
        """Test the find_first_by_x_path method of the AutomationElement class.

        :param main_window: The main window of the test application.
        """
        element = main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        assert element.class_name == KnownClassNames.TabItem.value

    def test_find_first_child(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_first_child method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        element = main_window.find_first_child(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first_descendant(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_first_descendant method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        element = main_window.find_first_descendant(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first_nested(self, main_window: Window, condition_factory: ConditionFactory):
        """Test the find_first_nested method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        element = main_window.find_first_nested(condition_factory.by_class_name(class_name=KnownClassNames.TabControl))
        assert element.class_name == KnownClassNames.TabControl.value

    def test_find_first_with_options(
        self, main_window: Window, condition_factory: ConditionFactory
    ):
        """Test the find_first_with_options method of the AutomationElement class.

        :param main_window: The main window of the test application.
        :param condition_factory: The condition factory.
        """
        element = main_window.find_first_with_options(
            TreeScope.Descendants,
            condition_factory.by_class_name(class_name=KnownClassNames.TabControl),
            TreeTraversalOptions.Default,
            main_window.raw_element,
        )
        assert element.class_name == KnownClassNames.TabControl.value

    def test_focus(self, generic_element: AutomationElement):
        """Test the focus method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        generic_element.focus()

    def test_focus_native(self, generic_element: AutomationElement):
        """Test the focus_native method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        generic_element.focus_native()

    def test_get_clickable_point(self, generic_element: AutomationElement):
        """Test the get_clickable_point method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        point = generic_element.get_clickable_point()
        assert point is not None

    def test_get_current_metadata_value(self):
        """Test the get_current_metadata_value method of the AutomationElement class."""
        pass

    def test_get_supported_patterns(self, generic_element: AutomationElement):
        """Test the get_supported_patterns method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        patterns = generic_element.get_supported_patterns()
        assert patterns != []

    def test_get_supported_patterns_direct(self, generic_element: AutomationElement):
        """Test the get_supported_patterns_direct method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        patterns = generic_element.get_supported_patterns_direct()
        assert patterns != []

    def test_get_supported_properties_direct(self, generic_element: AutomationElement):
        """Test the get_supported_properties_direct method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        properties = generic_element.get_supported_properties_direct()
        assert properties != []

    def test_right_click(self, generic_element: AutomationElement):
        """Test the right_click method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        for _ in [False, True]:
            generic_element.right_click(_)

    def test_right_double_click(self, generic_element: AutomationElement):
        """Test the right_double_click method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        for _ in [False, True]:
            generic_element.right_double_click(_)

    def test_set_focus(self, generic_element: AutomationElement):
        """Test the set_focus method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        generic_element.set_focus()

    def test_set_foreground(self, generic_element: AutomationElement):
        """Test the set_foreground method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        generic_element.set_foreground()

    def test_to_string(self, generic_element: AutomationElement):
        """Test the to_string method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        test_string = generic_element.to_string()
        assert test_string == "AutomationId:, Name:Simple Controls, ControlType:tab item, FrameworkId:WPF"

    def test_try_get_clickable_point(self, generic_element: AutomationElement):
        """Test the try_get_clickable_point method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        found, point = generic_element.try_get_clickable_point()
        assert found
        assert point is not None

    def test_as_calendar(self, generic_element: AutomationElement):
        """Test the as_calendar method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        calendar = generic_element.as_calendar()
        assert calendar is not None
        assert isinstance(calendar, Calendar)

    def test_as_check_box(self, generic_element: AutomationElement):
        """Test the as_check_box method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        check_box = generic_element.as_check_box()
        assert check_box is not None
        assert isinstance(check_box, CheckBox)

    def test_as_combo_box(self, generic_element: AutomationElement):
        """Test the as_combo_box method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        combo_box = generic_element.as_combo_box()
        assert combo_box is not None
        assert isinstance(combo_box, ComboBox)

    def test_as_data_grid_view(self, generic_element: AutomationElement):
        """Test the as_data_grid_view method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        data_grid_view = generic_element.as_data_grid_view()
        assert data_grid_view is not None
        assert isinstance(data_grid_view, DataGridView)

    def test_as_date_time_picker(self, generic_element: AutomationElement):
        """Test the as_date_time_picker method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        date_time_picker = generic_element.as_date_time_picker()
        assert date_time_picker is not None
        assert isinstance(date_time_picker, DateTimePicker)

    def test_as_label(self, generic_element: AutomationElement):
        """Test the as_label method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        label = generic_element.as_label()
        assert label is not None
        assert isinstance(label, Label)

    def test_as_grid(self, generic_element: AutomationElement):
        """Test the as_grid method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        grid = generic_element.as_grid()
        assert grid is not None
        assert isinstance(grid, Grid)

    def test_as_grid_row(self, generic_element: AutomationElement):
        """Test the as_grid_row method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        grid_row = generic_element.as_grid_row()
        assert grid_row is not None
        assert isinstance(grid_row, GridRow)

    def test_as_grid_cell(self, generic_element: AutomationElement):
        """Test the as_grid_cell method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        grid_cell = generic_element.as_grid_cell()
        assert grid_cell is not None
        assert isinstance(grid_cell, GridCell)

    def test_as_grid_header_item(self, generic_element: AutomationElement):
        """Test the as_grid_header_item method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        grid_header_item = generic_element.as_grid_header_item()
        assert grid_header_item is not None
        assert isinstance(grid_header_item, GridHeaderItem)

    def test_as_list_box(self, generic_element: AutomationElement):
        """Test the as_list_box method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        list_box = generic_element.as_list_box()
        assert list_box is not None
        assert isinstance(list_box, ListBox)

    def test_as_list_box_item(self, generic_element: AutomationElement):
        """Test the as_list_box_item method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        list_box_item = generic_element.as_list_box_item()
        assert list_box_item is not None
        assert isinstance(list_box_item, ListBoxItem)

    def test_as_menu(self, generic_element: AutomationElement):
        """Test the as_menu method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        menu = generic_element.as_menu()
        assert menu is not None
        assert isinstance(menu, Menu)

    def test_as_menu_item(self, generic_element: AutomationElement):
        """Test the as_menu_item method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        menu_item = generic_element.as_menu_item()
        assert menu_item is not None
        assert isinstance(menu_item, MenuItem)

    def test_as_progress_bar(self, generic_element: AutomationElement):
        """Test the as_progress_bar method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        progress_bar = generic_element.as_progress_bar()
        assert progress_bar is not None
        assert isinstance(progress_bar, ProgressBar)

    def test_as_radio_button(self, generic_element: AutomationElement):
        """Test the as_radio_button method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        radio_button = generic_element.as_radio_button()
        assert radio_button is not None
        assert isinstance(radio_button, RadioButton)

    def test_as_slider(self, generic_element: AutomationElement):
        """Test the as_slider method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        slider = generic_element.as_slider()
        assert slider is not None
        assert isinstance(slider, Slider)

    def test_as_spinner(self, generic_element: AutomationElement):
        """Test the as_spinner method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        spinner = generic_element.as_spinner()
        assert spinner is not None
        assert isinstance(spinner, Spinner)

    def test_as_tab(self, generic_element: AutomationElement):
        """Test the as_tab method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        tab = generic_element.as_tab()
        assert tab is not None
        assert isinstance(tab, Tab)

    def test_as_tab_item(self, generic_element: AutomationElement):
        """Test the as_tab_item method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        tab_item = generic_element.as_tab_item()
        assert tab_item is not None
        assert isinstance(tab_item, TabItem)

    def test_as_text_box(self, generic_element: AutomationElement):
        """Test the as_text_box method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        text_box = generic_element.as_text_box()
        assert text_box is not None
        assert isinstance(text_box, TextBox)

    def test_as_thumb(self, generic_element: AutomationElement):
        """Test the as_thumb method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        thumb = generic_element.as_thumb()
        assert thumb is not None
        assert isinstance(thumb, Thumb)

    def test_as_title_bar(self, generic_element: AutomationElement):
        """Test the as_title_bar method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        title_bar = generic_element.as_title_bar()
        assert title_bar is not None
        assert isinstance(title_bar, TitleBar)

    def test_as_toggle_button(self, generic_element: AutomationElement):
        """Test the as_toggle_button method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        toggle_button = generic_element.as_toggle_button()
        assert toggle_button is not None
        assert isinstance(toggle_button, ToggleButton)

    def test_as_tree(self, generic_element: AutomationElement):
        """Test the as_tree method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        tree = generic_element.as_tree()
        assert tree is not None
        assert isinstance(tree, Tree)

    def test_as_tree_item(self, generic_element: AutomationElement):
        """Test the as_tree_item method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        tree_item = generic_element.as_tree_item()
        assert tree_item is not None
        assert isinstance(tree_item, TreeItem)

    def test_as_window(self, generic_element: AutomationElement):
        """Test the as_window method of the AutomationElement class.

        :param generic_element: The generic element.
        """
        window = generic_element.as_window()
        assert window is not None
        assert isinstance(window, Window)
