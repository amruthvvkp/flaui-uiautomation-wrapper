"""
This module contains a helper class with some commonly used conditions for FlaUI automation framework.
It defines two classes: PropertyCondition and ConditionFactory.

PropertyCondition is a Pydantic BaseModel that wraps a PropertyCondition object from FlaUI.Core.Conditions module.
It provides methods to create and combine conditions, compare values, and get property and value of the condition.

ConditionFactory is also a Pydantic BaseModel that wraps a ConditionFactory object from FlaUI.Core.Conditions module.
It provides methods to create PropertyConditions based on automation id, control type, class name, name, and text.
"""

from __future__ import annotations

from typing import Any, Union

from FlaUI.Core.Conditions import (  # pyright: ignore
    AndCondition as CSAndCondition,
    ConditionFactory as CSConditionFactory,
    NotCondition as CSNotCondition,
    OrCondition as CSOrCondition,
    PropertyCondition as CSPropertyCondition,
)
from pydantic import BaseModel, ConfigDict

from flaui.core.definitions import ControlType, PropertyConditionFlags
from flaui.core.framework_types import FrameworkType
from flaui.lib.enums import KnownClassNames


class PropertyCondition(BaseModel):
    """PropertyCondition wraps a PropertyCondition object from FlaUI.Core.Conditions module. This class provides methods to create and combine conditions, compare values, and get property and value of the condition."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    cs_condition: Union[CSPropertyCondition, CSOrCondition, CSAndCondition, CSNotCondition]

    def And(self, new_condition: PropertyCondition) -> PropertyCondition:
        """Adds the given condition with an "and".

        :param new_condition: New condition
        :return: PropertyCondition
        """
        return PropertyCondition(cs_condition=self.cs_condition.And(new_condition.cs_condition))

    def Equals(self, value: PropertyCondition) -> bool:
        """Compares the value to another value

        :param value: Value to compare
        :return: True/False
        """
        return self.cs_condition.Equals(value.cs_condition.cs_condition)

    def Not(self, new_condition: PropertyCondition) -> PropertyCondition:
        """Adds the given condition with an "not".

        :param new_condition: New condition
        :return: PropertyCondition
        """
        return PropertyCondition(cs_condition=self.cs_condition.Not(new_condition.cs_condition))

    def Or(self, new_condition: PropertyCondition) -> PropertyCondition:
        """Packs this condition into a not condition.

        :param new_condition: New condition
        :return: PropertyCondition
        """
        return PropertyCondition(cs_condition=self.cs_condition.Or(new_condition.cs_condition))

    @property
    def Property(self) -> Any:
        """The property that should be checked.

        :return: Property
        """
        return self.cs_condition.Property

    @property
    def PropertyConditionFlags(self) -> PropertyConditionFlags:
        """Optional flags that are used when checking the property.

        :return: Property Condition Flags
        """
        return PropertyConditionFlags(self.cs_condition.PropertyConditionFlags)

    def ToString(self) -> str:
        """Converts element to string

        :return: Converted value
        """
        return self.cs_condition.ToString()

    @property
    def Value(self) -> Union[str, Any]:
        """The value that is used for checking.

        :return: Value
        """
        return self.cs_condition.Value


class ConditionFactory(BaseModel):
    """ConditionFactory wraps a ConditionFactory object from FlaUI.Core.Conditions module. This class provides methods to create PropertyConditions based on automation id, control type, class name, name, and text."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_cf: CSConditionFactory

    def by_automation_id(
        self,
        automation_id: str,
        condition_flags_property_condition_flags: PropertyConditionFlags = PropertyConditionFlags.None_,
    ) -> PropertyCondition:
        """Creates a condition to search by an automation id.

        :param automation_id: Automation ID
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            cs_condition=self.raw_cf.ByAutomationId(automation_id, condition_flags_property_condition_flags.value)
        )

    def by_control_type(self, control_type: ControlType) -> PropertyCondition:
        """Creates a condition to search by a ControlType.

        :param control_type: Types of controls in Microsoft UI Automation.
        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.ByControlType(control_type.value))

    def by_class_name(
        self,
        class_name: Union[str, KnownClassNames],
        condition_flags_property_condition_flags: PropertyConditionFlags = PropertyConditionFlags.None_,
    ) -> PropertyCondition:
        """Creates a condition to search by a class name.

        :param class_name: Class Name
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            cs_condition=self.raw_cf.ByClassName(
                class_name if isinstance(class_name, str) else class_name.value,
                condition_flags_property_condition_flags.value,
            )
        )

    def by_name(
        self, name: str, condition_flags_property_condition_flags: PropertyConditionFlags = PropertyConditionFlags.None_
    ) -> PropertyCondition:
        """Creates a condition to search by a name.

        :param name: Name
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.ByName(name, condition_flags_property_condition_flags.value))

    def by_text(
        self, text: str, condition_flags_property_condition_flags: PropertyConditionFlags = PropertyConditionFlags.None_
    ) -> PropertyCondition:
        """Creates a condition to search by a text.

        :param text: Text value
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.ByText(text, condition_flags_property_condition_flags.value))

    def by_framework_id(
        self,
        framework_id: str,
        condition_flags_property_condition_flags: PropertyConditionFlags = PropertyConditionFlags.None_,
    ) -> PropertyCondition:
        """Creates a condition to search by a Framework Id.

        :param framework_id: Framework ID
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            cs_condition=self.raw_cf.ByFrameworkId(framework_id, condition_flags_property_condition_flags.value)
        )

    def by_framework_type(self, framework_type: FrameworkType) -> PropertyCondition:
        """Creates a condition to search by a Framework Type.

        :param framework_type: Framework Type
        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.ByFrameworkType(framework_type.value))

    def by_process_id(self, process_id: int) -> PropertyCondition:
        """Creates a condition to search by a process id.

        :param process_id: Process ID
        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.ByProcessId(process_id))

    def by_localized_control_type(
        self,
        localized_control_type: str,
        condition_flags_property_condition_flags: PropertyConditionFlags = PropertyConditionFlags.None_,
    ) -> PropertyCondition:
        """Creates a condition to search by a localized control type.

        :param localized_control_type: Localized Control Type
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            cs_condition=self.raw_cf.ByLocalizedControlType(
                localized_control_type, condition_flags_property_condition_flags
            )
        )

    def by_help_text(
        self,
        help_text: str,
        condition_flags_property_condition_flags: PropertyConditionFlags = PropertyConditionFlags.None_,
    ) -> PropertyCondition:
        """Creates a condition to search by a help text.

        :param help_text: Help text
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            cs_condition=self.raw_cf.ByHelpText(help_text, condition_flags_property_condition_flags.value)
        )

    def by_value(
        self,
        value: str,
        condition_flags_property_condition_flags: PropertyConditionFlags = PropertyConditionFlags.None_,
    ) -> PropertyCondition:
        """Creates a condition to search by a value.

        :param value: Value
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            cs_condition=self.raw_cf.ByValue(value, condition_flags_property_condition_flags.value)
        )

    def menu(self) -> PropertyCondition:
        """Searches for a Menu/MenuBar.

        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.ByControlType(ControlType.Menu.value)).Or(
            self.raw_cf.ByControlType(ControlType.MenuBar.value)
        )

    def grid(self) -> PropertyCondition:
        """Searches for a DataGrid/List.

        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.Grid())

    def horizontal_scroll_bar(self) -> PropertyCondition:
        """Searches for a horizontal scrollbar.

        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.HorizontalScrollBar())

    def vertical_scroll_bar(self) -> PropertyCondition:
        """Searches for a vertical scrollbar.

        :return: Property Condition
        """
        return PropertyCondition(cs_condition=self.raw_cf.VerticalScrollBar())
