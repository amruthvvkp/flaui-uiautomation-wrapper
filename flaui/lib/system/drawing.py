"""This module provides a wrapper class for System.Drawing namespace objects. It also defines an Enum class KnownColor that specifies the known system colors. Wrapper class for System.Drawing namespace objects"""
from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import Field
from pydantic_settings import BaseSettings
from System.Drawing import Color as CSColor, KnownColor as CSKnownColor  # pyright: ignore

# Reference: https://learn.microsoft.com/en-us/dotnet/api/system.drawing.color?view=net-6.0
# # TODO: Consider integrating PIL.ImageColor as a bridge for Python usage, https://pillow.readthedocs.io/en/stable/_modules/PIL/ImageColor.html
class KnownColor(Enum):
    """Specifies the known system colors"""

    ActiveBorder = CSKnownColor.ActiveBorder
    ActiveCaption = CSKnownColor.ActiveCaption
    ActiveCaptionText = CSKnownColor.ActiveCaptionText
    AliceBlue = CSKnownColor.AliceBlue
    AntiqueWhite = CSKnownColor.AntiqueWhite
    AppWorkspace = CSKnownColor.AppWorkspace
    Aqua = CSKnownColor.Aqua
    Aquamarine = CSKnownColor.Aquamarine
    Azure = CSKnownColor.Azure
    Beige = CSKnownColor.Beige
    Bisque = CSKnownColor.Bisque
    Black = CSKnownColor.Black
    BlanchedAlmond = CSKnownColor.BlanchedAlmond
    Blue = CSKnownColor.Blue
    BlueViolet = CSKnownColor.BlueViolet
    Brown = CSKnownColor.Brown
    BurlyWood = CSKnownColor.BurlyWood
    ButtonFace = CSKnownColor.ButtonFace
    ButtonHighlight = CSKnownColor.ButtonHighlight
    ButtonShadow = CSKnownColor.ButtonShadow
    CadetBlue = CSKnownColor.CadetBlue
    Chartreuse = CSKnownColor.Chartreuse
    Chocolate = CSKnownColor.Chocolate
    CompareTo = CSKnownColor.CompareTo
    Control = CSKnownColor.Control
    ControlDark = CSKnownColor.ControlDark
    ControlDarkDark = CSKnownColor.ControlDarkDark
    ControlLight = CSKnownColor.ControlLight
    ControlLightLight = CSKnownColor.ControlLightLight
    ControlText = CSKnownColor.ControlText
    Coral = CSKnownColor.Coral
    CornflowerBlue = CSKnownColor.CornflowerBlue
    Cornsilk = CSKnownColor.Cornsilk
    Crimson = CSKnownColor.Crimson
    Cyan = CSKnownColor.Cyan
    DarkBlue = CSKnownColor.DarkBlue
    DarkCyan = CSKnownColor.DarkCyan
    DarkGoldenrod = CSKnownColor.DarkGoldenrod
    DarkGray = CSKnownColor.DarkGray
    DarkGreen = CSKnownColor.DarkGreen
    DarkKhaki = CSKnownColor.DarkKhaki
    DarkMagenta = CSKnownColor.DarkMagenta
    DarkOliveGreen = CSKnownColor.DarkOliveGreen
    DarkOrange = CSKnownColor.DarkOrange
    DarkOrchid = CSKnownColor.DarkOrchid
    DarkRed = CSKnownColor.DarkRed
    DarkSalmon = CSKnownColor.DarkSalmon
    DarkSeaGreen = CSKnownColor.DarkSeaGreen
    DarkSlateBlue = CSKnownColor.DarkSlateBlue
    DarkSlateGray = CSKnownColor.DarkSlateGray
    DarkTurquoise = CSKnownColor.DarkTurquoise
    DarkViolet = CSKnownColor.DarkViolet
    DeepPink = CSKnownColor.DeepPink
    DeepSkyBlue = CSKnownColor.DeepSkyBlue
    Desktop = CSKnownColor.Desktop
    DimGray = CSKnownColor.DimGray
    DodgerBlue = CSKnownColor.DodgerBlue
    Equals = CSKnownColor.Equals
    Finalize = CSKnownColor.Finalize
    Firebrick = CSKnownColor.Firebrick
    FloralWhite = CSKnownColor.FloralWhite
    ForestGreen = CSKnownColor.ForestGreen
    Format = CSKnownColor.Format
    Fuchsia = CSKnownColor.Fuchsia
    Gainsboro = CSKnownColor.Gainsboro
    GetHashCode = CSKnownColor.GetHashCode
    GetName = CSKnownColor.GetName
    GetNames = CSKnownColor.GetNames
    GetType = CSKnownColor.GetType
    GetTypeCode = CSKnownColor.GetTypeCode
    GetUnderlyingType = CSKnownColor.GetUnderlyingType
    GetValues = CSKnownColor.GetValues
    GhostWhite = CSKnownColor.GhostWhite
    Gold = CSKnownColor.Gold
    Goldenrod = CSKnownColor.Goldenrod
    GradientActiveCaption = CSKnownColor.GradientActiveCaption
    GradientInactiveCaption = CSKnownColor.GradientInactiveCaption
    Gray = CSKnownColor.Gray
    GrayText = CSKnownColor.GrayText
    Green = CSKnownColor.Green
    GreenYellow = CSKnownColor.GreenYellow
    HasFlag = CSKnownColor.HasFlag
    Highlight = CSKnownColor.Highlight
    HighlightText = CSKnownColor.HighlightText
    Honeydew = CSKnownColor.Honeydew
    HotPink = CSKnownColor.HotPink
    HotTrack = CSKnownColor.HotTrack
    InactiveBorder = CSKnownColor.InactiveBorder
    InactiveCaption = CSKnownColor.InactiveCaption
    InactiveCaptionText = CSKnownColor.InactiveCaptionText
    IndianRed = CSKnownColor.IndianRed
    Indigo = CSKnownColor.Indigo
    Info = CSKnownColor.Info
    InfoText = CSKnownColor.InfoText
    IsDefined = CSKnownColor.IsDefined
    Ivory = CSKnownColor.Ivory
    Khaki = CSKnownColor.Khaki
    Lavender = CSKnownColor.Lavender
    LavenderBlush = CSKnownColor.LavenderBlush
    LawnGreen = CSKnownColor.LawnGreen
    LemonChiffon = CSKnownColor.LemonChiffon
    LightBlue = CSKnownColor.LightBlue
    LightCoral = CSKnownColor.LightCoral
    LightCyan = CSKnownColor.LightCyan
    LightGoldenrodYellow = CSKnownColor.LightGoldenrodYellow
    LightGray = CSKnownColor.LightGray
    LightGreen = CSKnownColor.LightGreen
    LightPink = CSKnownColor.LightPink
    LightSalmon = CSKnownColor.LightSalmon
    LightSeaGreen = CSKnownColor.LightSeaGreen
    LightSkyBlue = CSKnownColor.LightSkyBlue
    LightSlateGray = CSKnownColor.LightSlateGray
    LightSteelBlue = CSKnownColor.LightSteelBlue
    LightYellow = CSKnownColor.LightYellow
    Lime = CSKnownColor.Lime
    LimeGreen = CSKnownColor.LimeGreen
    Linen = CSKnownColor.Linen
    Magenta = CSKnownColor.Magenta
    Maroon = CSKnownColor.Maroon
    MediumAquamarine = CSKnownColor.MediumAquamarine
    MediumBlue = CSKnownColor.MediumBlue
    MediumOrchid = CSKnownColor.MediumOrchid
    MediumPurple = CSKnownColor.MediumPurple
    MediumSeaGreen = CSKnownColor.MediumSeaGreen
    MediumSlateBlue = CSKnownColor.MediumSlateBlue
    MediumSpringGreen = CSKnownColor.MediumSpringGreen
    MediumTurquoise = CSKnownColor.MediumTurquoise
    MediumVioletRed = CSKnownColor.MediumVioletRed
    MemberwiseClone = CSKnownColor.MemberwiseClone
    Menu = CSKnownColor.Menu
    MenuBar = CSKnownColor.MenuBar
    MenuHighlight = CSKnownColor.MenuHighlight
    MenuText = CSKnownColor.MenuText
    MidnightBlue = CSKnownColor.MidnightBlue
    MintCream = CSKnownColor.MintCream
    MistyRose = CSKnownColor.MistyRose
    Moccasin = CSKnownColor.Moccasin
    NavajoWhite = CSKnownColor.NavajoWhite
    Navy = CSKnownColor.Navy
    OldLace = CSKnownColor.OldLace
    Olive = CSKnownColor.Olive
    OliveDrab = CSKnownColor.OliveDrab
    Orange = CSKnownColor.Orange
    OrangeRed = CSKnownColor.OrangeRed
    Orchid = CSKnownColor.Orchid
    Overloads = CSKnownColor.Overloads
    PaleGoldenrod = CSKnownColor.PaleGoldenrod
    PaleGreen = CSKnownColor.PaleGreen
    PaleTurquoise = CSKnownColor.PaleTurquoise
    PaleVioletRed = CSKnownColor.PaleVioletRed
    PapayaWhip = CSKnownColor.PapayaWhip
    Parse = CSKnownColor.Parse
    PeachPuff = CSKnownColor.PeachPuff
    Peru = CSKnownColor.Peru
    Pink = CSKnownColor.Pink
    Plum = CSKnownColor.Plum
    PowderBlue = CSKnownColor.PowderBlue
    Purple = CSKnownColor.Purple
    Red = CSKnownColor.Red
    ReferenceEquals = CSKnownColor.ReferenceEquals
    RosyBrown = CSKnownColor.RosyBrown
    RoyalBlue = CSKnownColor.RoyalBlue
    SaddleBrown = CSKnownColor.SaddleBrown
    Salmon = CSKnownColor.Salmon
    SandyBrown = CSKnownColor.SandyBrown
    ScrollBar = CSKnownColor.ScrollBar
    SeaGreen = CSKnownColor.SeaGreen
    SeaShell = CSKnownColor.SeaShell
    Sienna = CSKnownColor.Sienna
    Silver = CSKnownColor.Silver
    SkyBlue = CSKnownColor.SkyBlue
    SlateBlue = CSKnownColor.SlateBlue
    SlateGray = CSKnownColor.SlateGray
    Snow = CSKnownColor.Snow
    SpringGreen = CSKnownColor.SpringGreen
    SteelBlue = CSKnownColor.SteelBlue
    Tan = CSKnownColor.Tan
    Teal = CSKnownColor.Teal
    Thistle = CSKnownColor.Thistle
    ToObject = CSKnownColor.ToObject
    ToString = CSKnownColor.ToString
    Tomato = CSKnownColor.Tomato
    Transparent = CSKnownColor.Transparent
    TryParse = CSKnownColor.TryParse
    Turquoise = CSKnownColor.Turquoise
    Violet = CSKnownColor.Violet
    Wheat = CSKnownColor.Wheat
    White = CSKnownColor.White
    WhiteSmoke = CSKnownColor.WhiteSmoke
    Window = CSKnownColor.Window
    WindowFrame = CSKnownColor.WindowFrame
    WindowText = CSKnownColor.WindowText
    Yellow = CSKnownColor.Yellow
    YellowGreen = CSKnownColor.YellowGreen


class ColorData(BaseSettings):
    """Represents an ARGB (alpha, red, green, blue) System.Drawing.Color color object."""
    cs_object: Any = Field(...)

    @property
    def is_named_color(self) -> bool:
        """Gets a value indicating whether this System.Drawing.Color structure is a named
        color or a member of the System.Drawing.KnownColor enumeration.

        :return: True if this System.Drawing.Color was created by using either the System.Drawing.Color.FromName(System.String)
        method or the System.Drawing.Color.FromKnownColor(System.Drawing.KnownColor) method; otherwise, False.
        """
        return self.cs_object.IsNamedColor

    @property
    def is_known_color(self) -> bool:
        """Gets a value indicating whether this System.Drawing.Color structure is a predefined
        color. Predefined colors are represented by the elements of the System.Drawing.KnownColor
        enumeration.

        :return: True if this System.Drawing.Color was created from a predefined color by using
        either the System.Drawing.Color.FromName(System.String) method or the System.Drawing.Color.FromKnownColor(System.Drawing.KnownColor)
        method; otherwise, False.
        """
        return self.cs_object.IsKnownColor

    @property
    def is_empty(self) -> bool:
        """Specifies whether this System.Drawing.Color structure is uninitialized.

        :return: This property returns True if this color is uninitialized; otherwise, False.
        """
        return self.cs_object.IsEmpty

    @property
    def is_system_color(self) -> str:
        """Gets a value indicating whether this System.Drawing.Color structure is a system
        color. A system color is a color that is used in a Windows display element. System
        colors are represented by elements of the System.Drawing.KnownColor enumeration.

        :return: True if this System.Drawing.Color was created from a system color by using either
        the System.Drawing.Color.FromName(System.String) method or the System.Drawing.Color.FromKnownColor(System.Drawing.KnownColor)
        method; otherwise, False.
        """
        return self.cs_object.IsSystemColor

    @property
    def name(self) -> str:
        """Gets the name of this System.Drawing.Color.

        :return: The name of this System.Drawing.Color.
        """
        return self.cs_object.Name

    @property
    def a(self) -> bytes:
        """Gets the alpha component value of this System.Drawing.Color structure.

        :return: The alpha component value of this System.Drawing.Color.
        """
        return self.cs_object.A

    @property
    def b(self) -> bytes:
        """Gets the blue component value of this System.Drawing.Color structure.

        :return: The blue component value of this System.Drawing.Color.
        """
        return self.cs_object.B

    @property
    def r(self) -> bytes:
        """Gets the red component value of this System.Drawing.Color structure.

        :return: The red component value of this System.Drawing.Color.
        """
        return self.cs_object.R

    @property
    def g(self) -> bytes:
        """Gets the green component value of this System.Drawing.Color structure.

        :return: The green component value of this System.Drawing.Color.
        """
        return self.cs_object.G

    def equals(self, another_color: ColorData) -> bool:
        """Indicates whether the current object is equal to another object of the same type.

        :param another_color: An object to compare with this object.
        :return: True if the current object is equal to other; otherwise, False.
        """
        return self.cs_object.Equals(another_color.cs_object)

    def get_brightness(self) -> float:
        """Gets the hue-saturation-lightness (HSL) lightness value for this System.Drawing.Color
        structure.

        :return: The lightness of this System.Drawing.Color. The lightness ranges from 0.0 through
        1.0, where 0.0 represents black and 1.0 represents white.
        """
        return self.cs_object.GetBrightness()

    def get_hash_code(self) -> int:
        """Returns a hash code for this System.Drawing.Color structure.

        :return: An integer value that specifies the hash code for this System.Drawing.Color.
        """
        return self.cs_object.GetHashCode()

    def get_hue(self) -> float:
        """Gets the hue-saturation-lightness (HSL) hue value, in degrees, for this System.Drawing.Color
        structure.

        :return: The hue, in degrees, of this System.Drawing.Color. The hue is measured in degrees,
        ranging from 0.0 through 360.0, in HSL color space.
        """
        return self.cs_object.GetHashCode()

    def get_saturation(self) -> float:
        """Gets the hue-saturation-lightness (HSL) saturation value for this System.Drawing.Color
        structure.

        :return: The saturation of this System.Drawing.Color. The saturation ranges from 0.0 through
        1.0, where 0.0 is grayscale and 1.0 is the most saturated.
        """
        return self.cs_object.GetSaturation()

    def to_argb(self) -> int:
        """Gets the 32-bit ARGB value of this System.Drawing.Color structure.

        :return: The 32-bit ARGB value of this System.Drawing.Color.
        """
        return self.cs_object.ToArgb()

    def to_known_color(self) -> KnownColor:
        """Gets the System.Drawing.KnownColor value of this System.Drawing.Color structure.

        :return: An element of the System.Drawing.KnownColor enumeration, if the System.Drawing.Color
        is created from a predefined color by using either the System.Drawing.Color.FromName(System.String)
        method or the System.Drawing.Color.FromKnownColor(System.Drawing.KnownColor)
        method; otherwise, 0.
        """
        return KnownColor(self.cs_object.ToKnownColor())

    def to_string(self) -> int:
        """Converts this System.Drawing.Color structure to a human-readable string.

        :return: A string that is the name of this System.Drawing.Color, if the System.Drawing.Color
        is created from a predefined color by using either the System.Drawing.Color.FromName(System.String)
        method or the System.Drawing.Color.FromKnownColor(System.Drawing.KnownColor)
        method; otherwise, a string that consists of the ARGB component names and their
        values.
        """
        return self.cs_object.ToString()

# Treating this as an Enum class is resulting in the below error -
# Unhandled Exception: System.ArgumentException: We should never receive instances of other managed types
#    at Python.Runtime.Converter.ToManagedValue(BorrowedReference value, Type obType, Object& result, Boolean setError)
#    at Python.Runtime.MethodBinder.TryConvertArgument(BorrowedReference op, Type parameterType, Object& arg, Boolean& isOut)
#    at Python.Runtime.MethodBinder.TryConvertArguments(ParameterInfo[] pi, Boolean paramsArray, BorrowedReference args, Int32 pyArgCount, Dictionary`2 kwargDict, ArrayList defaultArgList, Int32& outs)
#    at Python.Runtime.MethodBinder.Bind(BorrowedReference inst, BorrowedReference args, Dictionary`2 kwargDict, MethodBase[] methods, Boolean matchGenerics)
#    at Python.Runtime.MethodBinder.Bind(BorrowedReference inst, BorrowedReference args, BorrowedReference kw, MethodBase info, MethodBase[] methodinfo)
#    at Python.Runtime.MethodBinder.Invoke(BorrowedReference inst, BorrowedReference args, BorrowedReference kw, MethodBase info, MethodBase[] methodinfo)
#    at Python.Runtime.MethodObject.Invoke(BorrowedReference target, BorrowedReference args, BorrowedReference kw, MethodBase info)
#    at Python.Runtime.MethodObject.Invoke(BorrowedReference inst, BorrowedReference args, BorrowedReference kw)
#    at Python.Runtime.ClassBase.tp_richcompare(BorrowedReference ob, BorrowedReference other, Int32 op)
class Color:
    """Represents an ARGB (alpha, red, green, blue) color from System.Drawing.Color object"""
    # X11 colour table from https://drafts.csswg.org/css-color-4/, with
    # gray/grey spelling issues fixed.  This is a superset of HTML 4.0
    # colour names used in CSS 1.
    AliceBlue = ColorData(cs_object=CSColor.AliceBlue)
    AntiqueWhite = ColorData(cs_object=CSColor.AntiqueWhite)
    Aqua = ColorData(cs_object=CSColor.Aqua)
    Aquamarine = ColorData(cs_object=CSColor.Aquamarine)
    Azure = ColorData(cs_object=CSColor.Azure)
    Beige = ColorData(cs_object=CSColor.Beige)
    Bisque = ColorData(cs_object=CSColor.Bisque)
    Black = ColorData(cs_object=CSColor.Black)
    BlanchedAlmond = ColorData(cs_object=CSColor.BlanchedAlmond)
    Blue = ColorData(cs_object=CSColor.Blue)
    BlueViolet = ColorData(cs_object=CSColor.BlueViolet)
    Brown = ColorData(cs_object=CSColor.Brown)
    BurlyWood = ColorData(cs_object=CSColor.BurlyWood)
    CadetBlue = ColorData(cs_object=CSColor.CadetBlue)
    Chartreuse = ColorData(cs_object=CSColor.Chartreuse)
    Chocolate = ColorData(cs_object=CSColor.Chocolate)
    Coral = ColorData(cs_object=CSColor.Coral)
    CornflowerBlue = ColorData(cs_object=CSColor.CornflowerBlue)
    Cornsilk = ColorData(cs_object=CSColor.Cornsilk)
    Crimson = ColorData(cs_object=CSColor.Crimson)
    Cyan = ColorData(cs_object=CSColor.Cyan)
    DarkBlue = ColorData(cs_object=CSColor.DarkBlue)
    DarkCyan = ColorData(cs_object=CSColor.DarkCyan)
    DarkGoldenrod = ColorData(cs_object=CSColor.DarkGoldenrod)
    DarkGray = ColorData(cs_object=CSColor.DarkGray)
    DarkGreen = ColorData(cs_object=CSColor.DarkGreen)
    DarkKhaki = ColorData(cs_object=CSColor.DarkKhaki)
    DarkMagenta = ColorData(cs_object=CSColor.DarkMagenta)
    DarkOliveGreen = ColorData(cs_object=CSColor.DarkOliveGreen)
    DarkOrange = ColorData(cs_object=CSColor.DarkOrange)
    DarkOrchid = ColorData(cs_object=CSColor.DarkOrchid)
    DarkRed = ColorData(cs_object=CSColor.DarkRed)
    DarkSalmon = ColorData(cs_object=CSColor.DarkSalmon)
    DarkSeaGreen = ColorData(cs_object=CSColor.DarkSeaGreen)
    DarkSlateBlue = ColorData(cs_object=CSColor.DarkSlateBlue)
    DarkSlateGray = ColorData(cs_object=CSColor.DarkSlateGray)
    DarkTurquoise = ColorData(cs_object=CSColor.DarkTurquoise)
    DarkViolet = ColorData(cs_object=CSColor.DarkViolet)
    DeepPink = ColorData(cs_object=CSColor.DeepPink)
    DeepSkyBlue = ColorData(cs_object=CSColor.DeepSkyBlue)
    DimGray = ColorData(cs_object=CSColor.DimGray)
    DodgerBlue = ColorData(cs_object=CSColor.DodgerBlue)
    Firebrick = ColorData(cs_object=CSColor.Firebrick)
    FloralWhite = ColorData(cs_object=CSColor.FloralWhite)
    ForestGreen = ColorData(cs_object=CSColor.ForestGreen)
    Fuchsia = ColorData(cs_object=CSColor.Fuchsia)
    Gainsboro = ColorData(cs_object=CSColor.Gainsboro)
    GhostWhite = ColorData(cs_object=CSColor.GhostWhite)
    Gold = ColorData(cs_object=CSColor.Gold)
    Goldenrod = ColorData(cs_object=CSColor.Goldenrod)
    Gray = ColorData(cs_object=CSColor.Gray)
    Green = ColorData(cs_object=CSColor.Green)
    GreenYellow = ColorData(cs_object=CSColor.GreenYellow)
    Honeydew = ColorData(cs_object=CSColor.Honeydew)
    HotPink = ColorData(cs_object=CSColor.HotPink)
    IndianRed = ColorData(cs_object=CSColor.IndianRed)
    Indigo = ColorData(cs_object=CSColor.Indigo)
    Ivory = ColorData(cs_object=CSColor.Ivory)
    Khaki = ColorData(cs_object=CSColor.Khaki)
    Lavender = ColorData(cs_object=CSColor.Lavender)
    LavenderBlush = ColorData(cs_object=CSColor.LavenderBlush)
    LawnGreen = ColorData(cs_object=CSColor.LawnGreen)
    LemonChiffon = ColorData(cs_object=CSColor.LemonChiffon)
    LightBlue = ColorData(cs_object=CSColor.LightBlue)
    LightCoral = ColorData(cs_object=CSColor.LightCoral)
    LightCyan = ColorData(cs_object=CSColor.LightCyan)
    LightGoldenrodYellow = ColorData(cs_object=CSColor.LightGoldenrodYellow)
    LightGray = ColorData(cs_object=CSColor.LightGray)
    LightGreen = ColorData(cs_object=CSColor.LightGreen)
    LightPink = ColorData(cs_object=CSColor.LightPink)
    LightSalmon = ColorData(cs_object=CSColor.LightSalmon)
    LightSeaGreen = ColorData(cs_object=CSColor.LightSeaGreen)
    LightSkyBlue = ColorData(cs_object=CSColor.LightSkyBlue)
    LightSlateGray = ColorData(cs_object=CSColor.LightSlateGray)
    LightSteelBlue = ColorData(cs_object=CSColor.LightSteelBlue)
    LightYellow = ColorData(cs_object=CSColor.LightYellow)
    Lime = ColorData(cs_object=CSColor.Lime)
    LimeGreen = ColorData(cs_object=CSColor.LimeGreen)
    Linen = ColorData(cs_object=CSColor.Linen)
    Magenta = ColorData(cs_object=CSColor.Magenta)
    Maroon = ColorData(cs_object=CSColor.Maroon)
    MediumAquamarine = ColorData(cs_object=CSColor.MediumAquamarine)
    MediumBlue = ColorData(cs_object=CSColor.MediumBlue)
    MediumOrchid = ColorData(cs_object=CSColor.MediumOrchid)
    MediumPurple = ColorData(cs_object=CSColor.MediumPurple)
    MediumSeaGreen = ColorData(cs_object=CSColor.MediumSeaGreen)
    MediumSlateBlue = ColorData(cs_object=CSColor.MediumSlateBlue)
    MediumSpringGreen = ColorData(cs_object=CSColor.MediumSpringGreen)
    MediumTurquoise = ColorData(cs_object=CSColor.MediumTurquoise)
    MediumVioletRed = ColorData(cs_object=CSColor.MediumVioletRed)
    MemberwiseClone = ColorData(cs_object=CSColor.MemberwiseClone)
    MidnightBlue = ColorData(cs_object=CSColor.MidnightBlue)
    MintCream = ColorData(cs_object=CSColor.MintCream)
    MistyRose = ColorData(cs_object=CSColor.MistyRose)
    Moccasin = ColorData(cs_object=CSColor.Moccasin)
    NavajoWhite = ColorData(cs_object=CSColor.NavajoWhite)
    Navy = ColorData(cs_object=CSColor.Navy)
    OldLace = ColorData(cs_object=CSColor.OldLace)
    Olive = ColorData(cs_object=CSColor.Olive)
    OliveDrab = ColorData(cs_object=CSColor.OliveDrab)
    Orange = ColorData(cs_object=CSColor.Orange)
    OrangeRed = ColorData(cs_object=CSColor.OrangeRed)
    Orchid = ColorData(cs_object=CSColor.Orchid)
    Overloads = ColorData(cs_object=CSColor.Overloads)
    PaleGoldenrod = ColorData(cs_object=CSColor.PaleGoldenrod)
    PaleGreen = ColorData(cs_object=CSColor.PaleGreen)
    PaleTurquoise = ColorData(cs_object=CSColor.PaleTurquoise)
    PaleVioletRed = ColorData(cs_object=CSColor.PaleVioletRed)
    PapayaWhip = ColorData(cs_object=CSColor.PapayaWhip)
    PeachPuff = ColorData(cs_object=CSColor.PeachPuff)
    Peru = ColorData(cs_object=CSColor.Peru)
    Pink = ColorData(cs_object=CSColor.Pink)
    Plum = ColorData(cs_object=CSColor.Plum)
    PowderBlue = ColorData(cs_object=CSColor.PowderBlue)
    Purple = ColorData(cs_object=CSColor.Purple)
    Red = ColorData(cs_object=CSColor.Red)
    RosyBrown = ColorData(cs_object=CSColor.RosyBrown)
    RoyalBlue = ColorData(cs_object=CSColor.RoyalBlue)
    SaddleBrown = ColorData(cs_object=CSColor.SaddleBrown)
    Salmon = ColorData(cs_object=CSColor.Salmon)
    SandyBrown = ColorData(cs_object=CSColor.SandyBrown)
    SeaGreen = ColorData(cs_object=CSColor.SeaGreen)
    SeaShell = ColorData(cs_object=CSColor.SeaShell)
    Sienna = ColorData(cs_object=CSColor.Sienna)
    Silver = ColorData(cs_object=CSColor.Silver)
    SkyBlue = ColorData(cs_object=CSColor.SkyBlue)
    SlateBlue = ColorData(cs_object=CSColor.SlateBlue)
    SlateGray = ColorData(cs_object=CSColor.SlateGray)
    Snow = ColorData(cs_object=CSColor.Snow)
    SpringGreen = ColorData(cs_object=CSColor.SpringGreen)
    SteelBlue = ColorData(cs_object=CSColor.SteelBlue)
    Tan = ColorData(cs_object=CSColor.Tan)
    Teal = ColorData(cs_object=CSColor.Teal)
    Thistle = ColorData(cs_object=CSColor.Thistle)
    Tomato = ColorData(cs_object=CSColor.Tomato)
    Transparent = ColorData(cs_object=CSColor.Transparent)
    Turquoise = ColorData(cs_object=CSColor.Turquoise)
    Violet = ColorData(cs_object=CSColor.Violet)
    Wheat = ColorData(cs_object=CSColor.Wheat)
    White = ColorData(cs_object=CSColor.White)
    WhiteSmoke = ColorData(cs_object=CSColor.WhiteSmoke)
    Yellow = ColorData(cs_object=CSColor.Yellow)
    YellowGreen = ColorData(cs_object=CSColor.YellowGreen)

    @staticmethod
    def from_argb(
        argb: Optional[int] = None,
        alpha: Optional[int] = None,
        base_color: Optional[ColorData] = None,
        red: Optional[int] = None,
        green: Optional[int] = None,
        blue: Optional[int] = None,
    ) -> ColorData:
        """
        Creates a ColorData object from various input formats matching C# System.Drawing.Color

        :param argb: A value specifying the 32-bit ARGB value, defaults to None
        :param alpha: The alpha component. Valid values are 0 through 255, defaults to None
        :param base_color: The System.Drawing.Color from which to create the new System.Drawing.Color, defaults to None
        :param red: The red component. Valid values are 0 through 255, defaults to None
        :param green: The green component. Valid values are 0 through 255, defaults to None
        :param blue: The blue component. Valid values are 0 through 255, defaults to None
        :raises ValueError: On invalid input combination
        :return: The ColorData object representing the color.
        """

        # Check for valid input combinations
        if all(x is not None for x in [alpha, red, green, blue]):  # Check if all components are provided (including None)
            # ARGB with all components provided
            return ColorData(cs_object=CSColor.FromArgb(alpha, red, green, blue))
        elif all(x is not None for x in [red, green, blue]) and alpha is None:
            # RGB with implicit alpha 255
            return ColorData(cs_object=CSColor.FromArgb(red, green, blue))
        elif alpha is not None and base_color is not None:
            # Set alpha for existing color
            return ColorData(cs_object=CSColor.FromArgb(alpha, base_color.cs_object))
        elif argb is not None and any([alpha, red, green, blue]) is False:

            # Single ARGB value
            alpha = (argb >> 24) & 0xFF  # Extract alpha (shift 24 bits and mask with 0xFF)
            red = (argb >> 16) & 0xFF    # Extract red (shift 16 bits and mask with 0xFF)
            green = (argb >> 8) & 0xFF   # Extract green (shift 8 bits and mask with 0xFF)
            blue = argb & 0xFF           # Extract blue (mask with 0xFF)
            return ColorData(cs_object=CSColor.FromArgb(alpha, red, green, blue))
        else:
            raise ValueError(
                "Invalid arguments sent as input, cannot create ColorData object."
            )
    @staticmethod
    def from_known_color(known_color: KnownColor) -> ColorData:
        """Creates a System.Drawing.Color structure from the specified predefined color.

        :param known_color: An element of the System.Drawing.KnownColor enumeration.
        :return: The System.Drawing.Color that this method creates.
        """
        return ColorData(cs_object=CSColor.FromKnownColor(known_color.value))

    @staticmethod
    def from_name(name: str) -> ColorData:
        """Creates a System.Drawing.Color structure from the specified name of a predefined
        color.

        :param name: A string that is the name of a predefined color. Valid names are the same as
        the names of the elements of the System.Drawing.KnownColor enumeration.
        :return: The System.Drawing.Color that this method creates.
        """
        return ColorData(cs_object=CSColor.FromName(name))
