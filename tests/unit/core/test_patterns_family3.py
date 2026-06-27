"""Unit tests for the Text/Window/Transform/Dock pattern family (``flaui.core.patterns``).

These exercise the wrapper plumbing with lightweight fakes (a ``SimpleNamespace`` stands in for the
native C# objects), so they need no running UI. The Text pattern is additionally covered end-to-end
by the textbox color UI test, which reads a document-range attribute through the new facade.
"""

from types import SimpleNamespace

from flaui.core.automation_elements import AutomationProperty
from flaui.core.definitions import (
    DockPosition,
    SupportedTextSelection,
    TextPatternRangeEndpoint,
    TextUnit,
    WindowVisualState,
    ZoomUnit,
)
from flaui.core.patterns import (
    DockPattern,
    Patterns,
    Text2Pattern,
    TextChildPattern,
    TextEditPattern,
    TextPattern,
    Transform2Pattern,
    TransformPattern,
    WindowPattern,
)
from flaui.core.text_range import TextRange


def _prop(value: object) -> SimpleNamespace:
    """Build a fake native ``AutomationProperty`` whose ``Value`` is ``value``."""
    return SimpleNamespace(Value=value)


class TestTextRange:
    """Validate the TextRange wrapper."""

    def test_clone_wraps_result(self) -> None:
        """``clone`` wraps the native clone in a :class:`TextRange`."""
        inner = SimpleNamespace()
        native = SimpleNamespace(Clone=lambda: inner)
        cloned = TextRange(raw_text_range=native).clone()
        assert isinstance(cloned, TextRange)
        assert cloned.raw_text_range is inner

    def test_get_text_delegates(self) -> None:
        """``get_text`` forwards the max-length argument and returns the text."""
        captured = {}
        native = SimpleNamespace(GetText=lambda n: (captured.update(n=n), "hello")[1])
        assert TextRange(raw_text_range=native).get_text(5) == "hello"
        assert captured["n"] == 5

    def test_enum_conversion_at_boundary(self) -> None:
        """Text-unit / endpoint enums are converted to their C# values at the boundary."""
        captured = {}
        native = SimpleNamespace(
            ExpandToEnclosingUnit=lambda u: captured.setdefault("unit", u),
            Move=lambda u, c: captured.update(move_unit=u, count=c) or c,
        )
        rng = TextRange(raw_text_range=native)
        rng.expand_to_enclosing_unit(TextUnit.Word)
        assert captured["unit"] == TextUnit.Word.value
        assert rng.move(TextUnit.Character, 3) == 3
        assert captured["move_unit"] == TextUnit.Character.value

    def test_find_text_none_returns_none(self) -> None:
        """``find_text`` returns ``None`` when the native call finds nothing."""
        native = SimpleNamespace(FindText=lambda t, b, i: None)
        assert TextRange(raw_text_range=native).find_text("x", False, True) is None

    def test_compare_endpoints_passes_raw(self) -> None:
        """``compare_endpoints`` unwraps the target range and converts the endpoints."""
        captured = {}
        target_native = SimpleNamespace()
        native = SimpleNamespace(
            CompareEndpoints=lambda s, t, e: captured.update(s=s, t=t, e=e) or 0,
        )
        target = TextRange(raw_text_range=target_native)
        result = TextRange(raw_text_range=native).compare_endpoints(
            TextPatternRangeEndpoint.Start, target, TextPatternRangeEndpoint.End
        )
        assert result == 0
        assert captured["s"] == TextPatternRangeEndpoint.Start.value
        assert captured["t"] is target_native
        assert captured["e"] == TextPatternRangeEndpoint.End.value


class TestTextPatterns:
    """Validate the Text, Text2, TextEdit, and TextChild pattern wrappers."""

    def test_text_pattern_surface(self) -> None:
        """TextPattern exposes the document range, selection mode, and range collections."""
        doc = SimpleNamespace()
        native = SimpleNamespace(
            DocumentRange=doc,
            SupportedTextSelection=SupportedTextSelection.Single.value,
            GetSelection=lambda: [SimpleNamespace(), SimpleNamespace()],
        )
        pattern = TextPattern(raw_pattern=native)
        assert isinstance(pattern.document_range, TextRange)
        assert pattern.document_range.raw_text_range is doc
        assert pattern.supported_text_selection == SupportedTextSelection.Single
        ranges = pattern.get_selection()
        assert len(ranges) == 2
        assert all(isinstance(r, TextRange) for r in ranges)

    def test_text2_extends_text_and_returns_caret_tuple(self) -> None:
        """Text2 inherits Text and returns the caret range plus its active flag."""
        caret = SimpleNamespace()
        native = SimpleNamespace(GetCaretRange=lambda: (caret, True))
        pattern = Text2Pattern(raw_pattern=native)
        assert isinstance(pattern, TextPattern)
        caret_range, is_active = pattern.get_caret_range()
        assert isinstance(caret_range, TextRange)
        assert caret_range.raw_text_range is caret
        assert is_active is True

    def test_text_edit_handles_missing_composition(self) -> None:
        """TextEdit returns ``None`` when there is no active composition."""
        native = SimpleNamespace(GetActiveComposition=lambda: None, GetConversionTarget=lambda: SimpleNamespace())
        pattern = TextEditPattern(raw_pattern=native)
        assert isinstance(pattern, TextPattern)
        assert pattern.get_active_composition() is None
        assert isinstance(pattern.get_conversion_target(), TextRange)

    def test_text_child_surface(self) -> None:
        """TextChild exposes its container element and enclosing text range."""
        native = SimpleNamespace(TextContainer=SimpleNamespace(), TextRange=SimpleNamespace())
        pattern = TextChildPattern(raw_pattern=native)
        assert pattern.text_container is not None
        assert isinstance(pattern.text_range, TextRange)


class TestWindowPattern:
    """Validate the Window pattern wrapper."""

    def test_properties_and_methods(self) -> None:
        """Window properties surface as AutomationProperty; methods convert/forward."""
        captured = {}
        native = SimpleNamespace(
            CanMaximize=_prop(True),
            CanMinimize=_prop(False),
            IsModal=_prop(False),
            IsTopmost=_prop(True),
            WindowInteractionState=_prop("Running"),
            WindowVisualState=_prop("Normal"),
            Close=lambda: captured.setdefault("closed", True),
            SetWindowVisualState=lambda s: captured.setdefault("state", s),
            WaitForInputIdle=lambda ms: (captured.update(ms=ms), True)[1],
        )
        pattern = WindowPattern(raw_pattern=native)
        assert isinstance(pattern.can_maximize, AutomationProperty)
        assert pattern.can_maximize.value is True
        assert pattern.is_topmost.value is True
        pattern.close()
        pattern.set_window_visual_state(WindowVisualState.Maximized)
        assert pattern.wait_for_input_idle(100) is True
        assert captured["closed"] is True
        assert captured["state"] == WindowVisualState.Maximized.value
        assert captured["ms"] == 100


class TestTransformPatterns:
    """Validate the Transform and Transform2 pattern wrappers."""

    def test_transform_methods(self) -> None:
        """Transform forwards move/resize/rotate to the native pattern."""
        captured = {}
        native = SimpleNamespace(
            CanMove=_prop(True),
            CanResize=_prop(True),
            CanRotate=_prop(False),
            Move=lambda x, y: captured.update(move=(x, y)),
            Resize=lambda w, h: captured.update(resize=(w, h)),
            Rotate=lambda d: captured.update(rotate=d),
        )
        pattern = TransformPattern(raw_pattern=native)
        assert pattern.can_move.value is True
        pattern.move(1.0, 2.0)
        pattern.resize(30.0, 40.0)
        pattern.rotate(90.0)
        assert captured == {"move": (1.0, 2.0), "resize": (30.0, 40.0), "rotate": 90.0}

    def test_transform2_extends_transform_and_converts_zoom_unit(self) -> None:
        """Transform2 inherits Transform and converts the ZoomUnit at the boundary."""
        captured = {}
        native = SimpleNamespace(
            CanMove=_prop(True),
            CanResize=_prop(True),
            CanRotate=_prop(True),
            CanZoom=_prop(True),
            ZoomLevel=_prop(1.0),
            ZoomMaximum=_prop(4.0),
            ZoomMinimum=_prop(0.5),
            Zoom=lambda z: captured.update(zoom=z),
            ZoomByUnit=lambda u: captured.update(unit=u),
        )
        pattern = Transform2Pattern(raw_pattern=native)
        assert isinstance(pattern, TransformPattern)
        assert pattern.can_zoom.value is True
        assert pattern.zoom_maximum.value == 4.0
        pattern.zoom(2.0)
        pattern.zoom_by_unit(ZoomUnit.SmallIncrement)
        assert captured["zoom"] == 2.0
        assert captured["unit"] == ZoomUnit.SmallIncrement.value


class TestDockPattern:
    """Validate the Dock pattern wrapper."""

    def test_dock_position_and_set(self) -> None:
        """Dock exposes the position property and converts the enum on set."""
        captured = {}
        native = SimpleNamespace(
            DockPosition=_prop("Top"),
            SetDockPosition=lambda p: captured.setdefault("pos", p),
        )
        pattern = DockPattern(raw_pattern=native)
        assert isinstance(pattern.dock_position, AutomationProperty)
        pattern.set_dock_position(DockPosition.Left)
        assert captured["pos"] == DockPosition.Left.value


class TestFacadeAccessors:
    """Validate the new accessors on the ``Patterns`` facade."""

    def test_facade_wires_family3_accessors(self) -> None:
        """Each new facade accessor returns an accessor wired to the right pattern type."""
        raw_patterns = SimpleNamespace(
            Text=SimpleNamespace(IsSupported=True),
            Text2=SimpleNamespace(IsSupported=True),
            TextEdit=SimpleNamespace(IsSupported=False),
            TextChild=SimpleNamespace(IsSupported=False),
            Window=SimpleNamespace(IsSupported=True),
            Transform=SimpleNamespace(IsSupported=True),
            Transform2=SimpleNamespace(IsSupported=False),
            Dock=SimpleNamespace(IsSupported=False),
        )
        facade = Patterns(raw_patterns=raw_patterns)
        assert facade.text.pattern_type is TextPattern
        assert facade.text2.pattern_type is Text2Pattern
        assert facade.text_edit.pattern_type is TextEditPattern
        assert facade.text_child.pattern_type is TextChildPattern
        assert facade.window.pattern_type is WindowPattern
        assert facade.transform.pattern_type is TransformPattern
        assert facade.transform2.pattern_type is Transform2Pattern
        assert facade.dock.pattern_type is DockPattern
        assert facade.text.is_supported is True
        assert facade.dock.is_supported is False
