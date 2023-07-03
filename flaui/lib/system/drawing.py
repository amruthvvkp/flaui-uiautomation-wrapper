"""Wrapper class for System.Drawing namespace objects"""
from __future__ import annotations

from enum import Enum
from typing import Any
from typing import Optional

from pydantic import BaseSettings
from pydantic import Field
from System.Drawing import Color as CSColor  # pyright: ignore
from System.Drawing import KnownColor as CSKnownColor  # pyright: ignore

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


class Color(BaseSettings):
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

    def equals(self, another_color: ColorCollection) -> bool:
        """Indicates whether the current object is equal to another object of the same type.

        :param another_color: An object to compare with this object.
        :return: True if the current object is equal to other; otherwise, False.
        """
        return self.cs_object.Equals(another_color)

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

    def from_argb(
        self,
        argb: Optional[int] = None,
        alpha: Optional[int] = None,
        base_color: Optional[ColorCollection] = None,
        red: Optional[int] = None,
        green: Optional[int] = None,
        blue: Optional[int] = None,
    ) -> Color:
        """Creates a System.Drawing.Color structure from a 32-bit ARGB value.

        :param argb: A value specifying the 32-bit ARGB value, defaults to None
        :param alpha: The alpha component. Valid values are 0 through 255, defaults to None
        :param base_color: The System.Drawing.Color from which to create the new System.Drawing.Color, defaults to None
        :param red: The red component. Valid values are 0 through 255, defaults to None
        :param green: The green component. Valid values are 0 through 255, defaults to None
        :param blue: The blue component. Valid values are 0 through 255, defaults to None
        :raises ValueError: On invalid input combination, input needs to be one among - argb or alpha+base_color or red+green+blue or alpha+red+green+blue
        :return: The System.Drawing.Color that this method creates.
        """
        if all([alpha, red, green, blue]):
            return Color(cs_object=self.cs_object.FromArgb(alpha, red, green, blue))
        elif all([red, green, blue]):
            return Color(cs_object=self.cs_object.FromArgb(red, green, blue))
        elif all([alpha, base_color]):
            return Color(cs_object=self.cs_object.FromArgb(alpha, base_color))
        elif argb is not None and any([alpha, red, green, blue]) is False:
            return Color(cs_object=self.cs_object.FromArgb(argb))
        else:
            raise ValueError(
                "Invalid arguments sent as input, cannot fetch Color object from the given input parameters"
            )

    def from_known_color(self, known_color: KnownColor) -> Color:
        """Creates a System.Drawing.Color structure from the specified predefined color.

        :param known_color: An element of the System.Drawing.KnownColor enumeration.
        :return: The System.Drawing.Color that this method creates.
        """
        return Color(cs_object=self.cs_object.FromKnownColor(known_color))

    def from_name(self, name: str) -> Color:
        """Creates a System.Drawing.Color structure from the specified name of a predefined
        color.

        :param name: A string that is the name of a predefined color. Valid names are the same as
        the names of the elements of the System.Drawing.KnownColor enumeration.
        :return: The System.Drawing.Color that this method creates.
        """
        return Color(cs_object=self.cs_object.FromName(name))


class ColorCollection(Enum):
    """Represents an ARGB (alpha, red, green, blue) color"""

    AliceBlue = Color(cs_object=CSColor.AliceBlue)
    AntiqueWhite = Color(cs_object=CSColor.AntiqueWhite)
    Aqua = Color(cs_object=CSColor.Aqua)
    Aquamarine = Color(cs_object=CSColor.Aquamarine)
    Azure = Color(cs_object=CSColor.Azure)
    Beige = Color(cs_object=CSColor.Beige)
    Bisque = Color(cs_object=CSColor.Bisque)
    Black = Color(cs_object=CSColor.Black)
    BlanchedAlmond = Color(cs_object=CSColor.BlanchedAlmond)
    Blue = Color(cs_object=CSColor.Blue)
    BlueViolet = Color(cs_object=CSColor.BlueViolet)
    Brown = Color(cs_object=CSColor.Brown)
    BurlyWood = Color(cs_object=CSColor.BurlyWood)
    CadetBlue = Color(cs_object=CSColor.CadetBlue)
    Chartreuse = Color(cs_object=CSColor.Chartreuse)
    Chocolate = Color(cs_object=CSColor.Chocolate)
    Coral = Color(cs_object=CSColor.Coral)
    CornflowerBlue = Color(cs_object=CSColor.CornflowerBlue)
    Cornsilk = Color(cs_object=CSColor.Cornsilk)
    Crimson = Color(cs_object=CSColor.Crimson)
    Cyan = Color(cs_object=CSColor.Cyan)
    DarkBlue = Color(cs_object=CSColor.DarkBlue)
    DarkCyan = Color(cs_object=CSColor.DarkCyan)
    DarkGoldenrod = Color(cs_object=CSColor.DarkGoldenrod)
    DarkGray = Color(cs_object=CSColor.DarkGray)
    DarkGreen = Color(cs_object=CSColor.DarkGreen)
    DarkKhaki = Color(cs_object=CSColor.DarkKhaki)
    DarkMagenta = Color(cs_object=CSColor.DarkMagenta)
    DarkOliveGreen = Color(cs_object=CSColor.DarkOliveGreen)
    DarkOrange = Color(cs_object=CSColor.DarkOrange)
    DarkOrchid = Color(cs_object=CSColor.DarkOrchid)
    DarkRed = Color(cs_object=CSColor.DarkRed)
    DarkSalmon = Color(cs_object=CSColor.DarkSalmon)
    DarkSeaGreen = Color(cs_object=CSColor.DarkSeaGreen)
    DarkSlateBlue = Color(cs_object=CSColor.DarkSlateBlue)
    DarkSlateGray = Color(cs_object=CSColor.DarkSlateGray)
    DarkTurquoise = Color(cs_object=CSColor.DarkTurquoise)
    DarkViolet = Color(cs_object=CSColor.DarkViolet)
    DeepPink = Color(cs_object=CSColor.DeepPink)
    DeepSkyBlue = Color(cs_object=CSColor.DeepSkyBlue)
    DimGray = Color(cs_object=CSColor.DimGray)
    DodgerBlue = Color(cs_object=CSColor.DodgerBlue)
    Firebrick = Color(cs_object=CSColor.Firebrick)
    FloralWhite = Color(cs_object=CSColor.FloralWhite)
    ForestGreen = Color(cs_object=CSColor.ForestGreen)
    Fuchsia = Color(cs_object=CSColor.Fuchsia)
    Gainsboro = Color(cs_object=CSColor.Gainsboro)
    GhostWhite = Color(cs_object=CSColor.GhostWhite)
    Gold = Color(cs_object=CSColor.Gold)
    Goldenrod = Color(cs_object=CSColor.Goldenrod)
    Gray = Color(cs_object=CSColor.Gray)
    Green = Color(cs_object=CSColor.Green)
    GreenYellow = Color(cs_object=CSColor.GreenYellow)
    Honeydew = Color(cs_object=CSColor.Honeydew)
    HotPink = Color(cs_object=CSColor.HotPink)
    IndianRed = Color(cs_object=CSColor.IndianRed)
    Indigo = Color(cs_object=CSColor.Indigo)
    Ivory = Color(cs_object=CSColor.Ivory)
    Khaki = Color(cs_object=CSColor.Khaki)
    Lavender = Color(cs_object=CSColor.Lavender)
    LavenderBlush = Color(cs_object=CSColor.LavenderBlush)
    LawnGreen = Color(cs_object=CSColor.LawnGreen)
    LemonChiffon = Color(cs_object=CSColor.LemonChiffon)
    LightBlue = Color(cs_object=CSColor.LightBlue)
    LightCoral = Color(cs_object=CSColor.LightCoral)
    LightCyan = Color(cs_object=CSColor.LightCyan)
    LightGoldenrodYellow = Color(cs_object=CSColor.LightGoldenrodYellow)
    LightGray = Color(cs_object=CSColor.LightGray)
    LightGreen = Color(cs_object=CSColor.LightGreen)
    LightPink = Color(cs_object=CSColor.LightPink)
    LightSalmon = Color(cs_object=CSColor.LightSalmon)
    LightSeaGreen = Color(cs_object=CSColor.LightSeaGreen)
    LightSkyBlue = Color(cs_object=CSColor.LightSkyBlue)
    LightSlateGray = Color(cs_object=CSColor.LightSlateGray)
    LightSteelBlue = Color(cs_object=CSColor.LightSteelBlue)
    LightYellow = Color(cs_object=CSColor.LightYellow)
    Lime = Color(cs_object=CSColor.Lime)
    LimeGreen = Color(cs_object=CSColor.LimeGreen)
    Linen = Color(cs_object=CSColor.Linen)
    Magenta = Color(cs_object=CSColor.Magenta)
    Maroon = Color(cs_object=CSColor.Maroon)
    MediumAquamarine = Color(cs_object=CSColor.MediumAquamarine)
    MediumBlue = Color(cs_object=CSColor.MediumBlue)
    MediumOrchid = Color(cs_object=CSColor.MediumOrchid)
    MediumPurple = Color(cs_object=CSColor.MediumPurple)
    MediumSeaGreen = Color(cs_object=CSColor.MediumSeaGreen)
    MediumSlateBlue = Color(cs_object=CSColor.MediumSlateBlue)
    MediumSpringGreen = Color(cs_object=CSColor.MediumSpringGreen)
    MediumTurquoise = Color(cs_object=CSColor.MediumTurquoise)
    MediumVioletRed = Color(cs_object=CSColor.MediumVioletRed)
    MemberwiseClone = Color(cs_object=CSColor.MemberwiseClone)
    MidnightBlue = Color(cs_object=CSColor.MidnightBlue)
    MintCream = Color(cs_object=CSColor.MintCream)
    MistyRose = Color(cs_object=CSColor.MistyRose)
    Moccasin = Color(cs_object=CSColor.Moccasin)
    NavajoWhite = Color(cs_object=CSColor.NavajoWhite)
    Navy = Color(cs_object=CSColor.Navy)
    OldLace = Color(cs_object=CSColor.OldLace)
    Olive = Color(cs_object=CSColor.Olive)
    OliveDrab = Color(cs_object=CSColor.OliveDrab)
    Orange = Color(cs_object=CSColor.Orange)
    OrangeRed = Color(cs_object=CSColor.OrangeRed)
    Orchid = Color(cs_object=CSColor.Orchid)
    Overloads = Color(cs_object=CSColor.Overloads)
    PaleGoldenrod = Color(cs_object=CSColor.PaleGoldenrod)
    PaleGreen = Color(cs_object=CSColor.PaleGreen)
    PaleTurquoise = Color(cs_object=CSColor.PaleTurquoise)
    PaleVioletRed = Color(cs_object=CSColor.PaleVioletRed)
    PapayaWhip = Color(cs_object=CSColor.PapayaWhip)
    PeachPuff = Color(cs_object=CSColor.PeachPuff)
    Peru = Color(cs_object=CSColor.Peru)
    Pink = Color(cs_object=CSColor.Pink)
    Plum = Color(cs_object=CSColor.Plum)
    PowderBlue = Color(cs_object=CSColor.PowderBlue)
    Purple = Color(cs_object=CSColor.Purple)
    Red = Color(cs_object=CSColor.Red)
    RosyBrown = Color(cs_object=CSColor.RosyBrown)
    RoyalBlue = Color(cs_object=CSColor.RoyalBlue)
    SaddleBrown = Color(cs_object=CSColor.SaddleBrown)
    Salmon = Color(cs_object=CSColor.Salmon)
    SandyBrown = Color(cs_object=CSColor.SandyBrown)
    SeaGreen = Color(cs_object=CSColor.SeaGreen)
    SeaShell = Color(cs_object=CSColor.SeaShell)
    Sienna = Color(cs_object=CSColor.Sienna)
    Silver = Color(cs_object=CSColor.Silver)
    SkyBlue = Color(cs_object=CSColor.SkyBlue)
    SlateBlue = Color(cs_object=CSColor.SlateBlue)
    SlateGray = Color(cs_object=CSColor.SlateGray)
    Snow = Color(cs_object=CSColor.Snow)
    SpringGreen = Color(cs_object=CSColor.SpringGreen)
    SteelBlue = Color(cs_object=CSColor.SteelBlue)
    Tan = Color(cs_object=CSColor.Tan)
    Teal = Color(cs_object=CSColor.Teal)
    Thistle = Color(cs_object=CSColor.Thistle)
    Tomato = Color(cs_object=CSColor.Tomato)
    Transparent = Color(cs_object=CSColor.Transparent)
    Turquoise = Color(cs_object=CSColor.Turquoise)
    Violet = Color(cs_object=CSColor.Violet)
    Wheat = Color(cs_object=CSColor.Wheat)
    White = Color(cs_object=CSColor.White)
    WhiteSmoke = Color(cs_object=CSColor.WhiteSmoke)
    Yellow = Color(cs_object=CSColor.Yellow)
    YellowGreen = Color(cs_object=CSColor.YellowGreen)
