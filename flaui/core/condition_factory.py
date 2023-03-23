# Helper class with some commonly used conditions.
from __future__ import annotations

from typing import Any
from typing import Union

from FlaUI.Core.Conditions import ConditionFactory as CSConditionFactory  # pyright: ignore
from FlaUI.Core.Conditions import PropertyCondition as CSPropertyCondition  # pyright: ignore
from pydantic import BaseModel
from pydantic import validate_arguments

from flaui.core.definitions import ControlType
from flaui.core.definitions import PropertyConditionFlags
from flaui.core.framework_types import FrameworkType


class PropertyCondition(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    condition: CSPropertyCondition

    def And(self, new_condition: ConditionFactory) -> PropertyCondition:
        """Adds the given condition with an "and".

        :param new_condition: New condition
        :return: PropertyCondition
        """
        return PropertyCondition(condition=self.condition.And(new_condition))

    def Equals(self, value: PropertyCondition) -> bool:
        """Compares the value to another value

        :param value: Value to compare
        :return: True/False
        """
        return self.condition.Equals(value.condition)

    def Not(self, new_condition: ConditionFactory) -> PropertyCondition:
        """Adds the given condition with an "not".

        :param new_condition: New condition
        :return: PropertyCondition
        """
        return PropertyCondition(condition=self.condition.Not(new_condition))

    def Or(self, new_condition: ConditionFactory) -> PropertyCondition:
        """Packs this condition into a not condition.

        :param new_condition: New condition
        :return: PropertyCondition
        """
        return PropertyCondition(condition=self.condition.Or(new_condition))

    @property
    def Property(self) -> Any:
        """The property that should be checked.

        :return: Property
        """
        return self.condition.Property

    @property
    def PropertyConditionFlags(self):
        """Optional flags that are used when checking the property.

        :return: Property Condition Flags
        """
        return PropertyConditionFlags

    def ToString(self) -> str:
        """Converts element to string

        :return: Converted value
        """
        return self.condition.ToString()

    @property
    def Value(self) -> Union[str, Any]:
        """The value that is used for checking.

        :return: Value
        """
        return self.condition.Value


class ConditionFactory(BaseModel):
    raw_cf: CSConditionFactory

    @validate_arguments
    def by_automation_id(
        self, automation_id: str, condition_flags_property_condition_flags=PropertyConditionFlags.none
    ):
        """Creates a condition to search by an automation id.

        :param automation_id: Automation ID
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            condition=self.raw_cf.ByAutomationId(automation_id, condition_flags_property_condition_flags)
        )

    @validate_arguments
    def by_control_type(self, control_type: ControlType):
        """Creates a condition to search by a ControlType.

        :param control_type: Types of controls in Microsoft UI Automation.
        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.ByControlType(control_type.value))

    @validate_arguments
    def by_class_name(self, class_name: str, condition_flags_property_condition_flags=PropertyConditionFlags.none):
        """Creates a condition to search by a class name.

        :param class_name: Class Name
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            condition=self.raw_cf.ByClassName(class_name, condition_flags_property_condition_flags)
        )

    @validate_arguments
    def by_name(self, name: str, condition_flags_property_condition_flags=PropertyConditionFlags.none):
        """Creates a condition to search by a name.

        :param name: Name
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.ByName(name, condition_flags_property_condition_flags))

    @validate_arguments
    def by_text(self, text: str, condition_flags_property_condition_flags=PropertyConditionFlags.none):
        """Creates a condition to search by a text.

        :param text: Text value
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.ByText(text, condition_flags_property_condition_flags))

    @validate_arguments
    def by_framework_id(self, framework_id: str, condition_flags_property_condition_flags=PropertyConditionFlags.none):
        """Creates a condition to search by a Framework Id.

        :param framework_id: Framework ID
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            condition=self.raw_cf.ByFrameworkId(framework_id, condition_flags_property_condition_flags)
        )

    @validate_arguments
    def by_framework_type(self, framework_type: FrameworkType):
        """Creates a condition to search by a Framework Type.

        :param framework_type: Framework Type
        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.ByFrameworkType(framework_type.value))

    @validate_arguments
    def by_process_id(self, process_id: int):
        """Creates a condition to search by a process id.

        :param process_id: Process ID
        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.ByProcessId(process_id))

    @validate_arguments
    def by_localized_control_type(
        self, localized_control_type: str, condition_flags_property_condition_flags=PropertyConditionFlags.none
    ):
        """Creates a condition to search by a localized control type.

        :param localized_control_type: Localized Control Type
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(
            condition=self.raw_cf.ByLocalizedControlType(
                localized_control_type, condition_flags_property_condition_flags
            )
        )

    @validate_arguments
    def by_help_text(self, help_text: str, condition_flags_property_condition_flags=PropertyConditionFlags.none):
        """Creates a condition to search by a help text.

        :param help_text: Help text
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.ByHelpText(help_text, condition_flags_property_condition_flags))

    @validate_arguments
    def by_value(self, value: str, condition_flags_property_condition_flags=PropertyConditionFlags.none):
        """Creates a condition to search by a value.

        :param value: Value
        :param condition_flags_property_condition_flags: Contains values used in creating property conditions, defaults to PropertyConditionFlags.none
        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.ByValue(value, condition_flags_property_condition_flags))

    @validate_arguments
    def menu(self):
        """Searches for a Menu/MenuBar.

        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.Menu())

    @validate_arguments
    def grid(self):
        """Searches for a DataGrid/List.

        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.Grid())

    @validate_arguments
    def horizontal_scroll_bar(self):
        """Searches for a horizontal scrollbar.

        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.HorizontalScrollBar())

    @validate_arguments
    def vertical_scroll_bar(self):
        """Searches for a vertical scrollbar.

        :return: Property Condition
        """
        return PropertyCondition(condition=self.raw_cf.VerticalScrollBar())

    class Config:
        arbitrary_types_allowed = True
