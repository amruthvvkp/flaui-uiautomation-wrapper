"""Unit tests pinning the class hierarchy of concrete automation elements.

In C# FlaUI every concrete element in ``FlaUI.Core.AutomationElements`` derives from
``AutomationElement``. ``GridRow`` and ``ListBoxItem`` used to derive only from the
``SelectionItemAutomationElement`` mixin, so common members such as ``name``, ``automation_id``,
``click`` and ``find_*`` were missing. A mock stands in for the C# element so these run without a UI.
"""

import inspect
from unittest.mock import MagicMock

from flaui.core import automation_elements
from flaui.core.automation_elements import (
    AutomationElement,
    ComboBoxItem,
    ElementModel,
    GridRow,
    ListBoxItem,
    SelectionItemAutomationElement,
    TabItem,
)
import pytest

SELECTION_ITEM_ELEMENTS = [GridRow, ListBoxItem, ComboBoxItem, TabItem]

# Abstract bases / mixins that are intentionally not AutomationElement subclasses.
NON_CONCRETE = {
    "ElementModel",
    "ElementBase",
    "InvokeAutomationElement",
    "ToggleAutomationElement",
    "SelectionItemAutomationElement",
}


def _concrete_element_classes() -> list[type]:
    """Return every element wrapper class defined in ``automation_elements`` built on ``ElementModel``."""
    return [
        cls
        for name, cls in inspect.getmembers(automation_elements, inspect.isclass)
        if cls.__module__ == automation_elements.__name__ and issubclass(cls, ElementModel) and name not in NON_CONCRETE
    ]


@pytest.mark.parametrize("cls", _concrete_element_classes(), ids=lambda c: c.__name__)
def test_concrete_elements_derive_from_automation_element(cls: type) -> None:
    """Every concrete element mirrors C# by deriving from ``AutomationElement``."""
    assert issubclass(cls, AutomationElement)


@pytest.mark.parametrize("cls", SELECTION_ITEM_ELEMENTS, ids=lambda c: c.__name__)
def test_selection_items_keep_selection_mixin(cls: type) -> None:
    """Selection-item elements are both ``AutomationElement`` and ``SelectionItemAutomationElement``."""
    assert issubclass(cls, AutomationElement)
    assert issubclass(cls, SelectionItemAutomationElement)


@pytest.mark.parametrize("cls", [GridRow, ListBoxItem], ids=lambda c: c.__name__)
def test_common_members_reach_the_csharp_element(cls: type) -> None:
    """Common ``AutomationElement`` members are available and forward to the C# element."""
    raw = MagicMock()
    raw.Name = "row name"
    raw.AutomationId = "row_id"
    raw_child = MagicMock()
    raw.FindFirstChild.return_value = raw_child

    element = cls(raw_element=raw)

    assert element.name == "row name"
    assert element.automation_id == "row_id"
    element.click()
    raw.Click.assert_called_once_with(False)
    child = element.find_first_child()
    assert isinstance(child, AutomationElement)
    assert child.raw_element is raw_child


@pytest.mark.parametrize("cls", [GridRow, ListBoxItem], ids=lambda c: c.__name__)
def test_selection_members_still_work(cls: type) -> None:
    """Selection-item behaviour still comes from the mixin and returns the same wrapper type."""
    raw = MagicMock()
    raw.IsSelected = True
    raw_selected = MagicMock()
    raw.Select.return_value = raw_selected

    element = cls(raw_element=raw)

    assert element.is_selected is True
    selected = element.select()
    assert type(selected) is cls
    assert selected.raw_element is raw_selected


def test_grid_row_overrides_cached_children() -> None:
    """``GridRow.cached_children`` keeps its own override (returns cells) over the base implementation."""
    raw = MagicMock()
    raw.CachedChildren = None
    raw.Cells = [MagicMock(), MagicMock()]

    cells = GridRow(raw_element=raw).cached_children

    assert [type(c).__name__ for c in cells] == ["GridCell", "GridCell"]
