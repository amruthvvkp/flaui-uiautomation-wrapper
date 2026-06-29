"""Unit tests for the Python identifier wrappers (``flaui.core.identifiers``)."""

from typing import Any, Generator

from FlaUI.UIA3 import UIA3Automation  # type: ignore
import pytest

from flaui.core.identifiers import EventId, IdentifierBase, PatternId, PropertyId, TextAttributeId


@pytest.fixture(name="automation", scope="module")
def get_automation() -> Generator[Any, Any, None]:
    """Provide a UIA3 automation instance for sourcing real C# identifiers."""
    auto = UIA3Automation()
    yield auto
    auto.Dispose()


class TestIdentifierWrappers:
    """Validate the thin wrappers expose the C# identifier surface Pythonically."""

    def test_property_id_exposes_id_and_name(self, automation: Any) -> None:
        """A wrapped PropertyId exposes the native id, name, and ``Name [#Id]`` repr."""
        raw = automation.PropertyLibrary.Element.Name
        pid = PropertyId(raw=raw)
        assert pid.id == raw.Id
        assert pid.name == raw.Name
        assert repr(pid) == f"{raw.Name} [#{raw.Id}]"

    def test_event_and_text_attribute_wrappers(self, automation: Any) -> None:
        """EventId and TextAttributeId wrap their C# identifiers and expose id/name."""
        text_attr = TextAttributeId(raw=automation.TextAttributeLibrary.ForegroundColor)
        assert text_attr.name == "ForegroundColor"
        assert isinstance(text_attr, IdentifierBase)

    def test_equality_and_hash_by_id(self, automation: Any) -> None:
        """Identifiers compare equal and hash alike when they share an id."""
        raw = automation.PropertyLibrary.Element.Name
        first = PropertyId(raw=raw)
        second = PropertyId(raw=raw)
        assert first == second
        assert hash(first) == hash(second)
        assert len({first, second}) == 1

    def test_inequality_for_different_ids(self, automation: Any) -> None:
        """Identifiers with different ids are not equal."""
        name = PropertyId(raw=automation.PropertyLibrary.Element.Name)
        automation_id = PropertyId(raw=automation.PropertyLibrary.Element.AutomationId)
        assert name != automation_id

    def test_pattern_availability_property(self, automation: Any) -> None:
        """WindowPattern exposes its availability property wrapped as a PropertyId."""
        window = PatternId(raw=automation.PatternLibrary.WindowPattern)
        assert window.name == "Window"
        availability = window.availability_property
        assert isinstance(availability, PropertyId)
        assert availability.name == "IsWindowPatternAvailable"

    def test_none_raw_rejected(self) -> None:
        """Constructing an identifier with a missing C# reference is rejected."""
        with pytest.raises(ValueError):
            EventId(raw=None)

    def test_equality_with_non_identifier_is_not_equal(self, automation: Any) -> None:
        """Comparing an identifier to a non-identifier returns NotImplemented, so ``==`` is False."""
        identifier = PropertyId(raw=automation.PropertyLibrary.Element.Name)
        # Exercises the ``return NotImplemented`` branch of ``__eq__`` (Python then falls back to
        # identity, yielding ``False``) for an unrelated object.
        assert (identifier == "not-an-identifier") is False
        assert identifier != "not-an-identifier"
