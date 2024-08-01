"""This module acts as a wrapper for classes listed in FlaUI.Core.Input namespace. It provides methods to interact with the keyboard and mouse."""

from enum import Enum
import time
from typing import Any, List, Optional, Tuple, Union

from FlaUI.Core.Input import (  # pyright: ignore
    Keyboard as CSKeyboard,
    Mouse as CSMouse,
    MouseButton as CSMouseButton,
    Touch as CSTouch,
    Wait as CSWait,
)

from flaui.core.automation_elements import AutomationElement
from flaui.core.windows_api import VirtualKeyShort
from flaui.lib.collections import TypeCast
from flaui.lib.system.drawing import Point


class Wait:
    """Various helper tools used in various places, wrapper over Wait class in FlaUI.Core.Input namespace"""

    DEFAULT_TIMEOUT = 1  # in seconds

    @staticmethod
    def until_input_is_processed(wait_timeout_in_secs: Optional[float] = None):
        """
        Waits a little to allow inputs (mouse, keyboard, ...) to be processed.

        :param wait_timeout_in_secs: An optional timeout. If no value or None is passed, the timeout is 100ms.
        """
        wait_time = wait_timeout_in_secs if wait_timeout_in_secs is not None else 0.1  # default to 100ms
        time.sleep(wait_time)

    @staticmethod
    def until_responsive(automation_element: AutomationElement, timeout_in_secs: Optional[float] = None):
        """
        Waits until the given element is responsive.

        :param automation_element: The element that should be waited for.
        :param timeout_in_secs: The timeout of the waiting.
        :return: True if the element was responsive, false otherwise.
        """
        return CSWait.UntilResponsive(
            automation_element, timeout_in_secs if timeout_in_secs is not None else Wait.DEFAULT_TIMEOUT
        )

    @staticmethod
    def until_responsive_hwnd(hWnd: Any, timeout: Optional[float] = None):
        """
        Waits until the given hwnd is responsive.

        :param hWnd: The hwnd that should be waited for.
        :param timeout: The timeout of the waiting.
        :return: True if the hwnd was responsive, false otherwise.
        """
        return CSWait.UntilResponsiveHwnd(hWnd, timeout if timeout is not None else Wait.DEFAULT_TIMEOUT)


class Keyboard:
    """Simulates Key input, wrapper over Keyboard class in FlaUI.Core.Input namespace"""

    @staticmethod
    def type(text: Union[str, List[VirtualKeyShort]]) -> None:
        """Types the given character.

        :param text: Text/Charecters/VirtualKeyShort key to enter
        """
        CSKeyboard.Type(text if isinstance(text, str) else [_.value for _ in text])

    @staticmethod
    def type_simultaneously(text: List[VirtualKeyShort]) -> None:
        """Types the given keys simultaneously (starting with the first).

        :param text: VirtualKeyShort key to enter
        """
        CSKeyboard.TypeSimultaneously([_.value for _ in text])

    @staticmethod
    def type_scan_code(scan_code: int, is_extended_key: bool) -> None:
        """Types the given scan-code.

        :param scan_code: Scan code
        :param is_extended_key: Is Extended Key
        """
        CSKeyboard.TypeScanCode(scan_code, is_extended_key)

    @staticmethod
    def type_virtual_key_code(virtual_keycode: int) -> None:
        """Types the given virtual key-code.

        :param virtual_keycode: Virtual key-code
        """
        CSKeyboard.TypeVirtualKeyCode(virtual_keycode)

    @staticmethod
    def press(virtual_key: VirtualKeyShort) -> None:
        """Presses the given key.

        :param virtual_key: Virtual key
        """
        CSKeyboard.Press(virtual_key.value)

    @staticmethod
    def press_scan_code(scan_code: int, is_extended_key: bool) -> None:
        """Presses the given scan-code.

        :param scan_code: Scan code
        :param is_extended_key: Is Extended Key
        """
        CSKeyboard.PressScanCode(scan_code, is_extended_key)

    @staticmethod
    def press_virtual_key_code(virtual_keycode: int) -> None:
        """Presses the given virtual key-code.

        :param virtual_keycode: Virtual key-code
        """
        CSKeyboard.PressVirtualKeyCode(virtual_keycode)

    @staticmethod
    def release(virtual_key: VirtualKeyShort) -> None:
        """Releases the given key

        :param virtual_key: Virtual Key
        """
        CSKeyboard.Release(virtual_key.value)

    @staticmethod
    def release_scan_code(scan_code: int, is_extended_key: bool) -> None:
        """Releases the given scan-code.

        :param scan_code: Scan code
        :param is_extended_key: Is Extended Key
        """
        CSKeyboard.ReleaseScanCode(scan_code, is_extended_key)

    @staticmethod
    def release_virtual_key_code(virtual_keycode: int) -> None:
        """Releases the given virtual key-code.

        :param virtual_keycode: Virtual key-code
        """
        CSKeyboard.ReleaseVirtualKeyCode(virtual_keycode)

    @staticmethod
    def pressing(virtual_keys: List[VirtualKeyShort]) -> None:
        """Presses the given keys and releases them when the returned object is disposed.

        :param virtual_keys: Virtual keys to enter
        """
        CSKeyboard.Pressing([_.value for _ in virtual_keys])


class MouseButton(Enum):
    """Wrapper for MouseButton class in FlaUI.Core.Input C# namespace"""

    Left = CSMouseButton.Left  # The left mouse button
    Middle = CSMouseButton.Middle  # The middle mouse button
    Right = CSMouseButton.Right  # The right mouse button
    XButton1 = CSMouseButton.XButton1  # The fourth mouse button
    XButton2 = CSMouseButton.XButton2  # The fifth mouse button


class Mouse:
    """Mouse class to simulate mouse input, wrapper over Mouse class in FlaUI.Core.Input namespace"""

    position: Point = Point(raw_value=CSMouse.Position)  # The current position of the mouse cursor
    are_buttons_swapped: bool = CSMouse.AreButtonsSwapped  # Flag to indicate if the buttons are swapped (left-handed).

    @staticmethod
    def move_by(delta_x: int, delta_y: int) -> None:
        """Moves the mouse by a given delta from the current position.

        :param delta_x: The delta for the x-axis
        :param delta_y: The delta for y-axis
        """
        CSMouse.MoveBy(delta_x, delta_y)

    @staticmethod
    def move_to(new_x: Optional[int] = None, new_y: Optional[int] = None, new_position: Optional[Point] = None) -> None:
        """Moves the mouse to a new position.

        :param new_x: The new position on x-axis
        :param new_y: The new position on y-axis
        :param new_position: The new position for the mouse.
        """
        if (new_x is not None and new_y is not None) or new_position is not None:
            CSMouse.MoveTo(new_position.raw_value) if new_position is not None else CSMouse.MoveTo(new_x, new_y)
        else:
            raise ValueError(
                "`new_x, new_y or new_position argument needs to be sent for the Mouse to move to a new position`"
            )

    @staticmethod
    def click(point: Optional[Point] = None, mouse_button: MouseButton = MouseButton.Left) -> None:
        """Clicks the specified mouse button at the current location.

        :param point:The position to move to before clicking.
        :param mouse_button: The mouse button to click. Defaults to the left button, defaults to MouseButton.Left
        """
        CSMouse.Click(mouse_button.value) if point is None else CSMouse.Click(point.raw_value, mouse_button.value)

    @staticmethod
    def double_click(point: Optional[Point] = None, mouse_button: MouseButton = MouseButton.Left) -> None:
        """Double-Clicks the specified mouse button at the current location.

        :param point:The position to move to before clicking.
        :param mouse_button: The mouse button to click. Defaults to the left button, defaults to MouseButton.Left
        """
        CSMouse.DoubleClick(mouse_button.value) if point is None else CSMouse.Click(point.raw_value, mouse_button.value)

    @staticmethod
    def down(mouse_button: MouseButton = MouseButton.Left) -> None:
        """Sends a mouse down command for the specified mouse button.

        :param mouse_button: The mouse button to press, defaults to MouseButton.Left
        """
        CSMouse.Down(mouse_button.value)

    @staticmethod
    def up(mouse_button: MouseButton = MouseButton.Left) -> None:
        """Sends a mouse up command for the specified mouse button.

        :param mouse_button: The mouse button to press, defaults to MouseButton.Left
        """
        CSMouse.Up(mouse_button.value)

    @staticmethod
    def scroll(lines: int) -> None:
        """Simulates scrolling of the mouse wheel up or down.

        :param lines: Lines to scroll
        """
        CSMouse.Scroll(lines)

    @staticmethod
    def horizontal_scroll(lines: int) -> None:
        """Simulates horizontal scrolling of the mouse wheel left or right.

        :param lines: Lines to scroll horizontally
        """
        CSMouse.HorizontalScroll(lines)

    @staticmethod
    def drag_horizontally(starting_point: Point, distance: int, mouse_button: MouseButton = MouseButton.Left) -> None:
        """Drags the mouse horizontally.

        :param starting_point: Starting point of the drag
        :param distance: The distance to drag, + for right, - for left
        :param mouse_button: The mouse button to use for dragging, defaults to MouseButton.Left
        """
        CSMouse.DragHorizontally(starting_point.raw_value, distance, mouse_button.value)

    @staticmethod
    def drag_vertically(starting_point: Point, distance: int, mouse_button: MouseButton = MouseButton.Left) -> None:
        """Drags the mouse vertically.

        :param starting_point: Starting point of the drag
        :param distance: The distance to drag, + for right, - for left
        :param mouse_button: The mouse button to use for dragging, defaults to MouseButton.Left
        """
        CSMouse.DragVertically(starting_point.raw_value, distance, mouse_button.value)

    @staticmethod
    def drag(
        starting_point: Point,
        distance_x: Optional[int] = None,
        distance_y: Optional[int] = None,
        ending_point: Optional[Point] = None,
        mouse_button: MouseButton = MouseButton.Left,
    ) -> None:
        """Drags the mouse vertically.

        :param starting_point: Starting point of the drag
        :param distance_x: The x distance to drag, + for right, - for left
        :param distance_y: The y distance to drag, + for right, - for left
        :param ending_point: Ending point of the drag
        :param mouse_button: The mouse button to use for dragging, defaults to MouseButton.Left
        """
        if (distance_x is not None and distance_y is not None) or ending_point is not None:
            CSMouse.DragVertically(
                starting_point.raw_value, distance_x, distance_y, mouse_button.value
            ) if ending_point is None else CSMouse.DragVertically(
                starting_point.raw_value, ending_point.raw_value, mouse_button.value
            )
        else:
            raise ValueError(
                "`distance_x and distance_y or ending_point has to be sent to the arguments to drag the mouse."
            )

    @staticmethod
    def left_click(point: Optional[Point]) -> None:
        """Performs a left click.

        :param: point: The position to move before clicking.
        """
        CSMouse.LeftClick() if point is None else CSMouse.LeftClick(point.raw_value)

    @staticmethod
    def left_double_click(point: Optional[Point]) -> None:
        """Performs a left double click.

        :param: point: The position to move before clicking.
        """
        CSMouse.LeftDoubleClick() if point is None else CSMouse.LeftDoubleClick(point.raw_value)

    @staticmethod
    def right_click(point: Optional[Point]) -> None:
        """Performs a right click.

        :param: point: The position to move before clicking.
        """
        CSMouse.RightClick() if point is None else CSMouse.RightClick(point.raw_value)

    @staticmethod
    def right_double_click(point: Optional[Point]) -> None:
        """Performs a right double click.

        :param: point: The position to move before clicking.
        """
        CSMouse.RightDoubleClick() if point is None else CSMouse.RightDoubleClick(point.raw_value)


class Touch:
    """Touch class to simulate touch input, wrapper over Touch class in FlaUI.Core.Input namespace"""

    @staticmethod
    def tap(points: Optional[List[Point]] = None) -> None:
        """Performs a tap on the given point or points.

        :param points: Point to touch, defaults to None
        """
        CSTouch.Tap() if points is None else CSTouch.Tap([_.raw_value for _ in points])

    @staticmethod
    def hold(duration: int, points: Optional[List[Point]] = None) -> None:
        """Performs a hold on the given point or points.

        :param duration: The duration of the hold in milliseconds
        :param points: Point to touch, defaults to None
        """
        CSTouch.Hold(TypeCast.cs_timespan(duration), [_.raw_value for _ in points] if points else None)

    @staticmethod
    def pinch(center: Point, start_radius: int, end_radius: int, duration: int, angle: int = 45) -> None:
        """Performs a pinch with two fingers.

        :param center: The center point of the pinch.
        :param start_radius: The starting radius.
        :param end_radius: The end radius.
        :param duration: The duration of the action.
        :param angle: The angle of the two points, relative to the x-axis, defaults to 45
        """
        CSTouch.Pinch(center.raw_value, start_radius, end_radius, TypeCast.cs_timespan(duration), angle)

    @staticmethod
    def transition(duration: int, start_end_points: Tuple[Point, Point]) -> None:
        """Transitions all the points from the start point to the end points.

        :param duration: The duration for the action.
        :param start_end_points: The list of start/end point tuples.
        """
        CSTouch.Transition(TypeCast.cs_timespan(duration), [_.raw_value for _ in start_end_points])

    @staticmethod
    def drag(duration: int, start_point: Point, end_point: Point) -> None:
        """Performs a touch-drag from the start point to the end point.

        :param duration: The duration of the action.
        :param start_point: The starting point of the drag.
        :param end_point: The end point of the drag.
        """
        CSTouch.Drag(TypeCast.cs_timespan(duration), start_point.raw_value, end_point.raw_value)

    @staticmethod
    def rotate(center: Point, radius: int, start_angle: int, end_angle: int, duration: int) -> None:
        """Performs a 2-finger rotation around the given point where the first finger is at the center and the second is rotated around.

        :param center: The center point of the rotation.
        :param radius: The radius of the rotation.
        :param start_angle: The starting angle (in rad).
        :param end_angle: The ending angle (in rad).
        :param duration: The total duration for the transition.
        """
        CSTouch.Rotate(center.raw_value, radius, start_angle, end_angle, TypeCast.cs_timespan(duration))
