"""Unit tests for the pattern-access architecture (``flaui.core.patterns``).

These exercise the wrapper plumbing with lightweight fakes, so they need no running UI: a
``SimpleNamespace`` stands in for the native C# ``IAutomationPattern<T>`` / pattern objects.
"""

from types import SimpleNamespace

import pytest

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns import AutomationPattern, InvokePattern, ValuePattern
from flaui.lib.exceptions import PatternNotSupportedException


class TestPatternBase:
    """Validate the shared pattern base behaviour."""

    def test_none_raw_pattern_rejected(self) -> None:
        """Constructing a pattern with a missing native object raises ``PatternNotSupportedException``."""
        with pytest.raises(PatternNotSupportedException):
            InvokePattern(raw_pattern=None)

    def test_raw_pattern_is_exposed(self) -> None:
        """The native pattern object is reachable via ``raw_pattern`` as an escape hatch."""
        native = SimpleNamespace()
        assert InvokePattern(raw_pattern=native).raw_pattern is native


class TestAutomationPattern:
    """Validate the ``IAutomationPattern<T>`` accessor wrapper."""

    @staticmethod
    def _accessor(supported: bool, native: object) -> AutomationPattern[InvokePattern]:
        """Build an accessor backed by a fake native ``IAutomationPattern<T>``."""
        raw = SimpleNamespace(
            IsSupported=supported,
            Pattern=native,
            PatternOrDefault=native if supported else None,
        )
        return AutomationPattern[InvokePattern](raw_automation_pattern=raw, pattern_type=InvokePattern)

    def test_is_supported_reflects_native(self) -> None:
        """``is_supported`` reads the native ``IsSupported`` flag."""
        assert self._accessor(True, SimpleNamespace()).is_supported is True
        assert self._accessor(False, None).is_supported is False

    def test_pattern_wraps_native(self) -> None:
        """``pattern`` wraps the native pattern in the configured Python class."""
        native = SimpleNamespace()
        wrapped = self._accessor(True, native).pattern
        assert isinstance(wrapped, InvokePattern)
        assert wrapped.raw_pattern is native

    def test_pattern_or_default_none_when_unsupported(self) -> None:
        """``pattern_or_default`` returns ``None`` when the pattern is unsupported."""
        assert self._accessor(False, None).pattern_or_default is None

    def test_try_get_pattern(self) -> None:
        """``try_get_pattern`` reports support and returns the wrapped pattern."""
        supported, wrapped = self._accessor(True, SimpleNamespace()).try_get_pattern()
        assert supported is True
        assert isinstance(wrapped, InvokePattern)

        unsupported, missing = self._accessor(False, None).try_get_pattern()
        assert unsupported is False
        assert missing is None


class TestPatternProperties:
    """Validate that pattern properties surface as ``AutomationProperty`` wrappers."""

    def test_value_pattern_exposes_automation_properties(self) -> None:
        """``ValuePattern`` wraps its native properties as :class:`AutomationProperty`."""
        native = SimpleNamespace(Value=SimpleNamespace(Value="hello"), IsReadOnly=SimpleNamespace(Value=False))
        pattern = ValuePattern(raw_pattern=native)
        assert isinstance(pattern.value, AutomationProperty)
        assert pattern.value.value == "hello"
        assert pattern.is_read_only.value is False

    def test_value_pattern_set_value_delegates_to_native(self) -> None:
        """``set_value`` forwards to the native ``SetValue``."""
        captured = {}
        native = SimpleNamespace(SetValue=lambda v: captured.setdefault("value", v))
        ValuePattern(raw_pattern=native).set_value("typed")
        assert captured["value"] == "typed"
