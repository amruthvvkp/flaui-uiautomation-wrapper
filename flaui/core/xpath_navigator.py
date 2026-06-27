"""Python wrapper for the C# ``FlaUI.Core.AutomationElementXPathNavigator``.

The navigator is a custom ``System.Xml.XPath.XPathNavigator`` that walks the UI Automation tree, the
same engine that backs :meth:`~flaui.core.automation_elements.AutomationElement.find_first_by_x_path`
and :meth:`~flaui.core.automation_elements.AutomationElement.find_all_by_x_path`. Most users only
need those high-level methods; this wrapper exposes the navigator directly for advanced, manual tree
navigation while keeping 1:1 parity with FlaUI C#.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from flaui.lib.exceptions import handle_csharp_exceptions

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement


class AutomationElementXPathNavigator(BaseModel):
    """Wraps the C# ``AutomationElementXPathNavigator`` for XPath-based tree navigation."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_navigator: Any = Field(..., description="The underlying C# AutomationElementXPathNavigator object")

    @classmethod
    def from_element(cls, element: "AutomationElement") -> "AutomationElementXPathNavigator":
        """Create a navigator rooted at the given element.

        :param element: The element to use as the navigation root.
        :return: A new :class:`AutomationElementXPathNavigator`.
        """
        from FlaUI.Core import AutomationElementXPathNavigator as CSNavigator  # pyright: ignore

        return cls(raw_navigator=CSNavigator(element.raw_element))

    @property
    @handle_csharp_exceptions
    def current_element(self) -> "AutomationElement":
        """Return the element at the navigator's current position.

        :return: The current :class:`~flaui.core.automation_elements.AutomationElement`.
        """
        from flaui.core.automation_elements import AutomationElement

        return AutomationElement(raw_element=self.raw_navigator.UnderlyingObject)

    @property
    @handle_csharp_exceptions
    def name(self) -> str:
        """Return the name of the current node (its control type, or attribute name).

        :return: The node name.
        """
        return self.raw_navigator.Name

    @property
    @handle_csharp_exceptions
    def value(self) -> str:
        """Return the string value of the current node.

        :return: The node value.
        """
        return self.raw_navigator.Value

    @property
    @handle_csharp_exceptions
    def node_type(self) -> str:
        """Return the XPath node type of the current node (e.g. ``Root``, ``Element``).

        :return: The node type as a string.
        """
        return str(self.raw_navigator.NodeType)

    @handle_csharp_exceptions
    def clone(self) -> "AutomationElementXPathNavigator":
        """Return an independent copy of this navigator at the same position.

        :return: A cloned navigator.
        """
        return AutomationElementXPathNavigator(raw_navigator=self.raw_navigator.Clone())

    @handle_csharp_exceptions
    def move_to_root(self) -> None:
        """Move the navigator to the root element."""
        self.raw_navigator.MoveToRoot()

    @handle_csharp_exceptions
    def move_to_first_child(self) -> bool:
        """Move to the first child of the current element.

        :return: ``True`` if moved, ``False`` if there is no child.
        """
        return self.raw_navigator.MoveToFirstChild()

    @handle_csharp_exceptions
    def move_to_parent(self) -> bool:
        """Move to the parent of the current element.

        :return: ``True`` if moved, ``False`` if already at the root.
        """
        return self.raw_navigator.MoveToParent()

    @handle_csharp_exceptions
    def move_to_next(self) -> bool:
        """Move to the next sibling of the current element.

        :return: ``True`` if moved, ``False`` if there is no next sibling.
        """
        return self.raw_navigator.MoveToNext()

    @handle_csharp_exceptions
    def move_to_previous(self) -> bool:
        """Move to the previous sibling of the current element.

        :return: ``True`` if moved, ``False`` if there is no previous sibling.
        """
        return self.raw_navigator.MoveToPrevious()

    @handle_csharp_exceptions
    def get_attribute(self, name: str) -> Optional[str]:
        """Return the value of a named attribute on the current element.

        Supported attribute names mirror the C# navigator: ``AutomationId``, ``Name``, ``ClassName``,
        ``HelpText``, ``IsPassword``, ``FullDescription``, ``ItemType``, ``AcceleratorKey``,
        ``AccessKey``, ``IsEnabled``, ``IsOffscreen``, ``ProcessId``.

        :param name: The attribute name.
        :return: The attribute value, or an empty string when unset.
        """
        return self.raw_navigator.GetAttribute(name, "")
