"""Tests for mouse input functionality, ported from C# MouseTests.cs."""

import time

from flaui.core.application import Application
from flaui.core.definitions import ControlType
from flaui.core.input import Mouse, MouseButton
from flaui.lib.system.drawing import Point
from flaui.modules.automation import Automation
import pytest


class TestMouse:
    """Tests for mouse input operations."""

    def test_mouse_move(self) -> None:
        """Test mouse movement operations.

        Ported from MouseTests.cs::MoveTest
        """
        # Set mouse to origin
        Mouse.position = Point(raw_value=(0, 0))

        # Move mouse relative
        Mouse.move_by(800, 0, post_wait=True)
        Mouse.move_by(0, 400, post_wait=True)
        Mouse.move_by(-400, -200, post_wait=True)

    @pytest.mark.skipif(
        True,  # Skip by default as Paint UI varies by Windows version
        reason="MS Paint UI varies significantly by Windows version",
    )
    def test_mouse_click_and_drag(self, automation: Automation) -> None:
        """Test mouse clicking and dragging in MS Paint.

        Ported from MouseTests.cs::ClickTest
        """
        app = Application()
        app.launch("mspaint")
        try:
            window = app.get_main_window(automation)

            # Calculate mouse position in paint canvas
            bounds = window.bounding_rectangle
            mouse_x = bounds.left + 100
            mouse_y = bounds.top + 300

            # Draw a simple shape
            Mouse.position = Point(raw_value=(mouse_x, mouse_y))
            Mouse.down(MouseButton.Left)
            Mouse.move_by(100, 10)
            Mouse.move_by(10, 50)
            Mouse.up(MouseButton.Left)

            time.sleep(0.5)

            # Close window without saving
            window.close()
            time.sleep(0.5)

            # Handle "Don't Save" dialog
            try:
                dialog = window.find_first_child(window.condition_factory.by_control_type(ControlType.Window))
                if dialog is not None:
                    dont_save = dialog.find_first_child(dialog.condition_factory.by_name("Don't save"))
                    if dont_save is not None:
                        dont_save.click()
            except Exception:
                pass

        finally:
            try:
                app.close()
            except Exception:
                pass

    @pytest.mark.bug(
        "GH-91",
        "Mouse position reads can return 0,0 under runner; flaky in full-file execution",
        run=True,
    )
    def test_mouse_move_one_pixel(self) -> None:
        """Test moving mouse by exactly one pixel.

        Ported from MouseTests.cs::MoveOnePixelTest
        """
        start_position = Mouse.position

        # Move by 1 pixel in X direction
        Mouse.move_by(1, 0, post_wait=True)

        # Retry-read position briefly to avoid flakiness in CI
        for _ in range(20):
            new_position = Mouse.position
            if new_position.x == start_position.x + 1 and new_position.y == start_position.y:
                break
            time.sleep(0.05)
        new_position = Mouse.position
        assert new_position.x == start_position.x + 1, "Mouse should move 1 pixel in X"
        assert new_position.y == start_position.y, "Mouse Y should not change"

    @pytest.mark.bug(
        "GH-91",
        "Mouse move deltas intermittently not reflected under pytest capture; flaky in batch",
        run=True,
    )
    def test_mouse_move_zero(self) -> None:
        """Test moving mouse by zero in one direction.

        Ported from MouseTests.cs::MoveZeroTest
        """
        # Move by 0 in X direction
        start_position = Mouse.position
        Mouse.move_by(0, 10, post_wait=True)
        # Retry-read position briefly to avoid flakiness in CI
        for _ in range(20):
            new_position = Mouse.position
            if new_position.x == start_position.x and new_position.y == start_position.y + 10:
                break
            time.sleep(0.05)
        new_position = Mouse.position
        assert new_position.x == start_position.x, "Mouse X should not change"
        assert new_position.y == start_position.y + 10, "Mouse should move 10 pixels in Y"

        # Move by 0 in Y direction
        start_position = Mouse.position
        Mouse.move_by(10, 0, post_wait=True)
        for _ in range(20):
            new_position = Mouse.position
            if new_position.x == start_position.x + 10 and new_position.y == start_position.y:
                break
            time.sleep(0.05)
        new_position = Mouse.position
        assert new_position.x == start_position.x + 10, "Mouse should move 10 pixels in X"
        assert new_position.y == start_position.y, "Mouse Y should not change"

        # Move by 0 in both directions
        start_position = Mouse.position
        Mouse.move_by(0, 0, post_wait=True)
        for _ in range(20):
            new_position = Mouse.position
            if new_position.x == start_position.x and new_position.y == start_position.y:
                break
            time.sleep(0.05)
        new_position = Mouse.position
        assert new_position.x == start_position.x, "Mouse X should not change"
        assert new_position.y == start_position.y, "Mouse Y should not change"

    @pytest.mark.bug(
        "GH-91",
        "Mouse drag end position intermittently not updated under test runner; flaky in batch",
        run=True,
    )
    def test_mouse_drag(self) -> None:
        """Test mouse drag operation.

        Ported from MouseTests.cs::DragTest
        """
        start_pos = Point(raw_value=(500, 500))
        end_pos = Point(raw_value=(700, 700))

        Mouse.position = start_pos

        # Perform drag (requires both starting and ending points)
        Mouse.drag(start_pos, end_pos, post_wait=True)

        # Verify final position with a brief retry and small tolerance
        final_pos = Mouse.position
        for _ in range(20):
            if abs(final_pos.x - end_pos.x) <= 2 and abs(final_pos.y - end_pos.y) <= 2:
                break
            time.sleep(0.05)
            final_pos = Mouse.position
        assert abs(final_pos.x - end_pos.x) <= 2, f"Expected X={end_pos.x}, got {final_pos.x}"
        assert abs(final_pos.y - end_pos.y) <= 2, f"Expected Y={end_pos.y}, got {final_pos.y}"
