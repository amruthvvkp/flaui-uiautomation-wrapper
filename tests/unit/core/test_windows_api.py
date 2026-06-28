"""Unit tests covering the flaui.core.windows_api enum definitions."""

from enum import Enum
import inspect

from flaui.core import windows_api
from flaui.core.windows_api import VirtualKeyShort


def _module_enums() -> list[type]:
    """Return all Enum classes defined in the windows_api module."""
    return [
        obj
        for _, obj in inspect.getmembers(windows_api, inspect.isclass)
        if obj.__module__ == windows_api.__name__ and issubclass(obj, Enum)
    ]


def test_module_defines_enums() -> None:
    """The windows_api module defines a non-trivial set of enum classes."""
    enums = _module_enums()
    assert len(enums) > 10


def test_every_enum_has_members() -> None:
    """Every enum exported by windows_api has at least one member."""
    for enum_cls in _module_enums():
        assert list(enum_cls), f"{enum_cls.__name__} has no members"


def test_virtual_key_short_values_are_unique() -> None:
    """VirtualKeyShort members map to unique, hashable key codes."""
    values = [member.value for member in VirtualKeyShort]
    assert values, "VirtualKeyShort should expose members"
    assert len(set(values)) == len(values)
