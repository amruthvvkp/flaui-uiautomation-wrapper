"""Unit tests for the Point wrapper in ``flaui.lib.system.drawing``.

Covers the dual raw-value/Python-coords constructors, property getters/setters, arithmetic and
conversion helpers, equality/inequality, and the ``distance`` helper.
"""

import pytest

from flaui.lib.system.drawing import Point, Size
from System.Drawing import Point as CSPoint, Size as CSSize  # pyright: ignore


class TestPointConstruction:
    """Construction from the several accepted ``raw_value`` shapes."""

    def test_from_int_tuple(self) -> None:
        """A ``(x, y)`` integer tuple maps straight to the coordinates."""
        point = Point(raw_value=(10, 20))
        assert (point.x, point.y) == (10, 20)

    def test_from_float_tuple_rounds(self) -> None:
        """A float tuple is rounded to the nearest integer."""
        point = Point(raw_value=(10.4, 20.6))
        assert (point.x, point.y) == (10, 21)

    def test_from_single_int(self) -> None:
        """A single int constructs a Point at ``(value, value)`` per ``System.Drawing.Point(int)``."""
        point = Point(raw_value=5)
        assert isinstance(point.x, int) and isinstance(point.y, int)

    def test_from_cs_point_is_copied(self) -> None:
        """A C# Point is defensively copied so the wrapper never shares mutable state."""
        cs_point = CSPoint(3, 4)
        point = Point(raw_value=cs_point)
        assert (point.x, point.y) == (3, 4)
        point.x = 99
        assert cs_point.X == 3  # original untouched

    def test_from_size(self) -> None:
        """A Size can seed a Point via its underlying C# value."""
        point = Point(raw_value=Size(raw_value=(7, 8)))
        assert (point.x, point.y) == (7, 8)


class TestPointProperties:
    """Property getters/setters and ``is_empty``."""

    def test_setters(self) -> None:
        """The x/y setters write through to the underlying C# value."""
        point = Point(raw_value=(1, 1))
        point.x = 11
        point.y = 22
        assert (point.x, point.y) == (11, 22)

    def test_is_empty(self) -> None:
        """``is_empty`` is True only at the origin."""
        assert Point(raw_value=(0, 0)).is_empty is True
        assert Point(raw_value=(0, 1)).is_empty is False


class TestPointArithmetic:
    """Arithmetic helpers and operators."""

    def test_add_method(self) -> None:
        """``add`` returns ``point + size`` using the passed operands."""
        result = Point(raw_value=(0, 0)).add(Point(raw_value=(1, 2)), Size(raw_value=(3, 4)))
        assert (result.x, result.y) == (4, 6)

    def test_subtract_method(self) -> None:
        """``subtract`` returns ``point - size`` using the passed operands."""
        result = Point(raw_value=(0, 0)).subtract(Point(raw_value=(5, 5)), Size(raw_value=(1, 1)))
        assert (result.x, result.y) == (4, 4)

    def test_dunder_add_with_size(self) -> None:
        """``Point + Size`` translates the point by the size."""
        result = Point(raw_value=(10, 20)) + Size(raw_value=(3, 4))
        assert (result.x, result.y) == (13, 24)

    def test_dunder_add_rejects_non_size(self) -> None:
        """``Point + <non-Size>`` raises ``TypeError``."""
        with pytest.raises(TypeError):
            _ = Point(raw_value=(1, 1)) + 5  # type: ignore[operator]

    def test_dunder_sub_with_size(self) -> None:
        """``Point - Size`` translates the point by the negative of the size."""
        result = Point(raw_value=(10, 20)) - Size(raw_value=(3, 4))
        assert (result.x, result.y) == (7, 16)

    def test_dunder_sub_rejects_non_size(self) -> None:
        """``Point - <non-Size>`` raises ``TypeError``."""
        with pytest.raises(TypeError):
            _ = Point(raw_value=(1, 1)) - 5  # type: ignore[operator]

    def test_offset_by_coordinates(self) -> None:
        """``offset(x, y)`` mutates the point in place."""
        point = Point(raw_value=(10, 20))
        point.offset(1, 2)
        assert (point.x, point.y) == (11, 22)

    def test_offset_by_point(self) -> None:
        """``offset(point=...)`` mutates the point in place by another point."""
        point = Point(raw_value=(10, 20))
        point.offset(point=Point(raw_value=(2, 3)))
        assert (point.x, point.y) == (12, 23)


class TestPointConversionAndEquality:
    """Conversions, hashing, string and equality."""

    def test_to_size(self) -> None:
        """``to_size`` carries the coordinates over to a Size."""
        size = Point(raw_value=(3, 4)).to_size()
        assert (size.width, size.height) == (3, 4)

    def test_equals_and_get_hash_code(self) -> None:
        """``equals`` matches identical coordinates; ``get_hash_code`` returns an int."""
        point = Point(raw_value=(3, 4))
        assert point.equals(Point(raw_value=(3, 4))) is True
        assert point.equals(Point(raw_value=(5, 6))) is False
        assert isinstance(point.get_hash_code(), int)

    def test_to_string(self) -> None:
        """``to_string`` delegates to the C# representation."""
        assert Point(raw_value=(3, 4)).to_string() == "{X=3,Y=4}"

    def test_dunder_eq_and_ne(self) -> None:
        """``==``/``!=`` compare coordinates and reject non-Point operands."""
        point = Point(raw_value=(3, 4))
        assert point == Point(raw_value=(3, 4))
        assert point != Point(raw_value=(3, 5))
        assert (point == "not a point") is False
        assert (point != "not a point") is True


class TestPointDistance:
    """The ``distance`` helper across its argument shapes."""

    def test_distance_by_coordinates(self) -> None:
        """3-4-5 triangle distance from explicit coordinates."""
        assert Point(raw_value=(0, 0)).distance(other_x=3, other_y=4) == 5.0

    def test_distance_by_point(self) -> None:
        """3-4-5 triangle distance from another Point."""
        assert Point(raw_value=(0, 0)).distance(other_point=Point(raw_value=(3, 4))) == 5.0

    def test_distance_requires_arguments(self) -> None:
        """Calling ``distance`` with no target raises ``ValueError``."""
        with pytest.raises(ValueError):
            Point(raw_value=(0, 0)).distance()


def test_size_to_point_round_trip() -> None:
    """Size.to_point mirrors width/height onto the point coordinates."""
    point = Size(raw_value=(7, 9)).to_point()
    assert (point.x, point.y) == (7, 9)


def test_cs_size_into_point_helpers() -> None:
    """The CS interop types remain importable and constructable alongside the wrappers."""
    assert CSSize(CSPoint(1, 2)).Width == 1
