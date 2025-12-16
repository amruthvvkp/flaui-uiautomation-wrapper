"""This module acts as a wrapper for classes listed in FlaUI.Core.Input namespace. It provides methods to interact with the keyboard and mouse."""

from enum import Enum
import time
from typing import Any, Callable, List, Optional, Tuple, Union

from FlaUI.Core.Input import (  # pyright: ignore
    Interpolation as CSInterpolation,
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
    def type_key(virtual_key: VirtualKeyShort) -> None:
        """Types a single virtual key (press and release).

        :param virtual_key: VirtualKeyShort key to type
        """
        CSKeyboard.Type(virtual_key.value)

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


class _MousePositionDescriptor:
    """Descriptor to make Mouse.position work as a class-level property."""

    def __get__(self, obj, objtype=None) -> Point:
        """Get the current mouse position as a Point object."""
        pos = CSMouse.Position
        return Point(raw_value=(pos.X, pos.Y))

    def __set__(self, obj, value: Point) -> None:
        """Set the current mouse position from a Point object."""
        CSMouse.Position = value.raw_value


class Mouse:
    """Mouse class to simulate mouse input, wrapper over Mouse class in FlaUI.Core.Input namespace"""

    # The number of pixels the mouse is moved per millisecond (used to calculate duration)
    move_pixels_per_millisecond: float = 0.5
    # The number of pixels the mouse is moved per step (used to calculate interval)
    move_pixels_per_step: float = 10.0

    position = _MousePositionDescriptor()  # The current position of the mouse cursor

    @staticmethod
    def are_buttons_swapped() -> bool:
        """Flag to indicate if the buttons are swapped (left-handed)."""
        return CSMouse.AreButtonsSwapped

    @staticmethod
    def _apply_post_wait(post_wait: Optional[Union[bool, float, Callable[[], None]]]) -> None:
        """Applies post-wait logic after mouse operations."""
        if not post_wait:
            return
        if callable(post_wait):
            post_wait()
            return
        if isinstance(post_wait, (int, float)):
            Wait.until_input_is_processed(float(post_wait))
            return
        # post_wait is True
        Wait.until_input_is_processed()

    @staticmethod
    def move_by(
        delta_x: int,
        delta_y: int,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Moves the mouse by a given delta from the current position.

        :param delta_x: The delta for the x-axis
        :param delta_y: The delta for y-axis
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.MoveBy(delta_x, delta_y)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def move_to(
        new_x: Optional[int] = None,
        new_y: Optional[int] = None,
        new_position: Optional[Point] = None,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Moves the mouse to a new position.

        :param new_x: The new position on x-axis
        :param new_y: The new position on y-axis
        :param new_position: The new position for the mouse.
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        if (new_x is not None and new_y is not None) or new_position is not None:
            CSMouse.MoveTo(new_position.raw_value) if new_position is not None else CSMouse.MoveTo(new_x, new_y)
        else:
            raise ValueError(
                "`new_x, new_y or new_position argument needs to be sent for the Mouse to move to a new position`"
            )
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def click(
        point: Optional[Point] = None,
        mouse_button: MouseButton = MouseButton.Left,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Clicks the specified mouse button at the current location.

        :param point:The position to move to before clicking.
        :param mouse_button: The mouse button to click. Defaults to the left button, defaults to MouseButton.Left
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.Click(mouse_button.value) if point is None else CSMouse.Click(point.raw_value, mouse_button.value)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def double_click(
        point: Optional[Point] = None,
        mouse_button: MouseButton = MouseButton.Left,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Double-Clicks the specified mouse button at the current location.

        :param point:The position to move to before clicking.
        :param mouse_button: The mouse button to click. Defaults to the left button, defaults to MouseButton.Left
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.DoubleClick(mouse_button.value) if point is None else CSMouse.DoubleClick(
            point.raw_value, mouse_button.value
        )
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def down(
        mouse_button: MouseButton = MouseButton.Left,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Sends a mouse down command for the specified mouse button.

        :param mouse_button: The mouse button to press, defaults to MouseButton.Left
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.Down(mouse_button.value)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def up(
        mouse_button: MouseButton = MouseButton.Left,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Sends a mouse up command for the specified mouse button.

        :param mouse_button: The mouse button to press, defaults to MouseButton.Left
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.Up(mouse_button.value)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def scroll(lines: int, post_wait: Optional[Union[bool, float, Callable[[], None]]] = None) -> None:
        """Simulates scrolling of the mouse wheel up or down.

        :param lines: Lines to scroll
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.Scroll(lines)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def horizontal_scroll(lines: int, post_wait: Optional[Union[bool, float, Callable[[], None]]] = None) -> None:
        """Simulates horizontal scrolling of the mouse wheel left or right.

        :param lines: Lines to scroll horizontally
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.HorizontalScroll(lines)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def drag_horizontally(
        starting_point: Point,
        distance: int,
        mouse_button: MouseButton = MouseButton.Left,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Drags the mouse horizontally.

        :param starting_point: Starting point of the drag
        :param distance: The distance to drag, + for right, - for left
        :param mouse_button: The mouse button to use for dragging, defaults to MouseButton.Left
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.DragHorizontally(starting_point.raw_value, distance, mouse_button.value)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def drag_vertically(
        starting_point: Point,
        distance: int,
        mouse_button: MouseButton = MouseButton.Left,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Drags the mouse vertically.

        :param starting_point: Starting point of the drag
        :param distance: The distance to drag, + for right, - for left
        :param mouse_button: The mouse button to use for dragging, defaults to MouseButton.Left
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.DragVertically(starting_point.raw_value, distance, mouse_button.value)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def drag(
        starting_point: Point,
        ending_point: Optional[Point] = None,
        distance_x: Optional[int] = None,
        distance_y: Optional[int] = None,
        mouse_button: MouseButton = MouseButton.Left,
        post_wait: Optional[Union[bool, float, Callable[[], None]]] = None,
    ) -> None:
        """Drags the mouse from starting point to ending point or by distance.

        :param starting_point: Starting point of the drag
        :param ending_point: Ending point of the drag (if using point-to-point drag)
        :param distance_x: The x distance to drag, + for right, - for left
        :param distance_y: The y distance to drag, + for right, - for left
        :param mouse_button: The mouse button to use for dragging, defaults to MouseButton.Left
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        if ending_point is not None:
            CSMouse.Drag(starting_point.raw_value, ending_point.raw_value, mouse_button.value)
        elif distance_x is not None and distance_y is not None:
            CSMouse.Drag(starting_point.raw_value, distance_x, distance_y, mouse_button.value)
        else:
            raise ValueError("`ending_point or (distance_x and distance_y) must be provided to drag the mouse.")
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def left_click(point: Optional[Point], post_wait: Optional[Union[bool, float, Callable[[], None]]] = None) -> None:
        """Performs a left click.

        :param: point: The position to move before clicking.
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.LeftClick() if point is None else CSMouse.LeftClick(point.raw_value)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def left_double_click(
        point: Optional[Point], post_wait: Optional[Union[bool, float, Callable[[], None]]] = None
    ) -> None:
        """Performs a left double click.

        :param: point: The position to move before clicking.
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.LeftDoubleClick() if point is None else CSMouse.LeftDoubleClick(point.raw_value)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def right_click(point: Optional[Point], post_wait: Optional[Union[bool, float, Callable[[], None]]] = None) -> None:
        """Performs a right click.

        :param: point: The position to move before clicking.
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.RightClick() if point is None else CSMouse.RightClick(point.raw_value)
        Mouse._apply_post_wait(post_wait)

    @staticmethod
    def right_double_click(
        point: Optional[Point], post_wait: Optional[Union[bool, float, Callable[[], None]]] = None
    ) -> None:
        """Performs a right double click.

        :param: point: The position to move before clicking.
        :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
        """
        CSMouse.RightDoubleClick() if point is None else CSMouse.RightDoubleClick(point.raw_value)
        Mouse._apply_post_wait(post_wait)


class Interpolation:
    """Interpolation tool to transition points during a time frame, wrapper over Interpolation class in FlaUI.Core.Input namespace"""

    @staticmethod
    def execute(
        action: Any,
        start_end_points: List[Tuple[Point, Point]],
        duration_ms: int,
        interval_ms: int = 10,
        skip_initial_position: bool = False,
    ) -> None:
        """Transitions the given points from start to end in the given duration.

        :param action: The action (callable) to execute for each interval with Point[] argument
        :param start_end_points: A list of tuples with start/end points
        :param duration_ms: The total duration for the transition in milliseconds
        :param interval_ms: The interval of each step in milliseconds, defaults to 10
        :param skip_initial_position: Skip firing action for initial position, defaults to False
        """
        from System import (  # pyright: ignore
            Action as CSAction,  # pyright: ignore
            Array,
            Tuple as CSTuple,
        )
        from System.Drawing import Point as CSPoint  # pyright: ignore

        # Convert Python action to C# Action<Point[]>
        def cs_action_wrapper(points):
            """Wrapper to convert C# Point[] to Python Point list and call the Python action."""
            # Convert C# Point[] to Python Point list
            py_points = [Point(raw_value=p) for p in points]
            action(py_points)

        cs_action = CSAction[Array[CSPoint]](cs_action_wrapper)

        # Convert start/end points to C# Tuple<Point, Point>[]
        cs_tuples = [CSTuple.Create(p[0].raw_value, p[1].raw_value) for p in start_end_points]
        cs_array = Array[CSTuple[CSPoint, CSPoint]](cs_tuples)

        CSInterpolation.Execute(
            cs_action,
            cs_array,
            TypeCast.cs_timespan(duration_ms),
            TypeCast.cs_timespan(interval_ms),
            skip_initial_position,
        )

    @staticmethod
    def execute_single(
        action: Any,
        start_point: Point,
        end_point: Point,
        duration_ms: int,
        interval_ms: int = 10,
        skip_initial_position: bool = False,
    ) -> None:
        """Transitions a single point from start to end in the given duration.

        :param action: The action (callable) to execute for each interval with Point argument
        :param start_point: The starting point
        :param end_point: The end point
        :param duration_ms: The total duration for the transition in milliseconds
        :param interval_ms: The interval of each step in milliseconds, defaults to 10
        :param skip_initial_position: Skip firing action for initial position, defaults to False
        """
        from System import Action as CSAction  # pyright: ignore
        from System.Drawing import Point as CSPoint  # pyright: ignore

        # Convert Python action to C# Action<Point>
        def cs_action_wrapper(point):
            """Wrapper to convert C# Point to Python Point and call the Python action."""
            action(Point(raw_value=point))

        cs_action = CSAction[CSPoint](cs_action_wrapper)

        CSInterpolation.Execute(
            cs_action,
            start_point.raw_value,
            end_point.raw_value,
            TypeCast.cs_timespan(duration_ms),
            TypeCast.cs_timespan(interval_ms),
            skip_initial_position,
        )

    @staticmethod
    def execute_rotation(
        action: Any,
        center_point: Point,
        radius: float,
        start_angle: float,
        end_angle: float,
        duration_ms: int,
        interval_ms: int = 10,
        skip_initial_position: bool = False,
    ) -> None:
        """Performs a rotation transition around the given point.

        :param action: The action (callable) to execute for each interval with Point argument
        :param center_point: The center point of the rotation
        :param radius: The radius of the rotation
        :param start_angle: The starting angle (in radians)
        :param end_angle: The ending angle (in radians)
        :param duration_ms: The total duration for the transition in milliseconds
        :param interval_ms: The interval of each step in milliseconds, defaults to 10
        :param skip_initial_position: Skip firing action for initial position, defaults to False
        """
        from System import Action as CSAction  # pyright: ignore
        from System.Drawing import Point as CSPoint  # pyright: ignore

        # Convert Python action to C# Action<Point>
        def cs_action_wrapper(point):
            """Wrapper to convert C# Point to Python Point and call the Python action."""
            action(Point(raw_value=point))

        cs_action = CSAction[CSPoint](cs_action_wrapper)

        CSInterpolation.ExecuteRotation(
            cs_action,
            center_point.raw_value,
            radius,
            start_angle,
            end_angle,
            TypeCast.cs_timespan(duration_ms),
            TypeCast.cs_timespan(interval_ms),
            skip_initial_position,
        )


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
