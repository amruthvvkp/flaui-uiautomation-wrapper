"""Runnable recipes for the *Utilities* guide: the helpers ported from FlaUI C#.

Run it from the project root::

    uv run pytest examples/pytest/test_utilities.py -v

Covers waiting (``Wait``), keyboard and mouse input, the ``System.Drawing`` types, screenshots,
highlight overlays, and the small tools in ``flaui.core.tools``. The guide includes each recipe's
Python tab from this file via the ``# --8<-- [start:name]`` / ``# --8<-- [end:name]`` markers.
"""

from pathlib import Path
from typing import Generator

from flaui.core.automation_elements import Tab, Window
from flaui.core.condition_factory import ConditionFactory
from flaui.core.definitions import ControlType
from flaui.modules.automation import Automation
import pytest


@pytest.fixture
def window(main_window: Window) -> Window:
    """Alias the main window to the ``window`` name the recipes use."""
    return main_window


@pytest.fixture
def cf(condition_factory: ConditionFactory) -> ConditionFactory:
    """Alias the condition factory to the ``cf`` name the recipes use."""
    return condition_factory


@pytest.fixture
def complex_controls(window: Window, cf: ConditionFactory) -> Generator[Tab, None, None]:
    """Show the Complex Controls tab, then switch back to Simple Controls."""
    tab = window.find_first_descendant(cf.by_control_type(ControlType.Tab)).as_tab()
    tab.select_tab_item(1, post_wait=True)
    yield tab
    tab.select_tab_item(0, post_wait=True)


# ---------------------------------------------------------------------------------------------
# Waiting
# ---------------------------------------------------------------------------------------------


def test_wait(window: Window) -> None:
    """Wait for input to land, and for a window to accept input."""
    # --8<-- [start:wait]
    from flaui.core.input import Wait

    Wait.until_input_is_processed()  # let queued mouse/keyboard input settle
    Wait.until_responsive(window, timeout_in_secs=5)  # the window's UI thread accepts input
    busy_cleared = Wait.while_cursor_is_busy(timeout_in_secs=10)  # no spinning/hourglass cursor
    # --8<-- [end:wait]
    assert busy_cleared


# ---------------------------------------------------------------------------------------------
# Keyboard and mouse
# ---------------------------------------------------------------------------------------------


def test_keyboard_shortcut(window: Window, cf: ConditionFactory) -> None:
    """Hold a modifier with ``Keyboard.pressing`` to send a shortcut (Ctrl+A), then type."""
    text_box = window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
    text_box.text = "old text"
    # --8<-- [start:keyboard]
    from flaui.core.input import Keyboard, Wait
    from flaui.core.windows_api import VirtualKeyShort

    text_box.focus()
    with Keyboard.pressing([VirtualKeyShort.CONTROL]):  # held down inside the block...
        Keyboard.type_key(VirtualKeyShort.KEY_A)  # ...so this is Ctrl+A (select all)
    Keyboard.type("replaced")  # types over the selection
    Keyboard.type_key(VirtualKeyShort.TAB)  # single keys by name
    Wait.until_input_is_processed()
    # --8<-- [end:keyboard]
    assert text_box.text == "replaced"


def test_mouse(window: Window, cf: ConditionFactory) -> None:
    """Move the real cursor and click a point."""
    text_box = window.find_first_descendant(cf.by_automation_id("TextBox"))
    # --8<-- [start:mouse]
    from flaui.core.input import Mouse

    point = text_box.get_clickable_point()  # a screen Point inside the element
    Mouse.move_to(new_position=point)
    print(Mouse.position)  # Point(x=..., y=...)
    Mouse.click(point, post_wait=True)
    Mouse.scroll(-2)  # negative scrolls down
    # --8<-- [end:mouse]
    assert text_box.properties.has_keyboard_focus.value


# ---------------------------------------------------------------------------------------------
# Drawing types
# ---------------------------------------------------------------------------------------------


def test_drawing_types(window: Window) -> None:
    """Point, Size, Rectangle and Color wrap System.Drawing values."""
    # --8<-- [start:drawing]
    from flaui.lib.system.drawing import Color, Point, Rectangle, Size

    bounds = window.bounding_rectangle  # Rectangle, in screen pixels
    print(bounds.left, bounds.top, bounds.width, bounds.height)
    middle = bounds.center()  # Point

    p = Point(raw_value=(10, 20))  # build your own from Python values...
    moved = p + Size(raw_value=(5, 5))  # ...and combine them like the C# operators
    box = Rectangle(raw_value=[0, 0, 100, 50])  # x, y, width, height
    inside = box.contains(Point(raw_value=(10, 10)))

    blue = Color.from_name("Blue")  # or Color.Red, Color.from_argb(...)
    # --8<-- [end:drawing]
    assert bounds.contains(middle)
    assert (moved.x, moved.y) == (15, 25)
    assert inside
    assert (blue.r, blue.g, blue.b) == (0, 0, 255)


# ---------------------------------------------------------------------------------------------
# Screenshots and highlighting
# ---------------------------------------------------------------------------------------------


def test_capture(window: Window, tmp_path: Path) -> None:
    """Screenshot a window, the screen, or any element to a file."""
    # --8<-- [start:capture]
    from flaui.core.capturing import Capture, CaptureSettings

    with Capture.element(window) as image:  # the image is disposed when the block ends
        image.to_file(str(tmp_path / "window.png"))

    with Capture.main_screen(CaptureSettings(output_scale=0.5)) as screen:  # half size
        screen.to_file(str(tmp_path / "screen.png"))

    window.capture_to_file(str(tmp_path / "shortcut.png"))  # one-liner on any element
    # --8<-- [end:capture]
    assert (tmp_path / "window.png").stat().st_size > 0
    assert (tmp_path / "screen.png").stat().st_size > 0
    assert (tmp_path / "shortcut.png").stat().st_size > 0


def test_capture_overlays(window: Window, tmp_path: Path) -> None:
    """Draw the mouse cursor and an info bar onto a screenshot."""
    # --8<-- [start:capture_overlays]
    from flaui.core.capturing import Capture, InfoOverlay, InfoOverlayPosition, MouseOverlay
    from flaui.lib.system.drawing import Color

    with Capture.element(window) as image:
        info = InfoOverlay(
            image,
            overlay_string_format="{dt:HH:mm:ss} / {name}",  # time and machine name
            overlay_position=InfoOverlayPosition.BottomRight,
            overlay_text_color=Color.Yellow,
        )
        image.apply_overlays(MouseOverlay(image), info).to_file(str(tmp_path / "annotated.png"))
    # --8<-- [end:capture_overlays]
    assert (tmp_path / "annotated.png").stat().st_size > 0


def test_video_recorder_settings(tmp_path: Path) -> None:
    """Configure a screen recording that stamps the elapsed time on every frame."""
    # --8<-- [start:video_recorder]
    from flaui.core.capturing import (
        Capture,
        CaptureImage,
        CaptureSettings,
        InfoOverlay,
        MouseOverlay,
        VideoFormat,
        VideoRecorder,
        VideoRecorderSettings,
    )

    settings = VideoRecorderSettings(
        ffmpeg_path=r"C:\tools\ffmpeg.exe",  # or VideoRecorder.download_ffmpeg(folder)
        target_video_path=str(tmp_path / "run.mp4"),
        frame_rate=10,
        video_format=VideoFormat.xvid,  # bigger file, less CPU than x264
    )

    def frame(recorder: VideoRecorder) -> CaptureImage:
        """Capture one frame with the cursor and the elapsed recording time ({rt}) drawn on it."""
        image = Capture.main_screen(CaptureSettings(output_scale=0.5))
        info = InfoOverlay(image, overlay_string_format="{rt:hh\\:mm\\:ss}", record_time_span=recorder.record_time_span)
        return image.apply_overlays(info, MouseOverlay(image))

    # with VideoRecorder.start(settings, frame) as recorder:  # needs ffmpeg at settings.ffmpeg_path
    #     ...  # drive the application; leaving the block stops and encodes the video
    # --8<-- [end:video_recorder]
    from types import SimpleNamespace

    from System import TimeSpan  # type: ignore

    # Drive the frame callback once without ffmpeg, using a stand-in for the C# recorder.
    not_recording = VideoRecorder(raw_recorder=SimpleNamespace(RecordTimeSpan=TimeSpan.Zero))
    with frame(not_recording) as image:
        assert image.original_bounds.width > 0
    assert settings.cs_object.FrameRate == 10


def test_highlight(automation: Automation, window: Window, cf: ConditionFactory) -> None:
    """Draw a coloured frame around an element while debugging."""
    button = window.find_first_descendant(cf.by_automation_id("InvokableButton"))
    # --8<-- [start:highlight]
    from flaui.lib.system.drawing import Color

    button.draw_highlight(Color.Blue, duration=500)  # frame the element for 0.5 s

    overlay = automation.automation_base.overlay_manager  # or any rectangle on screen
    overlay.show(window.bounding_rectangle, Color.Red, duration_in_ms=500)
    # --8<-- [end:highlight]


def test_debug_details_and_xpath(automation: Automation, window: Window, cf: ConditionFactory) -> None:
    """Dump an element's properties and turn it into an XPath locator."""
    button = window.find_first_descendant(cf.by_automation_id("InvokableButton"))
    # --8<-- [start:debug]
    from flaui.core import debug

    print(debug.details(button))  # or button.details(): AutomationId, ControlType, Name, patterns

    desktop = automation.automation_base.get_desktop()
    xpath = button.get_xpath_to_element(desktop)  # e.g. "/Tab/TabItem[1]/Button[2]"
    same_button = window.find_first_by_x_path(xpath)  # the path is relative to the window
    # --8<-- [end:debug]
    assert "AutomationId: InvokableButton" in button.details()
    assert same_button.equals(button)


# ---------------------------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------------------------


@pytest.mark.usefixtures("complex_controls")
def test_item_realizer(window: Window, cf: ConditionFactory) -> None:
    """Realize a virtualized list so every item is in the automation tree."""
    # --8<-- [start:item_realizer]
    from flaui.core.tools import ItemRealizer

    large_list = window.find_first_descendant(cf.by_automation_id("LargeListView"))
    ItemRealizer.realize_items(large_list)  # scrolls through and realizes each item
    # --8<-- [end:item_realizer]
    assert large_list.find_all_children()


def test_system_info() -> None:
    """Read machine CPU and memory, e.g. to log alongside a slow test."""
    # --8<-- [start:system_info]
    from flaui.core.tools import SystemInfo

    print(f"CPU {SystemInfo.cpu_usage()}%  RAM {SystemInfo.physical_memory_used_percent()}% used")
    free_gb = SystemInfo.physical_memory_free() / 1024**3
    # --8<-- [end:system_info]
    assert free_gb > 0


def test_accessibility_text(window: Window) -> None:
    """Turn MSAA role / state values into readable text."""
    # --8<-- [start:accessibility_text]
    from flaui.core.tools import AccessibilityTextResolver

    legacy = window.raw_element.Patterns.LegacyIAccessible.Pattern  # MSAA view of the element
    role = AccessibilityTextResolver.get_role_text(legacy.Role.Value)  # e.g. "window"
    state = AccessibilityTextResolver.get_state_text(legacy.State.Value)  # e.g. "focusable"
    # --8<-- [end:accessibility_text]
    assert role
    assert isinstance(state, str)


def test_type_cast() -> None:
    """Convert between Python and .NET values at the boundary."""
    # --8<-- [start:type_cast]
    from flaui.lib.collections import TypeCast

    span = TypeCast.cs_timespan(1500)  # Python milliseconds -> System.TimeSpan
    items = TypeCast.py_list(span.ToString().split(":"))  # any C# IEnumerable -> Python list
    # --8<-- [end:type_cast]
    assert span.TotalSeconds == 1.5
    assert isinstance(items, list)
