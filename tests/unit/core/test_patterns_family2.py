"""Unit tests for the Table/Scroll/Selection pattern family (``flaui.core.patterns``).

These exercise the wrapper plumbing with lightweight fakes (a ``SimpleNamespace`` stands in for the
native C# pattern objects), so they need no running UI. End-to-end coverage of the facade against
real applications is provided by the family #1 UI tests; the C# library itself lacks UI tests for
most of these patterns (``GridItemPatternTests`` is ``[Ignore]``-d, no ``SelectionPatternTests``).
"""

from types import SimpleNamespace

from flaui.core.automation_elements import AutomationProperty
from flaui.core.definitions import ScrollAmount
from flaui.core.patterns import (
    GridItemPattern,
    Patterns,
    ScrollItemPattern,
    ScrollPattern,
    Selection2Pattern,
    SelectionItemPattern,
    SelectionPattern,
    TableItemPattern,
    TablePattern,
)


def _prop(value: object) -> SimpleNamespace:
    """Build a fake native ``AutomationProperty`` whose ``Value`` is ``value``."""
    return SimpleNamespace(Value=value)


class TestGridItemPattern:
    """Validate the GridItem pattern wrapper."""

    def test_properties_wrap_automation_property(self) -> None:
        """Each GridItem property surfaces as an :class:`AutomationProperty`."""
        native = SimpleNamespace(
            Column=_prop(1),
            ColumnSpan=_prop(2),
            Row=_prop(3),
            RowSpan=_prop(1),
            ContainingGrid=_prop("grid"),
        )
        pattern = GridItemPattern(raw_pattern=native)
        assert isinstance(pattern.column, AutomationProperty)
        assert pattern.column.value == 1
        assert pattern.column_span.value == 2
        assert pattern.row.value == 3
        assert pattern.row_span.value == 1
        assert pattern.containing_grid.value == "grid"


class TestTablePatterns:
    """Validate the Table and TableItem pattern wrappers."""

    def test_table_properties(self) -> None:
        """Table properties surface header collections and major-order."""
        native = SimpleNamespace(
            ColumnHeaders=_prop(["c"]),
            RowHeaders=_prop(["r"]),
            RowOrColumnMajor=_prop("RowMajor"),
        )
        pattern = TablePattern(raw_pattern=native)
        assert pattern.column_headers.value == ["c"]
        assert pattern.row_headers.value == ["r"]
        assert pattern.row_or_column_major.value == "RowMajor"

    def test_table_item_properties(self) -> None:
        """TableItem properties surface header-item collections."""
        native = SimpleNamespace(ColumnHeaderItems=_prop(["ch"]), RowHeaderItems=_prop(["rh"]))
        pattern = TableItemPattern(raw_pattern=native)
        assert pattern.column_header_items.value == ["ch"]
        assert pattern.row_header_items.value == ["rh"]


class TestScrollPatterns:
    """Validate the Scroll and ScrollItem pattern wrappers."""

    def test_scroll_properties(self) -> None:
        """Scroll properties surface scrollability, percent, and view size."""
        native = SimpleNamespace(
            HorizontallyScrollable=_prop(True),
            VerticallyScrollable=_prop(False),
            HorizontalScrollPercent=_prop(10.0),
            VerticalScrollPercent=_prop(0.0),
            HorizontalViewSize=_prop(50.0),
            VerticalViewSize=_prop(100.0),
        )
        pattern = ScrollPattern(raw_pattern=native)
        assert pattern.horizontally_scrollable.value is True
        assert pattern.vertically_scrollable.value is False
        assert pattern.horizontal_scroll_percent.value == 10.0
        assert pattern.vertical_view_size.value == 100.0

    def test_scroll_converts_enum_at_boundary(self) -> None:
        """``scroll`` forwards the C# enum values of the given ``ScrollAmount`` members."""
        captured = {}
        native = SimpleNamespace(Scroll=lambda h, v: captured.update(h=h, v=v))
        ScrollPattern(raw_pattern=native).scroll(ScrollAmount.SmallIncrement, ScrollAmount.NoAmount)
        assert captured["h"] == ScrollAmount.SmallIncrement.value
        assert captured["v"] == ScrollAmount.NoAmount.value

    def test_set_scroll_percent_delegates(self) -> None:
        """``set_scroll_percent`` forwards both percentages to the native pattern."""
        captured = {}
        native = SimpleNamespace(SetScrollPercent=lambda h, v: captured.update(h=h, v=v))
        ScrollPattern(raw_pattern=native).set_scroll_percent(25.0, -1)
        assert captured == {"h": 25.0, "v": -1}

    def test_scroll_into_view_delegates(self) -> None:
        """``scroll_into_view`` forwards to the native ``ScrollIntoView``."""
        called = {}
        native = SimpleNamespace(ScrollIntoView=lambda: called.setdefault("hit", True))
        ScrollItemPattern(raw_pattern=native).scroll_into_view()
        assert called["hit"] is True


class TestSelectionPatterns:
    """Validate the Selection, Selection2, and SelectionItem pattern wrappers."""

    def test_selection_properties(self) -> None:
        """Selection properties surface multi-select, requirement, and the selection."""
        native = SimpleNamespace(
            CanSelectMultiple=_prop(True),
            IsSelectionRequired=_prop(False),
            Selection=_prop(["item"]),
        )
        pattern = SelectionPattern(raw_pattern=native)
        assert pattern.can_select_multiple.value is True
        assert pattern.is_selection_required.value is False
        assert pattern.selection.value == ["item"]

    def test_selection2_extends_selection(self) -> None:
        """Selection2 inherits the Selection surface and adds current/first/last/count."""
        native = SimpleNamespace(
            CanSelectMultiple=_prop(True),
            IsSelectionRequired=_prop(False),
            Selection=_prop([]),
            CurrentSelectedItem=_prop("cur"),
            FirstSelectedItem=_prop("first"),
            LastSelectedItem=_prop("last"),
            ItemCount=_prop(3),
        )
        pattern = Selection2Pattern(raw_pattern=native)
        assert isinstance(pattern, SelectionPattern)
        assert pattern.can_select_multiple.value is True
        assert pattern.current_selected_item.value == "cur"
        assert pattern.first_selected_item.value == "first"
        assert pattern.last_selected_item.value == "last"
        assert pattern.item_count.value == 3

    def test_selection_item_properties_and_methods(self) -> None:
        """SelectionItem surfaces state/container and delegates its action methods."""
        calls = []
        native = SimpleNamespace(
            IsSelected=_prop(True),
            SelectionContainer=_prop("container"),
            AddToSelection=lambda: calls.append("add"),
            RemoveFromSelection=lambda: calls.append("remove"),
            Select=lambda: calls.append("select"),
        )
        pattern = SelectionItemPattern(raw_pattern=native)
        assert pattern.is_selected.value is True
        assert pattern.selection_container.value == "container"
        pattern.add_to_selection()
        pattern.remove_from_selection()
        pattern.select()
        assert calls == ["add", "remove", "select"]


class TestFacadeAccessors:
    """Validate the new accessors on the ``Patterns`` facade."""

    def test_facade_wires_new_accessors(self) -> None:
        """Each new facade accessor returns an accessor wired to the right pattern type."""
        raw_patterns = SimpleNamespace(
            GridItem=SimpleNamespace(IsSupported=True),
            Table=SimpleNamespace(IsSupported=True),
            TableItem=SimpleNamespace(IsSupported=False),
            Scroll=SimpleNamespace(IsSupported=True),
            ScrollItem=SimpleNamespace(IsSupported=False),
            Selection=SimpleNamespace(IsSupported=True),
            Selection2=SimpleNamespace(IsSupported=True),
            SelectionItem=SimpleNamespace(IsSupported=False),
        )
        facade = Patterns(raw_patterns=raw_patterns)
        assert facade.grid_item.pattern_type is GridItemPattern
        assert facade.table.pattern_type is TablePattern
        assert facade.table_item.pattern_type is TableItemPattern
        assert facade.scroll.pattern_type is ScrollPattern
        assert facade.scroll_item.pattern_type is ScrollItemPattern
        assert facade.selection.pattern_type is SelectionPattern
        assert facade.selection2.pattern_type is Selection2Pattern
        assert facade.selection_item.pattern_type is SelectionItemPattern
        # is_supported reads through to the native accessor
        assert facade.grid_item.is_supported is True
        assert facade.table_item.is_supported is False
