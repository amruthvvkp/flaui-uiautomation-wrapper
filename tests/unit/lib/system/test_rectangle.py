"""Tests for Rectangle utility methods, ported from C# RectangleTests.cs."""

from pydantic import ValidationError
import pytest

from flaui.lib.system.drawing import Point, Rectangle, Size
from System.Drawing import Rectangle as CSRectangle  # pyright: ignore


class TestRectangle:
    """Tests for Rectangle utility methods."""

    def test_empty_rectangle(self) -> None:
        """Test empty rectangle detection.

        Ported from RectangleTests.cs::EmptyTest
        """
        rectangle = Rectangle(raw_value=CSRectangle(0, 0, 0, 0))
        rectangle2 = Rectangle(raw_value=CSRectangle(0, 0, 1, 0))
        rectangle3 = Rectangle(raw_value=CSRectangle(0, 0, 0, 1))

        assert rectangle.is_empty is True
        assert rectangle2.is_empty is False
        assert rectangle3.is_empty is False

    def test_rectangle_center(self) -> None:
        """Test calculating rectangle center point.

        Ported from RectangleTests.cs::CenterTest
        """
        rectangle = Rectangle(raw_value=CSRectangle(10, 20, 30, 40))
        center = rectangle.center()

        assert center.x == 25
        assert center.y == 40

    def test_rectangle_cardinal_locations(self) -> None:
        """Test cardinal direction points on rectangle edges.

        Ported from RectangleTests.cs::LocationTest
        """
        rectangle = Rectangle(raw_value=CSRectangle(10, 20, 30, 40))

        # North (top center)
        north = rectangle.north()
        assert north.x == 25
        assert north.y == 20

        # East (right center)
        east = rectangle.east()
        assert east.x == 40
        assert east.y == 40

        # South (bottom center)
        south = rectangle.south()
        assert south.x == 25
        assert south.y == 60

        # West (left center)
        west = rectangle.west()
        assert west.x == 10
        assert west.y == 40

    def test_rectangle_exterior_points(self) -> None:
        """Test immediate exterior points just outside rectangle edges.

        Ported from RectangleTests.cs::ExteriorTest
        """
        rectangle = Rectangle(raw_value=CSRectangle(10, 20, 30, 40))

        # Immediate exterior north (1 pixel above top edge)
        ext_north = rectangle.immediate_exterior_north()
        assert ext_north.x == 25
        assert ext_north.y == 19

        # Immediate exterior east (1 pixel right of right edge)
        ext_east = rectangle.immediate_exterior_east()
        assert ext_east.x == 41
        assert ext_east.y == 40

        # Immediate exterior south (1 pixel below bottom edge)
        ext_south = rectangle.immediate_exterior_south()
        assert ext_south.x == 25
        assert ext_south.y == 61

        # Immediate exterior west (1 pixel left of left edge)
        ext_west = rectangle.immediate_exterior_west()
        assert ext_west.x == 9
        assert ext_west.y == 40

    def test_rectangle_interior_points(self) -> None:
        """Test immediate interior points just inside rectangle edges.

        Ported from RectangleTests.cs::InteriorTest
        """
        rectangle = Rectangle(raw_value=CSRectangle(10, 20, 30, 40))

        # Immediate interior north (1 pixel below top edge)
        int_north = rectangle.immediate_interior_north()
        assert int_north.x == 25
        assert int_north.y == 21

        # Immediate interior east (1 pixel left of right edge)
        int_east = rectangle.immediate_interior_east()
        assert int_east.x == 39
        assert int_east.y == 40

        # Immediate interior south (1 pixel above bottom edge)
        int_south = rectangle.immediate_interior_south()
        assert int_south.x == 25
        assert int_south.y == 59

        # Immediate interior west (1 pixel right of left edge)
        int_west = rectangle.immediate_interior_west()
        assert int_west.x == 11
        assert int_west.y == 40

    def test_construct_from_point_size_tuple(self) -> None:
        """A ``(Point, Size)`` tuple constructs the same rectangle as the LTWH list form."""
        from_tuple = Rectangle(raw_value=(Point(raw_value=(10, 20)), Size(raw_value=(30, 40))))
        from_list = Rectangle(raw_value=[10, 20, 30, 40])
        assert from_tuple == from_list

    def test_construct_rejects_invalid_input(self) -> None:
        """An un-parseable ``raw_value`` raises a validation error."""
        with pytest.raises(ValidationError):
            Rectangle(raw_value=[1, 2, 3])  # wrong length

    def test_edge_properties(self) -> None:
        """The edge/dimension properties expose the underlying C# values."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        assert rectangle.x == 10
        assert rectangle.y == 20
        assert rectangle.left == 10
        assert rectangle.top == 20
        assert rectangle.right == 40
        assert rectangle.bottom == 60
        assert rectangle.width == 30
        assert rectangle.height == 40

    def test_location_and_size_getters(self) -> None:
        """``location`` and ``size`` return wrapped Point/Size values."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        assert (rectangle.location.x, rectangle.location.y) == (10, 20)
        assert (rectangle.size.width, rectangle.size.height) == (30, 40)

    def test_setters(self) -> None:
        """The x/y/width/height/size setters write through to the C# value."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        rectangle.x = 1
        rectangle.y = 2
        rectangle.width = 3
        rectangle.height = 4
        assert (rectangle.x, rectangle.y, rectangle.width, rectangle.height) == (1, 2, 3, 4)
        rectangle.size = Size(raw_value=(7, 8))
        assert (rectangle.width, rectangle.height) == (7, 8)

    def test_contains(self) -> None:
        """``contains`` accepts both a coordinate tuple and a Point."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        assert rectangle.contains((15, 25)) is True
        assert rectangle.contains(Point(raw_value=(15, 25))) is True
        assert rectangle.contains((0, 0)) is False

    def test_equals_and_hash(self) -> None:
        """``equals`` matches identical rectangles; ``get_hash_code`` returns an int."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        assert rectangle.equals(Rectangle(raw_value=[10, 20, 30, 40])) is True
        assert rectangle.equals(Rectangle(raw_value=[0, 0, 1, 1])) is False
        assert isinstance(rectangle.get_hash_code(), int)

    def test_from_ltrb(self) -> None:
        """``from_ltrb`` builds a rectangle from left/top/right/bottom edges."""
        result = Rectangle(raw_value=[0, 0, 1, 1]).from_ltrb([10, 20, 40, 60])
        assert result == Rectangle(raw_value=[10, 20, 30, 40])

    def test_from_ltrb_requires_four_values(self) -> None:
        """``from_ltrb`` rejects inputs that are not exactly four integers."""
        with pytest.raises(ValueError):
            Rectangle(raw_value=[0, 0, 1, 1]).from_ltrb([1, 2, 3])

    def test_inflate(self) -> None:
        """``inflate`` returns a new, enlarged rectangle (does not mutate in place)."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        inflated = rectangle.inflate((2, 3))
        assert (inflated.x, inflated.y, inflated.width, inflated.height) == (8, 17, 34, 46)
        # original untouched
        assert (rectangle.x, rectangle.y, rectangle.width, rectangle.height) == (10, 20, 30, 40)

    def test_intersect_overlap(self) -> None:
        """``interset`` returns the overlapping region of two rectangles."""
        result = Rectangle(raw_value=[10, 20, 30, 40]).interset(Rectangle(raw_value=[15, 25, 30, 40]))
        assert result == Rectangle(raw_value=[15, 25, 25, 35])

    def test_intersect_no_overlap_is_empty(self) -> None:
        """Non-overlapping rectangles intersect to an empty rectangle."""
        result = Rectangle(raw_value=[0, 0, 5, 5]).interset(Rectangle(raw_value=[100, 100, 5, 5]))
        assert result.is_empty is True

    def test_intersects_with(self) -> None:
        """``intersects_with`` reports whether two rectangles overlap."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        assert rectangle.intersects_with(Rectangle(raw_value=[15, 25, 30, 40])) is True
        assert rectangle.intersects_with(Rectangle(raw_value=[100, 100, 5, 5])) is False

    def test_union(self) -> None:
        """``union`` returns the bounding rectangle of two rectangles."""
        result = Rectangle(raw_value=[0, 0, 5, 5]).union(
            (Rectangle(raw_value=[0, 0, 5, 5]), Rectangle(raw_value=[10, 10, 5, 5]))
        )
        assert result == Rectangle(raw_value=[0, 0, 15, 15])

    def test_offset_by_coordinates(self) -> None:
        """``offset(x, y)`` adjusts the rectangle location in place."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        rectangle.offset(5, 5)
        assert (rectangle.x, rectangle.y) == (15, 25)

    def test_offset_by_point(self) -> None:
        """``offset(point=...)`` adjusts the rectangle location in place."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        rectangle.offset(point=Point(raw_value=(5, 5)))
        assert (rectangle.x, rectangle.y) == (15, 25)

    def test_to_string(self) -> None:
        """``to_string`` delegates to the C# representation."""
        assert "X=10" in Rectangle(raw_value=[10, 20, 30, 40]).to_string()

    def test_dunder_eq_and_ne(self) -> None:
        """``==``/``!=`` compare edges and reject non-Rectangle operands."""
        rectangle = Rectangle(raw_value=[10, 20, 30, 40])
        assert rectangle == Rectangle(raw_value=[10, 20, 30, 40])
        assert rectangle != Rectangle(raw_value=[0, 0, 1, 1])
        assert (rectangle == "not a rectangle") is False
        assert (rectangle != "not a rectangle") is True

    def test_make_even(self) -> None:
        """``make_even`` rounds odd width/height down to the nearest even value."""
        result = Rectangle(raw_value=[0, 0, 31, 41]).make_even()
        assert (result.width, result.height) == (30, 40)
        # already-even dimensions are left untouched
        already_even = Rectangle(raw_value=[0, 0, 30, 40]).make_even()
        assert (already_even.width, already_even.height) == (30, 40)
