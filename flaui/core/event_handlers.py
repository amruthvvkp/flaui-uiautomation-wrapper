"""Support for registering UI Automation event handlers from Python.

UIA event registration takes a callback that C# invokes (on a background thread) when the event
fires. Two things make this tricky across the PythonNet boundary:

1. **Lifetime** — C#/UIA only holds the delegate; if the Python callback is garbage collected the
   callback target disappears. :class:`EventRegistration` keeps the callback (and the C# handler)
   alive in a module-level registry until it is explicitly unregistered.
2. **Threading** — events fire on UIA background threads. Callbacks therefore run off the main
   thread; exceptions are logged rather than propagated (a raised exception cannot cross back into
   the C# caller cleanly).

Most users register through the methods on
:class:`~flaui.core.automation_elements.AutomationElement` (e.g. ``register_automation_event``) and
the matching methods on :class:`~flaui.core.automation_base.AutomationBase`, which return an
:class:`EventRegistration` handle.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Callable, Set

logger = logging.getLogger(__name__)

# Strong references to live registrations so their callbacks are not garbage collected while C#
# still holds the delegate.
_live_registrations: Set["EventRegistration"] = set()
_registry_lock = threading.Lock()


class EventRegistration:
    """Handle to a registered UI Automation event; keeps the callback alive and allows unregistering.

    Use it as a context manager or call :meth:`unregister` / :meth:`dispose` when done.
    """

    def __init__(self, cs_handler: Any, callback: Callable[..., None], unregister: Callable[[Any], None]) -> None:
        """Store the C# handler and callback and add the registration to the keep-alive registry.

        :param cs_handler: The C# event-handler object returned by the native ``Register*`` call.
        :param callback: The Python callback bridged to C# (kept alive to prevent GC).
        :param unregister: A callable that unregisters ``cs_handler`` from C#.
        """
        self._cs_handler = cs_handler
        self._callback = callback
        self._unregister = unregister
        self._active = True
        with _registry_lock:
            _live_registrations.add(self)

    @property
    def raw_handler(self) -> Any:
        """Return the underlying C# event-handler object.

        :return: The native handler returned by the ``Register*`` call.
        """
        return self._cs_handler

    @property
    def is_active(self) -> bool:
        """Return whether the registration is still active.

        :return: ``True`` until :meth:`unregister` has been called.
        """
        return self._active

    def unregister(self) -> None:
        """Unregister the event handler from C# and drop the keep-alive reference."""
        if not self._active:
            return
        try:
            self._unregister(self._cs_handler)
        finally:
            self._active = False
            with _registry_lock:
                _live_registrations.discard(self)

    def dispose(self) -> None:
        """Alias for :meth:`unregister` (mirrors the C# disposable pattern)."""
        self.unregister()

    def __enter__(self) -> "EventRegistration":
        """Return self for use as a context manager.

        :return: This registration.
        """
        return self

    def __exit__(self, *exc: Any) -> None:
        """Unregister the handler when leaving the ``with`` block.

        :param exc: Exception info (unused).
        """
        self.unregister()


def coerce_event_id(event: Any) -> Any:
    """Return the raw C# ``EventId`` for an :class:`~flaui.core.identifiers.event_id.EventId` or raw value.

    :param event: A Python ``EventId`` wrapper or a raw C# ``EventId``.
    :return: The raw C# ``EventId``.
    """
    return getattr(event, "raw", event)


def coerce_property_id(property_id: Any) -> Any:
    """Return the raw C# ``PropertyId`` for a wrapper or raw value.

    :param property_id: A Python ``PropertyId`` wrapper or a raw C# ``PropertyId``.
    :return: The raw C# ``PropertyId``.
    """
    return getattr(property_id, "raw", property_id)


def coerce_tree_scope(tree_scope: Any) -> Any:
    """Return the raw C# ``TreeScope`` value for a :class:`~flaui.core.definitions.TreeScope` or raw value.

    :param tree_scope: A Python ``TreeScope`` enum member or a raw C# ``TreeScope`` value.
    :return: The raw C# ``TreeScope`` value.
    """
    return getattr(tree_scope, "value", tree_scope)


def safe_invoke(callback: Callable[..., None], *args: Any) -> None:
    """Invoke a user callback, logging (not raising) any exception.

    UIA events fire on background threads where a raised exception cannot cross back into the C#
    caller, so failures are logged instead.

    :param callback: The user-supplied callback.
    :param args: Arguments to pass to the callback.
    """
    try:
        callback(*args)
    except Exception:  # noqa: BLE001 - never let an exception escape into the C# event thread
        logger.exception("Unhandled exception in UI Automation event callback")


# ---------------------------------------------------------------------------
# Typed C# delegate builders.
#
# PythonNet does not auto-convert a plain Python function to a generic ``Action<...>`` when several
# overloads exist, so each register call needs an explicitly typed delegate. These builders import
# the C# types lazily (after the bridge is set up) and wrap the given Python function.
# ---------------------------------------------------------------------------


def make_automation_event_delegate(func: Callable[..., None]) -> Any:
    """Wrap a function as ``Action<AutomationElement, EventId>``.

    :param func: The bridge function to wrap.
    :return: A typed C# delegate.
    """
    from System import Action  # pyright: ignore

    from FlaUI.Core.AutomationElements import AutomationElement as CSAutomationElement  # pyright: ignore
    from FlaUI.Core.Identifiers import EventId as CSEventId  # pyright: ignore

    return Action[CSAutomationElement, CSEventId](func)


def make_property_changed_delegate(func: Callable[..., None]) -> Any:
    """Wrap a function as ``Action<AutomationElement, PropertyId, object>``.

    :param func: The bridge function to wrap.
    :return: A typed C# delegate.
    """
    from System import Action, Object  # pyright: ignore

    from FlaUI.Core.AutomationElements import AutomationElement as CSAutomationElement  # pyright: ignore
    from FlaUI.Core.Identifiers import PropertyId as CSPropertyId  # pyright: ignore

    return Action[CSAutomationElement, CSPropertyId, Object](func)


def make_structure_changed_delegate(func: Callable[..., None]) -> Any:
    """Wrap a function as ``Action<AutomationElement, StructureChangeType, int[]>``.

    :param func: The bridge function to wrap.
    :return: A typed C# delegate.
    """
    from System import Action, Array, Int32  # pyright: ignore

    from FlaUI.Core.AutomationElements import AutomationElement as CSAutomationElement  # pyright: ignore
    from FlaUI.Core.Definitions import StructureChangeType  # pyright: ignore

    return Action[CSAutomationElement, StructureChangeType, Array[Int32]](func)


def make_notification_delegate(func: Callable[..., None]) -> Any:
    """Wrap a function as the notification ``Action<AutomationElement, NotificationKind, ...>``.

    :param func: The bridge function to wrap.
    :return: A typed C# delegate.
    """
    from System import Action, String  # pyright: ignore

    from FlaUI.Core.AutomationElements import AutomationElement as CSAutomationElement  # pyright: ignore
    from FlaUI.Core.Definitions import NotificationKind, NotificationProcessing  # pyright: ignore

    return Action[CSAutomationElement, NotificationKind, NotificationProcessing, String, String](func)


def make_focus_changed_delegate(func: Callable[..., None]) -> Any:
    """Wrap a function as ``Action<AutomationElement>``.

    :param func: The bridge function to wrap.
    :return: A typed C# delegate.
    """
    from System import Action  # pyright: ignore

    from FlaUI.Core.AutomationElements import AutomationElement as CSAutomationElement  # pyright: ignore

    return Action[CSAutomationElement](func)


def make_active_text_position_delegate(func: Callable[..., None]) -> Any:
    """Wrap a function as ``Action<AutomationElement, ITextRange>``.

    :param func: The bridge function to wrap.
    :return: A typed C# delegate.
    """
    from System import Action  # pyright: ignore

    from FlaUI.Core import ITextRange  # pyright: ignore
    from FlaUI.Core.AutomationElements import AutomationElement as CSAutomationElement  # pyright: ignore

    return Action[CSAutomationElement, ITextRange](func)


def make_text_edit_delegate(func: Callable[..., None]) -> Any:
    """Wrap a function as ``Action<AutomationElement, TextEditChangeType, string[]>``.

    :param func: The bridge function to wrap.
    :return: A typed C# delegate.
    """
    from System import Action, Array, String  # pyright: ignore

    from FlaUI.Core.AutomationElements import AutomationElement as CSAutomationElement  # pyright: ignore
    from FlaUI.Core.Definitions import TextEditChangeType  # pyright: ignore

    return Action[CSAutomationElement, TextEditChangeType, Array[String]](func)
