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

    @property
    @handle_csharp_exceptions
    def underlying_object(self) -> "AutomationElement":
        """Return the element at the current position (C# ``UnderlyingObject``; same as :attr:`current_element`).

        :return: The current :class:`~flaui.core.automation_elements.AutomationElement`.
        """
        return self.current_element

    @property
    @handle_csharp_exceptions
    def local_name(self) -> str:
        """Return the local name of the current node; equal to :attr:`name` since the tree has no namespaces.

        :return: The node's local name.
        """
        return self.raw_navigator.LocalName

    @property
    @handle_csharp_exceptions
    def has_attributes(self) -> bool:
        """Return whether the current node has attributes (``True`` on element nodes).

        :return: ``True`` when the current node is an element, ``False`` when positioned on an attribute.
        """
        return self.raw_navigator.HasAttributes

    @property
    @handle_csharp_exceptions
    def is_empty_element(self) -> bool:
        """Return whether the current node is an empty element (always ``False`` for UIA elements).

        :return: The C# ``IsEmptyElement`` flag.
        """
        return self.raw_navigator.IsEmptyElement

    @handle_csharp_exceptions
    def move_to(self, other: "AutomationElementXPathNavigator") -> bool:
        """Move to the same position as another navigator over the same tree.

        :param other: The navigator whose position to copy.
        :return: ``True`` if moved, ``False`` if ``other`` is not an :class:`AutomationElementXPathNavigator`.
        """
        return self.raw_navigator.MoveTo(other.raw_navigator)

    @handle_csharp_exceptions
    def is_same_position(self, other: "AutomationElementXPathNavigator") -> bool:
        """Return whether this navigator is at the same position as another.

        :param other: The navigator to compare against.
        :return: ``True`` when both point at the same element (and attribute, if any).
        """
        return self.raw_navigator.IsSamePosition(other.raw_navigator)

    @handle_csharp_exceptions
    def move_to_first_attribute(self) -> bool:
        """Move to the first attribute of the current element.

        While on an attribute, :attr:`name` is the attribute name and :attr:`value` its value; call
        :meth:`move_to_parent` to return to the element.

        :return: ``True`` if moved, ``False`` if already on an attribute.
        """
        return self.raw_navigator.MoveToFirstAttribute()

    @handle_csharp_exceptions
    def move_to_next_attribute(self) -> bool:
        """Move to the next attribute of the current element.

        :return: ``True`` if moved, ``False`` when on the last attribute or not on an attribute.
        """
        return self.raw_navigator.MoveToNextAttribute()

    @handle_csharp_exceptions
    def move_to_attribute(self, local_name: str, namespace_uri: str = "") -> bool:
        """Move to the named attribute of the current element.

        :param local_name: The attribute name (see :meth:`get_attribute` for the supported names).
        :param namespace_uri: The attribute namespace; the UIA tree uses none, so keep the default.
        :return: ``True`` if moved, ``False`` if the attribute does not exist.
        """
        return self.raw_navigator.MoveToAttribute(local_name, namespace_uri)
