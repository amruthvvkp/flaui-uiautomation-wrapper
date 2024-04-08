"""
Wrapper objects for AutomationElement class.
"""

from __future__ import annotations

import abc
from datetime import date, datetime
from typing import Any, List, Optional, Tuple, Union

import arrow
from pydantic import BaseModel, Field
from System import TimeSpan  # pyright: ignore

from flaui.core.automation_type import AutomationType
from flaui.core.condition_factory import ConditionFactory, PropertyCondition
from flaui.core.definitions import ControlType, ExpandCollapseState, RowOrColumnMajor, ToggleState
from flaui.core.framework_types import FrameworkType
from flaui.lib.collections import TypeCast
from flaui.lib.system.drawing import ColorCollection

# ================================================================================
#   Element base Pydantic abstract class
# ================================================================================


class ElementModel(BaseModel, abc.ABC):
    """Base class for all automation elements"""

    raw_element: Any = Field(
        ..., title="Automation Element", description="Contains the C# automation element in raw form"
    )  # Consider making this a private property


class ElementBase(ElementModel, abc.ABC):
    """Automation Element base abstract class"""

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
    def automation_type(self) -> AutomationType:
        """The current AutomationType for this element

        :return: Automation Type
        """
        return AutomationType[self.raw_element.AutomationType.ToString()]

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
    def condition_factory(self) -> ConditionFactory:
        """Shortcut to the condition factory for the current automation, Returns condition factory object

        :return: Condition Factory
        """
        return ConditionFactory(raw_cf=self.raw_element.ConditionFactory)

    @property
    def control_type(self) -> ControlType:
        """The control type of the element

        :return: Control type
        """
        return ControlType[self.raw_element.ControlType.ToString()]

    @property
    def framework_automation_element(self) -> Any:
        """Object which contains the native wrapper element (UIA2 or UIA3) for this element

        :return: Framework automation element
        """
        return self.raw_element.FrameworkAutomationElement

    @property
    def framework_type(self):
        """The direct framework type of the element. Results in 'FrameworkType.Unknown' if it couldn't be resolved

        :return: Framework Type
        """
        raw = self.raw_element.FrameworkType  # type: ignore
        return FrameworkType.none if raw.ToString() == "None" else FrameworkType[raw.ToString()]

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
    def parent(self) -> AutomationElement:
        """Get the parent AutomationElement

        :return: Parent
        """
        return AutomationElement(raw_element=self.raw_element.Parent)

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


# =====================================================================================================
#   Pattern Elements Pydantic abstract models from FlaUI.Core.AutomationElements.PatternElements
# =====================================================================================================
class InvokeAutomationElement(ElementModel, abc.ABC):
    """An element that supports the InvokePattern"""

    def invoke(self) -> None:
        """Invokes the element"""
        self.raw_element.Invoke()


class ToggleAutomationElement(ElementModel, abc.ABC):
    """Class for an element that supports the TogglePattern"""

    @property
    def toggle_state(self) -> ToggleState:
        """Gets or sets the current toggle state.

        :return: ToggleState
        """
        return ToggleState(self.raw_element.ToggleState)

    def is_toggled(self) -> bool:
        """Gets or sets if the element is toggled.

        :return: True if toggled, else False
        """
        return self.raw_element.IsToggled

    def toggle(self) -> None:
        """Toggles the element."""
        self.raw_element.Toggle()

    def set_toggle_state(self, required_state: bool) -> None:
        """Sets toggled state

        :param required_state: True if you need the element to be toggled, else False
        :return: None
        """
        return self.toggle() if self.is_toggled() == required_state else None


class SelectionItemAutomationElement(ElementModel, abc.ABC):
    """An element which supports the SelectionItemPattern"""

    @property
    def is_selected(self) -> bool:
        """Value to get/set if this element is selected.

        :return: True if element is selected, else False
        """
        return self.raw_element.IsSelected

    def select(self) -> SelectionItemAutomationElement:
        """Selects the element.

        :return: SelectionItemAutomationElement
        """
        return SelectionItemAutomationElement(raw_element=self.raw_element.Select())

    def add_to_selection(self) -> SelectionItemAutomationElement:
        """Adds the element to the selection.

        :return: SelectionItemAutomationElement
        """
        return SelectionItemAutomationElement(raw_element=self.raw_element.AddToSelection())

    def remove_from_selection(self) -> SelectionItemAutomationElement:
        """Removes the element to the selection.

        :return: SelectionItemAutomationElement
        """
        return SelectionItemAutomationElement(raw_element=self.raw_element.RemoveFromSelection())


class ComboBoxItem(SelectionItemAutomationElement, abc.ABC):
    """Class to interact with a combobox item element."""

    @property
    def text(self) -> str:
        """Gets the text of the element.

        :return: Element text
        """
        return self.raw_element.Text


# ================================================================================
#   Element wrappers from FlaUI.Core.AutomationElements
# ================================================================================
class AutomationElement(ElementBase):
    """UI element which can be used in automation"""

    @property
    def automation(self) -> Any:
        """The current used automation object.

        :return: Automation object
        """
        return self.raw_element.Automation

    @property
    def item_status(self) -> str:
        """The item status of this element.

        :return: Item status value
        """
        return self.raw_element.ItemStatus

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

    def draw_highlight(self, color: ColorCollection = ColorCollection.Red, duration: int = 2000) -> None:
        """Draws a highlight around the element.

        :param color: Color used to highlight, defaults to ColorCollection.Red
        :param duration: Duration to highlight, defaults to 2000
        """
        self.raw_element.Automation.OverlayManager.Show(
            self.raw_element.Properties.BoundingRectangle.Value, color, duration
        )

    def equals(self, another_element: AutomationElement) -> bool:
        """Compares two elements.

        :param other_element: Another element
        :return: True/False
        """
        return self.raw_element.Equals(another_element.raw_element)

    def find_all(self, tree_scope: Any, condition: PropertyCondition) -> List[AutomationElement]:
        """Finds all children with the condition.

        :aram tree_scope: Treescope object
        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAll(tree_scope, condition.condition)]

    def find_all_by_x_path(self, x_path: str) -> List[AutomationElement]:
        """Finds all items which match the given xpath.

        :param x_path: Element XPath
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllByXPath(x_path)]

    def find_all_children(self, condition: PropertyCondition) -> List[AutomationElement]:
        """Finds all children with the condition.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllChildren(condition.condition)]

    def find_all_descendants(self, condition: PropertyCondition) -> List[AutomationElement]:
        """Finds all descendants with the condition.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllDescendants(condition.condition)]

    def find_all_nested(self, condition: PropertyCondition) -> List[AutomationElement]:
        """Finds all elements by iterating thru all conditions.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllNested(condition.condition)]

    def find_all_with_options(
        self, tree_scope: Any, condition: PropertyCondition, traversal_options: Any, root: Any
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
            for _ in self.raw_element.FindAllWithOptions(tree_scope, condition.condition, traversal_options, root)
        ]

    def find_at(self, tree_scope: Any, index: int, condition: PropertyCondition) -> AutomationElement:
        """Finds the element with the given index with the given condition.

        :param tree_scope: The scope to search.
        :param index: The index of the element to return (0-based).
        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindAt(tree_scope, index, condition.condition))

    def find_child_at(self, index: int, condition: PropertyCondition) -> AutomationElement:
        """Finds the child at the given position with the condition.

        :param index: The index of the child to find.
        :param condition: The condition.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindChildAt(index, condition.condition))

    def find_first(self, tree_scope: Any, condition: PropertyCondition) -> AutomationElement:
        """Finds the first element in the given scope with the given condition.

        :param tree_scope: The scope to search.
        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirst(tree_scope, condition.condition))

    def find_first_by_x_path(self, x_path: str) -> AutomationElement:
        """Finds for the first item which matches the given xpath.

        :param x_path: XPath to the element
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirstByXPath(x_path))

    def find_first_child(self, condition: PropertyCondition) -> AutomationElement:
        """Finds the first child.

        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirstChild(condition.condition))

    def find_first_descendant(self, condition: PropertyCondition) -> AutomationElement:
        """Finds the first descendant.

        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirstDescendant(condition.condition))

    def find_first_nested(self, conditions: Optional[Any]) -> AutomationElement:
        """Finds the first element by iterating thru all conditions.

        :param conditions: The conditions to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(
            raw_element=self.raw_element.FindFirstNested(conditions.raw_cf)  # type: ignore # pyright: ignore
        )

    def find_first_with_options(
        self, tree_scope: Any, condition: PropertyCondition, traversal_options: Any, root: Any
    ) -> AutomationElement:
        """Find first matching element in the specified order.

        :param tree_scope: A combination of values specifying the scope of the search.
        :param condition: A condition that represents the criteria to match.
        :param traversal_options: Value specifying the tree navigation order.
        :param root: An element with which to begin the search.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(
            raw_element=self.raw_element.FindFirstWithOptions(tree_scope, condition.condition, traversal_options, root)
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

    def get_hash_code(self) -> int:
        """Fetches the hash code of the current element

        :return: Hash code
        """
        return self.raw_element.GetHashCode()

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
        # return self.raw_element.RegisterActiveTextPositionChangedEvent(tree_scope, action)
        pass

    def register_automation_event(self, event: Any, tree_scope: Any, action: Any) -> Any:
        """Registers the given automation event.

        :param event: Event object
        :param tree_scope: Treescope object
        :param action: Action object
        :return: Registered event
        """
        # return self.raw_element.RegisterAutomationEvent(event, tree_scope, action)
        pass

    def register_notification_event(self) -> Any:
        """Registers a notification event.

        :return: None
        """
        # self.raw_element.RegisterNotificationEvent
        pass

    def register_property_changed_event(self) -> Any:
        """Registers a property changed event with the given property.

        :return: None
        """
        # self.raw_element.RegisterPropertyChangedEvent
        pass

    def register_structure_changed_event(self) -> Any:
        """Registers a structure changed event.

        :return: None
        """
        # self.raw_element.RegisterStructureChangedEvent
        pass

    def register_text_edit_text_changed_event_handler(self) -> Any:
        """Registers a text edit text changed event.

        :return: None
        """
        # self.raw_element.RegisterTextEditTextChangedEventHandler
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

    def try_get_clickable_point(self) -> Tuple[bool, Any]:  # TODO: Return C# Point class
        """Tries to get a clickable point of the element.

        :return: Tuple[flag, Point] - True if a point was found, false otherwise; The clickable point or null, if no point was found
        """
        return self.raw_element.TryGetClickablePoint()

    def AsCalendar(self) -> Calendar:
        """Converts the element to a Calendar.

        :return: Calendar element
        """
        return Calendar(raw_element=self.raw_element.AsCalendar())

    def AsCheckBox(self) -> CheckBox:
        """Converts the element to a CheckBox.

        :return: CheckBox element
        """
        return CheckBox(raw_element=self.raw_element.AsCheckBox())

    def AsComboBox(self) -> ComboBox:
        """Converts the element to a ComboBox.

        :return: ComboBox element
        """
        return ComboBox(raw_element=self.raw_element.AsComboBox())

    def AsDataGridView(self) -> DataGridView:
        """Converts the element to a DataGridView.

        :return: DataGridView element
        """
        return DataGridView(raw_element=self.raw_element.AsDataGridView())

    def AsDateTimePicker(self) -> DateTimePicker:
        """Converts the element to a DateTimePicker.

        :return: DateTimePicker element
        """
        return DateTimePicker(raw_element=self.raw_element.AsDateTimePicker())

    def AsLabel(self) -> Label:
        """Converts the element to a Label.

        :return: Label element
        """
        return Label(raw_element=self.raw_element.AsLabel())

    def AsGrid(self) -> Grid:
        """Converts the element to a Grid.

        :return: Grid element
        """
        return Grid(raw_element=self.raw_element.AsGrid())

    def AsGridRow(self) -> GridRow:
        """Converts the element to a GridRow.

        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.AsGridRow())

    def AsGridCell(self) -> GridCell:
        """Converts the element to a GridCell.

        :return: GridCell element
        """
        return GridCell(raw_element=self.raw_element.AsGridCell())

    def AsGridHeaderItem(self) -> GridHeaderItem:
        """Converts the element to a GridHeaderItem.

        :return: GridHeaderItem element
        """
        return GridHeaderItem(raw_element=self.raw_element.AsGridHeaderItem())

    # def AsHorizontalScrollBar(self) -> HorizontalScrollBar:
    #     """Converts the element to a HorizontalScrollBar.

    #     :return: HorizontalScrollBar element
    #     """
    #     return HorizontalScrollBar(raw_element=self.raw_element.AsHorizontalScrollBar())# TODO: Put in HorizontalScrollBar element and update this line

    def AsListBox(self) -> ListBox:
        """Converts the element to a ListBox.

        :return: ListBox element
        """
        return ListBox(raw_element=self.raw_element.AsListBox())

    def AsListBoxItem(self) -> ListBoxItem:
        """Converts the element to a ListBoxItem.

        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.AsListBoxItem())

    def AsMenu(self) -> Menu:
        """Converts the element to a Menu.

        :return: Menu element
        """
        return Menu(raw_element=self.raw_element.AsMenu())

    def AsMenuItem(self) -> MenuItem:
        """Converts the element to a MenuItem.

        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.AsMenuItem())

    def AsProgressBar(self) -> ProgressBar:
        """Converts the element to a ProgressBar.

        :return: ProgressBar element
        """
        return ProgressBar(raw_element=self.raw_element.AsProgressBar())

    def AsRadioButton(self) -> RadioButton:
        """Converts the element to a RadioButton.

        :return: RadioButton element
        """
        return RadioButton(raw_element=self.raw_element.AsRadioButton())

    def AsSlider(self) -> Slider:
        """Converts the element to a Slider.

        :return: Slider element
        """
        return Slider(raw_element=self.raw_element.AsSlider())

    def AsSpinner(self) -> Spinner:
        """Converts the element to a Spinner.

        :return: Spinner element
        """
        return Spinner(raw_element=self.raw_element.AsSpinner())

    def AsTab(self) -> Tab:
        """Converts the element to a Tab.

        :return: Tab element
        """
        return Tab(raw_element=self.raw_element.AsTab())

    def AsTabItem(self) -> TabItem:
        """Converts the element to a TabItem.

        :return: TabItem element
        """
        return TabItem(raw_element=self.raw_element.AsTabItem())

    def AsTextBox(self) -> TextBox:
        """Converts the element to a TextBox.

        :return: TextBox element
        """
        return TextBox(raw_element=self.raw_element.AsTextBox())

    def AsThumb(self) -> Thumb:
        """Converts the element to a Thumb.

        :return: Thumb element
        """
        return Thumb(raw_element=self.raw_element.AsThumb())

    def AsTitleBar(self) -> TitleBar:
        """Converts the element to a TitleBar.

        :return: TitleBar element
        """
        return TitleBar(raw_element=self.raw_element.AsTitleBar())

    def AsToggleButton(self) -> ToggleButton:
        """Converts the element to a ToggleButton.

        :return: ToggleButton element
        """
        return ToggleButton(raw_element=self.raw_element.AsToggleButton())

    def AsTree(self) -> Tree:
        """Converts the element to a Tree.

        :return: Tree element
        """
        return Tree(raw_element=self.raw_element.AsTree())

    def AsTreeItem(self) -> TreeItem:
        """Converts the element to a TreeItem.

        :return: TreeItem element
        """
        return TreeItem(raw_element=self.raw_element.AsTreeItem())

    # def AsVerticalScrollBar(self) -> VerticalScrollBar:
    #     """Converts the element to a VerticalScrollBar.

    #     :return: VerticalScrollBar element
    #     """
    #     return VerticalScrollBar(raw_element=self.raw_element.AsVerticalScrollBar()) # Build VerticalScrollBar class and update this line

    def AsWindow(self) -> Window:
        """Converts the element to a Window.

        :return: Window element
        """
        return Window(raw_element=self.raw_element.AsWindow())


# TODO: Next things to do
# 1. Build other classes
# 2. Finally add AutomationElementExtensions
# 3. Write unit tests
# 4. Fix return class types for certain functions which use system libraries


class Button(AutomationElement, InvokeAutomationElement):
    """Class to interact with a button element"""

    pass


class Calendar(AutomationElement):
    """Class to interact with a calendar element. Not supported for Windows Forms calendar"""

    @property
    def selected_dates(self) -> date:
        """Gets the selected dates in the calendar. For Win32 multiple selection calendar the returned array has two dates,
        the first date and the last date of the selected range. For WPF calendar the returned array contains all selected dates

        :return: Selected dates
        """
        return arrow.get(self.raw_element.SelectedDates).date()

    def select_date(self, date: date) -> None:
        """Deselects other selected dates and selects the specified date.

        :param date: Date object
        """
        self.raw_element.SelectDate(arrow.get(date).date())

    def select_range(self, dates: List[date]) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method deselects other selected dates and selects the specified range.
        For any other type of SelectionMode it deselects other selected dates and selects only the last date in the range.
        For Win32 multiple selection calendar the "dates" parameter should contain two dates, the first and the last date of the range to be selected.
        For Win32 single selection calendar this method selects only the second date from the "dates" array.
        For WPF calendar all dates should be specified in the "dates" parameter, not only the first and the last date of the range.

        :param dates: Date ranges
        """
        self.raw_element.SelectRange(dates)

    def add_to_selection(self, date: date) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method adds the specified date to current selection.
        For any other type of SelectionMode it deselects other selected dates and selects the specified date.
        This method is supported only for WPF calendar.

        :param date: Date object
        """
        self.raw_element.AddToSelection(arrow.get(date).date())

    def add_range_to_selection(self, dates: List[date]) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method adds the specified range to current selection.
        For any other type of SelectionMode it deselects other selected dates and selects only the last date in the range.
        This method is supported only for WPF calendar.

        :param dates: Date ranges
        """
        self.raw_element.AddRangeToSelection(dates)


class CheckBox(AutomationElement, ToggleAutomationElement):
    """Class to interact with a checkbox element"""

    @property
    def is_checked(self) -> bool:
        """Flag if the element is checked

        :return: Element is checked
        """
        return self.raw_element.IsChecked

    @property
    def text(self) -> str:
        """Gets the text of the element

        :return: Element text
        """
        return self.raw_element.Text


class ComboBox(AutomationElement):
    """Class to interact with a combobox element"""

    @property
    def AnimationDuration(self, time_span: int = 100) -> Any:
        """Timespan to wait until the animation for opening/closing is finished.

        :param time_span: Timespan in milliseconds, defaults to 100
        :return: C# TimeSpan object from System namespace
        """
        return self.raw_element.AnimationDuration(
            TimeSpan.FromMilliseconds(time_span)
        )  # TODO: Check if get/set property is needed to work here

    @property
    def editable_text(self) -> str:
        """The text of the editable element inside the combobox.
        Only works if the combobox is editable.

        :return: Editable text of the element
        """
        return self.raw_element.EditableText

    @property
    def is_editable(self) -> bool:
        """Flag which indicates, if the combobox is editable or not

        :return: True If element editable, else False
        """
        return self.raw_element.IsEditable

    @property
    def is_read_only(self) -> bool:
        """Flag which indicates, if the combobox is read-only or not

        :return: True If element read-only, else False
        """
        return self.raw_element.IsReadOnly

    @property
    def value(self) -> str:
        """Selected value of the Combobox element

        :return: Element selected value
        """
        return self.raw_element.Value

    @property
    def selected_items(self) -> List[str]:
        """Gets all selected items

        :return: Selected items
        """
        return [ComboBoxItem(raw_element=_) for _ in self.raw_element.SelectedItems]  # type: ignore # pyright: ignore

    @property
    def selected_item(self) -> ComboBoxItem:
        """Gets the first selected item or null otherwise

        :return: Selected item
        """
        return ComboBoxItem(raw_element=self.raw_element.SelectedItem)

    @property
    def items(self) -> List[str]:
        """Gets all available items from the ComboBox element

        :return: Item
        """
        return [ComboBoxItem(raw_element=_) for _ in self.raw_element.Items]  # type: ignore # pyright: ignore

    @property
    def expand_collapse_state(self) -> ExpandCollapseState:
        """Gets the ExpandCollapseStateof the element

        :return: Expand/Collapse state
        """
        return ExpandCollapseState(self.raw_element.ExpandCollapseState)

    def expand(self) -> None:
        """Expands the element"""
        self.raw_element.Expand()

    def collapse(self) -> None:
        """Collapses the element"""
        self.raw_element.Collapse()

    def select(self, value: Union[int, str]) -> ComboBoxItem:
        """Select an item by index/the first item which matches the given text..

        :param value: Index value/The text to search for
        :return: The first found item or null if no item matches.
        """
        return ComboBoxItem(raw_element=self.raw_element.Select(value))


class DataGridView(AutomationElement):
    """Class to interact with a WinForms DataGridView"""

    @property
    def has_add_row(self) -> bool:
        """Flag to indicate if the grid has the "Add New Item" row or not.
        /// This needs to be set as FlaUI cannot find out if this is the case or not.

        :return: True if has Add row, else False
        """
        return self.raw_element.HasAddRow

    @property
    def header(self) -> Union[DataGridViewHeader, None]:
        """Gets the header element or null if the header is disabled.

        :return: DataGridViewHeader element if header element exists, else None
        """
        raw_element = self.raw_element.Header
        return DataGridViewHeader(raw_element=raw_element) if raw_element else raw_element

    @property
    def rows(self) -> List[DataGridViewRow]:
        """Gets all the data rows.

        :return: List of DatGridViewRow elements
        """
        return [DataGridViewRow(raw_element=_) for _ in self.raw_element.Rows]  # type: ignore


class DataGridViewHeader(AutomationElement):
    """Creates a DataGridViewHeader element"""

    @property
    def columns(self) -> List[DataGridViewHeaderItem]:
        """Gets the header items.

        :return: List of DataGridViewHeaderItem
        """
        return [DataGridViewHeaderItem(raw_element=_) for _ in self.raw_element.DataGridViewHeaderItem]


class DataGridViewHeaderItem(AutomationElement):
    """Class to interact with a WinForms DataGridView header item"""

    @property
    def text(self) -> str:
        """Gets the text of the header item.

        :return: DataGridViewHeaderItem text
        """
        return self.raw_element.Text


class DataGridViewRow(AutomationElement):
    """Creates a DataGridViewRow element."""

    @property
    def cells(self) -> List[DataGridViewCell]:
        """Gets all cells.

        :return: Cell elements
        """
        return [DataGridViewCell(raw_element=_) for _ in self.raw_element.Cells]


class DataGridViewCell(AutomationElement):
    """Class to interact with a WinForms DataGridView cell."""

    @property
    def value(self) -> str:
        """Value in the cell.

        :return: Cell value
        """
        return self.raw_element.Value

    # TODO: Check Get/Set actions while testing
    def get_value(self) -> str:
        """Gets the value in the cell.

        :return: Cell value
        """
        return self.raw_element.Value

    def set_value(self, value: str) -> None:
        """Sets the value in the cell.

        :param value: Value to set
        """
        self.raw_element.Value(value)


class DateTimePicker(AutomationElement):
    """Class to interact with a DateTimePicker element"""

    @property
    def selected_date(self) -> Union[datetime, None]:
        """Gets the selected date in the DateTimePicker.
        For Win32, setting SelectedDate to null will uncheck the DateTimePicker control and disable it.
        Also for Win32, if the control is unchecked then SelectedDate will return null.

        :return: Datetime object if exists, else None
        """
        raw_element = self.raw_element.SelectedDate
        return arrow.get(raw_element).datetime if raw_element else None

    # TODO: Check Get/Set method during testing
    def get_selected_date(self) -> Union[datetime, None]:
        """Gets the selected date in the DateTimePicker.
        For Win32, setting SelectedDate to null will uncheck the DateTimePicker control and disable it.
        Also for Win32, if the control is unchecked then SelectedDate will return null.

        :return: Datetime object if exists, else None
        """
        raw_element = self.raw_element.SelectedDate
        return arrow.get(raw_element).datetime if raw_element else None

    def set_selected_date(self, datetime: datetime) -> None:
        """Sets the selected date in the DateTimePicker.
        For Win32, setting SelectedDate to null will uncheck the DateTimePicker control and disable it.
        Also for Win32, if the control is unchecked then SelectedDate will return null.

        :return: Datetime object if exists, else None
        """
        self.raw_element.SelectedDate(datetime)


class Grid(AutomationElement):
    """Element for grids and tables"""

    @property
    def row_count(self) -> int:
        """Gets the total row count.

        :return: Row Count
        """
        return self.raw_element.RowCount

    @property
    def column_count(self) -> int:
        """Gets the total column count.

        :return: Column Count
        """
        return self.raw_element.ColumnCount

    @property
    def column_headers(self) -> List[AutomationElement]:
        """Gets all column header elements.

        :return: List of column header elements
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.ColumnHeaders]

    @property
    def row_headers(self) -> List[AutomationElement]:
        """Gets all row header elements.

        :return: List of row header elements
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.RowHeaders]

    @property
    def row_or_column_major(self) -> RowOrColumnMajor:
        """Gets whether the data should be read primarily by row or by column.

        :return: Row/Column
        """
        return RowOrColumnMajor(self.raw_element.RowOrColumnMajor)

    @property
    def header(self) -> GridHeader:
        """Gets the header item.

        :return: Header item
        """
        return GridHeader(raw_element=self.raw_element.Header)

    @property
    def rows(self) -> List[GridRow]:
        """Returns the rows which are currently visible to UIA. Might not be the full list (eg. in virtualized lists)!
        /// Use "GetRowByIndex" to make sure to get the correct row.

        :return: List of GridRow elements
        """
        return [GridRow(raw_element=_) for _ in self.raw_element.Rows]  # type: ignore

    @property
    def selected_items(self) -> List[GridRow]:
        """Gets all selected items.

        :return: List of GridRow elements
        """
        return [GridRow(raw_element=_) for _ in self.raw_element.SelectedItems]  # type: ignore

    @property
    def selected_item(self) -> Union[GridRow, None]:
        """Gets the first selected item or null otherwise.

        :return: GridRow element if selected, else None
        """
        raw_element = self.raw_element.SelectedItem
        return GridRow(raw_element=raw_element) if raw_element else raw_element

    def select(self, row_index: Optional[int], column_index: Optional[int], text_to_find: Optional[str]) -> GridRow:
        """Select the first row by text in the given Row index or a combination of Column index along with text_to_find.

        :param row_index: Row index
        :param column_index: Column index
        :param text_to_find: Text to find in the column
        :raises ValueError: On invalid input combination
        :return: GridRow element
        """
        if all([column_index, text_to_find]):
            return GridRow(raw_element=self.raw_element.Select(column_index, text_to_find))
        elif all([row_index]):
            return GridRow(raw_element=self.raw_element.Select(row_index))
        else:
            raise ValueError("Invalid input sent to the function, cannot select the row")

    def add_to_selection(
        self, row_index: Optional[int], column_index: Optional[int], text_to_find: Optional[str]
    ) -> GridRow:
        """Add a row to the selection by index or by text in the given column.

        :param row_index: Row index
        :param column_index: Column index
        :param text_to_find: Text to find in the column
        :raises ValueError: On invalid input combination
        :return: GridRow element
        """
        if all([column_index, text_to_find]):
            return GridRow(raw_element=self.raw_element.AddToSelection(column_index, text_to_find))
        elif all([row_index]):
            return GridRow(raw_element=self.raw_element.AddToSelection(row_index))
        else:
            raise ValueError("Invalid input sent to the function, cannot add to the selection")

    def remove_from_selection(
        self, row_index: Optional[int], column_index: Optional[int], text_to_find: Optional[str]
    ) -> GridRow:
        """Remove a row to the selection by index or by text in the given column.

        :param row_index: Row index
        :param column_index: Column index
        :param text_to_find: Text to find in the column
        :raises ValueError: On invalid input combination
        :return: GridRow element
        """
        if all([column_index, text_to_find]):
            return GridRow(raw_element=self.raw_element.RemoveFromSelection(column_index, text_to_find))
        elif all([row_index]):
            return GridRow(raw_element=self.raw_element.RemoveFromSelection(row_index))
        else:
            raise ValueError("Invalid input sent to the function, cannot remove from the selection")

    def get_row_by_index(self, row_index: int) -> GridRow:
        """a row by index.

        :param row_index: Row index
        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.GetRowByIndex(row_index))

    def get_row_by_value(self, column_index: int, value: str) -> GridRow:
        """Get a row by text in the given column.

        :param column_index: Column index
        :param value: Value
        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.GetRowByValue(column_index, value))

    def get_rows_by_value(self, column_index: int, value: str, max_items: int = 0) -> List[GridRow]:
        """Get all rows where the value of the given column matches the given value.

        :param column_index: The column index to check.
        :param value: The value to check.
        :param max_items: Maximum numbers of items to return, 0 for all, defaults to 0
        :return: List of found rows as GridRow elements.
        """
        return [GridRow(raw_element=_) for _ in self.raw_element.GetRowsByValue(column_index, value, max_items)]  # type: ignore


class GridHeader(AutomationElement):
    """Header element for grids and tables."""

    @property
    def Columns(self) -> List[GridHeaderItem]:
        """Gets all header items from the grid header."""
        return [GridHeaderItem(raw_element=_) for _ in self.raw_element.Columns]


class GridHeaderItem(AutomationElement):
    """Header item for grids and tables."""

    @property
    def text(self) -> str:
        """Gets the text of the element.

        :return: Element text
        """
        return self.raw_element.Text


class GridRow(SelectionItemAutomationElement):
    """Row element for grids and tables."""

    @property
    def cells(self) -> GridCell:
        """Gets all the cells from the row.

        :return: GridCell element
        """
        return GridCell(raw_element=self.raw_element.Cells)

    @property
    def header(self) -> GridHeaderItem:
        """Gets the header item of the row.

        :return: GridHeaderItem element
        """
        return GridHeaderItem(raw_element=self.raw_element.Header)

    def find_cell_by_text(self, text_to_find: str) -> GridCell:
        """Find a cell by a given text.

        :param text_to_find: Text to find by
        :return: GridCell element
        """
        return GridCell(raw_element=self.raw_element.FindCellByText(text_to_find))

    def scroll_into_view(self) -> GridRow:
        """Scrolls the row into view.

        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.ScrollIntoView())


class GridCell(AutomationElement):
    """Cell element for grids and tables."""

    @property
    def containing_grid(self) -> Grid:
        """Gets the grid that contains this cell.

        :return: Grid element
        """
        return Grid(raw_element=self.raw_element.ContainingGrid)

    @property
    def containing_row(self) -> GridRow:
        """Gets the row that contains this cell.

        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.ContainingRow)


class Label(AutomationElement):
    """Class to interact with a label element"""

    @property
    def text(self) -> str:
        """Gets the text of the element.

        :return: Element text
        """
        return self.raw_element.Text


class ListBox(AutomationElement):
    """Class to interact with a list box element"""

    @property
    def Items(self) -> List[ListBoxItem]:
        """Returns all the list box items

        :return: List of ListBoxItem elements
        """
        return [ListBoxItem(raw_element=_) for _ in self.raw_element.Items]  # type: ignore

    @property
    def SelectedItems(self) -> List[ListBoxItem]:
        """Gets all selected items.

        :return: List of ListBoxItem elements
        """
        return [ListBoxItem(raw_element=_) for _ in self.raw_element.SelectedItems]  # type: ignore

    @property
    def SelectedItem(self) -> Union[ListBoxItem, None]:
        """Gets the first selected item or null otherwise.

        :return: ListBoxItem element if selected, else None
        """
        raw_element = self.raw_element.SelectedItem
        return ListBoxItem(raw_element=raw_element) if raw_element else None

    def select(self, value: Union[str, int]) -> ListBoxItem:
        """Selects an item by index or text.

        :param value: Text to select/Index to select by
        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.Select(value))

    def add_to_selection(self, value: Union[str, int]) -> ListBoxItem:
        """Add a row to the selection by index/by text.

        :param value: Text/Index
        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.AddToSelection(value))

    def remove_from_selection(self, value: Union[str, int]) -> ListBoxItem:
        """Remove a row to the selection by index/by text.

        :param value: Text/Index
        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.RemoveFromSelection(value))


class ListBoxItem(SelectionItemAutomationElement):
    """Class to interact with a list box item element"""

    @property
    def text(self) -> str:
        """Gets the text of the element.

        :return: Element text
        """
        return self.raw_element.Text

    def scroll_into_view(self) -> ListBoxItem:
        """Scrolls the element into view.

        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.ScrollIntoView())

    @property
    def is_checked(self) -> bool:
        """Gets if the listbox item is checked, if checking is supported

        :return: True if checked, else False
        """
        return self.raw_element.IsChecked

    # TODO: Get/Set method is to be checked in testing
    def get_is_checked(self) -> bool:
        """Gets if the listbox item is checked, if checking is supported

        :return: True if checked, else False
        """
        return self.raw_element.IsChecked

    def set_is_checked(self, value: bool) -> None:
        """Sets if the listbox item is checked, if checking is supported

        :return: True if checked, else False
        """
        self.raw_element.IsChecked(value)


class Menu(AutomationElement):
    """Class to interact with a menu or menubar element"""

    @property
    def items(self) -> MenuItems:
        """Gets all MenuItem which are inside this element.

        :return: List of Menu Items
        """
        return [MenuItems(menu_items=_) for _ in self.raw_element.Items]  # ignore: type # pyright: ignore

    @property
    def is_win_menu(self) -> bool:
        """Flag to indicate if the containing menu is a Win32 menu because that one needs special handling

        :return: True if the menu is Win32 model, else False
        """
        return self.raw_element.IsWin32Menu


class MenuItems(BaseModel):
    """Represents a list of MenuItem elements."""

    # TODO: Check how to properly parse the property attrs
    menu_items: List[MenuItem]

    # @property
    # def Length(self) -> int:
    #     return len(self.menu_items)

    # @property
    # def this(text: str) -> MenuItem:
    #     pass


class MenuItem(AutomationElement):
    """Class to interact with a menu item element."""

    @property
    def is_win_menu(self) -> bool:
        """Flag to indicate if the containing menu is a Win32 menu because that one needs special handling

        :return: True if the menu is Win32 model, else False
        """
        return self.raw_element.IsWin32Menu

    @property
    def text(self) -> str:
        """Gets the text of the element

        :return: Element text
        """
        return self.raw_element.Text

    @property
    def items(self) -> MenuItems:
        """Gets all MenuItem which are inside this element.

        :return: MenuItems
        """
        return MenuItems(
            menu_items=self.raw_element.Items
        )  # TODO: Find a way to fix menu items and then revisit this one

    def invoke(self) -> MenuItem:
        """Invokes the element.

        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.Invoke())

    def expand(self) -> MenuItem:
        """Expands the element.

        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.Expand())

    def collapse(self) -> MenuItem:
        """Collapses the element.

        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.Collapse())

    # TODO: Check Get/Set methods for IsChecked during testing
    @property
    def is_checked(self) -> bool:
        """Gets if a menu item is checked or unchecked, if checking is supported.
        /// For some applications, like WPF, setting this property doesn't execute the action that happens when a user clicks the menu item, only the checked state is changed.
        /// For WPF and Windows Forms applications, if you want to execute the action too, you need to use Invoke() method.

        :return: True if checked, else False
        """
        return self.raw_element.IsChecked

    def get_is_checked(self) -> bool:
        """Gets if a menu item is checked or unchecked, if checking is supported.
        /// For some applications, like WPF, setting this property doesn't execute the action that happens when a user clicks the menu item, only the checked state is changed.
        /// For WPF and Windows Forms applications, if you want to execute the action too, you need to use Invoke() method.

        :return: True if checked, else False
        """
        return self.raw_element.IsChecked

    def set_is_checked(self, value: bool) -> None:
        """Sets if a menu item is checked or unchecked, if checking is supported.
        /// For some applications, like WPF, setting this property doesn't execute the action that happens when a user clicks the menu item, only the checked state is changed.
        /// For WPF and Windows Forms applications, if you want to execute the action too, you need to use Invoke() method.

        :value: Flag to set
        :return: None
        """
        self.raw_element.IsChecked(value)


class ProgressBar(AutomationElement):
    """Class to interact with a progressbar element"""

    @property
    def minimum(self) -> float:
        """Gets the minimum value.

        :return: Value
        """
        return float(self.raw_element.Minimum)

    @property
    def maximum(self) -> float:
        """Gets the maximum value.

        :return: Value
        """
        return float(self.raw_element.Maximum)

    @property
    def value(self) -> float:
        """Gets the current value.

        :return: Value
        """
        return float(self.raw_element.Value)


class RadioButton(AutomationElement):
    """Class to interact with a radiobutton element"""

    @property
    def is_checked(self) -> bool:
        """Flag to get the selection of this element.

        :return: True if element is checked, else False
        """
        return self.raw_element.IsChecked

    # TODO: Check Get/Set methods during testing
    def get_is_checked(self) -> bool:
        """Flag to get the selection of this element.

        :return: True if element is checked, else False
        """
        return self.raw_element.IsChecked

    def set_is_checked(self, value: bool) -> None:
        """Flag to set the selection of this element.

        :return: None
        """
        self.raw_element.IsChecked(value)


class Slider(AutomationElement):
    """Class to interact with a slider element"""

    @property
    def minimum(self) -> float:
        """The minimum value.

        :return: Minimum value
        """
        return self.raw_element.Minimum

    @property
    def maximum(self) -> float:
        """The maximum value.

        :return: Maximum value
        """
        return self.raw_element.Maximum

    @property
    def small_change(self) -> float:
        """The value of a small change.

        :return: Small change
        """
        return self.raw_element.SmallChange

    @property
    def large_change(self) -> float:
        """The value of a large change.

        :return: Large change
        """
        return self.raw_element.LargeChange

    def large_increase_button(self) -> Button:
        """The button element used to perform a large increment.

        :return: Button element
        """
        return Button(raw_element=self.raw_element.LargeIncreaseButton())

    def large_decrease_button(self) -> Button:
        """The button element used to perform a large decrement.

        :return: Button element
        """
        return Button(raw_element=self.raw_element.LargeDecreaseButton())

    def thumb(self) -> Thumb:
        """The element used to drag.

        :return: Thumb element
        """
        return Thumb(raw_element=self.raw_element.Thumb())

    @property
    def is_only_value(self) -> bool:
        """Flag which indicates if the Slider supports range values (min->max) or only values (0-100).
        Only values are for example used when combining UIA3 and WinForms applications.

        :return: True if only value else False
        """
        return self.raw_element.IsOnlyValue

    @property
    def value(self) -> float:
        """Gets or sets the current value.

        :return: Value of the element
        """
        return self.raw_element.Value

    def small_increment(self):
        """Performs a small increment."""
        self.raw_element.SmallIncrement()

    def small_decrement(self):
        """Performs a small decrement."""
        self.raw_element.SmallDecrement()

    def large_increment(self):
        """Performs a large increment."""
        self.raw_element.LargeIncrement()

    def large_decrement(self):
        """Performs a large decrement."""
        self.raw_element.LargeDecrement()


class Spinner(AutomationElement):
    """Class to interact with a WinForms spinner element"""

    @property
    def minimum(self) -> float:
        """The minimum value.

        :return: Minimum value
        """
        return self.raw_element.Minimum

    @property
    def maximum(self) -> float:
        """The maximum value.

        :return: Maximum value
        """
        return self.raw_element.Maximum

    @property
    def small_change(self) -> float:
        """The value of a small change.

        :return: Small change
        """
        return self.raw_element.SmallChange

    def increase_button(self) -> Button:
        """The button element used to perform a large increment.

        :return: Button element
        """
        return Button(raw_element=self.raw_element.IncreaseButton())

    def decrease_button(self) -> Button:
        """The button element used to perform a large decrement.

        :return: Button element
        """
        return Button(raw_element=self.raw_element.DecreaseButton())

    @property
    def is_only_value(self) -> bool:
        """Flag which indicates if the Slider supports range values (min->max) or only values (0-100).
        Only values are for example used when combining UIA3 and WinForms applications.

        :return: True if only value else False
        """
        return self.raw_element.IsOnlyValue

    @property
    def value(self) -> float:
        """Gets or sets the current value.

        :return: Value of the element
        """
        return self.raw_element.Value

    def increment(self):
        """Performs a increment."""
        self.raw_element.SmallIncrement()

    def decrement(self):
        """Performs a decrement."""
        self.raw_element.SmallDecrement()


class Tab(AutomationElement):
    """Class to interact with a tab element."""

    def selected_tab_item(self) -> TabItem:
        """The currently selected TabItem

        :return: TabItem element
        """
        return TabItem(raw_element=self.raw_element.SelectedTabItem())

    @property
    def selected_tab_item_index(self) -> int:
        """The index of the currently selected TabItem

        :return: Selected index
        """
        return self.raw_element.SelectedTabItemIndex

    def tab_items(self) -> List[TabItem]:
        """All TabItem objects from this Tab

        :return: List of TabItem elements
        """
        return [TabItem(raw_element=_) for _ in self.raw_element.TabItems()]

    def select_tab_item(self, index: Optional[int] = None, value: Optional[str] = None) -> TabItem:
        """Selects a TabItem by index

        :param index: Selects by index value
        :param value: Selects by tab value
        :return: Selected TabItem element
        """
        return (
            TabItem(raw_element=self.raw_element.SelectTabItem(index))
            if index
            else TabItem(raw_element=self.raw_element.SelectTabItem(value))
        )


class TabItem(SelectionItemAutomationElement):
    """Class to interact with a tabitem element."""

    pass


class TextBox(AutomationElement):
    """Class to interact with a textbox element."""

    @property
    def Text(self) -> str:
        """Gets or sets the text of the element.

        :return: Element text
        """
        return self.raw_element.Text

    @property
    def IsReadOnly(self) -> bool:
        """Gets if the element is read only or not.

        :return: True if element is read only else False
        """
        return self.raw_element.IsReadOnly

    def Enter(self, value: str):
        """Simulate typing in text. This is slower than setting Text but raises more events.

        :param value: Value to enter in the element
        """
        self.raw_element.Enter(value)


class Thumb(AutomationElement):
    """Class to interact with a thumb element."""

    def slide_horizontally(self, distance: int):
        """Moves the slider horizontally.

        :param distance: The distance to move the slider, + for right, - for left.
        """
        self.raw_element.SlideHorizontally(distance)

    def slide_vertically(self, distance: int):
        """Moves the slider vertically.

        :param distance: The distance to move the slider, + for down, - for up.
        """
        self.raw_element.SlideVertically(distance)


class TitleBar(AutomationElement):
    """Class to interact with a titlebar element."""

    def minimize_button(self) -> Button:
        """Gets the minimize button element.

        :return: Minimize button
        """
        return Button(raw_element=self.raw_element.MinimizeButton())

    def maximize_button(self) -> Button:
        """Gets the maximize button element.

        :return: Maximize button
        """
        return Button(raw_element=self.raw_element.MaximizeButton())

    def restore_button(self) -> Button:
        """Gets the restore button element.

        :return: Restore button
        """
        return Button(raw_element=self.raw_element.RestoreButton())

    def close_button(self) -> Button:
        """Gets the close button element.

        :return: Close button
        """
        return Button(raw_element=self.raw_element.CloseButton())


class ToggleButton(AutomationElement):
    """Class to interact with a toggle button element."""

    def toggle(self):
        """Toggles the toggle button.
        **Note**: In some WPF scenarios, the bounded command might not be fired. Use AutomationElement.Click instead in that case.
        """
        self.raw_element.Toggle()


class Tree(AutomationElement):
    """Class to interact with a tree element."""

    @property
    def selected_tree_item(self) -> TreeItem:
        """The currently selected TreeItem" />

        :return: TreeItem element of selected tree item
        """
        return TreeItem(raw_element=self.raw_element.SelectedTreeItem)

    @property
    def items(self) -> List[TreeItem]:
        """All child TreeItem" /> objects from this Tree" />

        :return: List of TreeItem elements
        """
        return [TreeItem(raw_element=_) for _ in self.raw_element.Items]


class TreeItem(AutomationElement):
    """Class to interact with a treeitem element."""

    def items(self) -> List[TreeItem]:
        """All child TreeItem" /> objects from this TreeItem" />.

        :return: List of TreeItem elements
        """
        return [TreeItem(raw_element=_) for _ in self.raw_element.Items()]

    @property
    def text(self) -> str:
        """The text of the TreeItem" />.

        :return: Text value of element
        """
        return self.raw_element.Text

    @property
    def is_selected(self) -> bool:
        """Value to get/set if this element is selected.

        :return: True if selected else False
        """
        return self.raw_element.IsSelected

    @property
    def expand_collapse_state(self) -> ExpandCollapseState:
        """Gets the current expand / collapse state.

        :return: Current state enum object
        """
        return ExpandCollapseState(self.raw_element.ExpandCollapseState)

    def expand(self):
        """Expands the element."""
        self.raw_element.Expand()

    def collapse(self):
        """Collapses the element."""
        self.raw_element.Collapse()

    def select(self):
        """Selects the element."""
        self.raw_element.Select()

    def add_to_selection(self) -> TreeItem:
        """Add the element to the selection.

        :return: TreeItem element
        """
        return TreeItem(raw_element=self.raw_element.AddToSelection())

    def remove_from_selection(self) -> TreeItem:
        """Remove the element to the selection.

        :return: TreeItem element
        """
        return TreeItem(raw_element=self.raw_element.RemoveFromSelection())

    @property
    def is_checked(self) -> bool:
        """Gets or sets if the tree item is checked, if checking is supported.

        :return: True if checked else False
        """
        return self.raw_element.IsChecked  # TODO: Check Get/Set methods for checked property


class Window(AutomationElement):
    """Class to interact with a window element."""

    @property
    def title(self) -> str:
        """Gets the title of the window.

        :return: Title value
        """
        return self.raw_element.Title

    @property
    def is_modal(self) -> bool:
        """Gets if the window is modal.

        :return: True if window is modal, else False
        """
        return self.raw_element.IsModal

    @property
    def title_bar(self) -> TitleBar:
        """Gets the TitleBar of the window.

        :return: Title bar element
        """
        return TitleBar(raw_element=self.raw_element.TitleBar)

    @property
    def is_main_window(self) -> bool:
        """Flag to indicate, if the window is the application's main window.
        Is used so that it does not need to be looked up again in some cases (e.g. Context Menu).

        :return: True if the window is main window else False
        """
        return self.raw_element.IsMainWindow

    def modal_windows(self) -> List[Window]:
        """Gets a list of all modal child windows.

        :return: List of window elements
        """
        return [Window(raw_element=_) for _ in self.raw_element.ModalWindows()]

    def popup(self) -> Window:
        """Gets the current WPF popup window.

        :return: Pop up window
        """
        return Window(raw_element=self.raw_element.Popup())

    @property
    def context_menu(self) -> Menu:
        """Gets the context menu for the window.
        /// Note: It uses the FrameworkType of the window as lookup logic. Use GetContextMenuByFrameworkType" /> if you want to control this.

        :return: Context menu item
        """
        return Menu(raw_element=self.raw_element.ContextMenu)

    def get_context_menu_by_framework_type(self, framework_type: FrameworkType) -> Menu:
        """Gets the context menu by a given FrameworkType.

        :param framework_type: Framework Type
        :return: Menu item
        """
        return Menu(raw_element=self.raw_element.GetContextMenuByFrameworkType(framework_type))

    def close(self):
        """Closes the window."""
        self.raw_element.Close()

    def move(self, x: int, y: int):
        """Moves the window to the given coordinates.

        :param x: X cordinate
        :param y: Y cordinate
        """
        self.raw_element.Move(x, y)

    def set_transparency(self, alpha: bytes):
        """Brings the element to the foreground.

        :param alpha: Transparency value
        """
        self.raw_element.SetTransparency(alpha)
