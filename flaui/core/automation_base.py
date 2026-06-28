"""Python wrapper for FlaUI.Core.AutomationBase and factory for UIA2/UIA3 implementations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from flaui.core.automation_type import AutomationType
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.exceptions import handle_csharp_exceptions
from flaui.lib.system.drawing import Point

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement
    from flaui.core.overlay import OverlayManager


class AutomationBase(BaseModel):
    """Delegates to a C# FlaUI.Core.AutomationBase instance (UIA2 or UIA3)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_automation: Any = Field(..., description="Underlying C# AutomationBase instance")

    @field_validator("raw_automation")
    @classmethod
    def validate_raw_automation(cls, v: Any, info: ValidationInfo) -> Any:
        """Reject a missing C# automation reference."""
        if v is None:
            raise ValueError("raw_automation must not be None")
        return v

    @property
    @handle_csharp_exceptions
    def property_library(self) -> Any:
        """Return the C# property identifier library."""
        return self.raw_automation.PropertyLibrary

    @property
    @handle_csharp_exceptions
    def event_library(self) -> Any:
        """Return the C# event identifier library."""
        return self.raw_automation.EventLibrary

    @property
    @handle_csharp_exceptions
    def pattern_library(self) -> Any:
        """Return the C# pattern identifier library."""
        return self.raw_automation.PatternLibrary

    @property
    @handle_csharp_exceptions
    def text_attribute_library(self) -> Any:
        """Return the C# text attribute library."""
        return self.raw_automation.TextAttributeLibrary

    @property
    @handle_csharp_exceptions
    def condition_factory(self) -> ConditionFactory:
        """Return a Python wrapper around the C# ConditionFactory."""
        return ConditionFactory(raw_cf=self.raw_automation.ConditionFactory)

    @property
    @handle_csharp_exceptions
    def overlay_manager(self) -> "OverlayManager":
        """Return a Python wrapper around the C# overlay manager (visual-debugging overlays)."""
        from flaui.core.overlay import OverlayManager

        return OverlayManager(raw_overlay_manager=self.raw_automation.OverlayManager)

    @property
    @handle_csharp_exceptions
    def tree_walker_factory(self) -> Any:
        """Return the C# tree walker factory."""
        return self.raw_automation.TreeWalkerFactory

    @property
    @handle_csharp_exceptions
    def automation_type(self) -> AutomationType:
        """Return UIA2 or UIA3 for this automation stack."""
        return AutomationType[self.raw_automation.AutomationType.ToString()]

    @property
    @handle_csharp_exceptions
    def not_supported_value(self) -> Any:
        """Return the provider-specific sentinel for unsupported values."""
        return self.raw_automation.NotSupportedValue

    @property
    @handle_csharp_exceptions
    def mixed_attribute_value(self) -> Any:
        """Return the sentinel for mixed text attributes."""
        return self.raw_automation.MixedAttributeValue

    @property
    @handle_csharp_exceptions
    def transaction_timeout(self) -> Any:
        """Get the C# transaction timeout (TimeSpan)."""
        return self.raw_automation.TransactionTimeout

    @transaction_timeout.setter
    @handle_csharp_exceptions
    def transaction_timeout(self, value: Any) -> None:
        """Set the C# transaction timeout (TimeSpan)."""
        self.raw_automation.TransactionTimeout = value

    @property
    @handle_csharp_exceptions
    def connection_timeout(self) -> Any:
        """Get the C# connection timeout (TimeSpan)."""
        return self.raw_automation.ConnectionTimeout

    @connection_timeout.setter
    @handle_csharp_exceptions
    def connection_timeout(self, value: Any) -> None:
        """Set the C# connection timeout (TimeSpan)."""
        self.raw_automation.ConnectionTimeout = value

    @property
    @handle_csharp_exceptions
    def connection_recovery_behavior(self) -> Any:
        """Get connection recovery behavior (C# enum)."""
        return self.raw_automation.ConnectionRecoveryBehavior

    @connection_recovery_behavior.setter
    @handle_csharp_exceptions
    def connection_recovery_behavior(self, value: Any) -> None:
        """Set connection recovery behavior (C# enum)."""
        self.raw_automation.ConnectionRecoveryBehavior = value

    @property
    @handle_csharp_exceptions
    def coalesce_events(self) -> Any:
        """Get coalesce-events option (C# enum)."""
        return self.raw_automation.CoalesceEvents

    @coalesce_events.setter
    @handle_csharp_exceptions
    def coalesce_events(self, value: Any) -> None:
        """Set coalesce-events option (C# enum)."""
        self.raw_automation.CoalesceEvents = value

    @staticmethod
    def _to_cs_automation_element(element: Any) -> Any:
        """Unwrap a Python AutomationElement or pass through a C# element."""
        if element is None:
            return None
        raw = getattr(element, "raw_element", None)
        return raw if raw is not None else element

    @handle_csharp_exceptions
    def get_desktop(self) -> AutomationElement:
        """Return the desktop (root) element as a Python AutomationElement."""
        from flaui.core.automation_elements import AutomationElement as PyAutomationElement

        return PyAutomationElement(raw_element=self.raw_automation.GetDesktop())

    @handle_csharp_exceptions
    def from_point(self, point: Point) -> AutomationElement:
        """Return the element at the given screen point."""
        from flaui.core.automation_elements import AutomationElement as PyAutomationElement

        return PyAutomationElement(raw_element=self.raw_automation.FromPoint(point.raw_value))

    @handle_csharp_exceptions
    def from_handle(self, hwnd: int) -> AutomationElement:
        """Return the element for a window handle (HWND)."""
        from System import IntPtr  # pyright: ignore
        from flaui.core.automation_elements import AutomationElement as PyAutomationElement

        return PyAutomationElement(raw_element=self.raw_automation.FromHandle(IntPtr(hwnd)))

    @handle_csharp_exceptions
    def focused_element(self) -> Optional[AutomationElement]:
        """Return the currently focused element, or None when the provider has no focus."""
        from flaui.core.automation_elements import AutomationElement as PyAutomationElement

        raw = self.raw_automation.FocusedElement()
        if raw is None:
            return None
        return PyAutomationElement(raw_element=raw)

    @handle_csharp_exceptions
    def register_focus_changed_event(self, action: Any) -> Any:
        """Register a focus-changed handler.

        :param action: Callback ``(element) -> None`` invoked when focus changes.
        :return: An :class:`~flaui.core.event_handlers.EventRegistration` handle that keeps the
            callback alive and can unregister it.
        """
        from flaui.core.automation_elements import AutomationElement as PyAutomationElement
        from flaui.core.event_handlers import EventRegistration, make_focus_changed_delegate, safe_invoke

        def _handler(sender: Any) -> None:
            """Bridge the C# callback to the Python action."""
            safe_invoke(action, PyAutomationElement(raw_element=sender))

        handler = self.raw_automation.RegisterFocusChangedEvent(make_focus_changed_delegate(_handler))
        return EventRegistration(
            cs_handler=handler,
            callback=_handler,
            unregister=lambda h: self.raw_automation.UnregisterFocusChangedEvent(h),
        )

    @handle_csharp_exceptions
    def unregister_focus_changed_event(self, event_handler: Any) -> None:
        """Unregister a focus-changed handler returned by :meth:`register_focus_changed_event`.

        :param event_handler: The :class:`~flaui.core.event_handlers.EventRegistration` returned by
            :meth:`register_focus_changed_event`, or a raw C# handler.
        """
        from flaui.core.event_handlers import EventRegistration

        if isinstance(event_handler, EventRegistration):
            event_handler.unregister()
        else:
            self.raw_automation.UnregisterFocusChangedEvent(event_handler)

    @handle_csharp_exceptions
    def unregister_all_events(self) -> None:
        """Remove all registered UI Automation event handlers."""
        self.raw_automation.UnregisterAllEvents()

    @handle_csharp_exceptions
    def compare(self, element1: Any, element2: Any) -> bool:
        """Return whether two elements refer to the same underlying UI element."""
        return self.raw_automation.Compare(
            self._to_cs_automation_element(element1),
            self._to_cs_automation_element(element2),
        )

    @handle_csharp_exceptions
    def dispose(self) -> None:
        """Release automation resources (matches C# Dispose)."""
        self.raw_automation.Dispose()


def wrap_cs_automation(raw: Any) -> AutomationBase:
    """Wrap an existing C# AutomationBase (e.g. from AutomationElement.Automation) in Python.

    :param raw: C# FlaUI.Core.AutomationBase implementation instance
    :return: UIA2Automation or UIA3Automation Python wrapper
    :raises TypeError: If the object is not a supported automation implementation
    :raises ValueError: If raw is None
    """
    if raw is None:
        raise ValueError("automation reference is required")

    from FlaUI.UIA2 import UIA2Automation as CSUIA2Automation  # pyright: ignore
    from FlaUI.UIA3 import UIA3Automation as CSUIA3Automation  # pyright: ignore

    from flaui.uia2.automation import UIA2Automation
    from flaui.uia3.automation import UIA3Automation

    if isinstance(raw, CSUIA3Automation):
        return UIA3Automation(raw_automation=raw)
    if isinstance(raw, CSUIA2Automation):
        return UIA2Automation(raw_automation=raw)

    try:
        label = raw.AutomationType.ToString()
        if label == "UIA3":
            return UIA3Automation(raw_automation=raw)
        if label == "UIA2":
            return UIA2Automation(raw_automation=raw)
    except Exception:
        pass

    raise TypeError("Unsupported automation implementation: {!r}".format(type(raw)))
