"""Tests classes under C# System.Drawing namespace"""

from flaui.lib.system.drawing import Color
import pytest

class TestColor:
    """Tests python wrapper for C# System.Drawing.Color namespace"""
    def test_from_argb_single_value(self):
        """Tests creating a ColorData object from a single ARGB value"""
        color_object = Color.from_argb(argb=0xFF00FF00)
        assert color_object.name == "ff00ff00"

    def test_from_argb_all_components(self):
        """Tests creating a ColorData object from all RGB and alpha components"""
        color_object = Color.from_argb(alpha=128, red=255, green=0, blue=0)
        assert color_object.name == "80ff0000"  # Check ARGB value

    def test_from_argb_rgb_components(self):
        """Tests creating a ColorData object from RGB components (implicit alpha 255)"""
        color_object = Color.from_argb(red=0, green=255, blue=0)
        assert color_object.name == "ff00ff00"  # Check ARGB value

    def test_from_argb_alpha_with_base_color(self):
        """Tests creating a ColorData object by setting alpha for an existing color"""
        base_color = Color.from_argb(red=255, green=0, blue=0)
        color_object = Color.from_argb(alpha=128, base_color=base_color)
        assert color_object.name == "80ff0000"  # Check ARGB value

    def test_from_argb_invalid_input(self):
        """Tests for invalid input combinations"""
        with pytest.raises(ValueError):
            Color.from_argb(alpha=100, red=200, blue=50)  # All separate components

        with pytest.raises(ValueError):
            Color.from_argb(green=0)  # RGB with alpha

        with pytest.raises(ValueError):
            Color.from_argb(red=255, base_color=Color.from_argb(red=255, green=0, blue=0))  # No arguments
