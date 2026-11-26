"""Unit tests for the ``FlaUI.Core.Definitions`` enum ports in :mod:`flaui.core.definitions` (GH-157).

They check value parity against the bundled C# enums by reflection and that the values FlaUI hands back
(properties, automation options, event callbacks) arrive as Python enums.
"""

from enum import Enum, IntFlag
from typing import Any, Callable, Dict, List, Type

from System import Enum as CSEnum  # pyright: ignore

from FlaUI.Core import FrameworkType as CSFrameworkType  # pyright: ignore
import FlaUI.Core.Definitions as CSDefinitions  # pyright: ignore
from FlaUI.UIA3 import UIA3Automation as CSUIA3Automation  # pyright: ignore
import pytest

from flaui.core import event_handlers
from flaui.core.automation_elements import AutomationElement, AutomationProperty
from flaui.core.definitions import (
    AnnotationType,
    CoalesceEventsOptions,
    ConnectionRecoveryBehaviorOptions,
    FrameworkIds,
    HeadingLevel,
    LandmarkType,
    LiveSetting,
    NotificationKind,
    NotificationProcessing,
    OrientationType,
    StructureChangeType,
    StyleType,
    TextEditChangeType,
    ToggleState,
    TreeScope,
    VisualEffects,
    to_cs_enum,
    to_python_enum,
)
from flaui.core.framework_types import FrameworkType
from flaui.uia3.automation import UIA3Automation

PORTED_ENUMS: List[Type[Enum]] = [
    AnnotationType,
    CoalesceEventsOptions,
    ConnectionRecoveryBehaviorOptions,
    HeadingLevel,
    LandmarkType,
    LiveSetting,
    NotificationKind,
    NotificationProcessing,
    OrientationType,
    StructureChangeType,
    StyleType,
    TextEditChangeType,
    VisualEffects,
]


def _cs_members(enum_type: Type[Enum]) -> Dict[str, int]:
    """Return the C# enum's members as ``{python_name: int_value}``.

    :param enum_type: The Python port; its name is looked up in ``FlaUI.Core.Definitions``.
    :return: Member names (``None`` mapped to ``None_``) and their integer values.
    """
    cs_type = getattr(CSDefinitions, enum_type.__name__)
    names = CSEnum.GetNames(cs_type)
    return {("None_" if name == "None" else name): int(CSEnum.Parse(cs_type, name)) for name in names}


class TestValueParity:
    """Each ported enum mirrors its C# counterpart member for member."""

    @pytest.mark.parametrize("enum_type", PORTED_ENUMS, ids=lambda e: e.__name__)
    def test_members_and_values_match_csharp(self, enum_type: Type[Enum]) -> None:
        """Member names and integer values are identical to the C# enum."""
        python_members = {name: int(member.value) for name, member in enum_type.__members__.items()}
        assert python_members == _cs_members(enum_type)

    @pytest.mark.parametrize("enum_type", PORTED_ENUMS, ids=lambda e: e.__name__)
    def test_every_csharp_value_converts(self, enum_type: Type[Enum]) -> None:
        """Every C# member converts to the Python member of the same name, inferred from its C# type."""
        cs_type = getattr(CSDefinitions, enum_type.__name__)
        for name in CSEnum.GetNames(cs_type):
            converted = to_python_enum(CSEnum.Parse(cs_type, name))
            assert converted is enum_type["None_" if name == "None" else name]

    @pytest.mark.parametrize("enum_type", PORTED_ENUMS, ids=lambda e: e.__name__)
    def test_round_trip_to_csharp(self, enum_type: Type[Enum]) -> None:
        """Converting a Python member to C# and back returns the same member."""
        for member in enum_type.__members__.values():
            cs_value = to_cs_enum(member)
            assert str(cs_value.GetType().FullName) == f"FlaUI.Core.Definitions.{enum_type.__name__}"
            assert to_python_enum(cs_value) is member


class TestConversionHelpers:
    """Edge cases of :func:`to_python_enum` / :func:`to_cs_enum`."""

    def test_combined_visual_effects_flags(self) -> None:
        """A combined C# ``[Flags]`` value converts to the matching :class:`IntFlag` combination."""
        combined = CSDefinitions.VisualEffects.Shadow | CSDefinitions.VisualEffects.Glow
        converted = to_python_enum(combined)
        assert isinstance(converted, IntFlag)
        assert converted == VisualEffects.Shadow | VisualEffects.Glow
        assert int(to_cs_enum(converted)) == int(combined)

    @pytest.mark.parametrize("value", [None, 5, "text", ToggleState.On])
    def test_unmapped_values_pass_through(self, value: Any) -> None:
        """``None``, plain Python values and Python enum members are returned unchanged."""
        assert to_python_enum(value) is value

    def test_unmapped_csharp_enum_passes_through(self) -> None:
        """C# enums that keep their existing handling (e.g. ``ToggleState``) are not converted implicitly."""
        raw = CSDefinitions.ToggleState.On
        assert to_python_enum(raw) is raw

    def test_undefined_csharp_value_passes_through(self) -> None:
        """``default(HeadingLevel)`` (0, not a defined member) is returned unchanged instead of raising."""
        raw = CSEnum.ToObject(CSDefinitions.HeadingLevel, 0)
        assert to_python_enum(raw) is raw

    def test_explicit_target_enum(self) -> None:
        """An explicit ``enum_type`` is honoured, including for enums outside the automatic map."""
        assert to_python_enum(CSDefinitions.ToggleState.On, ToggleState) is ToggleState.On

    def test_to_cs_enum_passes_raw_values_through(self) -> None:
        """Raw C# values are handed back unchanged."""
        raw = CSDefinitions.LiveSetting.Polite
        assert to_cs_enum(raw) is raw


class TestFrameworkIds:
    """:class:`FrameworkIds` mirrors the C# ``FrameworkIds.Convert`` overloads."""

    @pytest.mark.parametrize(
        ("framework_id", "framework_type"),
        [
            ("WPF", FrameworkType.Wpf),
            ("WinForm", FrameworkType.WinForms),
            ("Win32", FrameworkType.Win32),
            ("XAML", FrameworkType.Xaml),
            ("Qt", FrameworkType.Qt),
        ],
    )
    def test_round_trip(self, framework_id: str, framework_type: FrameworkType) -> None:
        """Framework id strings and framework types convert both ways."""
        assert FrameworkIds.convert(framework_id) is framework_type
        assert FrameworkIds.convert(framework_type) == framework_id

    def test_unknown_values(self) -> None:
        """Unrecognised ids map to ``Unknown``; ``Unknown``/``none`` map back like the C# helper."""
        assert FrameworkIds.convert("bogus") is FrameworkType.Unknown
        assert FrameworkIds.convert(FrameworkType.Unknown) is None
        assert FrameworkIds.convert(FrameworkType.none) == ""

    def test_accepts_raw_csharp_framework_type(self) -> None:
        """A raw C# ``FrameworkType`` is accepted too."""
        assert FrameworkIds.convert(CSFrameworkType.Wpf) == "WPF"


class TestBoundaryConversion:
    """Values FlaUI returns arrive as the Python enums."""

    def test_automation_property_value_converts(self) -> None:
        """``AutomationProperty.cast_to_py_wrapper`` converts ported C# enums."""
        assert AutomationProperty.cast_to_py_wrapper(CSDefinitions.OrientationType.Vertical) is OrientationType.Vertical
        assert AutomationProperty.cast_to_py_wrapper(getattr(CSDefinitions.HeadingLevel, "None")) is HeadingLevel.None_

    def test_automation_options_round_trip(self) -> None:
        """``coalesce_events`` / ``connection_recovery_behavior`` read and accept the Python enums."""
        automation = UIA3Automation(raw_automation=CSUIA3Automation())
        try:
            original_coalesce = automation.coalesce_events
            original_recovery = automation.connection_recovery_behavior
            assert isinstance(original_coalesce, CoalesceEventsOptions)
            assert isinstance(original_recovery, ConnectionRecoveryBehaviorOptions)

            automation.coalesce_events = CoalesceEventsOptions.Disabled
            assert automation.coalesce_events is CoalesceEventsOptions.Disabled
            automation.connection_recovery_behavior = ConnectionRecoveryBehaviorOptions.Disabled
            assert automation.connection_recovery_behavior is ConnectionRecoveryBehaviorOptions.Disabled

            automation.coalesce_events = original_coalesce
            automation.connection_recovery_behavior = original_recovery
        finally:
            automation.dispose()


class _FakeElement:
    """Stand-in C# element that records the delegate passed to each ``Register*`` call."""

    def __init__(self) -> None:
        """Start with no recorded handler."""
        self.delegate: Callable[..., None] = lambda *_: None
        self.text_edit_type: Any = None

    def RegisterNotificationEvent(self, _scope: Any, delegate: Callable[..., None]) -> object:  # noqa: N802
        """Record the notification delegate."""
        self.delegate = delegate
        return object()

    def RegisterStructureChangedEvent(self, _scope: Any, delegate: Callable[..., None]) -> object:  # noqa: N802
        """Record the structure-changed delegate."""
        self.delegate = delegate
        return object()

    def RegisterTextEditTextChangedEventHandler(  # noqa: N802
        self, _scope: Any, change_type: Any, delegate: Callable[..., None]
    ) -> object:
        """Record the text-edit delegate and the change type it was registered for."""
        self.text_edit_type = change_type
        self.delegate = delegate
        return object()


@pytest.fixture(name="fake_element")
def get_fake_element(monkeypatch: pytest.MonkeyPatch) -> _FakeElement:
    """Return a fake C# element; the delegate builders hand back the Python bridge function unchanged.

    :param monkeypatch: Pytest monkeypatch fixture.
    :return: The fake element.
    """
    for builder in ("make_notification_delegate", "make_structure_changed_delegate", "make_text_edit_delegate"):
        monkeypatch.setattr(event_handlers, builder, lambda func: func)
    return _FakeElement()


class TestEventCallbackConversion:
    """Event callbacks receive Python enums instead of raw C# values."""

    def test_notification_event(self, fake_element: _FakeElement) -> None:
        """The notification kind and processing are converted."""
        received: List[Any] = []
        element = AutomationElement(raw_element=fake_element)
        element.register_notification_event(TreeScope.Element, lambda *args: received.append(args))
        fake_element.delegate(
            object(),
            CSDefinitions.NotificationKind.ActionCompleted,
            CSDefinitions.NotificationProcessing.MostRecent,
            "done",
            "activity",
        )
        _, kind, processing, display, activity = received[0]
        assert kind is NotificationKind.ActionCompleted
        assert processing is NotificationProcessing.MostRecent
        assert (display, activity) == ("done", "activity")

    def test_structure_changed_event(self, fake_element: _FakeElement) -> None:
        """The structure change type is converted."""
        received: List[Any] = []
        element = AutomationElement(raw_element=fake_element)
        element.register_structure_changed_event(TreeScope.Subtree, lambda *args: received.append(args))
        fake_element.delegate(object(), CSDefinitions.StructureChangeType.ChildAdded, [1, 2])
        assert received[0][1] is StructureChangeType.ChildAdded
        assert received[0][2] == [1, 2]

    def test_text_edit_event(self, fake_element: _FakeElement) -> None:
        """The registration takes a Python enum and the callback receives one."""
        received: List[Any] = []
        element = AutomationElement(raw_element=fake_element)
        element.register_text_edit_text_changed_event_handler(
            TreeScope.Element, TextEditChangeType.AutoCorrect, lambda *args: received.append(args)
        )
        assert fake_element.text_edit_type == CSDefinitions.TextEditChangeType.AutoCorrect
        fake_element.delegate(object(), CSDefinitions.TextEditChangeType.Composition, ["a"])
        assert received[0][1] is TextEditChangeType.Composition
