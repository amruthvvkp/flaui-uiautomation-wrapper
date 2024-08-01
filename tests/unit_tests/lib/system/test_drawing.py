"""
This module contains unit tests for the drawing.py module. It tests the following classes and functions:
- KnownColor
- Color
- ColorCollection
"""

from flaui.lib.system.drawing import Color, ColorData, KnownColor
from System.Drawing import Color as CSColor, KnownColor as CSKnownColor  # pyright: ignore


def test_known_color():
    """Unit tests for the class KnownColor"""
    assert all([_ in KnownColor.__members__ for _ in list(vars(CSKnownColor).keys()) if "_" not in _])


def test_color_model():
    """Unit tests for the Pydantic model Color"""
    color = ColorData(cs_object=CSColor.AliceBlue)
    assert color.name == "AliceBlue"
    assert color.r == 240
    assert color.g == 248
    assert color.b == 255
    assert color.a == 255
    assert color.cs_object == CSColor.AliceBlue
    assert color.is_empty is False
    assert color.is_known_color is True
    assert color.is_named_color is True
    assert color.is_system_color is False

    assert color != ColorData(cs_object=CSColor.AntiqueWhite)
    assert color.equals(ColorData(cs_object=CSColor.AliceBlue)) is True
    assert color.equals(ColorData(cs_object=CSColor.AntiqueWhite)) is False

    assert color.get_brightness() is not None
    assert color.get_hue() is not None
    assert color.get_hash_code() is not None
    assert color.get_saturation() is not None

    assert color.to_argb() == -984833
    assert color.to_known_color() == KnownColor["AliceBlue"]
    assert color.to_string() == "Color [AliceBlue]"

    assert Color.from_argb(-984833) == Color.from_argb(alpha=255, red=240, green=248, blue=255)
    assert Color.from_known_color(KnownColor["AliceBlue"]) == ColorData(cs_object=CSColor.AliceBlue)
    assert Color.from_name("AliceBlue") == ColorData(cs_object=CSColor.AliceBlue)


def test_color_collection():
    """Unit tests for the mapped class ColorCollection"""
    expected_keys = [_ for _ in list(vars(CSColor).keys()) if "_" not in _]
    actual_keys = [_ for _ in list(vars(Color).keys()) if "_" not in _]

    # These excluded keys are a part of the C# Class but we don't need them at this moment
    excluded_keys = [
        "R",
        "G",
        "B",
        "A",
        "IsKnownColor",
        "IsEmpty",
        "IsNamedColor",
        "IsSystemColor",
        "Name",
        "Empty",
        "FromArgb",
        "FromKnownColor",
        "FromName",
        "Equals",
        "GetBrightness",
        "GetHashCode",
        "GetHue",
        "GetSaturation",
        "ToArgb",
        "ToKnownColor",
        "ToString",
    ]
    assert all([_ in actual_keys for _ in expected_keys if _ not in excluded_keys])
