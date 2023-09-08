"""This module contains constants for the WPF application element map."""

from enum import IntEnum


class ApplicationTabIndex(IntEnum):
    """This class is used to store the tab index for the WPF application."""
    SIMPLE_CONTROLS = 0
    COMPLEX_CONTROLS = 1
    MORE_CONTROLS = 2
