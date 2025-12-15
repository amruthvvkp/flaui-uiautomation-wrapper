"""UI tests for the module automation_elements.py, equivalent of C# tests from FlaUI GitHub repository - src\\FlaUI.Core.UITests\\AutomationElementTests.cs."""

from pathlib import Path
from typing import Any, Generator

from dirty_equals import (
    HasAttributes,
    HasLen,
    IsAnyStr,
    IsFalseLike,
    IsInstance,
    IsList,
    IsPositiveFloat,
    IsStr,
    IsTrueLike,
)
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
    Properties,
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
from flaui.core.definitions import ControlType, TreeScope, TreeTraversalOptions
from flaui.core.framework_types import FrameworkType
from flaui.lib.enums import UIAutomationTypes
from flaui.lib.exceptions import ElementNotFound
from flaui.lib.system.drawing import Point, Rectangle
from hamcrest import assert_that, calling, instance_of, raises
from loguru import logger
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


class TestAutomationElement:
    """Tests Automation elements"""

    @pytest.fixture(name="window")
    def get_main_window(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Window, Any, None]:
        """Get the main window of the test application.

        :param test_application: The test application to get the main window from.
        :yield: Main Window)
        """
        window = test_application.main_window
        yield window

    def test_parent(
        self,
        window: Window,
    ) -> None:
        """Test the parent property of the AutomationElement class."""
        assert window.find_first_child().parent == HasAttributes(control_type=ControlType.Window), (
            "Parent should be Window"
        )

    def test_is_available(
        self,
        window: Window,
    ) -> None:
        """Test the is_available property of the AutomationElement class."""
        assert window == HasAttributes(is_available=IsTrueLike), "Window should be available"

        # window.close()
        # Retry.WhileTrue(lambda: window.is_available, timeout=5)
        # time.sleep(2)  # Adding a 2 second delay for Window to close properly
        # assert window == HasAttributes(is_available=IsFalseLike), "Window should not be available"


class TestAutomationElementAdditional:
    """Additional UI tests for all other properties in Python class"""

    def test_class_properties(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        ui_automation_type: UIAutomationTypes,
    ) -> None:
        """Test the class properties of the AutomationElement class."""
        # Debugging output
        logger.debug("Debug: Window properties")
        logger.debug(f"Name: {test_application.main_window.name}")

        assert test_application.main_window == HasAttributes(
            actual_height=IsPositiveFloat,
            actual_width=IsPositiveFloat,
            automation_type=AutomationType.UIA2
            if ui_automation_type == UIAutomationTypes.UIA2
            else AutomationType.UIA3,
            class_name=IsAnyStr,
            framework_type=FrameworkType.WinForms
            if isinstance(test_application, WinFormsApplicationElements)
            else FrameworkType.Wpf,
            is_available=IsTrueLike,
            is_enabled=IsTrueLike,
            is_offscreen=IsFalseLike,
            name=IsStr(regex=r"^FlaUI (WinForms|WPF) Test App$", case=None),
            parent=IsInstance(AutomationElement),
            properties=IsInstance(Properties),
        ), "Properties should match"
        assert isinstance(test_application.main_window.bounding_rectangle, Rectangle), "Bounding rectangle should exist"
        assert isinstance(test_application.main_window.condition_factory, ConditionFactory), (
            "Condition factory should exist"
        )

    def test_no_element_exists(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the no_element_exists method of the AutomationElement class."""
        assert_that(
            calling(test_application.main_window.find_first_child).with_args(
                condition_factory.by_class_name(class_name="NoSuchClass")
            ),
            raises(ElementNotFound, "Element does not exist"),
        )

    def test_capture(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the capture method of the AutomationElement class."""
        from System.Drawing import Bitmap  # pyright: ignore

        assert_that(test_application.main_window.capture(), instance_of(Bitmap), "Capture should return a Bitmap")

    def test_capture_to_file(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, tmp_path: Path
    ) -> None:
        """Test the capture_to_file method of the AutomationElement class."""
        tmp_path.mkdir(parents=True, exist_ok=True)
        file_path = tmp_path / "test_capture.png"

        test_application.main_window.capture_to_file(str(file_path))

        assert file_path.exists() == IsTrueLike, "File should exist"
        file_path.unlink()

    def test_click(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the click method of the AutomationElement class."""
        for move_mouse in [False, True]:
            assert test_application.main_window.click(move_mouse) is None, "Click should be successful"

    def test_double_click(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the double_click method of the AutomationElement class."""
        for move_mouse in [False, True]:
            assert test_application.main_window.double_click(move_mouse) is None, "Double click should be successful"

    def test_find_all(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_all method of the AutomationElement class."""
        elements = test_application.main_window.find_all(
            TreeScope.Descendants, condition_factory.by_control_type(ControlType.TabItem)
        )
        for _ in elements:
            assert _ == HasAttributes(control_type=ControlType.TabItem), "ControlType should be TabItem"

    def test_find_all_by_x_path(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the find_all_by_x_path method of the AutomationElement class."""
        elements = test_application.main_window.find_all_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        for _ in elements:
            assert _ == HasAttributes(control_type=ControlType.TabItem), "ControlType should be TabItem"

    def test_find_all_children(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_all_children method of the AutomationElement class."""
        assert test_application.main_window.find_all_children(
            condition_factory.by_control_type(ControlType.Tab)
        ) == HasLen(1), "There should be one child element"

    def test_find_all_descendants(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_all_descendants method of the AutomationElement class."""
        assert test_application.main_window.find_all_descendants(
            condition_factory.by_control_type(ControlType.Tab)
        ) == HasLen(1), "There should be one descendant element"

    def test_find_all_nested(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_all_nested method of the AutomationElement class."""
        assert test_application.main_window.find_all_nested(
            condition_factory.by_control_type(ControlType.Tab)
        ) == HasLen(1), "There should be one nested element"

    # TODO: Check why this test case fails on UIA2 Winforms/WPF and UIA3 WinForms
    @pytest.mark.bug(
        "GH-81",
        "find_all_with_options fails on UIA2 (all) and UIA3+WinForms - TreeTraversalOptions support issue",
        run=True,
    )
    def test_find_all_with_options(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_all_with_options method of the AutomationElement class."""
        assert test_application.main_window.find_all_with_options(
            TreeScope.Descendants,
            condition_factory.by_class_name("TabControl"),
            TreeTraversalOptions.Default,
            test_application.main_window,
        ) == HasLen(1), "There should be one element"

    def test_find_at(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_at method of the AutomationElement class."""
        assert test_application.main_window.find_at(
            TreeScope.Descendants, 0, condition_factory.by_control_type(ControlType.Tab)
        ) == HasAttributes(control_type=ControlType.Tab), "ControlType should be Tab"

    def test_find_child_at(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_child_at method of the AutomationElement class."""
        assert test_application.main_window.find_child_at(
            0, condition_factory.by_control_type(ControlType.Tab)
        ) == HasAttributes(control_type=ControlType.Tab), "ControlType should be Tab"

    def test_find_first(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_first method of the AutomationElement class."""
        assert test_application.main_window.find_first(
            TreeScope.Descendants, condition_factory.by_control_type(ControlType.Tab)
        ) == HasAttributes(control_type=ControlType.Tab), "ControlType should be Tab"

    def test_find_first_by_x_path(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the find_first_by_x_path method of the AutomationElement class."""
        assert test_application.main_window.find_first_by_x_path(
            "/Tab/TabItem[@Name='Simple Controls']"
        ) == HasAttributes(control_type=ControlType.TabItem), "ControlType should be Tab"

    def test_find_first_child(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_first_child method of the AutomationElement class."""
        assert test_application.main_window.find_first_child(
            condition_factory.by_control_type(ControlType.Tab)
        ) == HasAttributes(control_type=ControlType.Tab), "ControlType should be Tab"

    def test_find_first_descendant(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_first_descendant method of the AutomationElement class."""
        assert test_application.main_window.find_first_descendant(
            condition_factory.by_control_type(ControlType.Tab)
        ) == HasAttributes(control_type=ControlType.Tab), "ControlType should be Tab"

    def test_find_first_nested(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_first_nested method of the AutomationElement class."""
        assert test_application.main_window.find_first_nested(
            condition_factory.by_control_type(ControlType.Tab)
        ) == HasAttributes(control_type=ControlType.Tab), "ControlType should be Tab"

    # TODO: Check why this test case fails on UIA2 Winforms
    @pytest.mark.bug(
        "GH-81",
        "find_first_with_options fails on UIA2+WinForms - TreeTraversalOptions support issue",
        run=True,
    )
    def test_find_first_with_options(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: ConditionFactory,
    ) -> None:
        """Test the find_first_with_options method of the AutomationElement class."""
        assert test_application.main_window.find_first_with_options(
            TreeScope.Descendants,
            condition_factory.by_control_type(ControlType.Tab),
            TreeTraversalOptions.Default,
            test_application.main_window,
        ) == HasAttributes(control_type=ControlType.Tab), "ControlType should be Tab"

    def test_focus(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the focus method of the AutomationElement class."""
        calling(test_application.main_window.focus)

    def test_focus_native(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the focus_native method of the AutomationElement class."""
        assert test_application.main_window.focus_native() is None, "Focus should be successful"

    def test_get_clickable_point(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the get_clickable_point method of the AutomationElement class."""
        assert isinstance(test_application.main_window.get_clickable_point(), Point), "Point should be returned"

    # def test_get_current_metadata_value(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
    #     """Test the get_current_metadata_value method of the AutomationElement class."""
    #     pass  # TODO: Build this test

    def test_get_supported_patterns(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Test the get_supported_patterns method of the AutomationElement class."""
        assert test_application.main_window.get_supported_patterns() == IsList(length=...), "List should be returned"  # type: ignore

    def test_get_supported_patterns_direct(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Test the get_supported_patterns_direct method of the AutomationElement class."""
        assert test_application.main_window.get_supported_patterns_direct() == IsList(length=...), (  # type: ignore
            "List should be returned"
        )

    def test_get_supported_properties_direct(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Test the get_supported_properties_direct method of the AutomationElement class."""
        assert test_application.main_window.get_supported_properties_direct() == IsList(length=...), (  # type: ignore
            "List should be returned"
        )

    def test_right_click(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the right_click method of the AutomationElement class."""
        for move_mouse in [False, True]:
            assert test_application.main_window.right_click(move_mouse) is None, "Right click should be successful"

    def test_right_double_click(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the right_double_click method of the AutomationElement class."""
        for move_mouse in [False, True]:
            assert test_application.main_window.right_double_click(move_mouse) is None, (
                "Right double click should be successful"
            )

    def test_set_focus(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the set_focus method of the AutomationElement class."""
        assert test_application.main_window.set_focus() is None, "Focus should be successful"

    def test_set_foreground(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the set_foreground method of the AutomationElement class."""
        assert test_application.main_window.set_foreground() is None, "Foreground should be set"

    def test_to_string(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the to_string method of the AutomationElement class using dirty_equals."""
        actual_string = test_application.main_window.to_string()

        assert actual_string == IsStr(
            regex=r"^AutomationId:(.*|Form1), Name:FlaUI (WPF|WinForms) Test App, ControlType:window, FrameworkId:(WPF|WinForm)$"
        )

    def test_try_get_clickable_point(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Test the try_get_clickable_point method of the AutomationElement class."""
        found, point = test_application.main_window.try_get_clickable_point()
        assert found == IsTrueLike, "Element should be found"
        assert isinstance(point, Point), "Point should be returned"

    def test_as_calendar(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_calendar method of the AutomationElement class."""
        calendar = test_application.main_window.as_calendar()
        assert isinstance(calendar, Calendar), "Calendar should be returned"

    def test_as_check_box(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_check_box method of the AutomationElement class."""
        check_box = test_application.main_window.as_check_box()
        assert isinstance(check_box, CheckBox), "CheckBox should be returned"

    def test_as_combo_box(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_combo_box method of the AutomationElement class."""
        combo_box = test_application.main_window.as_combo_box()
        assert isinstance(combo_box, ComboBox), "ComboBox should be returned"

    def test_as_data_grid_view(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_data_grid_view method of the AutomationElement class."""
        data_grid_view = test_application.main_window.as_data_grid_view()
        assert isinstance(data_grid_view, DataGridView), "DataGridView should be returned"

    def test_as_date_time_picker(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_date_time_picker method of the AutomationElement class."""
        date_time_picker = test_application.main_window.as_date_time_picker()
        assert isinstance(date_time_picker, DateTimePicker), "DateTimePicker should be returned"

    def test_as_label(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_label method of the AutomationElement class."""
        label = test_application.main_window.as_label()
        assert isinstance(label, Label), "Label should be returned"

    def test_as_grid(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_grid method of the AutomationElement class."""
        grid = test_application.main_window.as_grid()
        assert isinstance(grid, Grid), "Grid should be returned"

    def test_as_grid_row(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_grid_row method of the AutomationElement class."""
        grid_row = test_application.main_window.as_grid_row()
        assert isinstance(grid_row, GridRow), "GridRow should be returned"

    def test_as_grid_cell(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_grid_cell method of the AutomationElement class."""
        grid_cell = test_application.main_window.as_grid_cell()
        assert isinstance(grid_cell, GridCell), "GridCell should be returned"

    def test_as_grid_header_item(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_grid_header_item method of the AutomationElement class."""
        grid_header_item = test_application.main_window.as_grid_header_item()
        assert isinstance(grid_header_item, GridHeaderItem), "GridHeaderItem should be returned"

    def test_as_list_box(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_list_box method of the AutomationElement class."""
        list_box = test_application.main_window.as_list_box()
        assert isinstance(list_box, ListBox), "ListBox should be returned"

    def test_as_list_box_item(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_list_box_item method of the AutomationElement class."""
        list_box_item = test_application.main_window.as_list_box_item()
        assert isinstance(list_box_item, ListBoxItem), "ListBoxItem should be returned"

    def test_as_menu(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_menu method of the AutomationElement class."""
        menu = test_application.main_window.as_menu()
        assert isinstance(menu, Menu), "Menu should be returned"

    def test_as_menu_item(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_menu_item method of the AutomationElement class."""
        menu_item = test_application.main_window.as_menu_item()
        assert isinstance(menu_item, MenuItem), "MenuItem should be returned"

    def test_as_progress_bar(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_progress_bar method of the AutomationElement class."""
        progress_bar = test_application.main_window.as_progress_bar()
        assert isinstance(progress_bar, ProgressBar), "ProgressBar should be returned"

    def test_as_radio_button(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_radio_button method of the AutomationElement class."""
        radio_button = test_application.main_window.as_radio_button()
        assert isinstance(radio_button, RadioButton), "RadioButton should be returned"

    def test_as_slider(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_slider method of the AutomationElement class."""
        slider = test_application.main_window.as_slider()
        assert isinstance(slider, Slider), "Slider should be returned"

    def test_as_spinner(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_spinner method of the AutomationElement class."""
        spinner = test_application.main_window.as_spinner()
        assert isinstance(spinner, Spinner), "Spinner should be returned"

    def test_as_tab(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_tab method of the AutomationElement class."""
        tab = test_application.main_window.as_tab()
        assert isinstance(tab, Tab), "Tab should be returned"

    def test_as_tab_item(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_tab_item method of the AutomationElement class."""
        tab_item = test_application.main_window.as_tab_item()
        assert isinstance(tab_item, TabItem), "TabItem should be returned"

    def test_as_text_box(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_text_box method of the AutomationElement class."""
        text_box = test_application.main_window.as_text_box()
        assert isinstance(text_box, TextBox), "TextBox should be returned"

    def test_as_thumb(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_thumb method of the AutomationElement class."""
        thumb = test_application.main_window.as_thumb()
        assert isinstance(thumb, Thumb), "Thumb should be returned"

    def test_as_title_bar(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_title_bar method of the AutomationElement class."""
        title_bar = test_application.main_window.as_title_bar()
        assert isinstance(title_bar, TitleBar), "TitleBar should be returned"

    def test_as_toggle_button(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_toggle_button method of the AutomationElement class."""
        toggle_button = test_application.main_window.as_toggle_button()
        assert isinstance(toggle_button, ToggleButton), "ToggleButton should be returned"

    def test_as_tree(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_tree method of the AutomationElement class."""
        tree = test_application.main_window.as_tree()
        assert isinstance(tree, Tree), "Tree should be returned"

    def test_as_tree_item(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_tree_item method of the AutomationElement class."""
        tree_item = test_application.main_window.as_tree_item()
        assert isinstance(tree_item, TreeItem), "TreeItem should be returned"

    def test_as_window(self, test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
        """Test the as_window method of the AutomationElement class."""
        window = test_application.main_window.as_window()
        assert isinstance(window, Window), "Window should be returned"
