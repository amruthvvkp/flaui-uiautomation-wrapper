"""
Wrapper objects for AutomationElement class.
"""

from __future__ import annotations

import abc
from typing import Any, List, Optional, Union

import arrow
from pydantic import BaseModel, Field, parse_obj_as, validator

from flaui.lib.collections import TypeCast
from flaui.wrappers.core.automation_element_extensions import AutomationElementExtensions


class ElementBase(BaseModel, abc.ABC):
    """Automation Element base abstract class"""

    raw_element: Any = Field(
        ..., title="Automation Element", description="Contains the C# automation element in raw form"
    )  # Consider making this a private property

    @property
    def actual_height(self) -> int:
        """The height of this element

        :return: Actual Height
        """
        return self.raw_element.ActualHeight

    @property
    def actual_width(self) -> int:
        """The width of this element

        :return: Actual Width
        """
        return self.raw_element.ActualWidth

    @property
    def automation_id(self) -> str:
        """The automation id of the element

        :return: Automation ID
        """
        return self.raw_element.AutomationId

    @property
    def automation_type(self) -> Any:
        """The current AutomationType for this element

        :return: Automation Type
        """
        return self.raw_element.AutomationType

    @property
    def bounding_rectangle(self) -> Any:
        """The bounding rectangle of this element

        :return: Bounding Rectangle
        """
        return self.raw_element.BoundingRectangle

    @property
    def cached_children(self) -> Any:
        """Gets the cached children for this element

        :return: Cached Children
        """
        return self.raw_element.CachedChildren

    @property
    def cached_parent(self) -> Any:
        """Gets the cached parent for this element

        :return: Cached Parent
        """
        return self.raw_element.CachedParent

    @property
    def class_name(self) -> str:
        """The class name of the element

        :return: Class Name
        """
        return self.raw_element.ClassName

    @property
    def condition_factory(self) -> Any:
        """Shortcut to the condition factory for the current automation, Returns condition factory object

        :return: Condition Factory
        """
        return self.raw_element.ConditionFactory

    @property
    def control_type(self) -> str:
        """The control type of the element

        :return: Control type
        """
        return self.raw_element.ControlType

    @property
    def framework_automation_element(self) -> Any:
        """Object which contains the native wrapper element (UIA2 or UIA3) for this element

        :return: Framework automation element
        """
        return self.raw_element.FrameworkAutomationElement

    @property
    def framework_type(self) -> Any:
        """The direct framework type of the element. Results in 'FrameworkType.Unknown' if it couldn't be resolved

        :return: Framework Type
        """
        return self.raw_element.FrameworkType

    @property
    def help_text(self) -> str:
        """The help text of this element

        :return: Help text
        """
        return self.raw_element.HelpText

    @property
    def is_available(self) -> bool:
        """A flag that indicates if the element is still available. Can be false if the element is already unloaded from the UI

        :return: Element availability state
        """
        return self.raw_element.IsAvailable

    @property
    def is_enabled(self) -> bool:
        """Flag if the element is enabled or not

        :return: Element enabled state
        """
        return self.raw_element.IsEnabled

    @property
    def is_offscreen(self) -> bool:
        """Flag if the element off-screen or on-screen(visible)

        :return: Offscreen flag
        """
        return self.raw_element.IsOffscreen

    @property
    def name(self) -> str:
        """The name of the element

        :return: Element name
        """
        return self.raw_element.Name

    @property
    def parent(self) -> Any:
        """Get the parent AutomationElement

        :return: Parent
        """
        return self.raw_element.Parent

    @property
    def patterns(self) -> Any:
        """Standard UIA patterns of this element

        :return: UIA Patterns
        """
        return self.raw_element.Patterns

    @property
    def properties(self) -> Any:
        """Standard UIA properties of this element

        :return: UIA Properties
        """
        return self.raw_element.Properties

    # TODO: Get actual ControlType, ConditionalFactory class, BoundingRectangle object


class AutomationElement(ElementBase):
    """UI element which can be used in automation"""

    def capture(self) -> Any:
        """Captures the object as screenshot in Bitmap format.

        :return: Captured element image Bitmap object
        """
        return self.raw_element.Capture()

    def capture_to_file(self, file_path: str) -> None:
        """Captures the object as screenshot directly into the given file.

        :param file_path: The filepath where the screenshot should be saved.
        :return: None
        """
        self.raw_element.CaptureToFile(file_path)

    def click(self, move_mouse: bool = False) -> None:
        """Performs a left click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly(True) or instantly(False), defaults to False
        """
        self.raw_element.Click(move_mouse)

    def double_click(self, move_mouse: bool = False) -> None:
        """Performs a double left click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly(True) or instantly(False), defaults to False
        """
        self.raw_element.DoubleClick(move_mouse)

    def find_all(self, tree_scope: Any, condition: Optional[Any]) -> List[AutomationElement]:
        """Finds all children with the condition.

        :aram tree_scope: Treescope object
        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAll(tree_scope, condition)]

    def find_all_by_x_path(self, x_path: str) -> List[AutomationElement]:
        """Finds all items which match the given xpath.

        :param x_path: Element XPath
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllByXPath(x_path)]

    def find_all_children(self, condition: Optional[Any]) -> List[AutomationElement]:
        """Finds all children with the condition.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllChildren(condition)]

    def find_all_descendants(self, condition: Optional[Any]) -> List[AutomationElement]:
        """Finds all descendants with the condition.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllDescendants(condition)]

    def find_all_nested(self, condition: Optional[Any]) -> List[AutomationElement]:
        """Finds all elements by iterating thru all conditions.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllNested(condition)]

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
            AutomationElement(raw_element=_)
            for _ in self.raw_element.FindAllWithOptions(tree_scope, condition, traversal_options, root)
        ]

    def find_at(self, tree_scope: Any, index: int, condition: Optional[Any]) -> AutomationElement:
        """Finds the element with the given index with the given condition.

        :param tree_scope: The scope to search.
        :param index: The index of the element to return (0-based).
        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindAt(tree_scope, index, condition))

    def find_child_at(self, index: int, condition: Optional[Any]) -> AutomationElement:
        """Finds the child at the given position with the condition.

        :param index: The index of the child to find.
        :param condition: The condition.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindChildAt(index, condition))

    def find_first(self, tree_scope: Any, condition: Optional[Any]) -> AutomationElement:
        """Finds the first element in the given scope with the given condition.

        :param tree_scope: The scope to search.
        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirst(tree_scope, condition))

    def find_first_by_x_path(self, x_path: str) -> AutomationElement:
        """Finds for the first item which matches the given xpath.

        :param x_path: XPath to the element
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirstByXPath(x_path))

    def find_first_child(self, condition: Optional[Any]) -> AutomationElement:
        """Finds the first child.

        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirstChild(condition))

    def find_first_descendant(self, condition: Optional[Any]) -> AutomationElement:
        """Finds the first descendant.

        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirstDescendant(condition))

    def find_first_nested(self, conditions: Optional[Any]) -> AutomationElement:
        """Finds the first element by iterating thru all conditions.

        :param conditions: The conditions to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirstNested(conditions))

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
        return AutomationElement(
            raw_element=self.raw_element.FindFirstWithOptions(tree_scope, condition, traversal_options, root)
        )

    def focus(self) -> None:
        """Sets the focus to a control. If the control is a window, brings it to the foreground"""
        self.raw_element.Focus()

    def focus_native(self) -> None:
        """Sets the focus by using the Win32 SetFocus() method"""
        self.raw_element.FocusNative()

    def get_clickable_point(self) -> Any:
        """Gets a clickable point of the element.

        :return: Clickable point object
        """
        return self.raw_element.GetClickablePoint()

    def get_current_metadata_value(self, property_id: Any, meta_data_id: int) -> Any:
        """Gets metadata from the UI Automation element that indicates how the information should be interpreted.

        :param property_id: The property to retrieve.
        :param meta_data_id: Specifies the type of metadata to retrieve.
        :return: The metadata.
        """
        return self.raw_element.GetCurrentMetadataValue(property_id, meta_data_id)

    def get_supported_patterns(self) -> Any:
        """Gets the available patterns for an element via properties.

        :return: Available patterns for an element via properties.
        """
        return TypeCast.py_list(self.raw_element.GetSupportedPatterns())

    def get_supported_patterns_direct(self) -> Any:
        """Gets the available patterns for an element via UIA method. Does not work with cached elements and might be unreliable.

        :return: Available patterns
        """
        return TypeCast.py_list(self.raw_element.GetSupportedPatternsDirect())

    def get_supported_properties_direct(self) -> Any:
        """Gets the available properties for an element via UIA method. Does not work with cached elements and might be unreliable.

        :return: Available properties
        """
        return TypeCast.py_list(self.raw_element.GetSupportedPropertiesDirect())

    def is_pattern_supported(self, pattern_id: Any) -> bool:
        """Checks if the given pattern is available for the element via properties.

        :param pattern_id: Pattern
        :return: True if supported else False
        """
        return self.raw_element.IsPatternSupported(pattern_id)

    def is_pattern_supported_direct(self, pattern_id: Any) -> bool:
        """Checks if the given pattern is available for the element via UIA method. Does not work with cached elements and might be unreliable.

        :param pattern_id: Pattern ID
        :return: True if supported else False
        """
        return self.raw_element.IsPatternSupportedDirect(pattern_id)

    def is_property_supported_direct(self, property: Any) -> bool:
        """Method to check if the element supports the given property via UIA method. Does not work with cached elements and might be unreliable.

        :param pattern_id: Pattern ID
        :return: True if supported else False
        """
        return self.raw_element.IsPropertySupportedDirect(property)

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
        self.raw_element.RightClick(move_mouse)

    def right_double_click(self, move_mouse: bool = False) -> None:
        """Performs a double right click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly (true) or instantly (false)., defaults to False
        """
        self.raw_element.RightDoubleClick(move_mouse)

    def set_focus(self) -> None:
        """Sets the focus to a control. If the control is a window, brings it to the foreground"""
        self.raw_element.SetFocus()

    def set_foreground(self) -> None:
        """Brings a window to the foreground"""
        self.raw_element.SetForeground()

    def to_string(self) -> str:
        """Overrides the string representation of the element with something useful.

        :return: String object
        """
        return self.raw_element.ToString()

    # def as_button(self) -> Button:
    #     """Returns element as Button

    #     :return: Button object
    #     """
    #     return Button(element=self.element)


# class Button(AutomationElement):
#     """Class to interact with a button element"""

#     @validator("element")
#     def build_element(cls, v) -> Any:
#         return AutomationElementExtensions.as_button(v)

#     def invoke(self) -> None:
#         """Invokes the element
#         """
#         self.element.Invoke()


# class Calendar(AutomationElement):
#     """Class to interact with a calendar element. Not supported for Windows Forms calendar"""

#     @property
#     def selected_dates(self) -> Any:
#         """Gets the selected dates in the calendar. For Win32 multiple selection calendar the returned array has two dates, the first date and the last date of the selected range. For WPF calendar the returned array contains all selected dates

#         :return: Selected dates
#         """
#         return self.element.SelectedDates

#     @validator("element")
#     def build_element(cls, v) -> Any:
#         return AutomationElementExtensions.as_calendar(v)

#     def select_date(self, date: Any) -> None:
#         """Deselects other selected dates and selects the specified date.

#         :param date: Date object
#         """
#         self.element.SelectDate(arrow.get(date).date())

#     def select_range(self, dates: List[Any]) -> None:
#         """For WPF calendar with SelectionMode="MultipleRange" this method deselects other selected dates and selects the specified range.
#         /// For any other type of SelectionMode it deselects other selected dates and selects only the last date in the range.
#         /// For Win32 multiple selection calendar the "dates" parameter should contain two dates, the first and the last date of the range to be selected.
#         /// For Win32 single selection calendar this method selects only the second date from the "dates" array.
#         /// For WPF calendar all dates should be specified in the "dates" parameter, not only the first and the last date of the range.

#         :param dates: Date ranges
#         """
#         self.element.SelectRange(dates)

#     def add_to_selection(self, date: Any) -> None:
#         """For WPF calendar with SelectionMode="MultipleRange" this method adds the specified date to current selection.
#         /// For any other type of SelectionMode it deselects other selected dates and selects the specified date.
#         /// This method is supported only for WPF calendar.

#         :param date: Date object
#         """
#         self.element.AddToSelection(arrow.get(date).date())

#     def add_range_to_selection(self, dates: List[Any]) -> None:
#         """For WPF calendar with SelectionMode="MultipleRange" this method adds the specified range to current selection.
#         /// For any other type of SelectionMode it deselects other selected dates and selects only the last date in the range.
#         /// This method is supported only for WPF calendar.

#         :param dates: Date ranges
#         """
#         self.element.AddRangeToSelection(dates)


# class CheckBox(AutomationElement):
#     """Class to interact with a checkbox element"""

#     @property
#     def toggle_state(self) -> Any:
#         """The current toggle state

#         :return: Toggle state
#         """
#         return self.element.ToggleState  # TODO: Check if this ia a method/property

#     @property
#     def is_toggled(self) -> bool:
#         """Flag if the element is toggled

#         :return: Element toggled state
#         """
#         return self.element.IsToggled

#     @property
#     def is_checked(self) -> bool:
#         """Flag if the element is checked

#         :return: Element is checked
#         """
#         return self.element.IsChecked

#     @property
#     def text(self) -> str:
#         """Gets the text of the element

#         :return: Element text
#         """
#         return self.element.Text

#     @validator("element")
#     def build_element(cls, v) -> Any:
#         return AutomationElementExtensions.as_check_box(v)

#     def get_toggle_state(self) -> Any:
#         """Gets the current toggle state.

#         :return: Current toggle state
#         """
#         return self.element.get_ToggleState()

#     def set_toggle_state(self) -> None:
#         """Sets the current toggle state"""
#         self.element.set_ToggleState()

#     def get_is_toggled(self) -> Any:
#         """Gets if the element is toggled.

#         :return: Element toggled state
#         """
#         return self.element.get_IsToggled()

#     def set_is_toggled(self) -> None:
#         """Sets if the element is toggled"""
#         self.element.set_IsToggled()

#     def get_is_checked(self) -> Any:
#         """Gets if the checkbox is checked.

#         :return: Checkbox checked state
#         """
#         return self.element.get_IsChecked()

#     def set_is_checked(self) -> None:
#         """Sets if the checkbox is checked"""
#         self.element.set_IsChecked()


# class ComboBox(AutomationElement):
#     """Class to interact with a combobox element"""

#     @property
#     def editable_text(self) ->  str:
#         """The text of the editable element inside the combobox. Only works if the combobox is editable

#         :return: Editable text of the element
#         """
#         return self.element.EditableText

#     @property
#     def is_editable(self) -> bool:
#         """Flag which indicates, if the combobox is editable or not

#         :return: Is element editable
#         """
#         return self.element.IsEditable

#     @property
#     def is_read_only(self) -> bool:
#         """Flag which indicates, if the combobox is read-only or not

#         :return: Is element read-only
#         """
#         return self.element.IsReadOnly

#     @property
#     def value(self) -> str:
#         """Selected value of the Combobox element

#         :return: Element selected value
#         """
#         return self.element.Value

#     @property
#     def selected_items(self) -> List[str]:
#         """Gets all selected items

#         :return: Selected items
#         """
#         return TypeCast.py_list(self.element.SelectedItems)

#     @property
#     def selected_item(self) -> str:
#         """Gets the first selected item or null otherwise

#         :return: Selected item
#         """
#         return self.element.SelectedItem

#     @property
#     def items(self) -> List[str]:
#         """Gets all available items from the ComboBox element

#         :return: Item
#         """
#         return TypeCast.py_list(self.element.Items)

#     @property
#     def expand_collapse_state(self) -> Any:
#         """Gets the ExpandCollapseStateof the element

#         :return: Expand/Collapse state
#         """
#         return self.element.ExpandCollapseState

#     @validator("element")
#     def build_element(cls, v) -> Any:
#         return AutomationElementExtensions.as_combo_box(v)

#     def expand(self) -> None:
#         """Expands the element"""
#         self.element.Expand()

#     def collapse(self) -> None:
#         """Collapses the element"""
#         self.element.Collapse()

#     def select(self, value: Union[int, str]) -> Any:
#         """Select an item by index/the first item which matches the given text..

#         :param value: Index value/The text to search for
#         :return: The first found item or null if no item matches.
#         """
#         return self.element.Select(value)


# class DataGridViewHeader(BaseModel):
#     """Class to interact with a WinForms DataGridView header"""

#     header: Any
#     columns: List[str]


# class DataGridViewRow(BaseModel):
#     """Class to interact with a WinForms DataGridView row"""

#     row: Any
#     cells: List[str]


# class DataGridView(AutomationElement):
#     """Class to interact with a WinForms DataGridView"""

#     has_add_row: bool = Field(
#         None,
#         title="Has Add row",
#         description="Flag to indicate if the grid has the 'Add New Item' row or not. This needs to be set as FlaUI cannot find out if this is the case or not",
#     )
#     header: DataGridViewHeader = Field(
#         None, title="Header", description="Gets the header element or null if the header is disabled"
#     )
#     rows: List[DataGridViewRow] = Field(None, title="Rows", description="Gets all the data rows")

#     def __init__(self, *args, **kwargs):
#         """Creates a DataGridViewelement"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_data_grid_view(self.element)
#         self.has_add_row: bool = self.element.HasAddRow
#         self.header: DataGridViewHeader = DataGridViewHeader(
#             header=self.element.Header, columns=parse_obj_as(List[str], self.element.Header.Columns)
#         )
#         self.rows: List[DataGridViewRow] = [
#             DataGridViewRow(row=_, cells=_.Cells) for _ in TypeCast.py_list(self.element.Rows)
#         ]  # TODO: Test if parsing lis tof objects using parse_obj_as works


# class DateTimePicker(AutomationElement):
#     """Class to interact with a DateTimePicker element"""

#     selected_date: Any = Field(
#         None,
#         title="Selected date",
#         description="For Win32, setting SelectedDate to null will uncheck the DateTimePicker control and disable it. Also for Win32, if the control is unchecked then SelectedDate will return null",
#     )

#     def __init__(self, *args, **kwargs):
#         """Creates a DateTimePickerelement"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_date_time_picker(self.element)
#         self.selected_date = self.element.SelectedDate


# class Grid(AutomationElement):
#     """Element for grids and tables"""

#     row_count: int = Field(None, title="Row count", description="Gets the total row count")
#     column_count: int = Field(None, title="Column count", description="Gets the total column count")
#     column_headers: List[AutomationElement] = Field(
#         None, title="Column headers", description="Gets all column header elements"
#     )
#     row_headers: List[AutomationElement] = Field(None, title="Row headers", description="Gets all row header elements")
#     row_or_column_major: Any = Field(
#         None,
#         title="Data from Row or Column",
#         description="Gets whether the data should be read primarily by row or by column",
#     )
#     header: Any = Field(None, title="Header", description="Gets the header item")
#     rows: List[Any] = Field(
#         None,
#         title="Rows",
#         description="Returns the rows which are currently visible to UIA. Might not be the full list (eg. in virtualized lists)! Use GetRowByIndex to make sure to get the correct row",
#     )
#     selected_items: List[AutomationElement] = Field(
#         None, title="Selected items from the Grid", description="Gets all selected items from the Grid"
#     )
#     selected_item: Any = Field(
#         None,
#         title="Selected item from the Grid",
#         description="Gets the first selected item from the Grid or null otherwise",
#     )

#     def __init__(self, *args, **kwargs):
#         """Creates a grid object from a given element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_grid(self.element)
#         self.row_count: int = self.element.RowCount
#         self.column_count: int = self.element.ColumnCount
#         self.column_headers: List[AutomationElement] = [AutomationElement(element=_) for _ in self.element.ColumnHeaders)
#         self.row_headers: List[AutomationElement] = [AutomationElement(element=_) for _ in self.element.RowHeaders)
#         self.row_or_column_major: Any = self.element.RowOrColumnMajor
#         self.header: Any = self.element.Header
#         self.rows: List[Any] = [AutomationElement(element=_) for _ in self.element.Rows)
#         self.selected_items: List[AutomationElement] = [AutomationElement(element=_) for _ in self.element.SelectedItems)
#         self.selected_item: Any = self.element.SelectedItem

#     def select(self, row_index: int) -> Any:
#         """Select a row by index.

#         :param row_index: None
#         :return: Any
#         """
#         return self.element.Select(row_index)

#     def add_to_selection(
#         self, row_index: Optional[int] = None, column_index: Optional[int] = None, text_to_find: Optional[str] = None
#     ) -> Any:
#         """Add a row to the selection by index or by text in the given column.

#         :param row_index: Row index
#         :param columnIndex: Column index
#         :param textToFind: Text to find
#         :return: Any
#         """
#         if column_index and text_to_find:
#             return self.element.AddToSelection(column_index, text_to_find)
#         else:
#             return self.element.AddToSelection(row_index)

#     def remove_from_selection(
#         self, row_index: Optional[int] = None, column_index: Optional[int] = None, text_to_find: Optional[str] = None
#     ) -> Any:
#         """Remove a row to the selection by index or by text in the given column.

#         :param row_index: Row index
#         :param columnIndex: Column index
#         :param textToFind: Text to find
#         :return: Any
#         """
#         if column_index and text_to_find:
#             return self.element.RemoveFromSelection(column_index, text_to_find)
#         else:
#             return self.element.RemoveFromSelection(row_index)

#     def get_row_by_index(self, row_index: int) -> Any:
#         """Get a row by index.

#         :param row_index: Row index
#         :return: Any
#         """
#         return self.element.GetRowByIndex(row_index)

#     def get_row_by_value(self, column_index: int, value: str) -> Any:
#         """Get a row by text in the given column.

#         :param column_index: Column index
#         :param value: Value
#         :return: Any
#         """
#         return self.element.GetRowByValue(column_index, value)

#     def get_rows_by_value(self, column_index: int, value: str, max_items: int = 0) -> List[Any]:
#         """Get all rows where the value of the given column matches the given value.

#         :param column_index: The column index to check.
#         :param value: The value to check.
#         :param max_items: Maximum numbers of items to return, 0 for all, defaults to 0
#         :return: List of found rows.
#         """
#         return TypeCast.py_list(self.element.GetRowsByValue(column_index, value, max_items))


# class Label(AutomationElement):
#     """Class to interact with a label element"""

#     text: str = Field(None, title="Label text", description="Text from the label")

#     def __init__(self, *args, **kwargs):
#         """Creates a Label element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_label(self.element)
#         self.text: str = self.element.Text


# class ListBox(AutomationElement):
#     """Class to interact with a list box element"""

#     items: List[ListBoxItem] = Field(None, title="ListBox items", description="Returns all the list box items")
#     selected_item: ListBoxItem = Field(
#         None, title="Selected item", description="Gets the first selected item or null otherwise"
#     )
#     selected_items: List[ListBoxItem] = Field(None, title="Selected items", description="Gets all selected items")

#     def __init__(self, *args, **kwargs):
#         """Creates a ListBox element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_list_box(self.element)
#         self.items: List[ListBoxItem] = parse_obj_as(List[ListBoxItem], self.element.Items)
#         self.selected_item: ListBoxItem = parse_obj_as(ListBoxItem, self.element.SelectedItem)
#         self.selected_items: List[ListBoxItem] = parse_obj_as(List[ListBoxItem], self.element.SelectedItems)

#     def select(self, value: Union[str, int]) -> ListBoxItem:
#         """Selects an item by index.

#         :param value: Text to select/Index to select by
#         :return: ListBoxItem
#         """
#         return self.element.Select(value)

#     def add_to_selection(self, value: Union[str, int]) -> ListBoxItem:
#         """Add a row to the selection by index/by text.

#         :param value: Text/Index
#         :return: ListBoxItem
#         """
#         return self.element.AddToSelection(value)

#     def remove_from_selection(self, value: Union[str, int]) -> ListBoxItem:
#         """Remove a row to the selection by index/by text.

#         :param value: Text/Index
#         :return: ListBoxItem
#         """
#         return self.element.RemoveFromSelection(value)


# class ListBoxItem(AutomationElement):
#     """Class to interact with a list box item element"""

#     is_checked: bool = Field(
#         None,
#         title="ListBoxItem Is Checked",
#         description="Gets or sets if the listbox item is checked, if checking is supported",
#     )
#     text: str = Field(None, title="Text", description="Gets the text of the element")

#     def __init__(self, *args, **kwargs):
#         """Creates a ListBoxItem element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_list_box_item(self.element)
#         self.is_checked: bool = (
#             self.element.IsChecked
#         )  #   Gets or sets if the listbox item is checked, if checking is supported
#         self.text: str = self.element.Text  #   Gets the text of the element.

#     def scroll_into_view(self) -> ListBoxItem:
#         """Scrolls the element into view.

#         :return: ListBoxItem
#         """
#         return self.element.ScrollIntoView()


# class Menu(AutomationElement):
#     """Class to interact with a menu or menubar element"""

#     items: List[MenuItem] = Field(
#         None, title="Menu Items", description="Gets all Menu Items which are inside this element"
#     )
#     is_win_menu: bool = Field(
#         None,
#         title="Is Win32 Menu",
#         description="Flag to indicate if the menu is a Win32 menu because that one needs special handling",
#     )

#     def __init__(self, *args, **kwargs):
#         """Creates a Menu element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_menu(self.element)
#         self.items = parse_obj_as(List[MenuItem], self.element.Items)
#         self.is_win_menu = self.element.IsWin32Menu


# class MenuItem(AutomationElement):
#     """Class to interact with a menu item element"""

#     is_win_menu: bool = Field(
#         None,
#         title="Is Win32 Menu",
#         description="Flag to indicate if the menu is a Win32 menu because that one needs special handling",
#     )
#     text: str = Field(None, title="Menu Item text", description="Gets the text of the element")
#     is_checked: bool = Field(
#         None,
#         title="Is Checked",
#         description="Flag if a menu item is checked or unchecked, if checking is supported. For some applications, like WPF, setting this property doesn't execute the action that happens when a user clicks the menu item, only the checked state is changed. For WPF and Windows Forms applications, if you want to execute the action too, you need to use Invoke() method",
#     )

#     def __init__(self, *args, **kwargs):
#         """Creates a MenuItem element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_menu_item(self.element)
#         self.is_win_menu = self.element.IsWin32Menu
#         self.text = self.element.Text
#         self.is_checked = self.element.IsChecked

#     def collapse(self) -> MenuItem:
#         """Collapses the element

#         :return: MenuItem element
#         """

#         return self.element.Collapse()

#     def expand(self) -> MenuItem:
#         """Expands the element

#         :return: MenuItem element
#         """

#         return self.element.Expand()

#     def invoke(self) -> MenuItem:
#         """Invokes the element

#         :return: MenuItem element
#         """

#         return self.element.Invoke()


# # TODO: Test and build this class
# class MenuItems:
#     """Represents a list of MenuItem elements"""

#     def __init__(self, elements: List[Any]) -> None:
#         """Creates a MenuItem element.

#         :param elements: List of MenuItem objects
#         """
#         self.elements = elements
#         self.length = len(self.elements)  #   Gets the number of elements in the list.

#     def this(self, text: str) -> MenuItem:
#         """Gets the MenuItem with the given text.

#         :param text: Given text
#         :return: MenuItem for matched text
#         """
#         return self.elements.this(text)


# class ProgressBar(AutomationElement):
#     """Class to interact with a progressbar element"""

#     range_value_pattern: Any = Field(
#         None, title="Range value pattern", description="Pattern object for the IRangeValuePattern"
#     )
#     minimum: float = Field(None, title="Minimum", description="Gets the minimum value")
#     maximum: float = Field(None, title="Maximum", description="Gets the maximum value")
#     value: float = Field(None, title="Value", description="Gets the current value")

#     def __init__(self, *args, **kwargs):
#         """Creates a ProgressBar element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_progress_bar(self.element)
#         self.range_value_pattern: Any = self.element.RangeValuePattern
#         self.minimum: float = self.element.Minimum
#         self.maximum: float = self.element.Maximum
#         self.value: float = self.element.Value


# class RadioButton(AutomationElement):
#     """Class to interact with a radiobutton element"""

#     is_checked: bool = Field(None, title="Is Checked", description="Flag if the selection of this element is checked")

#     def __init__(self, *args, **kwargs):
#         """Creates a RadioButton element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_radio_button(self.element)
#         self.is_checked: bool = self.element.IsChecked


# class Slider(AutomationElement):
#     """Class to interact with a slider element"""

#     minimum: float = Field(None, title="Minimum", description="The minimum value")
#     maximum: float = Field(None, title="Maximum", description="The maximum value")
#     small_change: float = Field(None, title="Small change", description="The value of a small change")
#     large_change: float = Field(None, title="Large change", description="The value of a large change")
#     large_increase_button: Any = Field(
#         None, title="Large increase button", description="The button element used to perform a large increment"
#     )
#     large_decrease_button: Any = Field(
#         None, title="Large decrease button", description="The button element used to perform a large decrement"
#     )
#     thumb: Any = Field(None, title="Thumb", description="The element used to drag")
#     is_only_value: bool = Field(
#         None,
#         title="Is only value",
#         description="Flag which indicates if the Slider supports range values (min->max) or only values (0-100). Only values are for example used when combining UIA3 and WinForms applications",
#     )
#     value: float = Field(None, title="Element value", description="Element's current value")

#     def __init__(self, *args, **kwargs):
#         """Creates a Slider element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_slider(self.element)
#         self.minimum: float = self.element.Minimum
#         self.maximum: float = self.element.Maximum
#         self.small_change: float = self.element.SmallChange
#         self.large_change: float = self.element.LargeChange
#         self.large_increase_button: Any = self.element.LargeIncreaseButton
#         self.large_decrease_button: Any = self.element.LargeDecreaseButton
#         self.thumb: Any = self.element.Thumb
#         self.is_only_value: bool = self.element.IsOnlyValue
#         self.value: float = self.element.Value

#     def small_increment(self) -> None:
#         """Performs a small increment"""
#         self.element.SmallIncrement()

#     def small_decrement(self) -> None:
#         """Performs a small decrement"""
#         self.element.SmallDecrement()

#     def large_increment(self) -> None:
#         """Performs a large increment"""
#         self.element.LargeIncrement()

#     def large_decrement(self) -> None:
#         """Performs a large decrement"""
#         self.element.LargeDecrement()

#     def get_large_increase_button(self) -> Any:
#         """Gets large increase button

#         :return: Button element
#         """
#         return self.element.GetLargeIncreaseButton()

#     def get_large_decrease_button(self) -> Any:
#         """Gets large decrease button

#         :return: Button element
#         """
#         return self.element.GetLargeDecreaseButton()


# class Spinner(AutomationElement):
#     """Class to interact with a WinForms spinner element"""

#     minimum: float = Field(None, title="Minimum", description="The minimum value")
#     maximum: float = Field(None, title="Maximum", description="The maximum value")
#     small_change: float = Field(None, title="Small Change", description="The value of a small change")
#     increase_button: Any = Field(
#         None, title="Increase button", description="The button element used to perform a large increment"
#     )
#     decrease_button: Any = Field(
#         None, title="Decrease button", description="The button element used to perform a large decrement"
#     )
#     is_only_value: bool = Field(
#         None,
#         title="Is only value",
#         description="Flag which indicates if the Spinner supports range values (min->max) or only values (0-100). Only values are for example used when combining UIA3 and WinForms applications",
#     )
#     value: float = Field(None, title="Value", description="The current element value")

#     def __init__(self, *args, **kwargs):
#         """Creates a Spinner element"""
#         super().__init__(*args, **kwargs)
#         self.element = AutomationElementExtensions.as_spinner(self.element)
#         self.minimum: float = self.element.Minimum
#         self.maximum: float = self.element.Maximum
#         self.small_change: float = self.element.SmallChange
#         self.increase_button: Any = self.element.IncreaseButton
#         self.decrease_button: Any = self.element.DecreaseButton
#         self.is_only_value: bool = self.element.IsOnlyValue
#         self.value: float = self.element.Value

#     def increment(self):
#         """Performs increment"""
#         self.element.Increment()

#     def decrement(self):
#         """Performs decrement"""
#         self.element.Decrement()

#     def get_increase_button(self) -> Any:
#         """Method to get the increase button.

#         :return: Button
#         """
#         self.element.GetIncreaseButton()

#     def get_decrease_button(self) -> Any:
#         """Method to get the decrease button.

#         :return: Button
#         """
#         self.element.GetDecreaseButton()
#         self.element.GetDecreaseButton()
#         self.element.GetDecreaseButton()
#         :return: Button
#         """
#         self.element.GetDecreaseButton()
#         self.element.GetDecreaseButton()
#         self.element.GetDecreaseButton()
