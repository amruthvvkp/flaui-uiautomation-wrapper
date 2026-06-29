"""Unit tests for the core action pattern family (``flaui.core.patterns``).

Covers Invoke, Toggle, RangeValue, ExpandCollapse, and Grid. These wrappers also have end-to-end UI
coverage on real controls; the unit tests here exercise the wrapper plumbing with lightweight fakes
(a ``SimpleNamespace`` stands in for the native C# pattern objects), so they need no running UI.
"""

from types import SimpleNamespace

from flaui.core.automation_elements import AutomationElement, AutomationProperty
from flaui.core.patterns import (
    ExpandCollapsePattern,
    GridPattern,
    InvokePattern,
    Patterns,
    RangeValuePattern,
    TogglePattern,
    ValuePattern,
)


def _prop(value: object) -> SimpleNamespace:
    """Build a fake native ``AutomationProperty`` whose ``Value`` is ``value``.

    :param value: The value the fake property should report.
    :return: A namespace exposing ``Value``.
    """
    return SimpleNamespace(Value=value)


class TestInvokePattern:
    """Validate the Invoke pattern wrapper."""

    def test_invoke_delegates(self) -> None:
        """``invoke`` forwards to the native ``Invoke`` method."""
        called = {}
        pattern = InvokePattern(raw_pattern=SimpleNamespace(Invoke=lambda: called.setdefault("hit", True)))
        pattern.invoke()
        assert called["hit"] is True


class TestTogglePattern:
    """Validate the Toggle pattern wrapper."""

    def test_state_and_toggle(self) -> None:
        """Toggle exposes its state as an AutomationProperty and delegates ``toggle``."""
        called = {}
        native = SimpleNamespace(ToggleState=_prop("On"), Toggle=lambda: called.setdefault("hit", True))
        pattern = TogglePattern(raw_pattern=native)
        assert isinstance(pattern.toggle_state, AutomationProperty)
        assert pattern.toggle_state.value == "On"
        pattern.toggle()
        assert called["hit"] is True


class TestExpandCollapsePattern:
    """Validate the ExpandCollapse pattern wrapper."""

    def test_state_and_actions(self) -> None:
        """ExpandCollapse exposes its state and delegates expand/collapse."""
        calls = []
        native = SimpleNamespace(
            ExpandCollapseState=_prop("Collapsed"),
            Expand=lambda: calls.append("expand"),
            Collapse=lambda: calls.append("collapse"),
        )
        pattern = ExpandCollapsePattern(raw_pattern=native)
        assert pattern.expand_collapse_state.value == "Collapsed"
        pattern.expand()
        pattern.collapse()
        assert calls == ["expand", "collapse"]


class TestRangeValuePattern:
    """Validate the RangeValue pattern wrapper."""

    def test_properties_and_set_value(self) -> None:
        """RangeValue surfaces its range properties and delegates ``set_value``."""
        captured = {}
        native = SimpleNamespace(
            IsReadOnly=_prop(False),
            LargeChange=_prop(10.0),
            SmallChange=_prop(1.0),
            Maximum=_prop(100.0),
            Minimum=_prop(0.0),
            Value=_prop(42.0),
            SetValue=lambda v: captured.setdefault("v", v),
        )
        pattern = RangeValuePattern(raw_pattern=native)
        assert pattern.is_read_only.value is False
        assert pattern.large_change.value == 10.0
        assert pattern.small_change.value == 1.0
        assert pattern.maximum.value == 100.0
        assert pattern.minimum.value == 0.0
        assert pattern.value.value == 42.0
        pattern.set_value(55.0)
        assert captured["v"] == 55.0


class TestGridPattern:
    """Validate the Grid pattern wrapper."""

    def test_counts_and_get_item(self) -> None:
        """Grid surfaces row/column counts and wraps ``get_item`` as an AutomationElement."""
        cell = SimpleNamespace()
        native = SimpleNamespace(ColumnCount=_prop(3), RowCount=_prop(5), GetItem=lambda r, c: cell)
        pattern = GridPattern(raw_pattern=native)
        assert pattern.column_count.value == 3
        assert pattern.row_count.value == 5
        item = pattern.get_item(1, 2)
        assert isinstance(item, AutomationElement)
        assert item.raw_element is cell


class TestFacadeAccessors:
    """Validate the family-1 accessors on the ``Patterns`` facade."""

    def test_facade_wires_family1_accessors(self) -> None:
        """Each family-1 facade accessor returns an accessor wired to the right pattern type."""
        raw_patterns = SimpleNamespace(
            Invoke=SimpleNamespace(IsSupported=True),
            Toggle=SimpleNamespace(IsSupported=True),
            Value=SimpleNamespace(IsSupported=False),
            RangeValue=SimpleNamespace(IsSupported=True),
            ExpandCollapse=SimpleNamespace(IsSupported=False),
            Grid=SimpleNamespace(IsSupported=True),
        )
        facade = Patterns(raw_patterns=raw_patterns)
        assert facade.invoke.pattern_type is InvokePattern
        assert facade.toggle.pattern_type is TogglePattern
        assert facade.value.pattern_type is ValuePattern
        assert facade.range_value.pattern_type is RangeValuePattern
        assert facade.expand_collapse.pattern_type is ExpandCollapsePattern
        assert facade.grid.pattern_type is GridPattern
        assert facade.invoke.is_supported is True
        assert facade.value.is_supported is False
