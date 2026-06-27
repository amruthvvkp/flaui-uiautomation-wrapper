"""Wrapper for the UI Automation LegacyIAccessible pattern (``ILegacyIAccessiblePattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class LegacyIAccessiblePattern(PatternBase):
    """Represents the UI Automation LegacyIAccessible pattern bridging to MSAA ``IAccessible``."""

    @property
    @handle_csharp_exceptions
    def child_id(self) -> AutomationProperty:
        """Return the MSAA child id of the element.

        :return: An :class:`AutomationProperty` wrapping the child id.
        """
        return AutomationProperty(raw_property=self.raw_pattern.ChildId)

    @property
    @handle_csharp_exceptions
    def default_action(self) -> AutomationProperty:
        """Return the element's default action description.

        :return: An :class:`AutomationProperty` wrapping the default action.
        """
        return AutomationProperty(raw_property=self.raw_pattern.DefaultAction)

    @property
    @handle_csharp_exceptions
    def description(self) -> AutomationProperty:
        """Return the element's description.

        :return: An :class:`AutomationProperty` wrapping the description.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Description)

    @property
    @handle_csharp_exceptions
    def help(self) -> AutomationProperty:
        """Return the element's help text.

        :return: An :class:`AutomationProperty` wrapping the help text.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Help)

    @property
    @handle_csharp_exceptions
    def keyboard_shortcut(self) -> AutomationProperty:
        """Return the element's keyboard shortcut.

        :return: An :class:`AutomationProperty` wrapping the keyboard shortcut.
        """
        return AutomationProperty(raw_property=self.raw_pattern.KeyboardShortcut)

    @property
    @handle_csharp_exceptions
    def name(self) -> AutomationProperty:
        """Return the element's MSAA name.

        :return: An :class:`AutomationProperty` wrapping the name.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Name)

    @property
    @handle_csharp_exceptions
    def role(self) -> AutomationProperty:
        """Return the element's MSAA role.

        :return: An :class:`AutomationProperty` wrapping the ``AccessibilityRole`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Role)

    @property
    @handle_csharp_exceptions
    def state(self) -> AutomationProperty:
        """Return the element's MSAA state.

        :return: An :class:`AutomationProperty` wrapping the ``AccessibilityState`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.State)

    @property
    @handle_csharp_exceptions
    def selection(self) -> AutomationProperty:
        """Return the selected child elements.

        :return: An :class:`AutomationProperty` wrapping the selected elements.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Selection)

    @property
    @handle_csharp_exceptions
    def value(self) -> AutomationProperty:
        """Return the element's MSAA value.

        :return: An :class:`AutomationProperty` wrapping the value string.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Value)

    @handle_csharp_exceptions
    def do_default_action(self) -> None:
        """Perform the element's default action."""
        self.raw_pattern.DoDefaultAction()

    @handle_csharp_exceptions
    def select(self, flags_select: int) -> None:
        """Modify the selection using MSAA ``SELFLAG`` flags.

        :param flags_select: The MSAA ``SELFLAG`` bitmask describing the selection change.
        """
        self.raw_pattern.Select(flags_select)

    @handle_csharp_exceptions
    def set_value(self, value: str) -> None:
        """Set the element's value.

        :param value: The value to set.
        """
        self.raw_pattern.SetValue(value)
