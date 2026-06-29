"""Unit tests for the Size wrapper in ``flaui.lib.system.drawing``.

Covers the constructors, property getters/setters, arithmetic and conversion helpers, and
equality/inequality.
"""

import pytest

from flaui.lib.system.drawing import Point, Size
from System.Drawing import Size as CSSize  # pyright: ignore


class TestSizeConstruction:
    """Construction from the several accepted ``raw_value`` shapes."""

    def test_from_int_tuple(self) -> None:
        """A ``(width, height)`` integer tuple maps straight to the dimensions."""
        size = Size(raw_value=(3, 4))
        assert (size.width, size.height) == (3, 4)

    def test_from_float_tuple_rounds(self) -> None:
        """A float tuple is rounded to the nearest integer."""
        size = Size(raw_value=(3.4, 4.6))
        assert (size.width, size.height) == (3, 5)

    def test_from_cs_size(self) -> None:
        """A C# Size is accepted as-is."""
        size = Size(raw_value=CSSize(5, 6))
        assert (size.width, size.height) == (5, 6)

    def test_from_point(self) -> None:
        """A Point can seed a Size via its underlying C# value."""
        size = Size(raw_value=Point(raw_value=(7, 8)))
        assert (size.width, size.height) == (7, 8)


class TestSizeProperties:
    """Property getters/setters and ``is_empty``."""

    def test_setters(self) -> None:
        """The width/height setters write through to the underlying C# value."""
        size = Size(raw_value=(1, 1))
        size.width = 11
        size.height = 22
        assert (size.width, size.height) == (11, 22)

    def test_is_empty(self) -> None:
        """``is_empty`` is True only for a zero size."""
        assert Size(raw_value=(0, 0)).is_empty is True
        assert Size(raw_value=(0, 1)).is_empty is False


class TestSizeArithmetic:
    """Arithmetic helpers and operators."""

    def test_add_method(self) -> None:
        """``add`` returns the sum of the two sizes."""
        result = Size(raw_value=(3, 4)).add(Size(raw_value=(1, 1)))
        assert (result.width, result.height) == (4, 5)

    def test_subtract_method(self) -> None:
        """``subtract`` returns the difference of the two sizes."""
        result = Size(raw_value=(3, 4)).subtract(Size(raw_value=(1, 1)))
        assert (result.width, result.height) == (2, 3)

    def test_dunder_add_with_cs_size(self) -> None:
        """``Size + System.Drawing.Size`` returns the summed size."""
        result = Size(raw_value=(3, 4)) + CSSize(1, 1)
        assert (result.width, result.height) == (4, 5)

    def test_dunder_add_rejects_non_cs_size(self) -> None:
        """``Size + <non-CSSize>`` raises ``TypeError``."""
        with pytest.raises(TypeError):
            _ = Size(raw_value=(1, 1)) + 5  # type: ignore[operator]

    def test_dunder_sub_with_cs_size(self) -> None:
        """``Size - System.Drawing.Size`` returns the difference."""
        result = Size(raw_value=(5, 7)) - CSSize(1, 2)
        assert (result.width, result.height) == (4, 5)

    def test_dunder_sub_rejects_non_cs_size(self) -> None:
        """``Size - <non-CSSize>`` raises ``TypeError``."""
        with pytest.raises(TypeError):
            _ = Size(raw_value=(1, 1)) - 5  # type: ignore[operator]


class TestSizeConversionAndEquality:
    """Conversions, hashing, string and equality."""

    def test_to_point(self) -> None:
        """``to_point`` carries the dimensions over to a Point."""
        point = Size(raw_value=(3, 4)).to_point()
        assert (point.x, point.y) == (3, 4)

    def test_equals_and_get_hash_code(self) -> None:
        """``equals`` matches identical sizes; ``get_hash_code`` returns an int."""
        size = Size(raw_value=(3, 4))
        assert size.equals(Size(raw_value=(3, 4))) is True
        assert size.equals(Size(raw_value=(5, 6))) is False
        assert isinstance(size.get_hash_code(), int)

    def test_to_string(self) -> None:
        """``to_string`` delegates to the C# representation."""
        assert "Width=3" in Size(raw_value=(3, 4)).to_string()

    def test_dunder_eq_and_ne(self) -> None:
        """``==``/``!=`` compare dimensions and reject non-Size operands."""
        size = Size(raw_value=(3, 4))
        assert size == Size(raw_value=(3, 4))
        assert size != Size(raw_value=(3, 5))
        assert (size == "not a size") is False
        assert (size != "not a size") is True
