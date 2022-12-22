"""
Wrapper objects for AutomationElement class.
"""

from __future__ import annotations

from typing import Any, List, Optional, Union

import arrow

from flaui.lib.cast_type_converter import TypeConverter
from flaui.wrappers.core.automation_element_extensions import AutomationElementExtensions


class AutomationElement:
    """Wrapper object for each ui element which is should be automated."""

    def __init__(self, element: Any) -> None:
        """Builds AutomationElement class

        :param element: Element object
        """
        self.element = element
        self.actual_height: int = self.element.ActualHeight  #  The height of this element.
        self.actual_width: int = self.element.ActualWidth  # The width of this element.
        self.automation_id: str = self.element.AutomationId  #   The automation id of the element.
        self.automation_type: Any = self.element.AutomationType  #   The current AutomationType for this element.
        self.bounding_rectangle: Any = self.element.BoundingRectangle  #   The bounding rectangle of this element.
        self.cached_children: Any = self.element.CachedChildren  #   Gets the cached children for this element.
        self.cached_parent: Any = self.element.CachedParent  #   Gets the cached parent for this element.
        self.class_name: str = self.element.ClassName  #   The class name of the element.
        self.condition_factory: Any = (
            self.element.ConditionFactory
        )  #   Shortcut to the condition factory for the current automation.
        self.control_type: str = self.element.ControlType  #   The control type of the element.
        # TODO: Get actual ControlType, ConditionalFactory class, BoundingRectangle object
        self.framework_automation_element: Any = (
            self.element.FrameworkAutomationElement
        )  #   Object which contains the native wrapper element (UIA2 or UIA3) for this element.
        self.framework_type: Any = (
            self.element.FrameworkType
        )  #   The direct framework type of the element. Results in "FrameworkType.Unknown" if it couldn't be resolved.
        self.help_text: str = self.element.HelpText  #   The help text of this element.
        self.is_available: bool = (
            self.element.IsAvailable
        )  #    A flag that indicates if the element is still available. Can be false if the element is already unloaded from the ui.
        self.is_enabled: bool = self.element.IsEnabled  #   Flag if the element is enabled or not.
        self.is_offscreen: bool = self.element.IsOffscreen  #   Flag if the element off-screen or on-screen(visible).
        self.name: str = self.element.Name  #   The name of the element.
        self.parent: Any = self.element.Parent  #   Get the parent AutomationElement.
        self.patterns: Any = self.element.Patterns  #   Standard UIA patterns of this element.
        self.properties: Any = self.element.Properties  #   Standard UIA properties of this element.

    def return_automation_element(self, element: Any) -> AutomationElement:
        """Returns an instance of the class

        :param element: Element raw object
        :return: AutomationElement class
        """
        return AutomationElement(element)

    def capture(self) -> Any:
        """Captures the object as screenshot in Bitmap format.

        :return: Captured element image Bitmap object
        """
        return self.element.Capture()

    def capture_to_file(self, file_path: str) -> None:
        """Captures the object as screenshot directly into the given file.

        :param file_path: The filepath where the screenshot should be saved.
        :return: None
        """
        self.element.CaptureToFile(file_path)

    def click(self, move_mouse: bool = False) -> None:
        """Performs a left click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly(True) or instantly(False), defaults to False
        """
        self.element.Click(move_mouse)

    def double_click(self, move_mouse: bool = False) -> None:
        """Performs a double left click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly(True) or instantly(False), defaults to False
        """
        self.element.DoubleClick(move_mouse)

    def find_all(self, tree_scope: Any, condition: Optional[Any]) -> List[AutomationElement]:
        """Finds all children with the condition.

        :aram tree_scope: Treescope object
        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [
            self.return_automation_element(_)
            for _ in TypeConverter.cast_to_py_list(self.element.FindAll(tree_scope, condition))
        ]

    def find_all_by_x_path(self, x_path: str) -> List[AutomationElement]:
        """Finds all items which match the given xpath.

        :param x_path: Element XPath
        :return: The found elements or an empty list if no elements were found.
        """
        return [
            self.return_automation_element(_)
            for _ in TypeConverter.cast_to_py_list(self.element.FindAllByXPath(x_path))
        ]

    def find_all_children(self, condition: Optional[Any]) -> List[AutomationElement]:
        """Finds all children with the condition.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [
            self.return_automation_element(_)
            for _ in TypeConverter.cast_to_py_list(self.element.FindAllChildren(condition))
        ]

    def find_all_descendants(self, condition: Optional[Any]) -> List[AutomationElement]:
        """Finds all descendants with the condition.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [
            self.return_automation_element(_)
            for _ in TypeConverter.cast_to_py_list(self.element.FindAllDescendants(condition))
        ]

    def find_all_nested(self, condition: Optional[Any]) -> List[AutomationElement]:
        """Finds all elements by iterating thru all conditions.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [
            self.return_automation_element(_)
            for _ in TypeConverter.cast_to_py_list(self.element.FindAllNested(condition))
        ]

    def find_all_with_options(
        self, tree_scope: Any, condition: Optional[Any], traversal_options: Any, root: Any
    ) -> List[AutomationElement]:
        """Find all matching elements in the specified order.

        :param tree_scope: A combination of values specifying the scope of the search.
        :param condition: A condition that represents the criteria to match.
        :param traversal_options: Value specifying the tree navigation order.
        :param root: An element with which to begin the search.
        :return: The found elements or an empty list if no elements were found.
        """
        return [
            self.return_automation_element(_)
            for _ in TypeConverter.cast_to_py_list(
                self.element.FindAllWithOptions(tree_scope, condition, traversal_options, root)
            )
        ]

    def find_at(self, tree_scope: Any, index: int, condition: Optional[Any]) -> AutomationElement:
        """Finds the element with the given index with the given condition.

        :param tree_scope: The scope to search.
        :param index: The index of the element to return (0-based).
        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return self.return_automation_element(self.element.FindAt(tree_scope, index, condition))

    def find_child_at(self, index: int, condition: Optional[Any]) -> AutomationElement:
        """Finds the child at the given position with the condition.

        :param index: The index of the child to find.
        :param condition: The condition.
        :return: The found element or null if no element was found.
        """
        return self.return_automation_element(self.element.FindChildAt(index, condition))

    def find_first(self, tree_scope: Any, condition: Optional[Any]) -> AutomationElement:
        """Finds the first element in the given scope with the given condition.

        :param tree_scope: The scope to search.
        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return self.return_automation_element(self.element.FindFirst(tree_scope, condition))

    def find_first_by_x_path(self, x_path: str) -> AutomationElement:
        """Finds for the first item which matches the given xpath.

        :param x_path: XPath to the element
        :return: The found element or null if no element was found.
        """
        return self.return_automation_element(self.element.FindFirstByXPath(x_path))

    def find_first_child(self, condition: Optional[Any]) -> AutomationElement:
        """Finds the first child.

        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return self.return_automation_element(self.element.FindFirstChild(condition))

    def find_first_descendant(self, condition: Optional[Any]) -> AutomationElement:
        """Finds the first descendant.

        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return self.return_automation_element(self.element.FindFirstDescendant(condition))

    def find_first_nested(self, conditions: Optional[Any]) -> AutomationElement:
        """Finds the first element by iterating thru all conditions.

        :param conditions: The conditions to use.
        :return: The found element or null if no element was found.
        """
        return self.return_automation_element(self.element.FindFirstNested(conditions))

    def find_first_with_options(
        self, tree_scope: Any, condition: Optional[Any], traversal_options: Any, root: Any
    ) -> AutomationElement:
        """Find first matching element in the specified order.

        :param tree_scope: A combination of values specifying the scope of the search.
        :param condition: A condition that represents the criteria to match.
        :param traversal_options: Value specifying the tree navigation order.
        :param root: An element with which to begin the search.
        :return: The found element or null if no element was found.
        """
        return self.return_automation_element(
            self.element.FindFirstWithOptions(tree_scope, condition, traversal_options, root)
        )

    def focus(self) -> None:
        """Sets the focus to a control. If the control is a window, brings it to the foreground."""
        self.element.Focus()

    def focus_native(self) -> None:
        """Sets the focus by using the Win32 SetFocus() method."""
        self.element.FocusNative()

    def get_clickable_point(self) -> Any:
        """Gets a clickable point of the element.

        :return: Clickable point object
        """
        return self.element.GetClickablePoint()

    def get_current_metadata_value(self, property_id: Any, meta_data_id: int) -> Any:
        """Gets metadata from the UI Automation element that indicates how the information should be interpreted.

        :param property_id: The property to retrieve.
        :param meta_data_id: Specifies the type of metadata to retrieve.
        :return: The metadata.
        """
        return self.element.GetCurrentMetadataValue(property_id, meta_data_id)

    def get_supported_patterns(self) -> Any:
        """Gets the available patterns for an element via properties.

        :return: Available patterns for an element via properties.
        """
        return self.element.GetSupportedPatterns()

    def get_supported_patterns_direct(self) -> Any:
        """Gets the available patterns for an element via UIA method. Does not work with cached elements and might be unreliable.

        :return: Available patterns
        """
        return self.element.GetSupportedPatternsDirect()

    def get_supported_properties_direct(self) -> Any:
        """Gets the available properties for an element via UIA method. Does not work with cached elements and might be unreliable.

        :return: Available properties
        """
        return self.element.GetSupportedPropertiesDirect()

    def is_pattern_supported(self, pattern_id: Any) -> bool:
        """Checks if the given pattern is available for the element via properties.

        :param pattern_id: Pattern
        :return: True if supported else False
        """
        return self.element.IsPatternSupported(pattern_id)

    def is_pattern_supported_direct(self, pattern_id: Any) -> bool:
        """Checks if the given pattern is available for the element via UIA method. Does not work with cached elements and might be unreliable.

        :param pattern_id: Pattern ID
        :return: True if supported else False
        """
        return self.element.IsPatternSupportedDirect(pattern_id)

    def is_property_supported_direct(self, property: Any) -> bool:
        """Method to check if the element supports the given property via UIA method. Does not work with cached elements and might be unreliable.

        :param pattern_id: Pattern ID
        :return: True if supported else False
        """
        return self.element.IsPropertySupportedDirect(property)

    def register_active_text_position_changed_event(self, tree_scope: Any, action: Any) -> Any:
        """Registers a active text position changed event.

        :param tree_scope: Treescope object
        :param action: Action object
        :return: Registered event
        """
        # return self.element.RegisterActiveTextPositionChangedEvent(tree_scope, action)
        pass

    def register_automation_event(self, event: Any, tree_scope: Any, action: Any) -> Any:
        """Registers the given automation event.

        :param event: Event object
        :param tree_scope: Treescope object
        :param action: Action object
        :return: Registered event
        """
        # return self.element.RegisterAutomationEvent(event, tree_scope, action)
        pass

    def register_notification_event(self) -> Any:
        """Registers a notification event.

        :return: None
        """
        # self.element.RegisterNotificationEvent
        pass

    def register_property_changed_event(self) -> Any:
        """Registers a property changed event with the given property.

        :return: None
        """
        # self.element.RegisterPropertyChangedEvent
        pass

    def register_structure_changed_event(self) -> Any:
        """Registers a structure changed event.

        :return: None
        """
        # self.element.RegisterStructureChangedEvent
        pass

    def register_text_edit_text_changed_event_handler(self) -> Any:
        """Registers a text edit text changed event.

        :return: None
        """
        # self.element.RegisterTextEditTextChangedEventHandler
        pass

    def right_click(self, move_mouse: bool = False) -> None:
        """Performs a right click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly (true) or instantly (false)., defaults to False
        """
        self.element.RightClick(move_mouse)

    def right_double_click(self, move_mouse: bool = False) -> None:
        """Performs a double right click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly (true) or instantly (false)., defaults to False
        """
        self.element.RightDoubleClick(move_mouse)

    def set_focus(self) -> None:
        """Sets the focus to a control. If the control is a window, brings it to the foreground."""
        self.element.SetFocus()

    def set_foreground(self) -> None:
        """Brings a window to the foreground."""
        self.element.SetForeground()

    def to_string(self) -> str:
        """Overrides the string representation of the element with something useful.

        :return: String object
        """
        return self.element.ToString()

    def as_button(self) -> Button:
        """Returns element as Button

        :return: Button object
        """
        return Button(self.element)


class Button(AutomationElement):
    """Class to interact with a button element.

    :param AutomationElement: AutomationElement base object
    """

    def __init__(self, element: Any) -> None:
        """Creates a Button element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_button(element)

    def invoke(self) -> None:
        """Invokes the element."""
        self.element.Invoke()


class Calendar(AutomationElement):
    """Class to interact with a calendar element. Not supported for Windows Forms calendar.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a Calendar element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_calendar(element)
        self.selected_dates = self.element.SelectedDates

    def select_date(self, date: Any) -> None:
        """Deselects other selected dates and selects the specified date.

        :param date: Date object
        """
        self.element.SelectDate(arrow.get(date).date())

    def select_range(self, dates: List[Any]) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method deselects other selected dates and selects the specified range.
        /// For any other type of SelectionMode it deselects other selected dates and selects only the last date in the range.
        /// For Win32 multiple selection calendar the "dates" parameter should contain two dates, the first and the last date of the range to be selected.
        /// For Win32 single selection calendar this method selects only the second date from the "dates" array.
        /// For WPF calendar all dates should be specified in the "dates" parameter, not only the first and the last date of the range.

        :param dates: Date ranges
        """
        self.element.SelectRange(dates)

    def add_to_selection(self, date: Any) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method adds the specified date to current selection.
        /// For any other type of SelectionMode it deselects other selected dates and selects the specified date.
        /// This method is supported only for WPF calendar.

        :param date: Date object
        """
        self.element.AddToSelection(arrow.get(date).date())

    def add_range_to_selection(self, dates: List[Any]) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method adds the specified range to current selection.
        /// For any other type of SelectionMode it deselects other selected dates and selects only the last date in the range.
        /// This method is supported only for WPF calendar.

        :param dates: Date ranges
        """
        self.element.AddRangeToSelection(dates)


class CheckBox(AutomationElement):
    """Class to interact with a checkbox element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a ="CheckBox element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_check_box(element)
        self.toggle_state: Any = self.element.ToggleState  # TODO: Check if this ia a method/property
        self.is_toggled: bool = self.element.IsToggled
        self.is_checked: bool = self.element.IsChecked  #   Gets or sets if the checkbox is checked.
        self.text: str = self.element.Text  #   Gets the text of the element.

    def get_toogle_state(self) -> Any:
        """Gets the current toggle state.

        :return: Current toggle state
        """
        return self.element.get_ToggleState()

    def set_toogle_state(self) -> None:
        """Sets the current toggle state."""
        self.element.set_ToggleState()

    def get_is_toggled(self) -> Any:
        """Gets if the element is toggled.

        :return: Element toggled state
        """
        return self.element.get_IsToggled()

    def set_is_toggled(self) -> None:
        """Sets if the element is toggled."""
        self.element.set_IsToggled()

    def get_is_checked(self) -> Any:
        """Gets if the checkbox is checked.

        :return: Checkbox checked state
        """
        return self.element.get_IsChecked()

    def set_is_checked(self) -> None:
        """Sets if the checkbox is checked."""
        self.element.set_IsChecked()


class ComboBox(AutomationElement):
    """Class to interact with a combobox element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a ComboBoxelement.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_combo_box(element)
        self.editable_text: str = (
            self.element.EditableText
        )  #   The text of the editable element inside the combobox. Only works if the combobox is editable.
        self.is_editable: bool = self.element.IsEditable  #   Flag which indicates, if the combobox is editable or not.
        self.is_read_only: bool = (
            self.element.IsReadOnly
        )  #   Flag which indicates, if the combobox is read-only or not.
        self.value: str = self.element.Value  #   Getter / setter for the selected value.
        self.selected_items: List[str] = TypeConverter.cast_to_py_list(
            self.element.SelectedItems
        )  #   Gets all selected items.
        self.selected_item: str = self.element.SelectedItem  #   Gets the first selected item or null otherwise.
        self.items: List[str] = TypeConverter.cast_to_py_list(self.element.Items)  #   Gets all items.
        self.expand_collapse_state: Any = (
            self.element.ExpandCollapseState
        )  #   Gets the ExpandCollapseStateof the element.

    def expand(self) -> None:
        """Expands the element."""
        self.element.Expand()

    def collapse(self) -> None:
        """Collapses the element."""
        self.element.Collapse()

    def select(self, value: Union[int, str]) -> Any:
        """Select an item by index/the first item which matches the given text..

        :param value: Index value/The text to search for
        :return: The first found item or null if no item matches.
        """
        return self.element.Select(value)


class DataGridViewHeader:
    """Class to interact with a WinForms DataGridView header."""

    def __init__(self, header: Any) -> None:
        """Creates a DataGridViewHeaderelement.

        :param header: Header element of DataGridView object
        """
        self.header = header
        self.columns: List[str] = TypeConverter.cast_to_py_list(self.header.Columns)  #   Gets the header items.


class DataGridViewRow:
    """Class to interact with a WinForms DataGridView row."""

    def __init__(self, row: Any) -> None:
        """Creates a DataGridViewRow element.

        :param row: Row object
        """
        self.row = row
        self.cells: List[str] = self.row.Cells  #   Gets all cells.


class DataGridView(AutomationElement):
    """Class to interact with a WinForms DataGridView

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a DataGridViewelement.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_data_grid_view(element)
        self.has_add_row: bool = (
            self.element.HasAddRow
        )  #   Flag to indicate if the grid has the "Add New Item" row or not. This needs to be set as FlaUI cannot find out if this is the case or not.
        self.header: DataGridViewHeader = DataGridViewHeader(
            self.element.Header
        )  #   Gets the header element or null if the header is disabled.
        self.rows: List[DataGridViewRow] = [
            DataGridViewRow(_) for _ in TypeConverter.cast_to_py_list(self.element.Rows)
        ]  #   Gets all the data rows.


class DateTimePicker(AutomationElement):
    """Class to interact with a DateTimePicker element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a DateTimePickerelement.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_date_time_picker(element)
        self.selected_date = (
            self.element.SelectedDate
        )  #   For Win32, setting SelectedDate to null will uncheck the DateTimePicker control and disable it. Also for Win32, if the control is unchecked then SelectedDate will return null.


class Grid(AutomationElement):
    """Element for grids and tables.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a grid object from a given element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_grid(element)
        self.row_count: int = self.element.RowCount  #   Gets the total row count.
        self.column_count: int = self.element.ColumnCount  #   Gets the total column count.
        self.column_headers: List[AutomationElement] = [
            self.return_automation_element(_) for _ in TypeConverter.cast_to_py_list(self.element.ColumnHeaders)
        ]  #   Gets all column header elements.
        self.row_headers: List[AutomationElement] = [
            self.return_automation_element(_) for _ in TypeConverter.cast_to_py_list(self.element.RowHeaders)
        ]  #   Gets all row header elements.
        self.row_or_column_major: Any = (
            self.element.RowOrColumnMajor
        )  #   Gets whether the data should be read primarily by row or by column.
        self.header: Any = self.element.Header  #   Gets the header item
        self.rows: List[Any] = [
            _ for _ in TypeConverter.cast_to_py_list(self.element.Rows)
        ]  #   Returns the rows which are currently visible to UIA. Might not be the full list (eg. in virtualized lists)! Use GetRowByIndex to make sure to get the correct row.
        self.selected_items: List[Any] = [
            _ for _ in TypeConverter.cast_to_py_list(self.element.SelectedItems)
        ]  #   Gets all selected items.
        self.selected_item: Any = self.element.SelectedItem  #   Gets the first selected item or null otherwise.

    def select(self, row_index: int) -> Any:
        """Select a row by index.

        :param row_index: None
        :return: Any
        """
        return self.element.Select(row_index)

    def add_to_selection(
        self, row_index: Optional[int] = None, column_index: Optional[int] = None, text_to_find: Optional[str] = None
    ) -> Any:
        """Add a row to the selection by index or by text in the given column.

        :param row_index: Row index
        :param columnIndex: Column index
        :param textToFind: Text to find
        :return: Any
        """
        if column_index and text_to_find:
            return self.element.AddToSelection(column_index, text_to_find)
        else:
            return self.element.AddToSelection(row_index)

    def remove_from_selection(
        self, row_index: Optional[int] = None, column_index: Optional[int] = None, text_to_find: Optional[str] = None
    ) -> Any:
        """Remove a row to the selection by index or by text in the given column.

        :param row_index: Row index
        :param columnIndex: Column index
        :param textToFind: Text to find
        :return: Any
        """
        if column_index and text_to_find:
            return self.element.RemoveFromSelection(column_index, text_to_find)
        else:
            return self.element.RemoveFromSelection(row_index)

    def get_row_by_index(self, row_index: int) -> Any:
        """Get a row by index.

        :param row_index: Row index
        :return: Any
        """
        return self.element.GetRowByIndex(row_index)

    def get_row_by_value(self, column_index: int, value: str) -> Any:
        """Get a row by text in the given column.

        :param column_index: Column index
        :param value: Value
        :return: Any
        """
        return self.element.GetRowByValue(column_index, value)

    def get_rows_by_value(self, column_index: int, value: str, max_items: int = 0) -> List[Any]:
        """Get all rows where the value of the given column matches the given value.

        :param column_index: The column index to check.
        :param value: The value to check.
        :param max_items: Maximum numbers of items to return, 0 for all, defaults to 0
        :return: List of found rows.
        """
        return TypeConverter.cast_to_py_list(self.element.GetRowsByValue(column_index, value, max_items))


class Label(AutomationElement):
    """Class to interact with a label element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a Label element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_label(element)
        self.text: str = self.element.Text


class ListBox(AutomationElement):
    """Class to interact with a list box element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a ListBox element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_list_box(element)
        self.items: List[ListBoxItem] = TypeConverter.cast_to_py_list(
            self.element.Items
        )  #   Returns all the list box items
        self.selected_item: ListBoxItem = self.element.SelectedItem  #   Gets the first selected item or null otherwise.
        self.selected_items: ListBoxItem = self.element.SelectedItems  #   Gets all selected items.

    def select(self, value: Union[str, int]) -> ListBoxItem:
        """Selects an item by index.

        :param value: Text to select/Index to select by
        :return: ListBoxItem
        """
        return self.element.Select(value)

    def add_to_selection(self, value: Union[str, int]) -> ListBoxItem:
        """Add a row to the selection by index/by text.

        :param value: Text/Index
        :return: ListBoxItem
        """
        return self.element.AddToSelection(value)

    def remove_from_selection(self, value: Union[str, int]) -> ListBoxItem:
        """Remove a row to the selection by index/by text.

        :param value: Text/Index
        :return: ListBoxItem
        """
        return self.element.RemoveFromSelection(value)


class ListBoxItem(AutomationElement):
    """Class to interact with a list box item element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a ListBoxItem element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_list_box_item(element)
        self.is_checked: bool = (
            self.element.IsChecked
        )  #   Gets or sets if the listbox item is checked, if checking is supported
        self.text: str = self.element.Text  #   Gets the text of the element.

    def scroll_into_view(self) -> ListBoxItem:
        """Scrolls the element into view.

        :return: ListBoxItem
        """
        return self.element.ScrollIntoView()


class Menu(AutomationElement):
    """Class to interact with a menu or menubar element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a Menu element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_menu(element)
        self.items = self.element.Items  #   Gets all MenuItem which are inside this element.
        self.is_win_menu = (
            self.element.IsWin32Menu
        )  #   Flag to indicate if the menu is a Win32 menu because that one needs special handling


class MenuItem(AutomationElement):
    """Class to interact with a menu item element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a MenuItem element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_menu_item(element)
        self.is_win_menu = (
            self.element.IsWin32Menu
        )  #   Flag to indicate if the containing menu is a Win32 menu because that one needs special handling
        self.text = self.element.Text  #   Gets the text of the element.
        self.is_checked = (
            self.element.IsChecked
        )  #   Gets or sets if a menu item is checked or unchecked, if checking is supported. For some applications, like WPF, setting this property doesn't execute the action that happens when a user clicks the menu item, only the checked state is changed. For WPF and Windows Forms applications, if you want to execute the action too, you need to use Invoke() method.

    def collapse(self) -> MenuItem:
        """Collapses the element

        :return: MenuItem element
        """

        return self.element.Collapse()

    def expand(self) -> MenuItem:
        """Expands the element

        :return: MenuItem element
        """

        return self.element.Expand()

    def invoke(self) -> MenuItem:
        """Invokes the element

        :return: MenuItem element
        """

        return self.element.Invoke()


class MenuItems:
    """Represents a list of MenuItem elements."""

    def __init__(self, elements: List[Any]) -> None:
        """Creates a MenuItem element.

        :param elements: List of MenuItem objects
        """
        self.elements = elements
        self.length = len(self.elements)  #   Gets the number of elements in the list.

    def this(self, text: str) -> MenuItem:
        """Gets the MenuItem with the given text.

        :param text: Given text
        :return: MenuItem for matched text
        """
        return [_ for _ in self.elements if _.text == text][0]


class ProgressBar(AutomationElement):
    """Class to interact with a progressbar element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a ProgressBar element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_progress_bar(element)
        self.range_value_pattern: Any = self.element.RangeValuePattern  #   Pattern object for the IRangeValuePattern.
        self.minimum: float = self.element.Minimum  #   Gets the minimum value.
        self.maximum: float = self.element.Maximum  #   Gets the maximum value.
        self.value: float = self.element.Value  #   Gets the current value.


class RadioButton(AutomationElement):
    """Class to interact with a radiobutton element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a RadioButton element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_radio_button(element)
        self.is_checked: bool = self.element.IsChecked  #   Flag to get/set the selection of this element.


class Slider(AutomationElement):
    """Class to interact with a slider element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a Slider element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_slider(element)
        self.minimum: float = self.element.Minimum  #   The minimum value.
        self.maximum: float = self.element.Maximum  #   The maximum value.
        self.small_change: float = self.element.SmallChange  #   The value of a small change.
        self.large_change: float = self.element.LargeChange  #   The value of a large change.
        self.large_increase_button: Any = (
            self.element.LargeIncreaseButton
        )  #   The button element used to perform a large increment.
        self.large_decrease_button: Any = (
            self.element.LargeDecreaseButton
        )  #   The button element used to perform a large decrement.
        self.thumb: Any = self.element.Thumb  #   The element used to drag.
        self.is_only_value: bool = (
            self.element.IsOnlyValue
        )  #   Flag which indicates if the Slider supports range values (min->max) or only values (0-100). Only values are for example used when combining UIA3 and WinForms applications.
        self.value: float = self.element.Value  #   Gets or sets the current value.

    def small_increment(self) -> None:
        """Performs a small increment."""
        self.element.SmallIncrement()

    def small_decrement(self) -> None:
        """Performs a small decrement."""
        self.element.SmallDecrement()

    def large_increment(self) -> None:
        """Performs a large increment."""
        self.element.LargeIncrement()

    def large_decrement(self) -> None:
        """Performs a large decrement."""
        self.element.LargeDecrement()

    def get_large_increase_button(self) -> Any:
        """Gets large increase button

        :return: Button element
        """
        return self.element.GetLargeIncreaseButton()

    def get_large_decrease_button(self) -> Any:
        """Gets large decrease button

        :return: Button element
        """
        return self.element.GetLargeDecreaseButton()


class Spinner(AutomationElement):
    """Class to interact with a WinForms spinner element.

    :param AutomationElement: AutomationElement base
    """

    def __init__(self, element: Any) -> None:
        """Creates a Spinner element.

        :param element: Element object
        """
        super().__init__(element)
        self.element = AutomationElementExtensions.as_spinner(element)
        self.minimum: float = self.element.Minimum  #   The minimum value.
        self.maximum: float = self.element.Maximum  #   The maximum value.
        self.small_change: float = self.element.SmallChange  #   The value of a small change.
        self.increase_button: Any = (
            self.element.IncreaseButton
        )  #   The button element used to perform a large increment.
        self.decrease_button: Any = (
            self.element.DecreaseButton
        )  #   The button element used to perform a large decrement.
        self.is_only_value: bool = (
            self.element.IsOnlyValue
        )  #   Flag which indicates if the Spinner supports range values (min->max) or only values (0-100). Only values are for example used when combining UIA3 and WinForms applications.
        self.value: float = self.element.Value  #   Gets or sets the current value.

    def increment(self):
        """Performs increment."""
        self.element.Increment()

    def decrement(self):
        """Performs decrement."""
        self.element.Decrement()

    def get_increase_button(self) -> Any:
        """Method to get the increase button.

        :return: Button
        """
        self.element.GetIncreaseButton()

    def get_decrease_button(self) -> Any:
        """Method to get the decrease button.

        :return: Button
        """
        self.element.GetDecreaseButton()
