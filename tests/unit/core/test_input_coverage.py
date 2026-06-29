"""Unit tests closing coverage gaps in :mod:`flaui.core.input`.

The C# input back-ends (``CSKeyboard`` / ``CSMouse`` / ``CSTouch`` / ``CSWait``) are patched with
``MagicMock`` so these tests verify the Python wrappers forward the correct arguments without
generating real input. The focus is the thin delegating methods (scan-code/virtual-key variants,
Touch, the position descriptor, and the ``Wait`` helpers) that the live UI matrix does not exercise.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from flaui.core import input as input_module
from flaui.core.input import Interpolation, Keyboard, Mouse, MouseButton, Touch, Wait
from flaui.core.windows_api import VirtualKeyShort
from flaui.lib.system.drawing import Point


@pytest.fixture
def cs_keyboard(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch the C# Keyboard back-end with a mock and return it."""
    fake = MagicMock()
    monkeypatch.setattr(input_module, "CSKeyboard", fake)
    return fake


@pytest.fixture
def cs_mouse(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch the C# Mouse back-end with a mock and return it."""
    fake = MagicMock()
    monkeypatch.setattr(input_module, "CSMouse", fake)
    return fake


@pytest.fixture
def cs_touch(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch the C# Touch back-end with a mock and return it."""
    fake = MagicMock()
    monkeypatch.setattr(input_module, "CSTouch", fake)
    return fake


def _point(x: int = 1, y: int = 2) -> Point:
    """Build a Python ``Point`` backed by a real ``System.Drawing.Point``."""
    return Point(raw_value=(x, y))


# --------------------------------------------------------------------------- #
# Keyboard
# --------------------------------------------------------------------------- #
def test_keyboard_type_key(cs_keyboard: MagicMock) -> None:
    """``type_key`` types a single virtual key value."""
    key = list(VirtualKeyShort)[0]
    Keyboard.type_key(key)
    cs_keyboard.Type.assert_called_once_with(key.value)


def test_keyboard_type_simultaneously(cs_keyboard: MagicMock) -> None:
    """``type_simultaneously`` forwards the raw values of each key."""
    keys = list(VirtualKeyShort)[:2]
    Keyboard.type_simultaneously(keys)
    cs_keyboard.TypeSimultaneously.assert_called_once_with([k.value for k in keys])


def test_keyboard_scan_and_virtual_code_variants(cs_keyboard: MagicMock) -> None:
    """Scan-code / virtual-key-code press/release/type variants all delegate."""
    Keyboard.type_scan_code(10, True)
    Keyboard.type_virtual_key_code(20)
    Keyboard.press_scan_code(11, False)
    Keyboard.press_virtual_key_code(21)
    Keyboard.release_scan_code(12, True)
    Keyboard.release_virtual_key_code(22)

    cs_keyboard.TypeScanCode.assert_called_once_with(10, True)
    cs_keyboard.TypeVirtualKeyCode.assert_called_once_with(20)
    cs_keyboard.PressScanCode.assert_called_once_with(11, False)
    cs_keyboard.PressVirtualKeyCode.assert_called_once_with(21)
    cs_keyboard.ReleaseScanCode.assert_called_once_with(12, True)
    cs_keyboard.ReleaseVirtualKeyCode.assert_called_once_with(22)


def test_keyboard_press_release_pressing(cs_keyboard: MagicMock) -> None:
    """``press`` / ``release`` use a single value; ``pressing`` uses a value list."""
    key = list(VirtualKeyShort)[0]
    Keyboard.press(key)
    Keyboard.release(key)
    Keyboard.pressing([key])
    cs_keyboard.Press.assert_called_once_with(key.value)
    cs_keyboard.Release.assert_called_once_with(key.value)
    cs_keyboard.Pressing.assert_called_once_with([key.value])


# --------------------------------------------------------------------------- #
# Mouse
# --------------------------------------------------------------------------- #
def test_mouse_are_buttons_swapped(cs_mouse: MagicMock) -> None:
    """``are_buttons_swapped`` returns the C# flag."""
    cs_mouse.AreButtonsSwapped = True
    assert Mouse.are_buttons_swapped() is True


def test_mouse_move_by_and_move_to(cs_mouse: MagicMock) -> None:
    """``move_by`` and the coordinate / point ``move_to`` branches delegate correctly."""
    Mouse.move_by(5, 6)
    cs_mouse.MoveBy.assert_called_once_with(5, 6)

    Mouse.move_to(new_x=10, new_y=20)
    cs_mouse.MoveTo.assert_called_with(10, 20)

    point = _point()
    Mouse.move_to(new_position=point)
    cs_mouse.MoveTo.assert_called_with(point.raw_value)


def test_mouse_click_variants_with_point(cs_mouse: MagicMock) -> None:
    """Click / double-click with a point forward the point and button value."""
    point = _point()
    Mouse.click(point=point, mouse_button=MouseButton.Right)
    cs_mouse.Click.assert_called_once_with(point.raw_value, MouseButton.Right.value)

    Mouse.double_click(point=point)
    cs_mouse.DoubleClick.assert_called_once_with(point.raw_value, MouseButton.Left.value)


def test_mouse_button_down_up_scroll(cs_mouse: MagicMock) -> None:
    """``down`` / ``up`` / ``scroll`` / ``horizontal_scroll`` delegate."""
    Mouse.down(MouseButton.Middle)
    Mouse.up(MouseButton.Middle)
    Mouse.scroll(3)
    Mouse.horizontal_scroll(-2)
    cs_mouse.Down.assert_called_once_with(MouseButton.Middle.value)
    cs_mouse.Up.assert_called_once_with(MouseButton.Middle.value)
    cs_mouse.Scroll.assert_called_once_with(3)
    cs_mouse.HorizontalScroll.assert_called_once_with(-2)


def test_mouse_drag_variants(cs_mouse: MagicMock) -> None:
    """Directional drags and both point/distance ``drag`` forms delegate; bad args raise."""
    start = _point()
    Mouse.drag_horizontally(start, 40)
    cs_mouse.DragHorizontally.assert_called_once_with(start.raw_value, 40, MouseButton.Left.value)

    Mouse.drag_vertically(start, 30)
    cs_mouse.DragVertically.assert_called_once_with(start.raw_value, 30, MouseButton.Left.value)

    end = _point(9, 9)
    Mouse.drag(start, ending_point=end)
    cs_mouse.Drag.assert_called_with(start.raw_value, end.raw_value, MouseButton.Left.value)

    Mouse.drag(start, distance_x=5, distance_y=7)
    cs_mouse.Drag.assert_called_with(start.raw_value, 5, 7, MouseButton.Left.value)

    with pytest.raises(ValueError):
        Mouse.drag(start)


def test_mouse_explicit_click_helpers(cs_mouse: MagicMock) -> None:
    """left/right (double) click helpers cover both the point and no-point branches."""
    point = _point()
    Mouse.left_click(None)
    Mouse.left_click(point)
    Mouse.left_double_click(None)
    Mouse.left_double_click(point)
    Mouse.right_click(None)
    Mouse.right_click(point)
    Mouse.right_double_click(None)
    Mouse.right_double_click(point)

    cs_mouse.LeftClick.assert_any_call()
    cs_mouse.LeftClick.assert_any_call(point.raw_value)
    cs_mouse.LeftDoubleClick.assert_any_call()
    cs_mouse.LeftDoubleClick.assert_any_call(point.raw_value)
    cs_mouse.RightClick.assert_any_call()
    cs_mouse.RightClick.assert_any_call(point.raw_value)
    cs_mouse.RightDoubleClick.assert_any_call()
    cs_mouse.RightDoubleClick.assert_any_call(point.raw_value)


def test_mouse_position_descriptor(monkeypatch: pytest.MonkeyPatch) -> None:
    """The position descriptor reads a Point from, and writes a raw value to, the backend."""
    from types import SimpleNamespace

    fake = MagicMock()
    fake.Position = SimpleNamespace(X=10, Y=20)
    monkeypatch.setattr(input_module, "CSMouse", fake)

    pos = Mouse.position
    assert (pos.x, pos.y) == (10, 20)

    # Assign through an instance so the descriptor's __set__ fires (assigning on the
    # class itself would replace the descriptor instead of invoking it).
    target = _point(3, 4)
    Mouse().position = target
    assert (fake.Position.X, fake.Position.Y) == (3, 4)


# --------------------------------------------------------------------------- #
# Touch
# --------------------------------------------------------------------------- #
def test_touch_tap_variants(cs_touch: MagicMock) -> None:
    """``tap`` covers both the no-point and explicit-points branches."""
    Touch.tap()
    cs_touch.Tap.assert_called_with()
    pts = [_point(), _point(5, 6)]
    Touch.tap(pts)
    cs_touch.Tap.assert_called_with([p.raw_value for p in pts])


def test_touch_hold_with_and_without_points(cs_touch: MagicMock) -> None:
    """``hold`` forwards ``None`` for the points when none are supplied."""
    Touch.hold(500)
    args = cs_touch.Hold.call_args[0]
    assert args[1] is None
    Touch.hold(500, [_point()])
    assert cs_touch.Hold.call_args[0][1] is not None


def test_touch_pinch_transition_drag_rotate(cs_touch: MagicMock) -> None:
    """The remaining gesture wrappers delegate to their C# counterparts."""
    center = _point()
    Touch.pinch(center, 10, 20, 1000, angle=30)
    Touch.transition(1000, (_point(), _point(3, 3)))
    Touch.drag(1000, _point(), _point(4, 4))
    Touch.rotate(center, 50, 0, 90, 1000)
    cs_touch.Pinch.assert_called_once()
    cs_touch.Transition.assert_called_once()
    cs_touch.Drag.assert_called_once()
    cs_touch.Rotate.assert_called_once()


# --------------------------------------------------------------------------- #
# Wait
# --------------------------------------------------------------------------- #
def test_wait_until_responsive_variants(monkeypatch: pytest.MonkeyPatch) -> None:
    """``until_responsive`` / ``until_responsive_hwnd`` forward defaults to the C# Wait."""
    fake = MagicMock()
    fake.UntilResponsive.return_value = True
    fake.UntilResponsiveHwnd.return_value = False
    monkeypatch.setattr(input_module, "CSWait", fake)

    element = MagicMock()
    assert Wait.until_responsive(element) is True
    fake.UntilResponsive.assert_called_once_with(element, Wait.DEFAULT_TIMEOUT)

    assert Wait.until_responsive_hwnd(123) is False
    fake.UntilResponsiveHwnd.assert_called_once_with(123, Wait.DEFAULT_TIMEOUT)


def test_wait_until_input_is_processed_sleeps(monkeypatch: pytest.MonkeyPatch) -> None:
    """``until_input_is_processed`` defaults to a 100ms sleep, overridable by argument."""
    recorded: list[float] = []
    monkeypatch.setattr(input_module.time, "sleep", lambda t: recorded.append(t))
    Wait.until_input_is_processed()
    Wait.until_input_is_processed(0.25)
    assert recorded == [0.1, 0.25]


def test_while_cursor_is_busy_returns_true_when_idle(monkeypatch: pytest.MonkeyPatch) -> None:
    """When the cursor never reports busy, the wait returns ``True`` immediately."""
    # On hosts without a readable cursor the helper short-circuits to True; on a normal
    # desktop the cursor is idle, so either way a healthy environment returns True quickly.
    assert Wait.while_cursor_is_busy(timeout_in_secs=0.5, poll_interval_secs=0.01) is True


def test_apply_post_wait_truthy_non_numeric_uses_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """A truthy, non-callable, non-numeric post_wait falls through to the default wait.

    Note ``True`` itself is an ``int`` subclass, so it is handled by the numeric branch;
    only a value like a non-empty container/sentinel reaches the final default branch.
    """
    recorded: list[object] = []
    monkeypatch.setattr(Wait, "until_input_is_processed", lambda *a: recorded.append(a))
    Mouse._apply_post_wait(object())
    assert recorded == [()]


# --------------------------------------------------------------------------- #
# Interpolation
#
# These run real (sub-second) interpolations: the C# back-end calls back into the
# Python action wrapper on each step, exercising the C#<->Python point conversion. The
# UI matrix never interpolates, so this is the only place these wrappers are covered.
# --------------------------------------------------------------------------- #
def test_interpolation_execute_single_fires_action() -> None:
    """``execute_single`` invokes the action with Python ``Point`` objects per step."""
    received: list[Point] = []
    Interpolation.execute_single(received.append, _point(0, 0), _point(4, 4), duration_ms=30, interval_ms=5)
    assert received  # at least one step fired
    assert all(isinstance(p, Point) for p in received)


def test_interpolation_execute_multi_fires_action() -> None:
    """``execute`` invokes the action with a list of Python ``Point`` objects per step."""
    received: list[list[Point]] = []
    Interpolation.execute(
        received.append,
        [(_point(0, 0), _point(4, 4))],
        duration_ms=30,
        interval_ms=5,
    )
    assert received
    assert all(isinstance(p, Point) for step in received for p in step)


def test_interpolation_execute_rotation_fires_action() -> None:
    """``execute_rotation`` invokes the action with Python ``Point`` objects per step."""
    received: list[Point] = []
    Interpolation.execute_rotation(
        received.append,
        center_point=_point(50, 50),
        radius=10.0,
        start_angle=0.0,
        end_angle=1.5,
        duration_ms=30,
        interval_ms=5,
    )
    assert received
    assert all(isinstance(p, Point) for p in received)
