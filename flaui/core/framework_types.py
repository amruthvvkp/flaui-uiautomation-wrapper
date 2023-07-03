from enum import Enum

from FlaUI.Core import FrameworkType as CSFrameworkType  # pyright: ignore


class FrameworkType(Enum):
    none = None
    Unknown = CSFrameworkType.Unknown
    Wpf = CSFrameworkType.Wpf
    WinForms = CSFrameworkType.WinForms
    Win32 = CSFrameworkType.Win32
    Xaml = CSFrameworkType.Xaml
    Qt = CSFrameworkType.Qt
