"""Unit tests for AutomationElementCollection (iterator/collection protocol)."""

from types import SimpleNamespace

from flaui.core.automation_elements import AutomationElementCollection
from flaui.uia3 import UIA3Automation


def test_behaves_like_a_list() -> None:
    """The collection supports indexing, length, iteration, and truthiness."""
    collection = AutomationElementCollection([1, 2, 3])
    assert len(collection) == 3
    assert collection[0] == 1
    assert list(collection) == [1, 2, 3]
    assert bool(collection) is True
    assert bool(AutomationElementCollection()) is False


def test_first_returns_none_when_empty() -> None:
    """first returns None for an empty collection."""
    assert AutomationElementCollection().first is None


def test_first_returns_first_element() -> None:
    """first returns the leading element of a non-empty collection."""
    assert AutomationElementCollection(["a", "b"]).first == "a"


def test_filter_returns_a_new_collection() -> None:
    """filter keeps elements matching the predicate and returns a collection."""
    collection = AutomationElementCollection([1, 2, 3, 4])
    even = collection.filter(lambda value: value % 2 == 0)
    assert isinstance(even, AutomationElementCollection)
    assert list(even) == [2, 4]


def test_where_matches_attribute_values() -> None:
    """where keeps elements whose attributes equal the given values."""
    ok = SimpleNamespace(name="OK", automation_id="ok")
    cancel = SimpleNamespace(name="Cancel", automation_id="cancel")
    collection = AutomationElementCollection([ok, cancel])
    assert list(collection.where(name="OK")) == [ok]


def test_where_treats_missing_attribute_as_no_match() -> None:
    """where filters out elements lacking the requested attribute instead of raising."""
    collection = AutomationElementCollection([SimpleNamespace(name="OK")])
    assert list(collection.where(missing="x")) == []


def test_repr_shows_count_and_preview() -> None:
    """The repr surfaces the element count for quick debugging."""
    representation = repr(AutomationElementCollection([1, 2, 3, 4]))
    assert "AutomationElementCollection" in representation
    assert "len=4" in representation


def test_find_all_children_returns_collection() -> None:
    """find_all_children returns an AutomationElementCollection from a real element."""
    desktop = UIA3Automation().get_desktop()
    children = desktop.find_all_children()
    assert isinstance(children, AutomationElementCollection)
