"""Wrapper for the UI Automation MultipleView pattern (``IMultipleViewPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class MultipleViewPattern(PatternBase):
    """Represents the UI Automation MultipleView pattern for controls with several presentations."""

    @property
    @handle_csharp_exceptions
    def current_view(self) -> AutomationProperty:
        """Return the identifier of the current view.

        :return: An :class:`AutomationProperty` wrapping the current view id.
        """
        return AutomationProperty(raw_property=self.raw_pattern.CurrentView)

    @property
    @handle_csharp_exceptions
    def supported_views(self) -> AutomationProperty:
        """Return the identifiers of all supported views.

        :return: An :class:`AutomationProperty` wrapping the supported view ids.
        """
        return AutomationProperty(raw_property=self.raw_pattern.SupportedViews)

    @handle_csharp_exceptions
    def get_view_name(self, view: int) -> str:
        """Return the localized name of a view.

        :param view: The view identifier.
        :return: The view's localized name.
        """
        return self.raw_pattern.GetViewName(view)

    @handle_csharp_exceptions
    def set_current_view(self, view: int) -> None:
        """Switch the control to the given view.

        :param view: The view identifier to switch to.
        """
        self.raw_pattern.SetCurrentView(view)
