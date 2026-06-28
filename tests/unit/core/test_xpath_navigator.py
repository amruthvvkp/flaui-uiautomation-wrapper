"""Unit tests for :mod:`flaui.core.xpath_navigator` (GH-88).

Two angles are covered:

* a :class:`unittest.mock.MagicMock` stub navigator gives deterministic coverage of every
  delegating property/method, and
* a real navigator rooted at the desktop exercises ``from_element`` and the C# round-trip without
  launching an application.
"""

from typing import Generator
from unittest.mock import MagicMock

import pytest

from flaui.core.automation_elements import AutomationElement
from flaui.core.xpath_navigator import AutomationElementXPathNavigator
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


class TestDelegation:
    """Validate that each wrapper member forwards to the underlying C# navigator."""

    @pytest.fixture()
    def raw(self) -> MagicMock:
        """Return a stub C# navigator with deterministic return values."""
        stub = MagicMock(name="raw_navigator")
        stub.Name = "Window"
        stub.Value = "node-value"
        stub.NodeType = "Element"
        stub.MoveToFirstChild.return_value = True
        stub.MoveToParent.return_value = False
        stub.MoveToNext.return_value = True
        stub.MoveToPrevious.return_value = False
        stub.GetAttribute.return_value = "attr-value"
        return stub

    @pytest.fixture()
    def navigator(self, raw: MagicMock) -> AutomationElementXPathNavigator:
        """Return a navigator wrapping the stub."""
        return AutomationElementXPathNavigator(raw_navigator=raw)

    def test_name_value_node_type(self, navigator: AutomationElementXPathNavigator) -> None:
        """The scalar properties forward to the matching C# members."""
        assert navigator.name == "Window"
        assert navigator.value == "node-value"
        assert navigator.node_type == "Element"

    def test_current_element_wraps_underlying_object(
        self, navigator: AutomationElementXPathNavigator, raw: MagicMock
    ) -> None:
        """``current_element`` wraps ``UnderlyingObject`` in an :class:`AutomationElement`."""
        element = navigator.current_element
        assert isinstance(element, AutomationElement)
        assert element.raw_element is raw.UnderlyingObject

    def test_clone_returns_new_wrapper(self, navigator: AutomationElementXPathNavigator, raw: MagicMock) -> None:
        """``clone`` wraps the C# ``Clone()`` result in a new navigator."""
        clone = navigator.clone()
        assert isinstance(clone, AutomationElementXPathNavigator)
        assert clone.raw_navigator is raw.Clone.return_value

    def test_move_to_root_delegates(self, navigator: AutomationElementXPathNavigator, raw: MagicMock) -> None:
        """``move_to_root`` calls ``MoveToRoot`` and returns nothing."""
        assert navigator.move_to_root() is None
        raw.MoveToRoot.assert_called_once_with()

    def test_move_methods_return_bools(self, navigator: AutomationElementXPathNavigator) -> None:
        """The ``move_to_*`` navigation methods return the C# boolean result."""
        assert navigator.move_to_first_child() is True
        assert navigator.move_to_parent() is False
        assert navigator.move_to_next() is True
        assert navigator.move_to_previous() is False

    def test_get_attribute_passes_empty_default(
        self, navigator: AutomationElementXPathNavigator, raw: MagicMock
    ) -> None:
        """``get_attribute`` forwards the name and the C# empty-string default."""
        assert navigator.get_attribute("AutomationId") == "attr-value"
        raw.GetAttribute.assert_called_once_with("AutomationId", "")


class TestFromElement:
    """Validate construction from a real element and a live C# round-trip on the desktop tree."""

    @pytest.fixture(scope="class")
    def desktop(self) -> Generator[AutomationElement, None, None]:
        """Yield the desktop element from a UIA3 automation, disposing it afterwards."""
        automation = Automation(UIAutomationTypes.UIA3)
        try:
            yield automation.automation_base.get_desktop()
        finally:
            automation.cs_automation.Dispose()

    def test_from_element_builds_navigator(self, desktop: AutomationElement) -> None:
        """``from_element`` roots a navigator at the given element."""
        navigator = AutomationElementXPathNavigator.from_element(desktop)

        assert isinstance(navigator, AutomationElementXPathNavigator)
        assert navigator.raw_navigator is not None

    def test_real_navigator_round_trip(self, desktop: AutomationElement) -> None:
        """A real navigator exposes string node metadata and walks the tree."""
        navigator = AutomationElementXPathNavigator.from_element(desktop)

        navigator.move_to_root()
        assert isinstance(navigator.name, str)
        assert isinstance(navigator.value, str)
        assert isinstance(navigator.node_type, str)

        # The desktop always has children, so the first move down must succeed.
        assert navigator.move_to_first_child() is True
        assert isinstance(navigator.current_element, AutomationElement)

        clone = navigator.clone()
        assert isinstance(clone, AutomationElementXPathNavigator)
        assert isinstance(clone.get_attribute("Name"), str)
