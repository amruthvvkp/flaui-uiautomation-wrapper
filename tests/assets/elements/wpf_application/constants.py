"""This module contains constants for the WPF application element map."""

from enum import IntEnum

from FlaUI.Core.Input import VirtualKeyShort as CSVirtualKeyShort  # pyright: ignore

class ApplicationTabIndex(IntEnum):
    """This class is used to store the tab index for the WPF application."""
    SIMPLE_CONTROLS = 0
    COMPLEX_CONTROLS = 1
    MORE_CONTROLS = 2

class VirtualKey:
    """Wrapper class for FlaUI.Core.Input.VirtualKeyShort enum"""

    def __init__(self):
        self._enum = CSVirtualKeyShort

    def __getattr__(self, name):
        if name in dir(self._enum):
            return getattr(self._enum, name)
        else:
            raise AttributeError(f"No such virtual key: {name}")

    @classmethod
    def from_int(cls, value):
        """
        Converts an integer value to the corresponding VirtualKey enum member.

        Args:
            value (int): The integer value of the virtual key.

        Returns:
            VirtualKey: The corresponding VirtualKey enum member.

        Raises:
            ValueError: If the value doesn't correspond to any existing VirtualKey.
        """
        for name, member in cls._enum.__dict__.items():
            if isinstance(member, int) and member == value:
                return getattr(cls, name)
        raise ValueError(f"Invalid virtual key value: {value}")
