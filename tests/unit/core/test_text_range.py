"""Unit tests for :mod:`flaui.core.text_range` (GH-88).

``TextRange`` is a thin 1:1 wrapper over the C# ``ITextRange``; a :class:`unittest.mock.MagicMock`
stub gives deterministic coverage of every delegating method without a running application. Methods
that wrap results into :class:`Rectangle` are fed real ``System.Drawing.Rectangle`` values because
that wrapper validates its input type.
"""

from unittest.mock import MagicMock

from System.Drawing import Rectangle as CSRectangle  # type: ignore
import pytest

from flaui.core.automation_elements import AutomationElement
from flaui.core.definitions import TextPatternRangeEndpoint, TextUnit
from flaui.core.text_range import TextRange
from flaui.lib.exceptions import ElementNotFound
from flaui.lib.system.drawing import Rectangle


def _text_range(raw: MagicMock) -> TextRange:
    """Wrap a stub C# text range in a :class:`TextRange`.

    :param raw: The stub navigator/range mock.
    :return: A :class:`TextRange` around the stub.
    """
    return TextRange(raw_text_range=raw)


class TestValidation:
    """Validate the constructor guard."""

    def test_none_raises_element_not_found(self) -> None:
        """Constructing with a ``None`` native range raises :class:`ElementNotFound`."""
        with pytest.raises(ElementNotFound):
            TextRange(raw_text_range=None)


class TestVoidDelegation:
    """Validate the side-effecting methods forward to the native range."""

    def test_add_to_selection(self) -> None:
        """``add_to_selection`` calls the native method."""
        raw = MagicMock()
        _text_range(raw).add_to_selection()
        raw.AddToSelection.assert_called_once_with()

    def test_remove_from_selection(self) -> None:
        """``remove_from_selection`` calls the native method."""
        raw = MagicMock()
        _text_range(raw).remove_from_selection()
        raw.RemoveFromSelection.assert_called_once_with()

    def test_select(self) -> None:
        """``select`` calls the native method."""
        raw = MagicMock()
        _text_range(raw).select()
        raw.Select.assert_called_once_with()

    def test_scroll_into_view(self) -> None:
        """``scroll_into_view`` forwards the alignment flag."""
        raw = MagicMock()
        _text_range(raw).scroll_into_view(True)
        raw.ScrollIntoView.assert_called_once_with(True)

    def test_expand_to_enclosing_unit(self) -> None:
        """``expand_to_enclosing_unit`` forwards the text-unit value."""
        raw = MagicMock()
        _text_range(raw).expand_to_enclosing_unit(TextUnit.Word)
        raw.ExpandToEnclosingUnit.assert_called_once_with(TextUnit.Word.value)

    def test_move_endpoint_by_range(self) -> None:
        """``move_endpoint_by_range`` forwards endpoint values and the target's native range."""
        raw = MagicMock()
        target_raw = MagicMock()
        target = _text_range(target_raw)
        _text_range(raw).move_endpoint_by_range(
            TextPatternRangeEndpoint.Start, target, TextPatternRangeEndpoint.End
        )
        raw.MoveEndpointByRange.assert_called_once_with(
            TextPatternRangeEndpoint.Start.value, target_raw, TextPatternRangeEndpoint.End.value
        )


class TestValueDelegation:
    """Validate the methods that return scalar values or booleans."""

    def test_compare(self) -> None:
        """``compare`` forwards the other range and returns the native boolean."""
        raw = MagicMock()
        raw.Compare.return_value = True
        other_raw = MagicMock()
        assert _text_range(raw).compare(_text_range(other_raw)) is True
        raw.Compare.assert_called_once_with(other_raw)

    def test_compare_endpoints(self) -> None:
        """``compare_endpoints`` forwards endpoint values and returns the native int."""
        raw = MagicMock()
        raw.CompareEndpoints.return_value = -1
        other_raw = MagicMock()
        result = _text_range(raw).compare_endpoints(
            TextPatternRangeEndpoint.Start, _text_range(other_raw), TextPatternRangeEndpoint.End
        )
        assert result == -1
        raw.CompareEndpoints.assert_called_once_with(
            TextPatternRangeEndpoint.Start.value, other_raw, TextPatternRangeEndpoint.End.value
        )

    def test_get_attribute_value(self) -> None:
        """``get_attribute_value`` forwards the attribute and returns the native value."""
        raw = MagicMock()
        raw.GetAttributeValue.return_value = "attr"
        attribute = object()
        assert _text_range(raw).get_attribute_value(attribute) == "attr"
        raw.GetAttributeValue.assert_called_once_with(attribute)

    def test_get_text(self) -> None:
        """``get_text`` forwards the max length and returns the native text."""
        raw = MagicMock()
        raw.GetText.return_value = "hello"
        assert _text_range(raw).get_text() == "hello"
        raw.GetText.assert_called_once_with(-1)

    def test_move(self) -> None:
        """``move`` forwards the unit value/count and returns the native move count."""
        raw = MagicMock()
        raw.Move.return_value = 3
        assert _text_range(raw).move(TextUnit.Character, 3) == 3
        raw.Move.assert_called_once_with(TextUnit.Character.value, 3)

    def test_move_endpoint_by_unit(self) -> None:
        """``move_endpoint_by_unit`` forwards endpoint/unit values and the count."""
        raw = MagicMock()
        raw.MoveEndpointByUnit.return_value = 2
        result = _text_range(raw).move_endpoint_by_unit(TextPatternRangeEndpoint.End, TextUnit.Word, 2)
        assert result == 2
        raw.MoveEndpointByUnit.assert_called_once_with(
            TextPatternRangeEndpoint.End.value, TextUnit.Word.value, 2
        )


class TestWrappingDelegation:
    """Validate the methods that wrap native results into Python types."""

    def test_clone(self) -> None:
        """``clone`` wraps the native ``Clone()`` result in a new :class:`TextRange`."""
        raw = MagicMock()
        clone = _text_range(raw).clone()
        assert isinstance(clone, TextRange)
        assert clone.raw_text_range is raw.Clone.return_value

    def test_find_attribute_found_and_missing(self) -> None:
        """``find_attribute`` wraps a hit and returns ``None`` on a miss."""
        raw = MagicMock()
        raw.FindAttribute.return_value = MagicMock()
        found = _text_range(raw).find_attribute(object(), "v", False)
        assert isinstance(found, TextRange)

        raw.FindAttribute.return_value = None
        assert _text_range(raw).find_attribute(object(), "v", True) is None

    def test_find_text_found_and_missing(self) -> None:
        """``find_text`` wraps a hit and returns ``None`` on a miss."""
        raw = MagicMock()
        raw.FindText.return_value = MagicMock()
        assert isinstance(_text_range(raw).find_text("x", False, True), TextRange)

        raw.FindText.return_value = None
        assert _text_range(raw).find_text("x", True, False) is None

    def test_get_bounding_rectangles(self) -> None:
        """``get_bounding_rectangles`` wraps each native rectangle in a :class:`Rectangle`."""
        raw = MagicMock()
        raw.GetBoundingRectangles.return_value = [CSRectangle(0, 0, 10, 20), CSRectangle(1, 2, 3, 4)]
        rectangles = _text_range(raw).get_bounding_rectangles()
        assert len(rectangles) == 2
        assert all(isinstance(rect, Rectangle) for rect in rectangles)

    def test_get_children(self) -> None:
        """``get_children`` wraps each native child in an :class:`AutomationElement`."""
        raw = MagicMock()
        raw.GetChildren.return_value = [MagicMock(), MagicMock()]
        children = _text_range(raw).get_children()
        assert len(children) == 2
        assert all(isinstance(child, AutomationElement) for child in children)

    def test_get_enclosing_element(self) -> None:
        """``get_enclosing_element`` wraps the native element in an :class:`AutomationElement`."""
        raw = MagicMock()
        element = _text_range(raw).get_enclosing_element()
        assert isinstance(element, AutomationElement)
        assert element.raw_element is raw.GetEnclosingElement.return_value
