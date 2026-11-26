"""Unit tests for :mod:`flaui.core.condition_factory` (GH-88).

``ConditionFactory`` and ``PropertyCondition`` delegate to real C# condition objects, and
``PropertyCondition.cs_condition`` is type-validated against the C# condition types — so a mock will
not pass validation. These tests therefore drive a real ``ConditionFactory`` obtained from a UIA3
automation (no running application required).

They also lock in the fixes for three previously broken methods: ``Not`` (and-not semantics),
``Equals`` (condition equality), and ``by_localized_control_type``.
"""

from typing import Generator

import pytest

from flaui.core.condition_factory import (
    AndCondition,
    BoolCondition,
    ConditionFactory,
    FalseCondition,
    NotCondition,
    OrCondition,
    PropertyCondition,
    TrueCondition,
    wrap_condition,
)
from flaui.core.definitions import ControlType, PropertyConditionFlags
from flaui.core.framework_types import FrameworkType
from flaui.lib.enums import KnownClassNames, UIAutomationTypes
from flaui.modules.automation import Automation


@pytest.fixture(scope="module")
def condition_factory() -> Generator[ConditionFactory, None, None]:
    """Yield a real :class:`ConditionFactory` from a UIA3 automation, disposing it afterwards."""
    automation = Automation(UIAutomationTypes.UIA3)
    try:
        yield automation.cf
    finally:
        automation.cs_automation.Dispose()


class TestConditionFactoryBuilders:
    """Validate every ``ConditionFactory`` builder returns a populated :class:`PropertyCondition`."""

    def test_by_automation_id(self, condition_factory: ConditionFactory) -> None:
        """``by_automation_id`` builds a condition on the AutomationId property."""
        condition = condition_factory.by_automation_id("save-button")
        assert isinstance(condition, PropertyCondition)
        assert condition.cs_condition is not None

    def test_by_control_type(self, condition_factory: ConditionFactory) -> None:
        """``by_control_type`` builds a condition on the ControlType property."""
        assert isinstance(condition_factory.by_control_type(ControlType.Button), PropertyCondition)

    def test_by_class_name_str_and_enum(self, condition_factory: ConditionFactory) -> None:
        """``by_class_name`` accepts both a plain string and a :class:`KnownClassNames` member."""
        assert isinstance(condition_factory.by_class_name("TextBox"), PropertyCondition)
        known = next(iter(KnownClassNames))
        assert isinstance(condition_factory.by_class_name(known), PropertyCondition)

    def test_by_name(self, condition_factory: ConditionFactory) -> None:
        """``by_name`` builds a condition on the Name property."""
        assert isinstance(condition_factory.by_name("OK"), PropertyCondition)

    def test_by_text(self, condition_factory: ConditionFactory) -> None:
        """``by_text`` builds a condition on the text value."""
        assert isinstance(condition_factory.by_text("Submit"), PropertyCondition)

    def test_by_framework_id(self, condition_factory: ConditionFactory) -> None:
        """``by_framework_id`` builds a condition on the FrameworkId property."""
        assert isinstance(condition_factory.by_framework_id("WPF"), PropertyCondition)

    def test_by_framework_type(self, condition_factory: ConditionFactory) -> None:
        """``by_framework_type`` builds a condition on the framework type."""
        framework_type = next(ft for ft in FrameworkType if ft.value is not None)
        assert isinstance(condition_factory.by_framework_type(framework_type), PropertyCondition)

    def test_by_process_id(self, condition_factory: ConditionFactory) -> None:
        """``by_process_id`` builds a condition on the process id."""
        assert isinstance(condition_factory.by_process_id(1234), PropertyCondition)

    def test_by_localized_control_type(self, condition_factory: ConditionFactory) -> None:
        """``by_localized_control_type`` builds a condition (regression: previously passed the enum)."""
        assert isinstance(condition_factory.by_localized_control_type("button"), PropertyCondition)

    def test_by_help_text(self, condition_factory: ConditionFactory) -> None:
        """``by_help_text`` builds a condition on the help text."""
        assert isinstance(condition_factory.by_help_text("tooltip"), PropertyCondition)

    def test_by_value(self, condition_factory: ConditionFactory) -> None:
        """``by_value`` builds a condition on the value."""
        assert isinstance(condition_factory.by_value("42"), PropertyCondition)

    def test_menu(self, condition_factory: ConditionFactory) -> None:
        """``menu`` builds a Menu/MenuBar condition."""
        assert isinstance(condition_factory.menu(), PropertyCondition)

    def test_grid(self, condition_factory: ConditionFactory) -> None:
        """``grid`` builds a DataGrid/List condition."""
        assert isinstance(condition_factory.grid(), PropertyCondition)

    def test_scroll_bars(self, condition_factory: ConditionFactory) -> None:
        """The scrollbar helpers build their respective conditions."""
        assert isinstance(condition_factory.horizontal_scroll_bar(), PropertyCondition)
        assert isinstance(condition_factory.vertical_scroll_bar(), PropertyCondition)


class TestPropertyCondition:
    """Validate the combinators and accessors on :class:`PropertyCondition`."""

    @pytest.fixture()
    def conditions(self, condition_factory: ConditionFactory) -> tuple[PropertyCondition, PropertyCondition]:
        """Return two distinct conditions to combine."""
        return condition_factory.by_name("OK"), condition_factory.by_automation_id("btn1")

    def test_and_wrapper_and_raw(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``And`` accepts both a :class:`PropertyCondition` and a raw C# condition."""
        first, second = conditions
        assert isinstance(first.And(second), PropertyCondition)
        assert isinstance(first.And(second.cs_condition), PropertyCondition)

    def test_or_wrapper_and_raw(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``Or`` accepts both a :class:`PropertyCondition` and a raw C# condition."""
        first, second = conditions
        assert isinstance(first.Or(second), PropertyCondition)
        assert isinstance(first.Or(second.cs_condition), PropertyCondition)

    def test_not_builds_and_not(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``Not`` builds ``self AND NOT other`` (regression: previously raised ``TypeError``)."""
        first, second = conditions
        combined = first.Not(second)
        assert isinstance(combined, PropertyCondition)
        rendered = combined.ToString()
        assert "AND NOT" in rendered

    def test_not_accepts_raw_condition(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``Not`` also accepts a raw C# condition for the negated operand."""
        first, second = conditions
        assert isinstance(first.Not(second.cs_condition), PropertyCondition)

    def test_equals(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``Equals`` compares condition equality (regression: previously raised ``AttributeError``)."""
        first, second = conditions
        assert first.Equals(first) is True
        assert first.Equals(second) is False

    def test_property_value_and_flags(self, condition_factory: ConditionFactory) -> None:
        """``Property``, ``Value`` and ``PropertyConditionFlags`` expose the underlying condition data."""
        condition = condition_factory.by_name("OK")
        assert condition.Property is not None
        assert condition.Value == "OK"
        assert isinstance(condition.PropertyConditionFlags, PropertyConditionFlags)

    def test_to_string(self, condition_factory: ConditionFactory) -> None:
        """``ToString`` renders the condition as text."""
        assert isinstance(condition_factory.by_name("OK").ToString(), str)

    def test_str_matches_to_string(self, condition_factory: ConditionFactory) -> None:
        """``str(condition)`` returns the C# text form."""
        condition = condition_factory.by_name("OK")
        assert str(condition) == condition.ToString()


class TestPythonicCombinators:
    """Validate ``and_`` / ``or_`` / ``not_``, the ``&`` / ``|`` / ``~`` operators and the C# aliases (GH-158)."""

    @pytest.fixture()
    def conditions(self, condition_factory: ConditionFactory) -> tuple[PropertyCondition, PropertyCondition]:
        """Return two distinct conditions to combine."""
        return condition_factory.by_name("OK"), condition_factory.by_control_type(ControlType.Button)

    def test_and_method_and_operator_agree(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``a.and_(b)``, ``a & b`` and the legacy ``a.And(b)`` build the same :class:`AndCondition`."""
        first, second = conditions
        for combined in (first.and_(second), first & second, first.And(second)):
            assert isinstance(combined, AndCondition)
            assert isinstance(combined, PropertyCondition)  # backward-compatible type
            assert combined.child_count == 2
            assert str(combined) == str(first.and_(second))
            assert " AND " in str(combined)

    def test_or_method_and_operator_agree(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``a.or_(b)``, ``a | b`` and the legacy ``a.Or(b)`` build the same :class:`OrCondition`."""
        first, second = conditions
        for combined in (first.or_(second), first | second, first.Or(second)):
            assert isinstance(combined, OrCondition)
            assert combined.child_count == 2
            assert str(combined) == str(first.or_(second))
            assert " OR " in str(combined)

    def test_not_method_and_operator_agree(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``a.not_()``, ``~a`` and the parameterless legacy ``a.Not()`` negate ``a``."""
        first, _ = conditions
        for negated in (first.not_(), ~first, first.Not()):
            assert isinstance(negated, NotCondition)
            assert negated.condition.Equals(first)
            assert "NOT" in str(negated)

    def test_double_negation(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``~~a`` wraps ``a`` twice; the inner condition is again a :class:`NotCondition`."""
        first, _ = conditions
        double = ~~first
        assert isinstance(double, NotCondition)
        inner = double.condition
        assert isinstance(inner, NotCondition)
        assert inner.condition.Equals(first)

    def test_legacy_not_with_argument_is_and_not(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``a.Not(b)`` keeps its historical meaning, ``a & ~b``."""
        first, second = conditions
        legacy = first.Not(second)
        assert isinstance(legacy, AndCondition)
        assert str(legacy) == str(first & ~second)

    def test_operators_compose_with_precedence(
        self, condition_factory: ConditionFactory, conditions: tuple[PropertyCondition, PropertyCondition]
    ) -> None:
        """Mixed expressions follow Python precedence: ``~`` binds tighter than ``&``, ``&`` than ``|``."""
        first, second = conditions
        third = condition_factory.by_automation_id("btn1")
        expression = first & ~second | third
        assert isinstance(expression, OrCondition)
        left, right = expression.conditions
        assert isinstance(left, AndCondition)
        assert isinstance(left.conditions[1], NotCondition)
        assert right.Equals(third)

    def test_operators_accept_raw_csharp_conditions(
        self, conditions: tuple[PropertyCondition, PropertyCondition]
    ) -> None:
        """A raw C# condition works on either side of ``&`` and ``|``."""
        first, second = conditions
        raw = second.cs_condition
        assert str(first & raw) == str(first & second)
        assert str(raw & first) == str(second & first)
        assert str(first | raw) == str(first | second)
        assert str(raw | first) == str(second | first)

    def test_operators_reject_non_conditions(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """Combining with something that is not a condition raises ``TypeError``."""
        first, _ = conditions
        with pytest.raises(TypeError):
            _ = first & "OK"
        with pytest.raises(TypeError):
            first.or_(42)

    def test_junction_conditions_are_wrapped(self, conditions: tuple[PropertyCondition, PropertyCondition]) -> None:
        """``conditions`` returns Python wrappers that compare equal to the originals."""
        first, second = conditions
        children = (first & second).conditions
        assert [type(c) for c in children] == [PropertyCondition, PropertyCondition]
        assert children[0].Equals(first)
        assert children[1].Equals(second)


class TestTrueFalseConditions:
    """Validate the true/false conditions matching ``TrueCondition.Default`` / ``FalseCondition.Default`` (GH-158)."""

    def test_true_condition(self) -> None:
        """``ConditionFactory.true_condition()`` wraps ``TrueCondition.Default`` without a factory instance."""
        from FlaUI.Core.Conditions import TrueCondition as CSTrueCondition  # pyright: ignore

        condition = ConditionFactory.true_condition()
        assert isinstance(condition, TrueCondition)
        assert isinstance(condition, BoolCondition)
        assert condition.boolean_value is True
        assert condition.Equals(CSTrueCondition.Default)
        assert TrueCondition.default().Equals(condition)

    def test_false_condition(self) -> None:
        """``ConditionFactory.false_condition()`` wraps ``FalseCondition.Default``."""
        from FlaUI.Core.Conditions import FalseCondition as CSFalseCondition  # pyright: ignore

        condition = ConditionFactory.false_condition()
        assert isinstance(condition, FalseCondition)
        assert condition.boolean_value is False
        assert condition.Equals(CSFalseCondition.Default)
        assert not condition.Equals(ConditionFactory.true_condition())

    def test_true_false_combine(self, condition_factory: ConditionFactory) -> None:
        """True/false conditions combine like any other condition."""
        name = condition_factory.by_name("OK")
        assert isinstance(ConditionFactory.true_condition() & name, AndCondition)
        assert isinstance(ConditionFactory.false_condition() | name, OrCondition)
        assert isinstance(~ConditionFactory.true_condition(), NotCondition)

    def test_wrap_condition_dispatch(self, condition_factory: ConditionFactory) -> None:
        """``wrap_condition`` picks the Python class matching the C# condition type."""
        name = condition_factory.by_name("OK")
        assert type(wrap_condition(name.cs_condition)) is PropertyCondition
        assert type(wrap_condition(ConditionFactory.true_condition().cs_condition)) is TrueCondition
        assert type(wrap_condition(ConditionFactory.false_condition().cs_condition)) is FalseCondition
        assert type(wrap_condition((name & name).cs_condition)) is AndCondition
        assert type(wrap_condition((name | name).cs_condition)) is OrCondition
        assert type(wrap_condition((~name).cs_condition)) is NotCondition

    def test_menu_uses_or(self, condition_factory: ConditionFactory) -> None:
        """``menu()`` is ``Menu | MenuBar``."""
        menu = condition_factory.menu()
        assert isinstance(menu, OrCondition)
        expected = condition_factory.by_control_type(ControlType.Menu) | condition_factory.by_control_type(
            ControlType.MenuBar
        )
        assert str(menu) == str(expected)
