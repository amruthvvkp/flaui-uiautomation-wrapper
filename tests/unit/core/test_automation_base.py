"""Unit tests for the :class:`flaui.core.automation_base.AutomationBase` facade methods (GH-88).

Complements ``test_automation_base_wrappers.py`` (which covers the UIA2/UIA3 subtype wiring) by
exercising the property accessors, element factories, event registration, ``compare`` and the
``wrap_cs_automation`` fallback/error branches. A real UIA3 engine is used where a live automation
object is needed; small fakes drive the ``wrap_cs_automation`` branches that real C# instances can
never reach (they are caught by the ``isinstance`` checks first).
"""

import ctypes
from typing import Generator
from unittest.mock import MagicMock

from System import TimeSpan  # type: ignore
from System.Drawing import Point as CSPoint  # type: ignore
from pydantic import ValidationError
import pytest

from flaui.core.automation_base import AutomationBase, wrap_cs_automation
from flaui.core.automation_elements import AutomationElement
from flaui.core.condition_factory import ConditionFactory
from flaui.core.event_handlers import EventRegistration
from flaui.core.overlay import OverlayManager
from flaui.lib.system.drawing import Point
from flaui.uia3 import UIA3Automation


@pytest.fixture(scope="module")
def engine() -> Generator[UIA3Automation, None, None]:
    """Yield a real UIA3 automation engine, disposing it afterwards."""
    automation = UIA3Automation()
    try:
        yield automation
    finally:
        automation.dispose()


class TestValidation:
    """Validate the constructor guard."""

    def test_none_raw_automation_rejected(self) -> None:
        """Constructing the base with ``raw_automation=None`` raises a validation error."""
        with pytest.raises(ValidationError):
            AutomationBase(raw_automation=None)


class TestLibraryProperties:
    """Validate the identifier-library and factory accessors."""

    def test_libraries_present(self, engine: UIA3Automation) -> None:
        """All four identifier libraries are exposed."""
        assert engine.property_library is not None
        assert engine.event_library is not None
        assert engine.pattern_library is not None
        assert engine.text_attribute_library is not None

    def test_condition_factory(self, engine: UIA3Automation) -> None:
        """``condition_factory`` returns a Python :class:`ConditionFactory`."""
        assert isinstance(engine.condition_factory, ConditionFactory)

    def test_overlay_manager(self, engine: UIA3Automation) -> None:
        """``overlay_manager`` returns a Python :class:`OverlayManager`."""
        assert isinstance(engine.overlay_manager, OverlayManager)

    def test_tree_walker_factory(self, engine: UIA3Automation) -> None:
        """``tree_walker_factory`` exposes the C# factory."""
        assert engine.tree_walker_factory is not None

    def test_sentinel_values(self, engine: UIA3Automation) -> None:
        """The not-supported and mixed-attribute sentinels are accessible."""
        # These are provider sentinels; we only assert they can be read without error.
        _ = engine.not_supported_value
        _ = engine.mixed_attribute_value


class TestTimeoutAndBehaviorProperties:
    """Validate the get/set round-trips on the timeout and behavior properties."""

    def test_transaction_timeout_round_trip(self, engine: UIA3Automation) -> None:
        """``transaction_timeout`` is readable and settable."""
        original = engine.transaction_timeout
        engine.transaction_timeout = TimeSpan.FromSeconds(30)
        assert engine.transaction_timeout == TimeSpan.FromSeconds(30)
        engine.transaction_timeout = original

    def test_connection_timeout_round_trip(self, engine: UIA3Automation) -> None:
        """``connection_timeout`` is readable and settable."""
        original = engine.connection_timeout
        engine.connection_timeout = TimeSpan.FromSeconds(5)
        assert engine.connection_timeout == TimeSpan.FromSeconds(5)
        engine.connection_timeout = original

    def test_connection_recovery_behavior_round_trip(self, engine: UIA3Automation) -> None:
        """``connection_recovery_behavior`` is readable and settable."""
        original = engine.connection_recovery_behavior
        engine.connection_recovery_behavior = original
        assert engine.connection_recovery_behavior == original

    def test_coalesce_events_round_trip(self, engine: UIA3Automation) -> None:
        """``coalesce_events`` is readable and settable."""
        original = engine.coalesce_events
        engine.coalesce_events = original
        assert engine.coalesce_events == original


class TestElementFactories:
    """Validate the methods that produce :class:`AutomationElement` instances."""

    def test_from_point(self, engine: UIA3Automation) -> None:
        """``from_point`` returns the element at a screen coordinate."""
        element = engine.from_point(Point(raw_value=CSPoint(0, 0)))
        assert isinstance(element, AutomationElement)

    def test_from_handle(self, engine: UIA3Automation) -> None:
        """``from_handle`` returns the element for a window handle."""
        desktop_hwnd = ctypes.windll.user32.GetDesktopWindow()
        element = engine.from_handle(int(desktop_hwnd))
        assert isinstance(element, AutomationElement)

    def test_focused_element(self, engine: UIA3Automation) -> None:
        """``focused_element`` returns an element or ``None``."""
        focused = engine.focused_element()
        assert focused is None or isinstance(focused, AutomationElement)

    def test_focused_element_none_when_no_focus(self) -> None:
        """``focused_element`` returns ``None`` when the provider reports no focused element."""
        base = AutomationBase(raw_automation=MagicMock(**{"FocusedElement.return_value": None}))
        assert base.focused_element() is None


class TestToCsAutomationElement:
    """Validate the static element-unwrapping helper."""

    def test_none_returns_none(self) -> None:
        """``None`` maps to ``None``."""
        assert AutomationBase._to_cs_automation_element(None) is None

    def test_python_element_unwrapped(self, engine: UIA3Automation) -> None:
        """A Python :class:`AutomationElement` is unwrapped to its raw C# element."""
        desktop = engine.get_desktop()
        assert AutomationBase._to_cs_automation_element(desktop) is desktop.raw_element

    def test_raw_value_passthrough(self) -> None:
        """An object without ``raw_element`` passes through unchanged."""
        sentinel = object()
        assert AutomationBase._to_cs_automation_element(sentinel) is sentinel


class TestCompare:
    """Validate element identity comparison."""

    def test_compare_same_element(self, engine: UIA3Automation) -> None:
        """An element compares equal to itself."""
        desktop = engine.get_desktop()
        assert engine.compare(desktop, desktop) is True


class TestFocusChangedEvents:
    """Validate focus-changed registration and both unregister paths."""

    def test_register_then_unregister_via_registration(self, engine: UIA3Automation) -> None:
        """Registering returns an :class:`EventRegistration`; unregistering it deactivates it."""
        registration = engine.register_focus_changed_event(lambda _element: None)
        assert isinstance(registration, EventRegistration)
        assert registration.is_active is True

        engine.unregister_focus_changed_event(registration)
        assert registration.is_active is False

    def test_unregister_via_raw_handler(self, engine: UIA3Automation) -> None:
        """Passing a raw C# handler takes the non-registration unregister path."""
        registration = engine.register_focus_changed_event(lambda _element: None)
        # Pass the raw handler (not the EventRegistration) to exercise the else-branch.
        engine.unregister_focus_changed_event(registration.raw_handler)

    def test_unregister_all_events(self, engine: UIA3Automation) -> None:
        """``unregister_all_events`` runs without error."""
        engine.register_focus_changed_event(lambda _element: None)
        engine.unregister_all_events()


class TestWrapCsAutomationBranches:
    """Validate the ``wrap_cs_automation`` fallback and error branches."""

    def test_none_raises_value_error(self) -> None:
        """A ``None`` automation reference raises ``ValueError``."""
        with pytest.raises(ValueError):
            wrap_cs_automation(None)

    def test_fallback_label_uia3(self) -> None:
        """A non-C#-instance object reporting ``AutomationType == 'UIA3'`` wraps as UIA3."""

        class _FakeUia3:
            """Stand-in object that reports a UIA3 automation type."""

            class AutomationType:
                """Fake automation-type enum with a ToString."""

                @staticmethod
                def ToString() -> str:
                    """Return the UIA3 label."""
                    return "UIA3"

        wrapped = wrap_cs_automation(_FakeUia3())
        assert isinstance(wrapped, UIA3Automation)

    def test_fallback_label_uia2(self) -> None:
        """A non-C#-instance object reporting ``AutomationType == 'UIA2'`` wraps as UIA2."""
        from flaui.uia2 import UIA2Automation

        class _FakeUia2:
            """Stand-in object that reports a UIA2 automation type."""

            class AutomationType:
                """Fake automation-type enum with a ToString."""

                @staticmethod
                def ToString() -> str:
                    """Return the UIA2 label."""
                    return "UIA2"

        assert isinstance(wrap_cs_automation(_FakeUia2()), UIA2Automation)

    def test_unsupported_object_raises_type_error(self) -> None:
        """An object whose ``AutomationType`` access fails raises ``TypeError``."""
        with pytest.raises(TypeError):
            wrap_cs_automation(object())

    def test_unknown_label_raises_type_error(self) -> None:
        """A recognised-shape object with an unknown label raises ``TypeError``."""

        class _FakeUnknown:
            """Stand-in object that reports an unrecognised automation type."""

            class AutomationType:
                """Fake automation-type enum with a ToString."""

                @staticmethod
                def ToString() -> str:
                    """Return an unsupported label."""
                    return "UIA4"

        with pytest.raises(TypeError):
            wrap_cs_automation(_FakeUnknown())
