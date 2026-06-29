"""Unit tests for the remaining pattern family (``flaui.core.patterns``).

Covers Annotation, Styles, MultipleView, ItemContainer, VirtualizedItem, ObjectModel,
Spreadsheet/SpreadsheetItem, LegacyIAccessible, Drag/DropTarget, and SynchronizedInput. These
exercise the wrapper plumbing with lightweight fakes, so they need no running UI.
"""

from types import SimpleNamespace

from flaui.core.automation_elements import AutomationElement, AutomationProperty
from flaui.core.definitions import SynchronizedInputType
from flaui.core.patterns import (
    AnnotationPattern,
    DragPattern,
    DropTargetPattern,
    ItemContainerPattern,
    LegacyIAccessiblePattern,
    MultipleViewPattern,
    ObjectModelPattern,
    Patterns,
    SpreadsheetItemPattern,
    SpreadsheetPattern,
    StylesPattern,
    SynchronizedInputPattern,
    VirtualizedItemPattern,
)


def _prop(value: object) -> SimpleNamespace:
    """Build a fake native ``AutomationProperty`` whose ``Value`` is ``value``."""
    return SimpleNamespace(Value=value)


class TestPropertyOnlyPatterns:
    """Validate the patterns that expose only ``AutomationProperty`` members."""

    def test_annotation_properties(self) -> None:
        """Annotation exposes type, name, author, date, and target."""
        native = SimpleNamespace(
            AnnotationType=_prop(1),
            AnnotationTypeName=_prop("Comment"),
            Author=_prop("alice"),
            DateTime=_prop("2026-01-01"),
            Target=_prop("element"),
        )
        pattern = AnnotationPattern(raw_pattern=native)
        assert isinstance(pattern.annotation_type, AutomationProperty)
        assert pattern.annotation_type_name.value == "Comment"
        assert pattern.author.value == "alice"
        assert pattern.date_time.value == "2026-01-01"
        assert pattern.target.value == "element"

    def test_styles_properties(self) -> None:
        """Styles exposes color, shape, and style identifiers."""
        native = SimpleNamespace(
            ExtendedProperties=_prop("ext"),
            FillColor=_prop(255),
            FillPatternColor=_prop(128),
            FillPatternStyle=_prop("solid"),
            Shape=_prop("rect"),
            Style=_prop(7),
            StyleName=_prop("Heading"),
        )
        pattern = StylesPattern(raw_pattern=native)
        assert pattern.extended_properties.value == "ext"
        assert pattern.fill_color.value == 255
        assert pattern.fill_pattern_color.value == 128
        assert pattern.fill_pattern_style.value == "solid"
        assert pattern.shape.value == "rect"
        assert pattern.style.value == 7
        assert pattern.style_name.value == "Heading"

    def test_spreadsheet_item_properties(self) -> None:
        """SpreadsheetItem exposes formula and annotation collections."""
        native = SimpleNamespace(
            Formula=_prop("=A1+B1"),
            AnnotationObjects=_prop(["a"]),
            AnnotationTypes=_prop([1]),
        )
        pattern = SpreadsheetItemPattern(raw_pattern=native)
        assert pattern.formula.value == "=A1+B1"
        assert pattern.annotation_objects.value == ["a"]
        assert pattern.annotation_types.value == [1]

    def test_drag_and_drop_target_properties(self) -> None:
        """Drag and DropTarget expose their effect and grabbed-item properties."""
        drag = DragPattern(
            raw_pattern=SimpleNamespace(
                DropEffect=_prop("move"),
                DropEffects=_prop(["move", "copy"]),
                IsGrabbed=_prop(True),
                GrabbedItems=_prop([]),
            )
        )
        assert drag.drop_effect.value == "move"
        assert drag.drop_effects.value == ["move", "copy"]
        assert drag.is_grabbed.value is True
        assert drag.grabbed_items.value == []

        drop = DropTargetPattern(
            raw_pattern=SimpleNamespace(DropTargetEffect=_prop("link"), DropTargetEffects=_prop(["link"]))
        )
        assert drop.drop_target_effect.value == "link"
        assert drop.drop_target_effects.value == ["link"]

    def test_legacy_i_accessible_properties_and_methods(self) -> None:
        """LegacyIAccessible exposes MSAA properties and delegates its action methods."""
        calls = []
        native = SimpleNamespace(
            ChildId=_prop(0),
            DefaultAction=_prop("press"),
            Description=_prop("desc"),
            Help=_prop("help"),
            KeyboardShortcut=_prop("Ctrl+S"),
            Name=_prop("Save"),
            Role=_prop(43),
            State=_prop(0),
            Selection=_prop([]),
            Value=_prop("val"),
            DoDefaultAction=lambda: calls.append("default"),
            Select=lambda flags: calls.append(("select", flags)),
            SetValue=lambda v: calls.append(("set", v)),
        )
        pattern = LegacyIAccessiblePattern(raw_pattern=native)
        assert pattern.child_id.value == 0
        assert pattern.default_action.value == "press"
        assert pattern.description.value == "desc"
        assert pattern.help.value == "help"
        assert pattern.keyboard_shortcut.value == "Ctrl+S"
        assert pattern.name.value == "Save"
        assert pattern.role.value == 43
        assert pattern.state.value == 0
        assert pattern.selection.value == []
        assert pattern.value.value == "val"
        pattern.do_default_action()
        pattern.select(3)
        pattern.set_value("new")
        assert calls == ["default", ("select", 3), ("set", "new")]


class TestMethodPatterns:
    """Validate the patterns whose surface is mostly methods."""

    def test_multiple_view(self) -> None:
        """MultipleView exposes views and delegates name/set operations."""
        captured = {}
        native = SimpleNamespace(
            CurrentView=_prop(0),
            SupportedViews=_prop([0, 1]),
            GetViewName=lambda v: (captured.update(name_arg=v), "Details")[1],
            SetCurrentView=lambda v: captured.update(set_arg=v),
        )
        pattern = MultipleViewPattern(raw_pattern=native)
        assert pattern.current_view.value == 0
        assert pattern.supported_views.value == [0, 1]
        assert pattern.get_view_name(1) == "Details"
        assert captured["name_arg"] == 1
        pattern.set_current_view(1)
        assert captured["set_arg"] == 1

    def test_item_container_find(self) -> None:
        """ItemContainer unwraps ``start_after`` and wraps the result."""
        captured = {}
        found = SimpleNamespace()
        start = AutomationElement(raw_element=SimpleNamespace())
        native = SimpleNamespace(
            FindItemByProperty=lambda s, p, v: (captured.update(s=s, p=p, v=v), found)[1],
        )
        pattern = ItemContainerPattern(raw_pattern=native)
        result = pattern.find_item_by_property(start, "prop", "value")
        assert isinstance(result, AutomationElement)
        assert result.raw_element is found
        assert captured["s"] is start.raw_element

        # None start_after is forwarded as None.
        none_native = SimpleNamespace(FindItemByProperty=lambda s, p, v: None)
        assert ItemContainerPattern(raw_pattern=none_native).find_item_by_property(None, None, None) is None

    def test_virtualized_item_realize(self) -> None:
        """VirtualizedItem delegates ``realize`` to the native pattern."""
        called = {}
        pattern = VirtualizedItemPattern(raw_pattern=SimpleNamespace(Realize=lambda: called.setdefault("hit", True)))
        pattern.realize()
        assert called["hit"] is True

    def test_object_model(self) -> None:
        """ObjectModel returns the native underlying object model."""
        model = SimpleNamespace()
        pattern = ObjectModelPattern(raw_pattern=SimpleNamespace(GetUnderlyingObjectModel=lambda: model))
        assert pattern.get_underlying_object_model() is model

    def test_spreadsheet_get_item_by_name(self) -> None:
        """Spreadsheet wraps the named cell as an AutomationElement."""
        cell = SimpleNamespace()
        pattern = SpreadsheetPattern(raw_pattern=SimpleNamespace(GetItemByName=lambda n: cell))
        result = pattern.get_item_by_name("A1")
        assert isinstance(result, AutomationElement)
        assert result.raw_element is cell

    def test_synchronized_input_converts_enum(self) -> None:
        """SynchronizedInput converts the input-type enum and delegates cancel."""
        captured = {}
        native = SimpleNamespace(
            Cancel=lambda: captured.setdefault("cancelled", True),
            StartListening=lambda t: captured.setdefault("type", t),
        )
        pattern = SynchronizedInputPattern(raw_pattern=native)
        pattern.start_listening(SynchronizedInputType.KeyDown)
        pattern.cancel()
        assert captured["type"] == SynchronizedInputType.KeyDown.value
        assert captured["cancelled"] is True


class TestFacadeAccessors:
    """Validate the remaining accessors on the ``Patterns`` facade."""

    def test_facade_wires_remaining_accessors(self) -> None:
        """Each remaining facade accessor returns an accessor wired to the right pattern type."""
        raw_patterns = SimpleNamespace(
            Annotation=SimpleNamespace(IsSupported=True),
            Styles=SimpleNamespace(IsSupported=True),
            MultipleView=SimpleNamespace(IsSupported=False),
            ItemContainer=SimpleNamespace(IsSupported=True),
            VirtualizedItem=SimpleNamespace(IsSupported=False),
            ObjectModel=SimpleNamespace(IsSupported=False),
            Spreadsheet=SimpleNamespace(IsSupported=False),
            SpreadsheetItem=SimpleNamespace(IsSupported=False),
            LegacyIAccessible=SimpleNamespace(IsSupported=True),
            Drag=SimpleNamespace(IsSupported=False),
            DropTarget=SimpleNamespace(IsSupported=False),
            SynchronizedInput=SimpleNamespace(IsSupported=False),
        )
        facade = Patterns(raw_patterns=raw_patterns)
        assert facade.annotation.pattern_type is AnnotationPattern
        assert facade.styles.pattern_type is StylesPattern
        assert facade.multiple_view.pattern_type is MultipleViewPattern
        assert facade.item_container.pattern_type is ItemContainerPattern
        assert facade.virtualized_item.pattern_type is VirtualizedItemPattern
        assert facade.object_model.pattern_type is ObjectModelPattern
        assert facade.spreadsheet.pattern_type is SpreadsheetPattern
        assert facade.spreadsheet_item.pattern_type is SpreadsheetItemPattern
        assert facade.legacy_i_accessible.pattern_type is LegacyIAccessiblePattern
        assert facade.drag.pattern_type is DragPattern
        assert facade.drop_target.pattern_type is DropTargetPattern
        assert facade.synchronized_input.pattern_type is SynchronizedInputPattern
        assert facade.annotation.is_supported is True
        assert facade.drag.is_supported is False
