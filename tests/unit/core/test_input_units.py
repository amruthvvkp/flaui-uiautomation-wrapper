"""Unit tests for Keyboard/Mouse wrappers and the post-wait helper.

C# input back-ends (``CSKeyboard`` / ``CSMouse``) are patched out so these tests exercise the
Python wrapper logic without generating real keyboard/mouse events.
"""

from unittest.mock import MagicMock

import pytest

from flaui.core import input as input_module
from flaui.core.input import Keyboard, Mouse, MouseButton, Wait
from flaui.core.windows_api import VirtualKeyShort


def test_apply_post_wait_none_does_nothing() -> None:
    """A falsy post_wait performs no wait and raises nothing."""
    assert Mouse._apply_post_wait(None) is None


def test_apply_post_wait_invokes_callable() -> None:
    """A callable post_wait is invoked directly."""
    calls: list[bool] = []
    Mouse._apply_post_wait(lambda: calls.append(True))
    assert calls == [True]


def test_apply_post_wait_float_waits(monkeypatch: pytest.MonkeyPatch) -> None:
    """A numeric post_wait routes through Wait.until_input_is_processed."""
    recorded: dict[str, float] = {}
    monkeypatch.setattr(Wait, "until_input_is_processed", lambda t=None: recorded.update(t=t))
    Mouse._apply_post_wait(0.2)
    assert recorded["t"] == 0.2


def test_keyboard_type_string(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keyboard.type forwards a string straight to the C# backend."""
    fake = MagicMock()
    monkeypatch.setattr(input_module, "CSKeyboard", fake)
    Keyboard.type("abc")
    fake.Type.assert_called_once_with("abc")


def test_keyboard_type_virtual_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keyboard.type converts VirtualKeyShort members to their raw values."""
    fake = MagicMock()
    monkeypatch.setattr(input_module, "CSKeyboard", fake)
    key = list(VirtualKeyShort)[0]
    Keyboard.type([key])
    fake.Type.assert_called_once_with([key.value])


def test_mouse_click_without_point(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mouse.click with no point clicks at the current position."""
    fake = MagicMock()
    monkeypatch.setattr(input_module, "CSMouse", fake)
    Mouse.click()
    fake.Click.assert_called_once_with(MouseButton.Left.value)


def test_mouse_move_to_requires_coordinates() -> None:
    """Mouse.move_to raises ValueError when no destination is provided."""
    with pytest.raises(ValueError):
        Mouse.move_to()


def test_mouse_button_enum_has_values() -> None:
    """Each MouseButton member maps to a backing C# value."""
    assert all(member.value is not None for member in MouseButton)


@pytest.mark.parametrize(
    ("attribute", "cs_property"),
    [("move_pixels_per_millisecond", "MovePixelsPerMillisecond"), ("move_pixels_per_step", "MovePixelsPerStep")],
)
def test_mouse_speed_settings_reach_csharp(monkeypatch: pytest.MonkeyPatch, attribute: str, cs_property: str) -> None:
    """Assigning a mouse speed setting on the class writes the C# Mouse static property."""
    fake = MagicMock()
    setattr(fake, cs_property, 1.0)
    monkeypatch.setattr(input_module, "CSMouse", fake)

    setattr(Mouse, attribute, 3.5)

    assert getattr(fake, cs_property) == 3.5
    assert getattr(Mouse, attribute) == 3.5


def test_apply_post_wait_true_sleeps_100ms(monkeypatch: pytest.MonkeyPatch) -> None:
    """``post_wait=True`` waits the documented 100 ms, not 1 s (bool is an int subclass)."""
    sleeps: list[float] = []
    monkeypatch.setattr("flaui.core.input.time.sleep", sleeps.append)
    Mouse._apply_post_wait(True)
    assert sleeps == [0.1]


def test_apply_post_wait_float_sleeps_given_seconds(monkeypatch: pytest.MonkeyPatch) -> None:
    """A numeric post_wait sleeps for exactly that many seconds."""
    sleeps: list[float] = []
    monkeypatch.setattr("flaui.core.input.time.sleep", sleeps.append)
    Mouse._apply_post_wait(0.5)
    assert sleeps == [0.5]
