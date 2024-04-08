"""This module contains the enumeration of the framework types."""

from enum import Enum

from FlaUI.Core import FrameworkType as CSFrameworkType  # pyright: ignore


class FrameworkType(Enum):
    """Enums for handling the framework type."""

    none = None
    Unknown = CSFrameworkType.Unknown
    Wpf = CSFrameworkType.Wpf
    WinForms = CSFrameworkType.WinForms
    Win32 = CSFrameworkType.Win32
    Xaml = CSFrameworkType.Xaml
    Qt = CSFrameworkType.Qt
