"""Unit tests for the expect() fluent assertion API."""

from types import SimpleNamespace
from typing import Any

import pytest

from flaui.core.automation_elements import AutomationElement
from flaui.core.expectations import ElementAssertions, _read, _safe_bool, expect
from flaui.uia3 import UIA3Automation


@pytest.fixture
def desktop() -> AutomationElement:
    """Return the desktop element, which is always present and on-screen."""
    return UIA3Automation().get_desktop()


def test_to_be_visible_passes_for_desktop(desktop: AutomationElement) -> None:
    """The desktop is available and on-screen, so to_be_visible succeeds."""
    expect(desktop).to_be_visible(timeout=2000)


def test_negated_to_be_offscreen_passes_for_desktop(desktop: AutomationElement) -> None:
    """The desktop is not off-screen, so not_.to_be_offscreen succeeds."""
    expect(desktop).not_.to_be_offscreen(timeout=2000)


def test_to_be_offscreen_times_out_for_desktop(desktop: AutomationElement) -> None:
    """The desktop never goes off-screen, so to_be_offscreen raises on timeout."""
    with pytest.raises(AssertionError):
        expect(desktop).to_be_offscreen(timeout=300)


def test_to_have_name_with_wrong_value_raises(desktop: AutomationElement) -> None:
    """A mismatched expected name raises AssertionError after the timeout."""
    with pytest.raises(AssertionError):
        expect(desktop).to_have_name("definitely-not-the-desktop-name", timeout=300)


def test_not_returns_a_new_negated_instance(desktop: AutomationElement) -> None:
    """The not_ property yields a distinct, negated ElementAssertions instance."""
    assertions = expect(desktop)
    negated = assertions.not_
    assert isinstance(negated, ElementAssertions)
    assert negated is not assertions


def test_safe_bool_swallows_errors() -> None:
    """_safe_bool returns False when the getter raises and the value otherwise."""

    def _boom() -> bool:
        """Raise to simulate an attribute read failure."""
        raise RuntimeError("boom")

    assert _safe_bool(_boom) is False
    assert _safe_bool(lambda: True) is True


def test_read_returns_sentinel_on_error() -> None:
    """_read returns a unique sentinel (never equal to a real value) on failure."""

    class Boom:
        """Object whose attribute access always fails."""

        @property
        def value(self) -> Any:
            """Raise on access to simulate a broken C# property."""
            raise RuntimeError("boom")

    result = _read(Boom(), "value")
    assert result != "anything"
    assert result is not None


def test_to_be_enabled_passes_on_stub_element() -> None:
    """to_be_enabled succeeds against a stub element reporting is_enabled=True."""
    element = SimpleNamespace(is_enabled=True)
    expect(element, timeout=200).to_be_enabled()  # type: ignore[arg-type]


def test_to_be_enabled_times_out_when_disabled() -> None:
    """to_be_enabled raises AssertionError when the element is never enabled."""
    element = SimpleNamespace(is_enabled=False)
    with pytest.raises(AssertionError):
        expect(element, timeout=200).to_be_enabled()  # type: ignore[arg-type]


def test_to_be_checked_passes_on_stub_element() -> None:
    """to_be_checked succeeds against a stub element reporting is_checked=True."""
    element = SimpleNamespace(is_checked=True)
    expect(element, timeout=200).to_be_checked()  # type: ignore[arg-type]


def test_to_have_text_passes_on_stub_element() -> None:
    """to_have_text succeeds when the element's text equals the expectation."""
    element = SimpleNamespace(text="Done")
    expect(element, timeout=200).to_have_text("Done")  # type: ignore[arg-type]


def test_to_have_text_times_out_on_mismatch() -> None:
    """to_have_text raises AssertionError when the text never matches."""
    element = SimpleNamespace(text="Other")
    with pytest.raises(AssertionError):
        expect(element, timeout=200).to_have_text("Done")  # type: ignore[arg-type]


def test_to_have_value_passes_on_stub_element() -> None:
    """to_have_value succeeds when the element's value equals the expectation."""
    element = SimpleNamespace(value=42)
    expect(element, timeout=200).to_have_value(42)  # type: ignore[arg-type]
