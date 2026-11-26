"""Unit tests for :meth:`Tab.select_tab_item` (GH-85, audit A-3)."""

from unittest.mock import MagicMock

import pytest

from flaui.core.automation_elements import Tab, TabItem


def test_select_tab_item_by_index_returns_tab_item() -> None:
    """Selecting by index forwards to C# and returns the selected TabItem."""
    raw = MagicMock()
    item = Tab(raw_element=raw).select_tab_item(index=1)
    raw.SelectTabItem.assert_called_once_with(1)
    assert isinstance(item, TabItem)
    assert item.raw_element is raw.SelectTabItem.return_value


def test_select_tab_item_by_value() -> None:
    """Selecting by value forwards the text to C#."""
    raw = MagicMock()
    Tab(raw_element=raw).select_tab_item(value="Two")
    raw.SelectTabItem.assert_called_once_with("Two")


def test_select_tab_item_requires_index_or_value() -> None:
    """Neither index nor value is a ValueError."""
    with pytest.raises(ValueError):
        Tab(raw_element=MagicMock()).select_tab_item()


def test_select_tab_item_does_not_swallow_errors() -> None:
    """A failure in C# propagates instead of being logged and ignored."""
    raw = MagicMock()
    raw.SelectTabItem.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError):
        Tab(raw_element=raw).select_tab_item(index=0)


def test_select_tab_item_applies_post_wait() -> None:
    """The post_wait callable runs after a successful selection."""
    calls: list[int] = []
    Tab(raw_element=MagicMock()).select_tab_item(index=0, post_wait=lambda: calls.append(1))
    assert calls == [1]
