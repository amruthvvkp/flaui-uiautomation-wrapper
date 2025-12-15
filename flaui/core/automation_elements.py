"""
This module contains wrapper objects for AutomationElement class.
It defines two abstract classes, ElementModel and ElementBase, which are used as base classes for other classes that wrap AutomationElement objects.
ElementBase provides properties to access various attributes of the wrapped AutomationElement object.
"""

from __future__ import annotations

import abc
from datetime import date
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union, overload

import arrow
from loguru import logger
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from System import NullReferenceException  # pyright: ignore

from flaui.core.automation_type import AutomationType
from flaui.core.condition_factory import ConditionFactory, PropertyCondition
from flaui.core.definitions import (
    ControlType,
    ExpandCollapseState,
    RowOrColumnMajor,
    ToggleState,
    TreeScope,
    TreeTraversalOptions,
)
from flaui.core.framework_types import FrameworkType
from flaui.lib.collections import TypeCast
from flaui.lib.exceptions import ElementNotFound, handle_csharp_exceptions
from flaui.lib.system.drawing import (
    Color,
    ColorData,
    CSColor,  # pyright: ignore
    CSPoint,  # pyright: ignore
    CSRectangle,  # pyright: ignore
    CSSize,  # pyright: ignore
    Point,
    Rectangle,
    Size,
)

# ================================================================================
#   Element base Pydantic abstract class
# ================================================================================


class ElementModel(BaseModel, abc.ABC):  # pragma: no cover
    raw_element: Any = Field(
        ..., title="Automation Element", description="Contains the C# automation element in raw form"
    )  # Consider making this a private property

    @field_validator("raw_element")
    def validate_element_exists(cls, v: Any, info: ValidationInfo) -> Any:  # pragma: no cover
        """Validate the element exists

        :param v: Raw Element
        :return: Raw Element
        """
        if v is None:
            raise ElementNotFound("Element does not exist")
        return v


class ElementBase(ElementModel, abc.ABC):  # pragma: no cover
    """Automation Element base abstract class"""

    @property
    @handle_csharp_exceptions
    def actual_height(self) -> int:
        """The height of this element

        :return: Actual Height
        """
        return self.raw_element.ActualHeight

    @property
    @handle_csharp_exceptions
    def actual_width(self) -> int:
        """The width of this element

        :return: Actual Width
        """
        return self.raw_element.ActualWidth

    @property
    @handle_csharp_exceptions
    def automation_id(self) -> str:
        """The automation id of the element

        :return: Automation ID
        """
        return self.raw_element.AutomationId

    @property
    @handle_csharp_exceptions
    def automation_type(self) -> AutomationType:
        """The current AutomationType for this element

        :return: Automation Type
        """
        return AutomationType[self.raw_element.AutomationType.ToString()]

    @property
    @handle_csharp_exceptions
    def bounding_rectangle(self) -> Rectangle:
        """The bounding rectangle of this element

        :return: Bounding Rectangle
        """
        return Rectangle(raw_value=self.raw_element.BoundingRectangle)

    @property
    @handle_csharp_exceptions
    def cached_children(self) -> Any:
        """Gets the cached children for this element

        :return: Cached Children
        """
        return self.raw_element.CachedChildren

    @property
    @handle_csharp_exceptions
    def cached_parent(self) -> Any:
        """Gets the cached parent for this element

        :return: Cached Parent
        """
        return self.raw_element.CachedParent

    @property
    @handle_csharp_exceptions
    def class_name(self) -> str:
        """The class name of the element

        :return: Class Name
        """
        return self.raw_element.ClassName

    @property
    @handle_csharp_exceptions
    def condition_factory(self) -> ConditionFactory:
        """Shortcut to the condition factory for the current automation, Returns condition factory object

        :return: Condition Factory
        """
        return ConditionFactory(raw_cf=self.raw_element.ConditionFactory)

    @property
    @handle_csharp_exceptions
    def control_type(self) -> ControlType:
        """The control type of the element

        :return: Control type
        """
        return ControlType[self.raw_element.ControlType.ToString()]

    @property
    @handle_csharp_exceptions
    def framework_automation_element(self) -> Any:
        """Object which contains the native wrapper element (UIA2 or UIA3) for this element

        :return: Framework automation element
        """
        return self.raw_element.FrameworkAutomationElement

    @property
    @handle_csharp_exceptions
    def framework_type(self) -> FrameworkType:
        """The direct framework type of the element. Results in 'FrameworkType.Unknown' if it couldn't be resolved

        :return: Framework Type
        """
        raw = self.raw_element.FrameworkType  # type: ignore
        return FrameworkType.none if raw.ToString() == "None" else FrameworkType[raw.ToString()]

    @property
    @handle_csharp_exceptions
    def help_text(self) -> str:
        """The help text of this element

        :return: Help text
        """
        return self.raw_element.HelpText

    @property
    @handle_csharp_exceptions
    def is_available(self) -> bool:
        """A flag that indicates if the element is still available. Can be false if the element is already unloaded from the UI

        :return: Element availability state
        """
        return self.raw_element.IsAvailable

    @property
    @handle_csharp_exceptions
    def is_enabled(self) -> bool:
        """Flag if the element is enabled or not

        :return: Element enabled state
        """
        return self.raw_element.IsEnabled

    @property
    @handle_csharp_exceptions
    def is_offscreen(self) -> bool:
        """Flag if the element off-screen or on-screen(visible)

        :return: Offscreen flag
        """
        return self.raw_element.IsOffscreen

    @property
    @handle_csharp_exceptions
    def name(self) -> str:
        """The name of the element

        :return: Element name
        """
        return self.raw_element.Name

    @property
    @handle_csharp_exceptions
    def parent(self) -> AutomationElement:
        """Get the parent AutomationElement

        :return: Parent
        """
        return AutomationElement(raw_element=self.raw_element.Parent)

    @property
    @handle_csharp_exceptions
    def patterns(self) -> Any:
        """Standard UIA patterns of this element

        :return: UIA Patterns
        """
        return self.raw_element.Patterns

    @property
    @handle_csharp_exceptions
    def properties(self) -> Properties:
        """Standard UIA properties of this element

        :return: UIA Properties
        """
        return Properties(raw_properties=self.raw_element.Properties)


# =====================================================================================================
#   Pattern Elements Pydantic abstract models from FlaUI.Core.AutomationElements.PatternElements
# =====================================================================================================
class InvokeAutomationElement(ElementModel, abc.ABC):  # pragma: no cover
    """An element that supports the InvokePattern"""

    @handle_csharp_exceptions
    def invoke(self) -> None:
        """Invokes the element."""
        self.raw_element.Invoke()


class ToggleAutomationElement(ElementModel, abc.ABC):  # pragma: no cover
    """Class for an element that supports the TogglePattern"""

    @property
    @handle_csharp_exceptions
    def toggle_state(self) -> ToggleState:
        """Gets the current toggle state.

        :return: ToggleState
        """
        return ToggleState(self.raw_element.ToggleState)

    @toggle_state.setter
    @handle_csharp_exceptions
    def toggle_state(self, value: ToggleState) -> None:
        """Sets the current toggle state.

        :param value: ToggleState
        """
        self.raw_element.ToggleState = value.value

    @handle_csharp_exceptions
    def is_toggled(self) -> bool:
        """Gets if the element is toggled.

        :return: True if toggled, else False
        """
        return self.raw_element.IsToggled

    @handle_csharp_exceptions
    def toggle(self) -> None:
        """Toggles the element."""
        self.raw_element.Toggle()

    @handle_csharp_exceptions
    def set_toggle_state(self, required_state: bool) -> None:
        """Sets toggled state

        :param required_state: True if you need the element to be toggled, else False
        :return: None
        """
        return self.toggle() if self.is_toggled() == required_state else None


T = TypeVar("T", bound="SelectionItemAutomationElement")


class SelectionItemAutomationElement(ElementModel, abc.ABC):  # pragma: no cover
    """An element which supports the SelectionItemPattern"""

    @property
    @handle_csharp_exceptions
    def is_selected(self) -> bool:
        """Value to get/set if this element is selected.

        :return: True if element is selected, else False
        """
        return self.raw_element.IsSelected

    @handle_csharp_exceptions
    def select(self: T) -> T:
        """Selects the element.

        :return: Self
        """
        return self.__class__(raw_element=self.raw_element.Select())

    @handle_csharp_exceptions
    def add_to_selection(self: T) -> T:
        """Adds the element to the selection.

        :return: Self
        """
        return self.__class__(raw_element=self.raw_element.AddToSelection())

    @handle_csharp_exceptions
    def remove_from_selection(self: T) -> T:
        """Removes the element to the selection.

        :return: Self
        """
        return self.__class__(raw_element=self.raw_element.RemoveFromSelection())


# ================================================================================
#   Element wrappers from FlaUI.Core.AutomationElements
# ================================================================================
class AutomationElement(ElementBase):
    """UI element which can be used in automation"""

    @property
    @handle_csharp_exceptions
    def automation(self) -> Any:
        """The current used automation object.

        :return: Automation object
        """
        return self.raw_element.Automation

    # TODO: Create AutomationBase based on FlaUI.Core.AutomationBase and return that over here

    @property
    @handle_csharp_exceptions
    def item_status(self) -> str:
        """The item status of this element.

        :return: Item status value
        """
        return self.raw_element.ItemStatus

    @handle_csharp_exceptions
    def capture(self) -> Any:
        """Captures the object as screenshot in Bitmap format.

        :return: Captured element image Bitmap object
        """
        return self.raw_element.Capture()

    @handle_csharp_exceptions
    def capture_to_file(self, file_path: str) -> None:
        """Captures the object as screenshot directly into the given file.

        :param file_path: The filepath where the screenshot should be saved.
        :return: None
        """
        self.raw_element.CaptureToFile(file_path)

    @handle_csharp_exceptions
    def click(self, move_mouse: bool = False) -> None:
        """Performs a left click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly(True) or instantly(False), defaults to False
        """
        self.raw_element.Click(move_mouse)

    @handle_csharp_exceptions
    def double_click(self, move_mouse: bool = False) -> None:
        """Performs a double left click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly(True) or instantly(False), defaults to False
        """
        self.raw_element.DoubleClick(move_mouse)

    @handle_csharp_exceptions
    def draw_highlight(self, color: ColorData = Color.Red, duration: int = 2000) -> None:
        """Draw a highlight around the element with the given settings.

        :param color: Color object, defaults to ColorCollection.Red
        :param duration: Duration to highlight (in ms), defaults to 2000
        """
        self.raw_element.Automation.OverlayManager.Show(
            self.raw_element.Properties.BoundingRectangle.Value, color.cs_object, TypeCast.cs_timespan(duration)
        )

    @handle_csharp_exceptions
    def equals(self, another_element: AutomationElement) -> bool:
        """Compares two elements.

        :param other_element: Another element
        :return: True/False
        """
        return self.raw_element.Equals(another_element.raw_element)

    @handle_csharp_exceptions
    def find_all(self, tree_scope: TreeScope, condition: PropertyCondition) -> List[AutomationElement]:
        """Finds all children with the condition.

        :aram tree_scope: Treescope object
        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [
            AutomationElement(raw_element=_) for _ in self.raw_element.FindAll(tree_scope.value, condition.cs_condition)
        ]

    @handle_csharp_exceptions
    def find_all_by_x_path(self, x_path: str) -> List[AutomationElement]:
        """Finds all items which match the given xpath.

        :param x_path: Element XPath
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllByXPath(x_path)]

    @handle_csharp_exceptions
    def find_all_children(self, condition: Optional[PropertyCondition] = None) -> List[AutomationElement]:
        """Finds all children with the condition.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        if condition is None:
            return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllChildren()]
        else:
            return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllChildren(condition.cs_condition)]

    @handle_csharp_exceptions
    def find_all_descendants(self, condition: Optional[PropertyCondition] = None) -> List[AutomationElement]:
        """Finds all descendants with the condition.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        if condition is None:
            return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllDescendants()]
        else:
            return [
                AutomationElement(raw_element=_) for _ in self.raw_element.FindAllDescendants(condition.cs_condition)
            ]

    @handle_csharp_exceptions
    def find_all_nested(self, condition: PropertyCondition) -> List[AutomationElement]:
        """Finds all elements by iterating thru all conditions.

        :param condition: The search condition.
        :return: The found elements or an empty list if no elements were found.
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllNested(condition.cs_condition)]

    @handle_csharp_exceptions
    def find_all_with_options(
        self,
        tree_scope: TreeScope,
        condition: PropertyCondition,
        traversal_options: TreeTraversalOptions,
        root: AutomationElement,
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
            for _ in self.raw_element.FindAllWithOptions(
                tree_scope.value, condition.cs_condition, traversal_options.value, root.raw_element
            )
        ]

    @handle_csharp_exceptions
    def find_at(self, tree_scope: TreeScope, index: int, condition: PropertyCondition) -> AutomationElement:
        """Finds the element with the given index with the given condition.

        :param tree_scope: The scope to search.
        :param index: The index of the element to return (0-based).
        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindAt(tree_scope.value, index, condition.cs_condition))

    @handle_csharp_exceptions
    def find_child_at(self, index: int, condition: PropertyCondition) -> AutomationElement:
        """Finds the child at the given position with the condition.

        :param index: The index of the child to find.
        :param condition: The condition.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindChildAt(index, condition.cs_condition))

    @handle_csharp_exceptions
    def find_first(self, tree_scope: TreeScope, condition: PropertyCondition) -> AutomationElement:
        """Finds the first element in the given scope with the given condition.

        :param tree_scope: The scope to search.
        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirst(tree_scope.value, condition.cs_condition))

    @handle_csharp_exceptions
    def find_first_by_x_path(self, x_path: str) -> AutomationElement:
        """Finds for the first item which matches the given xpath.

        :param x_path: XPath to the element
        :return: The found element or null if no element was found.
        """
        return AutomationElement(raw_element=self.raw_element.FindFirstByXPath(x_path))

    @handle_csharp_exceptions
    def find_first_child(self, condition: Optional[PropertyCondition] = None) -> AutomationElement:
        """Finds the first child.

        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        if condition is None:
            return AutomationElement(raw_element=self.raw_element.FindFirstChild())
        else:
            return AutomationElement(raw_element=self.raw_element.FindFirstChild(condition.cs_condition))

    @handle_csharp_exceptions
    def find_first_descendant(self, condition: Optional[PropertyCondition] = None) -> AutomationElement:
        """Finds the first descendant.

        :param condition: The condition to use.
        :return: The found element or null if no element was found.
        """
        if condition is None:
            return AutomationElement(raw_element=self.raw_element.FindFirstDescendant())
        else:
            return AutomationElement(raw_element=self.raw_element.FindFirstDescendant(condition.cs_condition))

    @handle_csharp_exceptions
    def find_first_nested(self, conditions: Union[PropertyCondition, List[PropertyCondition]]) -> AutomationElement:
        """Finds the first element by iterating thru all conditions.

        C# signature: FindFirstNested(params ConditionBase[] nestedConditions)
        Iterates through children using each condition in sequence.

        :param conditions: Single condition or list of conditions to iterate through.
        :return: The found element or null if no element was found.
        """
        if isinstance(conditions, list):
            # Convert list to C# params array
            from FlaUI.Core.Conditions import ConditionBase
            from System import Array

            cs_conditions = Array[ConditionBase]([c.cs_condition for c in conditions])
            return AutomationElement(raw_element=self.raw_element.FindFirstNested(cs_conditions))
        else:
            return AutomationElement(raw_element=self.raw_element.FindFirstNested(conditions.cs_condition))

    @handle_csharp_exceptions
    def find_first_with_options(
        self, tree_scope: TreeScope, condition: PropertyCondition, traversal_options: TreeTraversalOptions, root: Any
    ) -> AutomationElement:
        """Find first matching element in the specified order.

        :param tree_scope: A combination of values specifying the scope of the search.
        :param condition: A condition that represents the criteria to match.
        :param traversal_options: Value specifying the tree navigation order.
        :param root: An element with which to begin the search.
        :return: The found element or null if no element was found.
        """
        return AutomationElement(
            raw_element=self.raw_element.FindFirstWithOptions(
                tree_scope.value, condition.cs_condition, traversal_options.value, root.raw_element
            )
        )

    @handle_csharp_exceptions
    def focus(self) -> None:
        """Sets the focus to a control. If the control is a window, brings it to the foreground"""
        self.raw_element.Focus()

    @handle_csharp_exceptions
    def focus_native(self) -> None:
        """Sets the focus by using the Win32 SetFocus() method"""
        self.raw_element.FocusNative()

    @handle_csharp_exceptions
    def get_clickable_point(self) -> Point:
        """Gets a clickable point of the element.

        :return: Clickable point object
        """
        return Point(raw_value=self.raw_element.GetClickablePoint())

    @handle_csharp_exceptions
    def get_current_metadata_value(self, property_id: Any, meta_data_id: int) -> Any:
        """Gets metadata from the UI Automation element that indicates how the information should be interpreted.

        :param property_id: The property to retrieve.
        :param meta_data_id: Specifies the type of metadata to retrieve.
        :return: The metadata.
        """
        return self.raw_element.GetCurrentMetadataValue(property_id, meta_data_id)

    @handle_csharp_exceptions
    def get_hash_code(self) -> int:
        """Fetches the hash code of the current element

        :return: Hash code
        """
        return self.raw_element.GetHashCode()

    @handle_csharp_exceptions
    def get_supported_patterns(self) -> Any:
        """Gets the available patterns for an element via properties.

        :return: Available patterns for an element via properties.
        """
        return TypeCast.py_list(self.raw_element.GetSupportedPatterns())

    @handle_csharp_exceptions
    def get_supported_patterns_direct(self) -> Any:
        """Gets the available patterns for an element via UIA method. Does not work with cached elements and might be unreliable.

        :return: Available patterns
        """
        return TypeCast.py_list(self.raw_element.GetSupportedPatternsDirect())

    @handle_csharp_exceptions
    def get_supported_properties_direct(self) -> Any:
        """Gets the available properties for an element via UIA method. Does not work with cached elements and might be unreliable.

        :return: Available properties
        """
        return TypeCast.py_list(self.raw_element.GetSupportedPropertiesDirect())

    @handle_csharp_exceptions
    def is_pattern_supported(self, pattern_id: Any) -> bool:
        """Checks if the given pattern is available for the element via properties.

        :param pattern_id: Pattern
        :return: True if supported else False
        """
        return self.raw_element.IsPatternSupported(pattern_id)

    @handle_csharp_exceptions
    def is_pattern_supported_direct(self, pattern_id: Any) -> bool:
        """Checks if the given pattern is available for the element via UIA method. Does not work with cached elements and might be unreliable.

        :param pattern_id: Pattern ID
        :return: True if supported else False
        """
        return self.raw_element.IsPatternSupportedDirect(pattern_id)

    @handle_csharp_exceptions
    def is_property_supported_direct(self, property: Any) -> bool:
        """Method to check if the element supports the given property via UIA method. Does not work with cached elements and might be unreliable.

        :param pattern_id: Pattern ID
        :return: True if supported else False
        """
        return self.raw_element.IsPropertySupportedDirect(property)

    @handle_csharp_exceptions
    def register_active_text_position_changed_event(self, tree_scope: TreeScope, action: Any) -> Any:
        """Registers a active text position changed event.

        :param tree_scope: Treescope object
        :param action: Action object
        :return: Registered event
        """
        # return self.raw_element.RegisterActiveTextPositionChangedEvent(tree_scope.value, action)
        pass

    @handle_csharp_exceptions
    def register_automation_event(self, event: Any, tree_scope: TreeScope, action: Any) -> Any:
        """Registers the given automation event.

        :param event: Event object
        :param tree_scope: Treescope object
        :param action: Action object
        :return: Registered event
        """
        # return self.raw_element.RegisterAutomationEvent(event, tree_scope, action)
        pass

    @handle_csharp_exceptions
    def register_notification_event(self) -> Any:
        """Registers a notification event.

        :return: None
        """
        # self.raw_element.RegisterNotificationEvent
        pass

    @handle_csharp_exceptions
    def register_property_changed_event(self) -> Any:
        """Registers a property changed event with the given property.

        :return: None
        """
        # self.raw_element.RegisterPropertyChangedEvent
        pass

    @handle_csharp_exceptions
    def register_structure_changed_event(self) -> Any:
        """Registers a structure changed event.

        :return: None
        """
        # self.raw_element.RegisterStructureChangedEvent
        pass

    @handle_csharp_exceptions
    def register_text_edit_text_changed_event_handler(self) -> Any:
        """Registers a text edit text changed event.

        :return: None
        """
        # self.raw_element.RegisterTextEditTextChangedEventHandler
        pass

    @handle_csharp_exceptions
    def right_click(self, move_mouse: bool = False) -> None:
        """Performs a right click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly (true) or instantly (false)., defaults to False
        """
        self.raw_element.RightClick(move_mouse)

    @handle_csharp_exceptions
    def right_double_click(self, move_mouse: bool = False) -> None:
        """Performs a double right click on the element.

        :param move_mouse: Flag to indicate, if the mouse should move slowly (true) or instantly (false)., defaults to False
        """
        self.raw_element.RightDoubleClick(move_mouse)

    @handle_csharp_exceptions
    def set_focus(self) -> None:
        """Sets the focus to a control. If the control is a window, brings it to the foreground"""
        self.raw_element.SetFocus()

    @handle_csharp_exceptions
    def set_foreground(self) -> None:
        """Brings a window to the foreground"""
        self.raw_element.SetForeground()

    @handle_csharp_exceptions
    def to_string(self) -> str:
        """Overrides the string representation of the element with something useful.

        :return: String object
        """
        return self.raw_element.ToString()

    @handle_csharp_exceptions
    def try_get_clickable_point(self) -> Tuple[bool, Point]:
        """Tries to get a clickable point of the element.

        :return: Tuple[flag, Point] - True if a point was found, false otherwise; The clickable point or null, if no point was found
        """
        flag, point = self.raw_element.TryGetClickablePoint()
        return (flag, Point(raw_value=point))

    @handle_csharp_exceptions
    def as_button(self) -> Button:
        """Converts the element to a Button.

        :return: Button element
        """
        from FlaUI.Core.AutomationElements import Button as CSButton  # pyright: ignore

        return Button(raw_element=CSButton(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_calendar(self) -> Calendar:
        """Converts the element to a Calendar.

        :return: Calendar element
        """
        from FlaUI.Core.AutomationElements import Calendar as CSCalendar  # pyright: ignore

        return Calendar(raw_element=CSCalendar(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_check_box(self) -> CheckBox:
        """Converts the element to a CheckBox.

        :return: CheckBox element
        """
        from FlaUI.Core.AutomationElements import CheckBox as CSCheckBox  # pyright: ignore

        return CheckBox(raw_element=CSCheckBox(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_combo_box(self) -> ComboBox:
        """Converts the element to a ComboBox.

        :return: ComboBox element
        """
        from FlaUI.Core.AutomationElements import ComboBox as CSComboBox  # pyright: ignore

        return ComboBox(raw_element=CSComboBox(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_data_grid_view(self) -> DataGridView:
        """Converts the element to a DataGridView.

        :return: DataGridView element
        """
        from FlaUI.Core.AutomationElements import DataGridView as CSDataGridView  # pyright: ignore

        return DataGridView(raw_element=CSDataGridView(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_date_time_picker(self) -> DateTimePicker:
        """Converts the element to a DateTimePicker.

        :return: DateTimePicker element
        """
        from FlaUI.Core.AutomationElements import DateTimePicker as CSDateTimePicker  # pyright: ignore

        return DateTimePicker(raw_element=CSDateTimePicker(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_label(self) -> Label:
        """Converts the element to a Label.

        :return: Label element
        """
        from FlaUI.Core.AutomationElements import Label as CSLabel  # pyright: ignore

        return Label(raw_element=CSLabel(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_grid(self) -> Grid:
        """Converts the element to a Grid.

        :return: Grid element
        """
        from FlaUI.Core.AutomationElements import Grid as CSGrid  # pyright: ignore

        return Grid(raw_element=CSGrid(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_grid_row(self) -> GridRow:
        """Converts the element to a GridRow.

        :return: GridRow element
        """
        from FlaUI.Core.AutomationElements import GridRow as CSGridRow  # pyright: ignore

        return GridRow(raw_element=CSGridRow(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_grid_cell(self) -> GridCell:
        """Converts the element to a GridCell.

        :return: GridCell element
        """
        from FlaUI.Core.AutomationElements import GridCell as CSGridCell  # pyright: ignore

        return GridCell(raw_element=CSGridCell(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_grid_header_item(self) -> GridHeaderItem:
        """Converts the element to a GridHeaderItem.

        :return: GridHeaderItem element
        """
        from FlaUI.Core.AutomationElements import GridHeaderItem as CSGridHeaderItem  # pyright: ignore

        return GridHeaderItem(raw_element=CSGridHeaderItem(self.framework_automation_element))

    @handle_csharp_exceptions
    # def as_horizontal_scroll_bar(self) -> HorizontalScrollBar:
    #     """Converts the element to a HorizontalScrollBar.

    #     :return: HorizontalScrollBar element
    #     """
    #     # TODO: Put in HorizontalScrollBar element and update this line
    #     from FlaUI.Core.AutomationElements import HorizontalScrollBar as CSHorizontalScrollBar  # pyright: ignore
    #     return HorizontalScrollBar(raw_element=CSHorizontalScrollBar(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_list_box(self) -> ListBox:
        """Converts the element to a ListBox.

        :return: ListBox element
        """
        from FlaUI.Core.AutomationElements import ListBox as CSListBox  # pyright: ignore

        return ListBox(raw_element=CSListBox(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_list_box_item(self) -> ListBoxItem:
        """Converts the element to a ListBoxItem.

        :return: ListBoxItem element
        """
        from FlaUI.Core.AutomationElements import ListBoxItem as CSListBoxItem  # pyright: ignore

        return ListBoxItem(raw_element=CSListBoxItem(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_menu(self) -> Menu:
        """Converts the element to a Menu.

        :return: Menu element
        """
        from FlaUI.Core.AutomationElements import Menu as CSMenu  # pyright: ignore

        return Menu(raw_element=CSMenu(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_menu_item(self) -> MenuItem:
        """Converts the element to a MenuItem.

        :return: MenuItem element
        """
        from FlaUI.Core.AutomationElements import MenuItem as CSMenuItem  # pyright: ignore

        return MenuItem(raw_element=CSMenuItem(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_progress_bar(self) -> ProgressBar:
        """Converts the element to a ProgressBar.

        :return: ProgressBar element
        """
        from FlaUI.Core.AutomationElements import ProgressBar as CSProgressBar  # pyright: ignore

        return ProgressBar(raw_element=CSProgressBar(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_radio_button(self) -> RadioButton:
        """Converts the element to a RadioButton.

        :return: RadioButton element
        """
        from FlaUI.Core.AutomationElements import RadioButton as CSRadioButton  # pyright: ignore

        return RadioButton(raw_element=CSRadioButton(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_slider(self) -> Slider:
        """Converts the element to a Slider.

        :return: Slider element
        """
        from FlaUI.Core.AutomationElements import Slider as CSSlider  # pyright: ignore

        return Slider(raw_element=CSSlider(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_spinner(self) -> Spinner:
        """Converts the element to a Spinner.

        :return: Spinner element
        """
        from FlaUI.Core.AutomationElements import Spinner as CSSpinner  # pyright: ignore

        return Spinner(raw_element=CSSpinner(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_tab(self) -> Tab:
        """Converts the element to a Tab.

        :return: Tab element
        """
        from FlaUI.Core.AutomationElements import Tab as CSTab  # pyright: ignore

        return Tab(raw_element=CSTab(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_tab_item(self) -> TabItem:
        """Converts the element to a TabItem.

        :return: TabItem element
        """
        from FlaUI.Core.AutomationElements import TabItem as CSTabItem  # pyright: ignore

        return TabItem(raw_element=CSTabItem(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_text_box(self) -> TextBox:
        """Converts the element to a TextBox.

        :return: TextBox element
        """
        from FlaUI.Core.AutomationElements import TextBox as CSTextBox  # pyright: ignore

        return TextBox(raw_element=CSTextBox(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_thumb(self) -> Thumb:
        """Converts the element to a Thumb.

        :return: Thumb element
        """
        from FlaUI.Core.AutomationElements import Thumb as CSThumb  # pyright: ignore

        return Thumb(raw_element=CSThumb(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_title_bar(self) -> TitleBar:
        """Converts the element to a TitleBar.

        :return: TitleBar element
        """
        from FlaUI.Core.AutomationElements import TitleBar as CSTitleBar  # pyright: ignore

        return TitleBar(raw_element=CSTitleBar(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_toggle_button(self) -> ToggleButton:
        """Converts the element to a ToggleButton.

        :return: ToggleButton element
        """
        from FlaUI.Core.AutomationElements import ToggleButton as CSToggleButton  # pyright: ignore

        return ToggleButton(raw_element=CSToggleButton(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_tree(self) -> Tree:
        """Converts the element to a Tree.

        :return: Tree element
        """
        from FlaUI.Core.AutomationElements import Tree as CSTree  # pyright: ignore

        return Tree(raw_element=CSTree(self.framework_automation_element))

    @handle_csharp_exceptions
    def as_tree_item(self) -> TreeItem:
        """Converts the element to a TreeItem.

        :return: TreeItem element
        """
        from FlaUI.Core.AutomationElements import TreeItem as CSTreeItem  # pyright: ignore

        return TreeItem(raw_element=CSTreeItem(self.framework_automation_element))

    @handle_csharp_exceptions
    # def as_vertical_scroll_bar(self) -> VerticalScrollBar:
    #     """Converts the element to a VerticalScrollBar.

    #     :return: VerticalScrollBar element
    #     """
    #     # TODO: Build VerticalScrollBar class and update this line
    #     return VerticalScrollBar(raw_element=self.raw_element.AsVerticalScrollBar())

    @handle_csharp_exceptions
    def as_window(self) -> Window:
        """Converts the element to a Window.

        :return: Window element
        """
        from FlaUI.Core.AutomationElements import Window as CSWindow  # pyright: ignore

        return Window(raw_element=CSWindow(self.framework_automation_element))


class Button(AutomationElement, InvokeAutomationElement):  # pragma: no cover
    """Class to interact with a button element"""

    pass


class Calendar(AutomationElement):
    """Class to interact with a calendar element. Not supported for Windows Forms calendar"""

    @property
    @handle_csharp_exceptions
    def selected_dates(self) -> List[date]:
        """Gets the selected dates in the calendar. For Win32 multiple selection calendar the returned array has two dates,
        the first date and the last date of the selected range. For WPF calendar the returned array contains all selected dates

        :return: Selected dates
        """
        return [arrow.get(_.ToString("o")).date() for _ in self.raw_element.SelectedDates]

    @handle_csharp_exceptions
    def select_date(self, date: date) -> None:
        """Deselects other selected dates and selects the specified date.

        :param date: Date object
        """
        self.raw_element.SelectDate(TypeCast.cs_datetime(date))

    @handle_csharp_exceptions
    def select_range(self, dates: List[date]) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method deselects other selected dates and selects the specified range.
        For any other type of SelectionMode it deselects other selected dates and selects only the last date in the range.
        For Win32 multiple selection calendar the "dates" parameter should contain two dates, the first and the last date of the range to be selected.
        For Win32 single selection calendar this method selects only the second date from the "dates" array.
        For WPF calendar all dates should be specified in the "dates" parameter, not only the first and the last date of the range.

        :param dates: Date ranges
        """
        self.raw_element.SelectRange([TypeCast.cs_datetime(_) for _ in dates])

    @handle_csharp_exceptions
    def add_to_selection(self, date: date) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method adds the specified date to current selection.
        For any other type of SelectionMode it deselects other selected dates and selects the specified date.
        This method is supported only for WPF calendar.

        :param date: Date object
        """
        self.raw_element.AddToSelection(TypeCast.cs_datetime(date))

    @handle_csharp_exceptions
    def add_range_to_selection(self, dates: List[date]) -> None:
        """For WPF calendar with SelectionMode="MultipleRange" this method adds the specified range to current selection.
        For any other type of SelectionMode it deselects other selected dates and selects only the last date in the range.
        This method is supported only for WPF calendar.

        :param dates: Date ranges
        """
        self.raw_element.AddRangeToSelection([TypeCast.cs_datetime(_) for _ in dates])


class CheckBox(AutomationElement, ToggleAutomationElement):
    """Class to interact with a checkbox element"""

    @property
    @handle_csharp_exceptions
    def is_checked(self) -> bool:
        """Flag if the element is checked

        :return: Element is checked
        """
        return self.raw_element.IsChecked

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the element

        :return: Element text
        """
        return self.raw_element.Text


class ComboBox(AutomationElement):
    """Class to interact with a combobox element"""

    @property
    @handle_csharp_exceptions
    def animation_duration(self) -> Any:
        """Timespan to wait until the animation for opening/closing is finished.

        :param time_span: Timespan in milliseconds, defaults to 100
        :return: C# TimeSpan object from System namespace
        """
        return self.raw_element.AnimationDuration

    @animation_duration.setter
    @handle_csharp_exceptions
    def animation_duration(self, time_span: int = 100) -> None:
        """Timespan to wait until the animation for opening/closing is finished.

        :param time_span: Timespan in milliseconds, defaults to 100
        """
        self.raw_element.AnimationDuration = TypeCast.cs_timespan(time_span)

    @property
    @handle_csharp_exceptions
    def editable_text(self) -> str:
        """The text of the editable element inside the combobox.
        Only works if the combobox is editable.

        :return: Editable text of the element
        """
        return self.raw_element.EditableText

    @editable_text.setter
    @handle_csharp_exceptions
    def editable_text(self, value: str) -> None:
        """Sets the text of the editable element inside the combobox.
        Only works if the combobox is editable.

        :param value: Text value
        """
        self.raw_element.EditableText = value

    @property
    @handle_csharp_exceptions
    def is_editable(self) -> bool:
        """Flag which indicates, if the combobox is editable or not

        :return: True If element editable, else False
        """
        return self.raw_element.IsEditable

    @property
    @handle_csharp_exceptions
    def is_read_only(self) -> bool:
        """Flag which indicates, if the combobox is read-only or not

        :return: True If element read-only, else False
        """
        return self.raw_element.IsReadOnly

    @property
    @handle_csharp_exceptions
    def value(self) -> str:
        """Selected value of the Combobox element

        :return: Element selected value
        """
        return self.raw_element.Value

    @property
    @handle_csharp_exceptions
    def selected_items(self) -> List[str]:
        """Gets all selected items

        :return: Selected items
        """
        return [ComboBoxItem(raw_element=_) for _ in self.raw_element.SelectedItems]  # type: ignore # pyright: ignore

    @property
    @handle_csharp_exceptions
    def selected_item(self) -> ComboBoxItem:
        """Gets the first selected item or null otherwise

        :return: Selected item
        """
        return ComboBoxItem(raw_element=self.raw_element.SelectedItem)

    @property
    @handle_csharp_exceptions
    def items(self) -> List[ComboBoxItem]:
        """Gets all available items from the ComboBox element

        :return: Item
        """
        return [ComboBoxItem(raw_element=_) for _ in self.raw_element.Items]  # type: ignore # pyright: ignore

    @property
    @handle_csharp_exceptions
    def expand_collapse_state(self) -> ExpandCollapseState:
        """Gets the ExpandCollapseStateof the element

        :return: Expand/Collapse state
        """
        return ExpandCollapseState(self.raw_element.ExpandCollapseState)

    @handle_csharp_exceptions
    def expand(self) -> None:
        """Expands the element"""
        self.raw_element.Expand()

    @handle_csharp_exceptions
    def collapse(self) -> None:
        """Collapses the element"""
        self.raw_element.Collapse()

    @handle_csharp_exceptions
    def select(self, value: Union[int, str]) -> ComboBoxItem:
        """Select an item by index/the first item which matches the given text..

        :param value: Index value/The text to search for
        :return: The first found item or null if no item matches.
        """
        return ComboBoxItem(raw_element=self.raw_element.Select(value))


class ComboBoxItem(AutomationElement, SelectionItemAutomationElement):  # pragma: no cover
    """Class to interact with a combobox item element."""

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the element

        :return: Element text
        """
        return self.raw_element.Text


class DataGridView(AutomationElement):
    """Class to interact with a WinForms DataGridView"""

    @property
    @handle_csharp_exceptions
    def has_add_row(self) -> bool:
        """Flag to indicate if the grid has the "Add New Item" row or not.
        /// This needs to be set as FlaUI cannot find out if this is the case or not.

        :return: True if has Add row, else False
        """
        return self.raw_element.HasAddRow

    @has_add_row.setter
    @handle_csharp_exceptions
    def has_add_row(self, value: bool) -> None:
        """Flag to indicate if the grid has the "Add New Item" row or not.

        :param value: True if has Add row, else False
        """
        self.raw_element.HasAddRow = value

    @property
    @handle_csharp_exceptions
    def header(self) -> DataGridViewHeader:
        """Gets the header element or null if the header is disabled.

        :return: DataGridViewHeader element if header element exists, else None
        """
        return DataGridViewHeader(raw_element=self.raw_element.Header)

    @property
    @handle_csharp_exceptions
    def rows(self) -> List[DataGridViewRow]:
        """Gets all the data rows.

        :return: List of DatGridViewRow elements
        """
        return [DataGridViewRow(raw_element=_) for _ in self.raw_element.Rows]  # type: ignore


class DataGridViewHeader(AutomationElement):
    """Creates a DataGridViewHeader element"""

    @property
    @handle_csharp_exceptions
    def columns(self) -> List[DataGridViewHeaderItem]:
        """Gets the header items.

        :return: List of DataGridViewHeaderItem
        """
        return [DataGridViewHeaderItem(raw_element=_) for _ in self.raw_element.Columns]


class DataGridViewHeaderItem(AutomationElement):
    """Class to interact with a WinForms DataGridView header item"""

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the header item.

        :return: DataGridViewHeaderItem text
        """
        return self.raw_element.Text


class DataGridViewRow(AutomationElement):
    """Creates a DataGridViewRow element."""

    @property
    @handle_csharp_exceptions
    def cells(self) -> List[DataGridViewCell]:
        """Gets all cells.

        :return: Cell elements
        """
        return [DataGridViewCell(raw_element=_) for _ in self.raw_element.Cells]


class DataGridViewCell(AutomationElement):
    """Class to interact with a WinForms DataGridView cell."""

    @property
    @handle_csharp_exceptions
    def value(self) -> str:
        """Value in the cell.

        :return: Cell value
        """
        return self.raw_element.Value

    @value.setter
    @handle_csharp_exceptions
    def value(self, value: str) -> None:
        """Sets the Value in the cell.

        :param value: Cell value
        """
        self.raw_element.Value = value


class DateTimePicker(AutomationElement):
    """Class to interact with a DateTimePicker element"""

    @property
    @handle_csharp_exceptions
    def selected_date(self) -> Optional[date]:
        """Gets the selected date in the DateTimePicker.
        For Win32, setting SelectedDate to null will uncheck the DateTimePicker control and disable it.
        Also for Win32, if the control is unchecked then SelectedDate will return null.

        :return: date object if exists, else None
        """
        _raw_date = self.raw_element.SelectedDate
        return arrow.get(_raw_date.Year, _raw_date.Month, _raw_date.Day).date() if _raw_date else None

    @selected_date.setter
    @handle_csharp_exceptions
    def selected_date(self, date: date) -> None:
        """Sets the selected date in the DateTimePicker.
        For Win32, setting SelectedDate to null will uncheck the DateTimePicker control and disable it.
        Also for Win32, if the control is unchecked then SelectedDate will return null.

        :return: date object if exists, else None
        """
        self.raw_element.SelectedDate = TypeCast.cs_datetime(date)


class Grid(AutomationElement):
    @property
    @handle_csharp_exceptions
    def row_count(self) -> int:
        """Gets the total row count.

        :return: Row Count
        """
        return self.raw_element.RowCount

    @property
    @handle_csharp_exceptions
    def column_count(self) -> int:
        """Gets the total column count.

        :return: Column Count
        """
        return self.raw_element.ColumnCount

    @property
    @handle_csharp_exceptions
    def column_headers(self) -> List[AutomationElement]:
        """Gets all column header elements.

        :return: List of column header elements
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.ColumnHeaders]

    @property
    @handle_csharp_exceptions
    def row_headers(self) -> List[AutomationElement]:
        """Gets all row header elements.

        :return: List of row header elements
        """
        return [AutomationElement(raw_element=_) for _ in self.raw_element.RowHeaders]

    @property
    @handle_csharp_exceptions
    def row_or_column_major(self) -> RowOrColumnMajor:
        """Gets whether the data should be read primarily by row or by column.

        :return: Row/Column
        """
        return RowOrColumnMajor(self.raw_element.RowOrColumnMajor)

    @property
    @handle_csharp_exceptions
    def header(self) -> GridHeader:
        """Gets the header item.

        :return: Header item
        """
        return GridHeader(raw_element=self.raw_element.Header)

    @property
    @handle_csharp_exceptions
    def rows(self) -> List[GridRow]:
        """Returns the rows which are currently visible to UIA. Might not be the full list (eg. in virtualized lists)!
        /// Use "GetRowByIndex" to make sure to get the correct row.

        :return: List of GridRow elements
        """
        return [GridRow(raw_element=_) for _ in self.raw_element.Rows]  # type: ignore

    @property
    @handle_csharp_exceptions
    def selected_items(self) -> List[GridRow]:
        """Gets all selected items.

        :return: List of GridRow elements
        """
        return [GridRow(raw_element=_) for _ in self.raw_element.SelectedItems]  # type: ignore

    @property
    @handle_csharp_exceptions
    def selected_item(self) -> GridRow:
        """Gets the first selected item or null otherwise.

        :return: GridRow element if selected, else None
        """
        return GridRow(raw_element=self.raw_element.SelectedItem)

    @handle_csharp_exceptions
    def _retry_while_null_reference_exception(self, func: Callable, message: str) -> Any:
        """Retries the function call if a NullReferenceException is thrown.
        Grid rows are not available immediately after the grid is loaded, so we need to retry the function call.
        Sometimes the function call is still not successful after the first retry, so we try it twice. We attempt to click on the grid before the second retry.

        :param func: Function to call
        :param message: Error message
        :return: Function result
        """
        attempts = 0
        while attempts < 2:
            try:
                return func()
            except NullReferenceException:
                # This is a workaround for a bug where the row is not yet available, Python.NET does not handle this exception correctly.
                # It rather throws a System.NullReferenceException: Object reference not set to an instance of an object.
                # This is a known issue:
                attempts += 1
                self.click()
                continue
        raise ValueError(message)

    # --- Overloads for select ---
    @overload
    def select(self, row_index: int, column_index: None = None, text_to_find: None = None) -> "GridRow": ...

    @overload
    def select(self, row_index: None = None, column_index: int = ..., text_to_find: str = ...) -> "GridRow": ...

    """Element for grids and tables"""

    @handle_csharp_exceptions
    def select(
        self, row_index: Optional[int] = None, column_index: Optional[int] = None, text_to_find: Optional[str] = None
    ) -> GridRow:
        """Select the first row by text in the given Row index or a combination of Column index along with text_to_find.

        :param row_index: Row index
        :param column_index: Column index
        :param text_to_find: Text to find in the column
        :raises ValueError: On invalid input combination
        :return: GridRow element
        """
        if all([column_index, text_to_find]):
            return GridRow(
                raw_element=self._retry_while_null_reference_exception(
                    lambda: self.raw_element.Select(column_index, text_to_find), "Row not found in column"
                )
            )
        elif all([row_index]) and not any([column_index, text_to_find]):
            return GridRow(
                raw_element=self._retry_while_null_reference_exception(
                    lambda: self.raw_element.Select(row_index), "Row not found in row index"
                )
            )

        else:
            raise ValueError("Invalid input sent to the function, cannot select the row")

    # --- Overloads for add_to_selection ---
    @overload
    def add_to_selection(self, row_index: int, column_index: None = None, text_to_find: None = None) -> "GridRow": ...

    @overload
    def add_to_selection(
        self, row_index: None = None, column_index: int = ..., text_to_find: str = ...
    ) -> "GridRow": ...

    @handle_csharp_exceptions
    def add_to_selection(
        self, row_index: Optional[int] = None, column_index: Optional[int] = None, text_to_find: Optional[str] = None
    ) -> GridRow:
        """Add a row to the selection by index or by text in the given column.

        :param row_index: Row index
        :param column_index: Column index
        :param text_to_find: Text to find in the column
        :raises ValueError: On invalid input combination
        :return: GridRow element
        """
        if all([column_index, text_to_find]):
            return GridRow(
                raw_element=self._retry_while_null_reference_exception(
                    lambda: self.raw_element.AddToSelection(column_index, text_to_find),
                    "Row not found in column, cannot add to selection",
                )
            )
        elif all([row_index]) and not any([column_index, text_to_find]):
            return GridRow(
                raw_element=self._retry_while_null_reference_exception(
                    lambda: self.raw_element.AddToSelection(row_index),
                    "Row not found in row index, cannot add to selection",
                )
            )
        else:
            raise ValueError("Invalid input sent to the function, cannot add to the selection")

    # --- Overloads for remove_from_selection ---
    @overload
    def remove_from_selection(
        self, row_index: int, column_index: None = None, text_to_find: None = None
    ) -> "GridRow": ...

    @overload
    def remove_from_selection(
        self, row_index: None = None, column_index: int = ..., text_to_find: str = ...
    ) -> "GridRow": ...
    @handle_csharp_exceptions
    def remove_from_selection(
        self, row_index: Optional[int] = None, column_index: Optional[int] = None, text_to_find: Optional[str] = None
    ) -> GridRow:
        """Remove a row to the selection by index or by text in the given column.

        :param row_index: Row index
        :param column_index: Column index
        :param text_to_find: Text to find in the column
        :raises ValueError: On invalid input combination
        :return: GridRow element
        """
        if all([column_index, text_to_find]):
            return GridRow(
                raw_element=self._retry_while_null_reference_exception(
                    lambda: self.raw_element.RemoveFromSelection(column_index, text_to_find),
                    "Row not found in column, cannot remove from selection",
                )
            )
        elif all([row_index]) and not any([column_index, text_to_find]):
            return GridRow(
                raw_element=self._retry_while_null_reference_exception(
                    lambda: self.raw_element.RemoveFromSelection(row_index),
                    "Row not found in row index, cannot remove from selection",
                )
            )
        else:
            raise ValueError("Invalid input sent to the function, cannot remove from the selection")

    @handle_csharp_exceptions
    def get_row_by_index(self, row_index: int) -> GridRow:
        """a row by index.

        :param row_index: Row index
        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.GetRowByIndex(row_index))

    @handle_csharp_exceptions
    def get_row_by_value(self, column_index: int, value: str) -> GridRow:
        """Get a row by text in the given column.

        :param column_index: Column index
        :param value: Value
        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.GetRowByValue(column_index, value))

    @handle_csharp_exceptions
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
    @handle_csharp_exceptions
    def columns(self) -> List[GridHeaderItem]:
        """Gets all header items from the grid header."""
        return [GridHeaderItem(raw_element=_) for _ in self.raw_element.Columns]


class GridHeaderItem(AutomationElement):
    """Header item for grids and tables."""

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the header item.

        :return: Text of the header item
        """
        return self.raw_element.Text


class GridRow(SelectionItemAutomationElement):
    """Row element for grids and tables."""

    @property
    @handle_csharp_exceptions
    def cells(self) -> List[GridCell]:
        """Gets all the cells from the row.

        :return: GridCell element
        """
        return [GridCell(raw_element=_) for _ in self.raw_element.Cells]

    @property
    @handle_csharp_exceptions
    def header(self) -> GridHeaderItem:
        """Gets the header item of the row.

        :return: GridHeaderItem element
        """
        return GridHeaderItem(raw_element=self.raw_element.Header)

    @handle_csharp_exceptions
    def find_cell_by_text(self, text_to_find: str) -> GridCell:
        """Find a cell by a given text.

        :param text_to_find: Text to find by
        :return: GridCell element
        """
        return GridCell(raw_element=self.raw_element.FindCellByText(text_to_find))

    @handle_csharp_exceptions
    def scroll_into_view(self) -> GridRow:
        """Scrolls the row into view.

        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.ScrollIntoView())


class GridCell(AutomationElement):
    """Cell element for grids and tables."""

    @property
    @handle_csharp_exceptions
    def containing_grid(self) -> Grid:
        """Gets the grid that contains this cell.

        :return: Grid element
        """
        return Grid(raw_element=self.raw_element.ContainingGrid)

    @property
    @handle_csharp_exceptions
    def containing_row(self) -> GridRow:
        """Gets the row that contains this cell.

        :return: GridRow element
        """
        return GridRow(raw_element=self.raw_element.ContainingRow)

    @property
    @handle_csharp_exceptions
    def value(self) -> str:
        """Gets the value of the cell.

        :return: Cell value
        """
        return self.raw_element.Value


class Label(AutomationElement):
    """Class to interact with a label element"""

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the element.

        :return: Element text
        """
        return self.raw_element.Text


class ListBox(AutomationElement):
    """Class to interact with a list box element"""

    @property
    @handle_csharp_exceptions
    def items(self) -> List[ListBoxItem]:
        """Returns all the list box items

        :return: List of ListBoxItem elements
        """
        return [ListBoxItem(raw_element=_) for _ in self.raw_element.Items]  # type: ignore

    @property
    @handle_csharp_exceptions
    def selected_items(self) -> List[ListBoxItem]:
        """Gets all selected items.

        :return: List of ListBoxItem elements
        """
        return [ListBoxItem(raw_element=_) for _ in self.raw_element.SelectedItems]  # type: ignore

    @property
    @handle_csharp_exceptions
    def selected_item(self) -> ListBoxItem:
        """Gets the first selected item or null otherwise.

        :return: ListBoxItem element if selected, else None
        """
        return ListBoxItem(raw_element=self.raw_element.SelectedItem)

    @handle_csharp_exceptions
    def select(self, value: Union[str, int]) -> ListBoxItem:
        """Selects an item by index or text.

        :param value: Text to select/Index to select by
        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.Select(value))

    @handle_csharp_exceptions
    def add_to_selection(self, value: Union[str, int]) -> ListBoxItem:
        """Add a row to the selection by index/by text.

        :param value: Text/Index
        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.AddToSelection(value))

    @handle_csharp_exceptions
    def remove_from_selection(self, value: Union[str, int]) -> ListBoxItem:
        """Remove a row to the selection by index/by text.

        :param value: Text/Index
        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.RemoveFromSelection(value))


class ListBoxItem(SelectionItemAutomationElement):
    """Class to interact with a list box item element"""

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the element.

        :return: Element text
        """
        return self.raw_element.Text

    @handle_csharp_exceptions
    def scroll_into_view(self) -> ListBoxItem:
        """Scrolls the element into view.

        :return: ListBoxItem element
        """
        return ListBoxItem(raw_element=self.raw_element.ScrollIntoView())

    @property
    @handle_csharp_exceptions
    def is_checked(self) -> bool:
        """Gets if the listbox item is checked, if checking is supported

        :return: True if checked, else False
        """
        return self.raw_element.IsChecked

    @is_checked.setter
    @handle_csharp_exceptions
    def is_checked(self, value: bool) -> None:
        """Sets if the listbox item is checked, if checking is supported

        :value: Flag to set
        :return: None
        """
        self.raw_element.IsChecked = value


class Menu(AutomationElement):
    """Class to interact with a menu or menubar element"""

    @property
    @handle_csharp_exceptions
    def items(self) -> List[MenuItem]:
        """Gets all MenuItem which are inside this element.

        :return: List of Menu Items
        """
        return [MenuItem(raw_element=_) for _ in self.raw_element.Items]  # ignore: type # pyright: ignore

    @handle_csharp_exceptions
    def get_item_by_name(self, name: str) -> MenuItem:
        """Gets the menu item by name.

        :param name: Name of the menu item
        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.Items[name])

    @property
    @handle_csharp_exceptions
    def is_win_menu(self) -> bool:
        """Flag to indicate if the containing menu is a Win32 menu because that one needs special handling

        :return: True if the menu is Win32 model, else False
        """
        return self.raw_element.IsWin32Menu

    @is_win_menu.setter
    @handle_csharp_exceptions
    def is_win_menu(self, value: bool) -> None:
        """Flag to indicate if the containing menu is a Win32 menu because that one needs special handling

        :return: True if the menu is Win32 model, else False
        """
        self.raw_element.IsWin32Menu = value


class MenuItem(AutomationElement):
    """Class to interact with a menu item element."""

    @property
    @handle_csharp_exceptions
    def is_win_menu(self) -> bool:
        """Flag to indicate if the containing menu is a Win32 menu because that one needs special handling

        :return: True if the menu is Win32 model, else False
        """
        return self.raw_element.IsWin32Menu

    @is_win_menu.setter
    @handle_csharp_exceptions
    def is_win_menu(self, value: bool) -> None:
        """Flag to indicate if the containing menu is a Win32 menu because that one needs special handling

        :return: True if the menu is Win32 model, else False
        """
        self.raw_element.IsWin32Menu = value

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the element

        :return: Element text
        """
        return self.raw_element.Text

    @property
    @handle_csharp_exceptions
    def items(self) -> List[MenuItem]:
        """Gets all MenuItem which are inside this element.

        :return: MenuItems
        """
        return [MenuItem(raw_element=_) for _ in self.raw_element.Items]

    @handle_csharp_exceptions
    def invoke(self) -> MenuItem:
        """Invokes the element.

        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.Invoke())

    @handle_csharp_exceptions
    def expand(self) -> MenuItem:
        """Expands the element.

        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.Expand())

    @handle_csharp_exceptions
    def collapse(self) -> MenuItem:
        """Collapses the element.

        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.Collapse())

    @property
    @handle_csharp_exceptions
    def is_checked(self) -> bool:
        """Gets if a menu item is checked or unchecked, if checking is supported.
        /// For some applications, like WPF, setting this property doesn't execute the action that happens when a user clicks the menu item, only the checked state is changed.
        /// For WPF and Windows Forms applications, if you want to execute the action too, you need to use Invoke() method.

        :return: True if checked, else False
        """
        return self.raw_element.IsChecked

    @is_checked.setter
    @handle_csharp_exceptions
    def is_checked(self, value: bool) -> None:
        """Sets if a menu item is checked or unchecked, if checking is supported.
        /// For some applications, like WPF, setting this property doesn't execute the action that happens when a user clicks the menu item, only the checked state is changed.
        /// For WPF and Windows Forms applications, if you want to execute the action too, you need to use Invoke() method.

        :value: Flag to set
        :return: None
        """
        self.raw_element.IsChecked = value

    @handle_csharp_exceptions
    def set_is_checked(self, value: bool) -> None:
        """Sets if a menu item is checked or unchecked, if checking is supported.
        /// For some applications, like WPF, setting this property doesn't execute the action that happens when a user clicks the menu item, only the checked state is changed.
        /// For WPF and Windows Forms applications, if you want to execute the action too, you need to use Invoke() method.

        :value: Flag to set
        :return: None
        """
        self.raw_element.IsChecked(value)

    @handle_csharp_exceptions
    def get_item_by_name(self, name: str) -> MenuItem:
        """Gets the menu item by name.

        :param name: Name of the menu item
        :return: MenuItem element
        """
        return MenuItem(raw_element=self.raw_element.Items[name])


class ProgressBar(AutomationElement):
    """Class to interact with a progressbar element"""

    @property
    @handle_csharp_exceptions
    def minimum(self) -> float:
        """Gets the minimum value.

        :return: Value
        """
        return float(self.raw_element.Minimum)

    @property
    @handle_csharp_exceptions
    def maximum(self) -> float:
        """Gets the maximum value.

        :return: Value
        """
        return float(self.raw_element.Maximum)

    @property
    @handle_csharp_exceptions
    def value(self) -> float:
        """Gets the current value.

        :return: Value
        """
        return float(self.raw_element.Value)


class RadioButton(AutomationElement):
    """Class to interact with a radiobutton element"""

    @property
    @handle_csharp_exceptions
    def is_checked(self) -> bool:
        """Flag to get the selection of this element.

        :return: True if element is checked, else False
        """
        return self.raw_element.IsChecked

    @is_checked.setter
    @handle_csharp_exceptions
    def is_checked(self, value: bool) -> None:
        """Flag to set the selection of this element.

        :value: True if element is checked, else False
        """
        self.raw_element.IsChecked = value


class Slider(AutomationElement):
    """Class to interact with a slider element"""

    @property
    @handle_csharp_exceptions
    def minimum(self) -> float:
        """The minimum value.

        :return: Minimum value
        """
        return self.raw_element.Minimum

    @property
    @handle_csharp_exceptions
    def maximum(self) -> float:
        """The maximum value.

        :return: Maximum value
        """
        return self.raw_element.Maximum

    @property
    @handle_csharp_exceptions
    def small_change(self) -> float:
        """The value of a small change.

        :return: Small change
        """
        return self.raw_element.SmallChange

    @property
    @handle_csharp_exceptions
    def large_change(self) -> float:
        """The value of a large change.

        :return: Large change
        """
        return self.raw_element.LargeChange

    @handle_csharp_exceptions
    def large_increase_button(self) -> Button:
        """The button element used to perform a large increment.

        :return: Button element
        """
        return Button(raw_element=self.raw_element.LargeIncreaseButton())

    @handle_csharp_exceptions
    def large_decrease_button(self) -> Button:
        """The button element used to perform a large decrement.

        :return: Button element
        """
        return Button(raw_element=self.raw_element.LargeDecreaseButton())

    @property
    @handle_csharp_exceptions
    def thumb(self) -> Thumb:
        """The element used to drag.

        :return: Thumb element
        """
        return Thumb(raw_element=self.raw_element.Thumb)

    @property
    @handle_csharp_exceptions
    def is_only_value(self) -> bool:
        """Flag which indicates if the Slider supports range values (min->max) or only values (0-100).
        Only values are for example used when combining UIA3 and WinForms applications.

        :return: True if only value else False
        """
        return self.raw_element.IsOnlyValue

    @property
    @handle_csharp_exceptions
    def value(self) -> float:
        """Gets the current value.

        :return: Value of the element
        """
        return self.raw_element.Value

    @value.setter
    @handle_csharp_exceptions
    def value(self, value: float) -> None:
        """Sets the value of the slider

        :param value: Value to set
        """
        self.raw_element.Value = value

    @handle_csharp_exceptions
    def small_increment(self):
        """Performs a small increment."""
        self.raw_element.SmallIncrement()

    @handle_csharp_exceptions
    def small_decrement(self):
        """Performs a small decrement."""
        self.raw_element.SmallDecrement()

    @handle_csharp_exceptions
    def large_increment(self):
        """Performs a large increment."""
        self.raw_element.LargeIncrement()

    @handle_csharp_exceptions
    def large_decrement(self):
        """Performs a large decrement."""
        self.raw_element.LargeDecrement()


class Spinner(AutomationElement):
    """Class to interact with a WinForms spinner element"""

    @property
    @handle_csharp_exceptions
    def minimum(self) -> float:
        """The minimum value.

        :return: Minimum value
        """
        return self.raw_element.Minimum

    @property
    @handle_csharp_exceptions
    def maximum(self) -> float:
        """The maximum value.

        :return: Maximum value
        """
        return self.raw_element.Maximum

    @property
    @handle_csharp_exceptions
    def small_change(self) -> float:
        """The value of a small change.

        :return: Small change
        """
        return self.raw_element.SmallChange

    @handle_csharp_exceptions
    def increase_button(self) -> Button:
        """The button element used to perform a large increment.

        :return: Button element
        """
        return Button(raw_element=self.raw_element.IncreaseButton())

    @handle_csharp_exceptions
    def decrease_button(self) -> Button:
        """The button element used to perform a large decrement.

        :return: Button element
        """
        return Button(raw_element=self.raw_element.DecreaseButton())

    @property
    @handle_csharp_exceptions
    def is_only_value(self) -> bool:
        """Flag which indicates if the Slider supports range values (min->max) or only values (0-100).
        Only values are for example used when combining UIA3 and WinForms applications.

        :return: True if only value else False
        """
        return self.raw_element.IsOnlyValue

    @property
    @handle_csharp_exceptions
    def value(self) -> float:
        """Gets the current value.

        :return: Value of the element
        """
        return self.raw_element.Value

    @value.setter
    @handle_csharp_exceptions
    def value(self, value: float) -> None:
        """Sets the value of the spinner

        :param value: Value to set
        """
        self.raw_element.Value = value

    @handle_csharp_exceptions
    def increment(self):
        """Performs a increment."""
        self.raw_element.Increment()

    @handle_csharp_exceptions
    def decrement(self):
        """Performs a decrement."""
        self.raw_element.Decrement()


class Tab(AutomationElement):
    """Class to interact with a tab element."""

    @handle_csharp_exceptions
    def selected_tab_item(self) -> TabItem:
        """The currently selected TabItem

        :return: TabItem element
        """
        return TabItem(raw_element=self.raw_element.SelectedTabItem)

    @property
    @handle_csharp_exceptions
    def selected_tab_item_index(self) -> int:
        """The index of the currently selected TabItem

        :return: Selected index
        """
        return self.raw_element.SelectedTabItemIndex

    @property
    @handle_csharp_exceptions
    def tab_items(self) -> List[TabItem]:
        """All TabItem objects from this Tab

        :return: List of TabItem elements
        """
        return [TabItem(raw_element=_) for _ in self.raw_element.TabItems]

    @overload
    def select_tab_item(self, index: int, value: None = None) -> None: ...

    @overload
    def select_tab_item(self, index: None = None, value: str = ...) -> None: ...

    @handle_csharp_exceptions
    def select_tab_item(self, index: Optional[int] = None, value: Optional[str] = None) -> None:
        """Selects a TabItem by index

        :param index: Selects by index value
        :param value: Selects by tab value
        """
        if index is None and value is None:
            raise ValueError("Either index or value have to be set for selected TabItem")
        try:
            self.raw_element.SelectTabItem(index) if index is not None else self.raw_element.SelectTabItem(value)
        except Exception as e:
            logger.error(e)


class TabItem(AutomationElement, SelectionItemAutomationElement):
    """Class to interact with a tabitem element."""

    pass


class TextBox(AutomationElement):
    """Class to interact with a textbox element."""

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the element.

        :return: Element text
        """
        return self.raw_element.Text

    @text.setter
    @handle_csharp_exceptions
    def text(self, value: str) -> None:
        """Sets the text of the element

        :param value: Value to set
        """
        self.raw_element.Text = value

    @property
    @handle_csharp_exceptions
    def is_read_only(self) -> bool:
        """Gets if the element is read only or not.

        :return: True if element is read only else False
        """
        return self.raw_element.IsReadOnly

    @handle_csharp_exceptions
    def enter(self, value: str):
        """Simulate typing in text. This is slower than setting Text but raises more events.

        :param value: Value to enter in the element
        """
        self.raw_element.Enter(value)


class Thumb(AutomationElement):
    """Class to interact with a thumb element."""

    @handle_csharp_exceptions
    def slide_horizontally(self, distance: int):
        """Moves the slider horizontally.

        :param distance: The distance to move the slider, + for right, - for left.
        """
        self.raw_element.SlideHorizontally(distance)

    @handle_csharp_exceptions
    def slide_vertically(self, distance: int):
        """Moves the slider vertically.

        :param distance: The distance to move the slider, + for down, - for up.
        """
        self.raw_element.SlideVertically(distance)


class TitleBar(AutomationElement):
    """Class to interact with a titlebar element."""

    @handle_csharp_exceptions
    def minimize_button(self) -> Button:
        """Gets the minimize button element.

        :return: Minimize button
        """
        return Button(raw_element=self.raw_element.MinimizeButton())

    @handle_csharp_exceptions
    def maximize_button(self) -> Button:
        """Gets the maximize button element.

        :return: Maximize button
        """
        return Button(raw_element=self.raw_element.MaximizeButton())

    @handle_csharp_exceptions
    def restore_button(self) -> Button:
        """Gets the restore button element.

        :return: Restore button
        """
        return Button(raw_element=self.raw_element.RestoreButton())

    @handle_csharp_exceptions
    def close_button(self) -> Button:
        """Gets the close button element.

        :return: Close button
        """
        return Button(raw_element=self.raw_element.CloseButton())


class ToggleButton(AutomationElement):
    """Class to interact with a toggle button element."""

    @handle_csharp_exceptions
    def toggle(self):
        """Toggles the toggle button.
        **Note**: In some WPF scenarios, the bounded command might not be fired. Use AutomationElement.Click instead in that case.
        """
        self.raw_element.Toggle()


class Tree(AutomationElement):
    """Class to interact with a tree element."""

    @property
    @handle_csharp_exceptions
    def selected_tree_item(self) -> TreeItem:
        """The currently selected TreeItem" />

        :return: TreeItem element of selected tree item
        """
        return TreeItem(raw_element=self.raw_element.SelectedTreeItem)

    @property
    @handle_csharp_exceptions
    def items(self) -> List[TreeItem]:
        """All child TreeItem" /> objects from this Tree" />

        :return: List of TreeItem elements
        """
        return [TreeItem(raw_element=_) for _ in self.raw_element.Items]


class TreeItem(AutomationElement):
    """Class to interact with a treeitem element."""

    @property
    @handle_csharp_exceptions
    def items(self) -> List[TreeItem]:
        """All child TreeItem" /> objects from this TreeItem" />.

        :return: List of TreeItem elements
        """
        return [TreeItem(raw_element=_) for _ in self.raw_element.Items]

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """The text of the TreeItem" />.

        :return: Text value of element
        """
        return self.raw_element.Text

    @property
    @handle_csharp_exceptions
    def is_selected(self) -> bool:
        """Value to get/set if this element is selected.

        :return: True if selected else False
        """
        return self.raw_element.IsSelected

    @property
    @handle_csharp_exceptions
    def expand_collapse_state(self) -> ExpandCollapseState:
        """Gets the current expand / collapse state.

        :return: Current state enum object
        """
        return ExpandCollapseState(self.raw_element.ExpandCollapseState)

    @handle_csharp_exceptions
    def expand(self):
        """Expands the element."""
        self.raw_element.Expand()

    @handle_csharp_exceptions
    def collapse(self):
        """Collapses the element."""
        self.raw_element.Collapse()

    @handle_csharp_exceptions
    def select(self):
        """Selects the element."""
        self.raw_element.Select()

    @handle_csharp_exceptions
    def add_to_selection(self) -> TreeItem:
        """Add the element to the selection.

        :return: TreeItem element
        """
        return TreeItem(raw_element=self.raw_element.AddToSelection())

    @handle_csharp_exceptions
    def remove_from_selection(self) -> TreeItem:
        """Remove the element to the selection.

        :return: TreeItem element
        """
        return TreeItem(raw_element=self.raw_element.RemoveFromSelection())

    @property
    @handle_csharp_exceptions
    def is_checked(self) -> bool:
        """Gets if the tree item is checked, if checking is supported.

        :return: True if checked else False
        """
        return self.raw_element.IsChecked

    @is_checked.setter
    @handle_csharp_exceptions
    def is_checked(self, value: bool) -> None:
        """Sets the tree item as checked, if checking is supported

        :param value: Value to set, True/False
        """
        self.raw_element.IsChecked = value


class Window(AutomationElement):
    """Class to interact with a window element."""

    @property
    @handle_csharp_exceptions
    def title(self) -> str:
        """Gets the title of the window.

        :return: Title value
        """
        return self.raw_element.Title

    @property
    @handle_csharp_exceptions
    def is_modal(self) -> bool:
        """Gets if the window is modal.

        :return: True if window is modal, else False
        """
        return self.raw_element.IsModal

    @property
    @handle_csharp_exceptions
    def title_bar(self) -> TitleBar:
        """Gets the TitleBar of the window.

        :return: Title bar element
        """
        return TitleBar(raw_element=self.raw_element.TitleBar)

    @property
    @handle_csharp_exceptions
    def is_main_window(self) -> bool:
        """Flag to indicate, if the window is the application's main window.
        Is used so that it does not need to be looked up again in some cases (e.g. Context Menu).

        :return: True if the window is main window else False
        """
        return self.raw_element.IsMainWindow

    @is_main_window.setter
    @handle_csharp_exceptions
    def is_main_window(self, value: bool) -> None:
        """Flag to indicate, if the window is the application's main window.
        Is used so that it does not need to be looked up again in some cases (e.g. Context Menu).

        :return: True if the window is main window else False
        """
        self.raw_element.IsMainWindow = value

    @handle_csharp_exceptions
    def modal_windows(self) -> List[Window]:
        """Gets a list of all modal child windows.

        :return: List of window elements
        """
        return [Window(raw_element=_) for _ in self.raw_element.ModalWindows()]

    @property
    @handle_csharp_exceptions
    def popup(self) -> Window:
        """Gets the current WPF popup window.

        :return: Pop up window
        """
        return Window(raw_element=self.raw_element.Popup)

    @property
    @handle_csharp_exceptions
    def context_menu(self) -> Menu:
        """Gets the context menu for the window.
        /// Note: It uses the FrameworkType of the window as lookup logic. Use GetContextMenuByFrameworkType" /> if you want to control this.

        :return: Context menu item
        """
        return Menu(raw_element=self.raw_element.ContextMenu)

    @handle_csharp_exceptions
    def get_context_menu_by_framework_type(self, framework_type: FrameworkType) -> Menu:
        """Gets the context menu by a given FrameworkType.

        :param framework_type: Framework Type
        :return: Menu item
        """
        return Menu(raw_element=self.raw_element.GetContextMenuByFrameworkType(framework_type))

    @handle_csharp_exceptions
    def close(self):
        """Closes the window."""
        self.raw_element.Close()

    @handle_csharp_exceptions
    def move(self, x: int, y: int):
        """Moves the window to the given coordinates.

        :param x: X cordinate
        :param y: Y cordinate
        """
        self.raw_element.Move(x, y)

    @handle_csharp_exceptions
    def set_transparency(self, alpha: bytes):
        """Brings the element to the foreground.

        :param alpha: Transparency value
        """
        self.raw_element.SetTransparency(alpha)


class IAutomationProperty(BaseModel, abc.ABC):
    """Interface for an automation property."""

    @property
    @abc.abstractmethod
    @handle_csharp_exceptions
    def value(self) -> Any:
        """Gets the value of the automation property."""
        pass

    @property
    @abc.abstractmethod
    @handle_csharp_exceptions
    def value_or_default(self) -> Any:
        """Gets the value of the automation property or a default value if not available."""
        pass

    @abc.abstractmethod
    @handle_csharp_exceptions
    def try_get_value(self) -> Tuple[bool, str]:
        """Tries to get the value of the automation property.

        :return: A tuple with the first element being True if the value was retrieved successfully, False otherwise.
        """
        pass

    @property
    @abc.abstractmethod
    @handle_csharp_exceptions
    def is_supported(self) -> bool:
        """Checks if the automation property is supported."""
        pass


class AutomationProperty(IAutomationProperty):
    raw_property: Any

    @property
    @handle_csharp_exceptions
    def framework_automation_element(self) -> AutomationElement:
        """Returns the FrameworkAutomationElement of the property.

        :return: The FrameworkAutomationElement of the property.
        """
        return AutomationElement(raw_element=self.raw_property.FrameworkAutomationElement)

    @property
    @handle_csharp_exceptions
    def is_supported(self) -> bool:
        """Returns if the property is supported.

        :return: True if the property is supported, False otherwise.
        """
        return self.raw_property.IsSupported

    @property
    @handle_csharp_exceptions
    def property_id(self) -> str:
        """Returns the property ID.

        :return: The property ID.
        """
        return self.raw_property.PropertyId.Id

    @property
    @handle_csharp_exceptions
    def to_string(self) -> str:
        """Returns the string representation of the property.

        :return: The string representation of the property.
        """
        return self.raw_property.ToString()

    @staticmethod
    @handle_csharp_exceptions
    def cast_to_py_wrapper(value):
        """Casts any possible value to Python equivalent wrapper if available

        :param value: Value to cast
        :return: Parsed value or raw Value
        """
        if isinstance(value, CSColor):
            return ColorData(cs_object=value)
        elif isinstance(value, CSPoint):
            return Point(raw_value=value)
        elif isinstance(value, CSSize):
            return Size(raw_value=value)
        elif isinstance(value, CSRectangle):
            return Rectangle(raw_value=value)
        else:
            return value

    @property
    @handle_csharp_exceptions
    def value(self) -> Any:
        """Returns the value of the property.

        :return: The value of the property.
        """
        return self.cast_to_py_wrapper(self.raw_property.Value)

    @property
    @handle_csharp_exceptions
    def value_or_default(self) -> Any:
        """Returns the value of the property or a default value if the value is None.

        :return: The value of the property or a default value if the value is None.
        """
        return self.cast_to_py_wrapper(self.raw_property.ValueOrDefault)

    @handle_csharp_exceptions
    def try_get_value(self) -> Tuple[bool, str]:
        """Tries to get the value of the property.

        :return: A tuple with the first element being True if the value was retrieved successfully, False otherwise.
        """
        return self.raw_property.TryGetValue()

    @handle_csharp_exceptions
    def __eq__(self, other) -> bool:
        """
        Checks if the current AutomationProperty is equal to another AutomationProperty.

        :param other: Another AutomationProperty object to compare with.
        :return: True if the current AutomationProperty is equal to the other AutomationProperty, False otherwise.
        """
        if isinstance(other, AutomationProperty):
            return self.value == other.value  # pyright: ignore
        return False

    @handle_csharp_exceptions
    def __str__(self):
        return str(self.value_or_default)


class Properties(BaseModel):
    raw_properties: Any

    @property
    @handle_csharp_exceptions
    def accelerator_key(self) -> AutomationProperty:
        """Returns the AcceleratorKey of the property.

        :return: The AcceleratorKey of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.AcceleratorKey)

    @property
    @handle_csharp_exceptions
    def access_key(self) -> AutomationProperty:
        """Returns the AccessKey of the property.

        :return: The AccessKey of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.AccessKey)

    @property
    @handle_csharp_exceptions
    def annotation_objects(self) -> AutomationProperty:
        """Returns the AnnotationObjects of the property.

        :return: The AnnotationObjects of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.AnnotationObjects)

    @property
    @handle_csharp_exceptions
    def annotation_types(self) -> AutomationProperty:
        """Returns the AnnotationTypes of the property.

        :return: The AnnotationTypes of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.AnnotationTypes)

    @property
    @handle_csharp_exceptions
    def aria_properties(self) -> AutomationProperty:
        """Returns the AriaProperties of the property.

        :return: The AriaProperties of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.AriaProperties)

    @property
    @handle_csharp_exceptions
    def aria_role(self) -> AutomationProperty:
        """Returns the AriaRole of the property.

        :return: The AriaRole of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.AriaRole)

    @property
    @handle_csharp_exceptions
    def automation_id(self) -> AutomationProperty:
        """Returns the AutomationId of the property.

        :return: The AutomationId of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.AutomationId)

    @property
    @handle_csharp_exceptions
    def bounding_rectangle(self) -> AutomationProperty:
        """Returns the BoundingRectangle of the property.

        :return: The BoundingRectangle of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.BoundingRectangle)

    @property
    @handle_csharp_exceptions
    def center_point(self) -> AutomationProperty:
        """Returns the CenterPoint of the property.

        :return: The CenterPoint of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.CenterPoint)

    @property
    @handle_csharp_exceptions
    def class_name(self) -> AutomationProperty:
        """Returns the ClassName of the property.

        :return: The ClassName of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.ClassName)

    @property
    @handle_csharp_exceptions
    def clickable_point(self) -> AutomationProperty:
        """Returns the ClickablePoint of the property.

        :return: The ClickablePoint of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.ClickablePoint)

    @property
    @handle_csharp_exceptions
    def controller_for(self) -> AutomationProperty:
        """Returns the ControllerFor of the property.

        :return: The ControllerFor of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.ControllerFor)

    @property
    @handle_csharp_exceptions
    def control_type(self) -> AutomationProperty:
        """Returns the ControlType of the property.

        :return: The ControlType of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.ControlType)

    @property
    @handle_csharp_exceptions
    def culture(self) -> AutomationProperty:
        """Returns the Culture of the property.

        :return: The Culture of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.Culture)

    @property
    @handle_csharp_exceptions
    def described_by(self) -> AutomationProperty:
        """Returns the DescribedBy of the property.

        :return: The DescribedBy of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.DescribedBy)

    @property
    @handle_csharp_exceptions
    def fill_color(self) -> AutomationProperty:
        """Returns the FillColor of the property.

        :return: The FillColor of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.FillColor)

    @property
    @handle_csharp_exceptions
    def fill_type(self) -> AutomationProperty:
        """Returns the FillType of the property.

        :return: The FillType of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.FillType)

    @property
    @handle_csharp_exceptions
    def flows_from(self) -> AutomationProperty:
        """Returns the FlowsFrom of the property.

        :return: The FlowsFrom of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.FlowsFrom)

    @property
    @handle_csharp_exceptions
    def flows_to(self) -> AutomationProperty:
        """Returns the FlowsTo of the property.

        :return: The FlowsTo of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.FlowsTo)

    @property
    @handle_csharp_exceptions
    def framework_id(self) -> AutomationProperty:
        """Returns the FrameworkId of the property.

        :return: The FrameworkId of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.FrameworkId)

    @property
    @handle_csharp_exceptions
    def full_description(self) -> AutomationProperty:
        """Returns the FullDescription of the property.

        :return: The FullDescription of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.FullDescription)

    @property
    @handle_csharp_exceptions
    def has_keyboard_focus(self) -> AutomationProperty:
        """Returns the HasKeyboardFocus of the property.

        :return: The HasKeyboardFocus of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.HasKeyboardFocus)

    @property
    @handle_csharp_exceptions
    def heading_level(self) -> AutomationProperty:
        """Returns the HeadingLevel of the property.

        :return: The HeadingLevel of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.HeadingLevel)

    @property
    @handle_csharp_exceptions
    def help_text(self) -> AutomationProperty:
        """Returns the HelpText of the property.

        :return: The HelpText of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.HelpText)

    @property
    @handle_csharp_exceptions
    def is_content_element(self) -> AutomationProperty:
        """Returns the IsContentElement of the property.

        :return: The IsContentElement of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsContentElement)

    @property
    @handle_csharp_exceptions
    def is_control_element(self) -> AutomationProperty:
        """Returns the IsControlElement of the property.

        :return: The IsControlElement of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsControlElement)

    @property
    @handle_csharp_exceptions
    def is_data_valid_for_form(self) -> AutomationProperty:
        """Returns the IsDataValidForForm of the property.

        :return: The IsDataValidForForm of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsDataValidForForm)

    @property
    @handle_csharp_exceptions
    def is_dialog(self) -> AutomationProperty:
        """Returns the IsDialog of the property.

        :return: The IsDialog of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsDialog)

    @property
    @handle_csharp_exceptions
    def is_enabled(self) -> AutomationProperty:
        """Returns the IsEnabled of the property.

        :return: The IsEnabled of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsEnabled)

    @property
    @handle_csharp_exceptions
    def is_keyboard_focusable(self) -> AutomationProperty:
        """Returns the IsKeyboardFocusable of the property.

        :return: The IsKeyboardFocusable of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsKeyboardFocusable)

    @property
    @handle_csharp_exceptions
    def is_offscreen(self) -> AutomationProperty:
        """Returns the IsOffscreen of the property.

        :return: The IsOffscreen of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsOffscreen)

    @property
    @handle_csharp_exceptions
    def is_password(self) -> AutomationProperty:
        """Returns the IsPassword of the property.

        :return: The IsPassword of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsPassword)

    @property
    @handle_csharp_exceptions
    def is_peripheral(self) -> AutomationProperty:
        """Returns the IsPeripheral of the property.

        :return: The IsPeripheral of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsPeripheral)

    @property
    @handle_csharp_exceptions
    def is_required_for_form(self) -> AutomationProperty:
        """Returns the IsRequiredForForm of the property.

        :return: The IsRequiredForForm of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.IsRequiredForForm)

    @property
    @handle_csharp_exceptions
    def item_status(self) -> AutomationProperty:
        """Returns the ItemStatus of the property.

        :return: The ItemStatus of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.ItemStatus)

    @property
    @handle_csharp_exceptions
    def item_type(self) -> AutomationProperty:
        """Returns the ItemType of the property.

        :return: The ItemType of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.ItemType)

    @property
    @handle_csharp_exceptions
    def labeled_by(self) -> AutomationProperty:
        """Returns the LabeledBy of the property.

        :return: The LabeledBy of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.LabeledBy)

    @property
    @handle_csharp_exceptions
    def landmark_type(self) -> AutomationProperty:
        """Returns the LandmarkType of the property.

        :return: The LandmarkType of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.LandmarkType)

    @property
    @handle_csharp_exceptions
    def level(self) -> AutomationProperty:
        """Returns the Level of the property.

        :return: The Level of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.Level)

    @property
    @handle_csharp_exceptions
    def live_setting(self) -> AutomationProperty:
        """Returns the LiveSetting of the property.

        :return: The LiveSetting of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.LiveSetting)

    @property
    @handle_csharp_exceptions
    def localized_control_type(self) -> AutomationProperty:
        """Returns the LocalizedControlType of the property.

        :return: The LocalizedControlType of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.LocalizedControlType)

    @property
    @handle_csharp_exceptions
    def localized_landmark_type(self) -> AutomationProperty:
        """Returns the LocalizedLandmarkType of the property.

        :return: The LocalizedLandmarkType of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.LocalizedLandmarkType)

    @property
    @handle_csharp_exceptions
    def name(self) -> AutomationProperty:
        """Returns the Name of the property.

        :return: The Name of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.Name)

    @property
    @handle_csharp_exceptions
    def native_window_handle(self) -> AutomationProperty:
        """Returns the NativeWindowHandle of the property.

        :return: The NativeWindowHandle of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.NativeWindowHandle)

    @property
    @handle_csharp_exceptions
    def optimize_for_visual_content(self) -> AutomationProperty:
        """Returns the OptimizeForVisualContent of the property.

        :return: The OptimizeForVisualContent of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.OptimizeForVisualContent)

    @property
    @handle_csharp_exceptions
    def orientation(self) -> AutomationProperty:
        """Returns the Orientation of the property.

        :return: The Orientation of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.Orientation)

    @property
    @handle_csharp_exceptions
    def outline_color(self) -> AutomationProperty:
        """Returns the OutlineColor of the property.

        :return: The OutlineColor of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.OutlineColor)

    @property
    @handle_csharp_exceptions
    def outline_thickness(self) -> AutomationProperty:
        """Returns the OutlineThickness of the property.

        :return: The OutlineThickness of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.OutlineThickness)

    @property
    @handle_csharp_exceptions
    def position_in_set(self) -> AutomationProperty:
        """Returns the PositionInSet of the property.

        :return: The PositionInSet of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.PositionInSet)

    @property
    @handle_csharp_exceptions
    def process_id(self) -> AutomationProperty:
        """Returns the ProcessId of the property.

        :return: The ProcessId of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.ProcessId)

    @property
    @handle_csharp_exceptions
    def provider_description(self) -> AutomationProperty:
        """Returns the ProviderDescription of the property.

        :return: The ProviderDescription of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.ProviderDescription)

    @property
    @handle_csharp_exceptions
    def rotation(self) -> AutomationProperty:
        """Returns the Rotation of the property.

        :return: The Rotation of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.Rotation)

    @property
    @handle_csharp_exceptions
    def runtime_id(self) -> AutomationProperty:
        """Returns the RuntimeId of the property.

        :return: The RuntimeId of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.RuntimeId)

    @property
    @handle_csharp_exceptions
    def size(self) -> AutomationProperty:
        """Returns the Size of the property.

        :return: The Size of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.Size)

    @property
    @handle_csharp_exceptions
    def size_of_set(self) -> AutomationProperty:
        """Returns the SizeOfSet of the property.

        :return: The SizeOfSet of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.SizeOfSet)

    @property
    @handle_csharp_exceptions
    def visual_effects(self) -> AutomationProperty:
        """Returns the VisualEffects of the property.

        :return: The VisualEffects of the property.
        """
        return AutomationProperty(raw_property=self.raw_properties.VisualEffects)
