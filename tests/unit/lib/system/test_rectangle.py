"""Tests for Rectangle utility methods, ported from C# RectangleTests.cs."""

from flaui.lib.system.drawing import Rectangle
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
