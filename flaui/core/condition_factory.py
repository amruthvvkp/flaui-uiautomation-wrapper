"""Search conditions for the FlaUI automation framework.

This module mirrors ``FlaUI.Core.Conditions``:

* :class:`ConditionBase` holds a C# condition and provides the combinators ``and_``, ``or_`` and
  ``not_``, plus the ``&``, ``|`` and ``~`` operators. The C#-named ``And``, ``Or`` and ``Not`` stay
  as backward-compatible aliases.
* :class:`PropertyCondition` wraps a single property check. Every other condition wrapper derives
  from it, so any condition can be passed where a ``PropertyCondition`` is expected.
* :class:`AndCondition`, :class:`OrCondition`, :class:`NotCondition`, :class:`TrueCondition` and
  :class:`FalseCondition` wrap the matching C# types; :func:`wrap_condition` picks the right one.
* :class:`ConditionFactory` wraps ``FlaUI.Core.Conditions.ConditionFactory`` and builds conditions
  by automation id, control type, class name, name, text and more.
"""

from __future__ import annotations

from typing import Any, List, Optional, Union

from FlaUI.Core.Conditions import (  # pyright: ignore
    AndCondition as CSAndCondition,
    ConditionBase as CSConditionBase,
    ConditionFactory as CSConditionFactory,
    FalseCondition as CSFalseCondition,
    NotCondition as CSNotCondition,
    OrCondition as CSOrCondition,
    TrueCondition as CSTrueCondition,
)
from pydantic import BaseModel, ConfigDict

from flaui.core.definitions import ControlType, PropertyConditionFlags
from flaui.core.framework_types import FrameworkType
from flaui.lib.enums import KnownClassNames
from flaui.lib.exceptions import handle_csharp_exceptions

# A Python condition wrapper or a raw C# ``ConditionBase``.
ConditionLike = Union["ConditionBase", Any]


def _to_cs(condition: ConditionLike) -> Any:
    """Return the C# condition behind ``condition``.

    :param condition: A Python condition wrapper or a raw C# condition.
    :return: The raw C# ``ConditionBase``.
    :raises TypeError: When ``condition`` is neither a wrapper nor a C# condition.
    """
    if isinstance(condition, ConditionBase):
        return condition.cs_condition
    if isinstance(condition, CSConditionBase):
        return condition
    raise TypeError(f"Expected a condition, got {type(condition).__name__}")


def wrap_condition(cs_condition: Any) -> PropertyCondition:
    """Wrap a raw C# condition in the matching Python class.

    :param cs_condition: A C# ``FlaUI.Core.Conditions.ConditionBase`` instance.
    :return: A :class:`TrueCondition`, :class:`FalseCondition`, :class:`AndCondition`,
        :class:`OrCondition`, :class:`NotCondition` or :class:`PropertyCondition`.
    """
    if isinstance(cs_condition, CSTrueCondition):
        return TrueCondition(cs_condition=cs_condition)
    if isinstance(cs_condition, CSFalseCondition):
        return FalseCondition(cs_condition=cs_condition)
    if isinstance(cs_condition, CSAndCondition):
        return AndCondition(cs_condition=cs_condition)
    if isinstance(cs_condition, CSOrCondition):
        return OrCondition(cs_condition=cs_condition)
    if isinstance(cs_condition, CSNotCondition):
        return NotCondition(cs_condition=cs_condition)
    return PropertyCondition(cs_condition=cs_condition)


class ConditionBase(BaseModel):
    """Base for every search condition; mirrors ``FlaUI.Core.Conditions.ConditionBase``.

    Combine conditions with the methods or the operators::

        ok_button = cf.by_name("OK") & cf.by_control_type(ControlType.Button)
        either = cf.by_automation_id("a") | cf.by_automation_id("b")
        not_ok = ~cf.by_name("OK")
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    cs_condition: CSConditionBase

    @handle_csharp_exceptions
    def and_(self, new_condition: ConditionLike) -> AndCondition:
        """Combine this condition with another using "and" (C# ``ConditionBase.And``).

        :param new_condition: Condition to combine with; a wrapper or a raw C# condition.
        :return: An :class:`AndCondition` that matches when both conditions match.
        """
        return AndCondition(cs_condition=self.cs_condition.And(_to_cs(new_condition)))

    @handle_csharp_exceptions
    def or_(self, new_condition: ConditionLike) -> OrCondition:
        """Combine this condition with another using "or" (C# ``ConditionBase.Or``).

        :param new_condition: Condition to combine with; a wrapper or a raw C# condition.
        :return: An :class:`OrCondition` that matches when either condition matches.
        """
        return OrCondition(cs_condition=self.cs_condition.Or(_to_cs(new_condition)))

    @handle_csharp_exceptions
    def not_(self) -> NotCondition:
        """Negate this condition (C# ``ConditionBase.Not``).

        :return: A :class:`NotCondition` that matches when this condition does not.
        """
        return NotCondition(cs_condition=self.cs_condition.Not())

    def And(self, new_condition: ConditionLike) -> AndCondition:
        """Combine with "and"; alias of :meth:`and_` kept for backward compatibility.

        :param new_condition: Condition to combine with; a wrapper or a raw C# condition.
        :return: An :class:`AndCondition`.
        """
        return self.and_(new_condition)

    def Or(self, new_condition: ConditionLike) -> OrCondition:
        """Combine with "or"; alias of :meth:`or_` kept for backward compatibility.

        :param new_condition: Condition to combine with; a wrapper or a raw C# condition.
        :return: An :class:`OrCondition`.
        """
        return self.or_(new_condition)

    def Not(self, new_condition: Optional[ConditionLike] = None) -> Union[NotCondition, AndCondition]:
        """Negate; kept for backward compatibility, prefer :meth:`not_` or ``~``.

        Without an argument this matches C# ``ConditionBase.Not()`` and negates this condition.
        With an argument it keeps the historical Python meaning, ``self AND NOT new_condition``,
        which is ``self & ~new_condition``.

        :param new_condition: Optional condition to negate and combine with this one.
        :return: A :class:`NotCondition` (no argument) or an :class:`AndCondition`.
        """
        if new_condition is None:
            return self.not_()
        return self.and_(wrap_condition(_to_cs(new_condition)).not_())

    def __and__(self, other: ConditionLike) -> AndCondition:
        """Return ``self & other``; see :meth:`and_`."""
        return self.and_(other)

    def __rand__(self, other: ConditionLike) -> AndCondition:
        """Return ``other & self`` when ``other`` is a raw C# condition."""
        return wrap_condition(_to_cs(other)).and_(self)

    def __or__(self, other: ConditionLike) -> OrCondition:
        """Return ``self | other``; see :meth:`or_`."""
        return self.or_(other)

    def __ror__(self, other: ConditionLike) -> OrCondition:
        """Return ``other | self`` when ``other`` is a raw C# condition."""
        return wrap_condition(_to_cs(other)).or_(self)

    def __invert__(self) -> NotCondition:
        """Return ``~self``; see :meth:`not_`."""
        return self.not_()

    @handle_csharp_exceptions
    def Equals(self, value: ConditionLike) -> bool:
        """Compare this condition to another (C# ``Equals``).

        C# compares property conditions by property, value and flags, but compares ``And``/``Or``/
        ``Not`` conditions by reference. To compare two combined conditions by content, compare
        ``str(a) == str(b)``.

        :param value: Condition to compare; a wrapper or a raw C# condition.
        :return: True when both conditions are equal.
        """
        other = value.cs_condition if isinstance(value, ConditionBase) else value
        return bool(self.cs_condition.Equals(other))

    @handle_csharp_exceptions
    def ToString(self) -> str:
        """Render the condition as text (C# ``ToString``).

        :return: Text form of the condition, e.g. ``(Name [#30005]: OK AND ControlType [#30003]: Button)``.
        """
        return str(self.cs_condition.ToString())

    def __str__(self) -> str:
        """Return the C# text form of the condition; see :meth:`ToString`."""
        return self.ToString()


class PropertyCondition(ConditionBase):
    """A condition that checks one property; mirrors ``FlaUI.Core.Conditions.PropertyCondition``.

    For backward compatibility every other condition wrapper derives from this class, so APIs
    typed as taking a ``PropertyCondition`` accept any condition. ``Property``, ``Value`` and
    ``PropertyConditionFlags`` are only meaningful on a real property condition.
    """

    @property
    def Property(self) -> Any:
        """The property that should be checked.

        :return: Property
        """
        return self.cs_condition.Property

    @property
    def PropertyConditionFlags(self) -> "PropertyConditionFlags":  # ty: ignore[invalid-type-form]
        """Optional flags that are used when checking the property.

        :return: Property Condition Flags
        """
        return PropertyConditionFlags(self.cs_condition.PropertyConditionFlags)

    @property
    def Value(self) -> Union[str, Any]:
        """The value that is used for checking.

        :return: Value
        """
        return self.cs_condition.Value


class BoolCondition(PropertyCondition):
    """A condition that is always true or always false; mirrors ``FlaUI.Core.Conditions.BoolCondition``."""

    @property
    @handle_csharp_exceptions
    def boolean_value(self) -> bool:
        """Return the fixed result of this condition.

        :return: True for a :class:`TrueCondition`, False for a :class:`FalseCondition`.
        """
        return bool(self.cs_condition.BooleanValue)


class TrueCondition(BoolCondition):
    """A condition that matches every element; mirrors ``FlaUI.Core.Conditions.TrueCondition``."""

    @classmethod
    @handle_csharp_exceptions
    def default(cls) -> TrueCondition:
        """Return the shared true condition (C# ``TrueCondition.Default``).

        :return: A :class:`TrueCondition`.
        """
        return cls(cs_condition=CSTrueCondition.Default)


class FalseCondition(BoolCondition):
    """A condition that matches no element; mirrors ``FlaUI.Core.Conditions.FalseCondition``."""

    @classmethod
    @handle_csharp_exceptions
    def default(cls) -> FalseCondition:
        """Return the shared false condition (C# ``FalseCondition.Default``).

        :return: A :class:`FalseCondition`.
        """
        return cls(cs_condition=CSFalseCondition.Default)


class JunctionConditionBase(PropertyCondition):
    """Base for conditions that join several conditions; mirrors ``JunctionConditionBase``."""

    @property
    @handle_csharp_exceptions
    def child_count(self) -> int:
        """Return how many conditions this junction joins.

        :return: Number of joined conditions.
        """
        return int(self.cs_condition.ChildCount)

    @property
    @handle_csharp_exceptions
    def conditions(self) -> List[PropertyCondition]:
        """Return the joined conditions.

        :return: The conditions, each wrapped in its matching Python class.
        """
        return [wrap_condition(_) for _ in self.cs_condition.Conditions]


class AndCondition(JunctionConditionBase):
    """A condition that matches when all its conditions match; mirrors ``AndCondition``."""


class OrCondition(JunctionConditionBase):
    """A condition that matches when any of its conditions match; mirrors ``OrCondition``."""


class NotCondition(PropertyCondition):
    """A condition that negates another; mirrors ``FlaUI.Core.Conditions.NotCondition``."""

    @property
    @handle_csharp_exceptions
    def condition(self) -> PropertyCondition:
        """Return the negated condition.

        :return: The inner condition, wrapped in its matching Python class.
        """
        return wrap_condition(self.cs_condition.Condition)


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
                localized_control_type, condition_flags_property_condition_flags.value
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
        return self.by_control_type(ControlType.Menu) | self.by_control_type(ControlType.MenuBar)

    @staticmethod
    def true_condition() -> TrueCondition:
        """Return a condition that matches every element (C# ``TrueCondition.Default``).

        Useful as the neutral start when building a condition up with ``&``.

        :return: A :class:`TrueCondition`.
        """
        return TrueCondition.default()

    @staticmethod
    def false_condition() -> FalseCondition:
        """Return a condition that matches no element (C# ``FalseCondition.Default``).

        Useful as the neutral start when building a condition up with ``|``.

        :return: A :class:`FalseCondition`.
        """
        return FalseCondition.default()

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
