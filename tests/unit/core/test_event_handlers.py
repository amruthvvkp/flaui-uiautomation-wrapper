"""Unit tests for :mod:`flaui.core.event_handlers` (GH-88).

These cover the pure-Python registration machinery (no running application needed) and the typed
C# delegate builders, which only require the PythonNet bridge set up by the global conftest.
"""

import logging
from typing import Any, Callable, Generator, List

import pytest

from flaui.core.definitions import TreeScope
from flaui.core.event_handlers import (
    EventRegistration,
    _live_registrations,
    coerce_event_id,
    coerce_property_id,
    coerce_tree_scope,
    make_active_text_position_delegate,
    make_automation_event_delegate,
    make_focus_changed_delegate,
    make_notification_delegate,
    make_property_changed_delegate,
    make_structure_changed_delegate,
    make_text_edit_delegate,
    safe_invoke,
)


@pytest.fixture(autouse=True)
def _clear_registry() -> Generator[None, None, None]:
    """Ensure the module-level keep-alive registry is empty around each test."""
    _live_registrations.clear()
    yield
    _live_registrations.clear()


def _make_registration() -> tuple[EventRegistration, List[Any]]:
    """Build an :class:`EventRegistration` with a stub handler and a recording unregister callable.

    :return: The registration and the list that records each unregistered handler.
    """
    unregistered: List[Any] = []
    handler = object()
    registration = EventRegistration(
        cs_handler=handler,
        callback=lambda *_: None,
        unregister=unregistered.append,
    )
    return registration, unregistered


class TestEventRegistration:
    """Validate the lifecycle, accessors, and context-manager behaviour."""

    def test_construction_registers_keepalive(self) -> None:
        """A new registration is tracked in the module-level keep-alive set and is active."""
        registration, _ = _make_registration()

        assert registration in _live_registrations
        assert registration.is_active is True

    def test_raw_handler_exposes_cs_handler(self) -> None:
        """``raw_handler`` returns the C# handler object passed at construction."""
        handler = object()
        registration = EventRegistration(handler, lambda *_: None, lambda _: None)

        assert registration.raw_handler is handler

    def test_unregister_invokes_callback_and_drops_keepalive(self) -> None:
        """``unregister`` calls the unregister callable, deactivates, and leaves the registry."""
        registration, unregistered = _make_registration()

        registration.unregister()

        assert unregistered == [registration.raw_handler]
        assert registration.is_active is False
        assert registration not in _live_registrations

    def test_unregister_is_idempotent(self) -> None:
        """Calling ``unregister`` twice only unregisters once."""
        registration, unregistered = _make_registration()

        registration.unregister()
        registration.unregister()

        assert len(unregistered) == 1

    def test_dispose_is_alias_for_unregister(self) -> None:
        """``dispose`` mirrors the C# disposable pattern by delegating to ``unregister``."""
        registration, unregistered = _make_registration()

        registration.dispose()

        assert registration.is_active is False
        assert len(unregistered) == 1

    def test_context_manager_unregisters_on_exit(self) -> None:
        """Using the registration as a context manager unregisters on block exit."""
        registration, unregistered = _make_registration()

        with registration as entered:
            assert entered is registration
            assert registration.is_active is True

        assert registration.is_active is False
        assert unregistered == [registration.raw_handler]

    def test_unregister_drops_keepalive_even_when_callback_raises(self) -> None:
        """A failing unregister callable still deactivates and drops the keep-alive reference."""

        def _boom(_: Any) -> None:
            """Stub unregister callable that always fails."""
            raise RuntimeError("unregister failed")

        registration = EventRegistration(object(), lambda *_: None, _boom)

        with pytest.raises(RuntimeError):
            registration.unregister()

        assert registration.is_active is False
        assert registration not in _live_registrations


class TestCoercion:
    """Validate the wrapper-or-raw coercion helpers."""

    def test_coerce_event_id_unwraps_and_passes_through(self) -> None:
        """A wrapper's ``raw`` is returned; a bare value passes through unchanged."""

        class _Wrapper:
            raw = "cs-event-id"

        sentinel = object()
        assert coerce_event_id(_Wrapper()) == "cs-event-id"
        assert coerce_event_id(sentinel) is sentinel

    def test_coerce_property_id_unwraps_and_passes_through(self) -> None:
        """A wrapper's ``raw`` is returned; a bare value passes through unchanged."""

        class _Wrapper:
            raw = "cs-property-id"

        sentinel = object()
        assert coerce_property_id(_Wrapper()) == "cs-property-id"
        assert coerce_property_id(sentinel) is sentinel

    def test_coerce_tree_scope_unwraps_enum_and_passes_through(self) -> None:
        """A ``TreeScope`` enum yields its ``value``; a raw value passes through unchanged."""
        assert coerce_tree_scope(TreeScope.Subtree) == TreeScope.Subtree.value

        sentinel = object()
        assert coerce_tree_scope(sentinel) is sentinel


class TestSafeInvoke:
    """Validate that callbacks are invoked and exceptions are logged, never raised."""

    def test_invokes_callback_with_args(self) -> None:
        """The callback runs with the forwarded positional arguments."""
        received: List[tuple[Any, ...]] = []

        safe_invoke(lambda *args: received.append(args), 1, "two", 3.0)

        assert received == [(1, "two", 3.0)]

    def test_swallows_and_logs_exception(self, caplog: pytest.LogCaptureFixture) -> None:
        """An exception in the callback is logged, not propagated, to protect the C# event thread."""

        def _boom() -> None:
            """Stub callback that always raises."""
            raise ValueError("callback blew up")

        with caplog.at_level(logging.ERROR, logger="flaui.core.event_handlers"):
            safe_invoke(_boom)  # must not raise

        assert any("Unhandled exception" in record.message for record in caplog.records)


class TestDelegateBuilders:
    """Validate that each typed delegate builder wraps a Python callable into a C# delegate."""

    @pytest.mark.parametrize(
        "builder",
        [
            make_automation_event_delegate,
            make_property_changed_delegate,
            make_structure_changed_delegate,
            make_notification_delegate,
            make_focus_changed_delegate,
            make_active_text_position_delegate,
            make_text_edit_delegate,
        ],
    )
    def test_builder_returns_delegate(self, builder: Callable[[Callable[..., None]], Any]) -> None:
        """Each builder returns a non-null C# ``Action`` delegate for the given function."""

        def _noop(*_: Any) -> None:
            """Placeholder callback handed to the delegate builder."""

        delegate = builder(_noop)

        assert delegate is not None
        assert "Action" in type(delegate).__name__
