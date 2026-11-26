"""Unit tests for the capturing/video wrappers (GH-95, GH-160).

Settings objects and enums only need the PythonNet bridge (set up by the global conftest). Real
screen/element captures are cheap and run here too; only ``VideoRecorder.start`` /
``download_ffmpeg`` (which need ffmpeg or network access) are deferred to the UI suite.
"""

from datetime import timedelta
from pathlib import Path
import shutil
import time
from typing import Any, Generator
from unittest.mock import MagicMock, patch

from FlaUI.Core.Capturing import MouseOverlay as CSMouseOverlay  # type: ignore
from System import TimeSpan  # type: ignore
from System.Drawing import Font, Rectangle as CSRectangle  # type: ignore
from pydantic import ValidationError
import pytest

from flaui.core.automation_elements import AutomationElement
from flaui.core.capturing import (
    Capture,
    CaptureImage,
    CaptureSettings,
    CaptureUtilities,
    ICaptureOverlay,
    InfoOverlay,
    InfoOverlayPosition,
    MouseOverlay,
    OverlayBase,
    VideoFormat,
    VideoRecorder,
    VideoRecorderSettings,
)
from flaui.lib.enums import UIAutomationTypes
from flaui.lib.system.drawing import Color, Point, Rectangle
from flaui.modules.automation import Automation


@pytest.fixture(scope="module")
def desktop() -> Generator[AutomationElement, None, None]:
    """Yield the desktop element from a UIA3 automation, disposing it afterwards."""
    automation = Automation(UIAutomationTypes.UIA3)
    try:
        yield automation.automation_base.get_desktop()
    finally:
        automation.cs_automation.Dispose()


class TestCaptureSettings:
    """Tests for :class:`CaptureSettings`."""

    def test_defaults(self) -> None:
        """Defaults match FlaUI's C# defaults."""
        settings = CaptureSettings()
        assert settings.output_width == -1
        assert settings.output_height == -1
        assert settings.output_scale == 1.0

    def test_cs_object_round_trips_values(self) -> None:
        """``cs_object`` builds a C# ``CaptureSettings`` carrying the model's values."""
        cs = CaptureSettings(output_width=800, output_height=600, output_scale=0.5).cs_object
        assert cs.OutputWidth == 800
        assert cs.OutputHeight == 600
        assert cs.OutputScale == 0.5

    def test_from_cs_round_trips(self) -> None:
        """``from_cs`` rebuilds the model from the C# object ``cs_object`` produced."""
        settings = CaptureSettings(output_width=320, output_height=-1, output_scale=0.25)
        assert CaptureSettings.from_cs(settings.cs_object) == settings

    @pytest.mark.parametrize(
        "kwargs", [{"output_width": -2}, {"output_height": -5}, {"output_scale": 0}, {"output_scale": -1.0}]
    )
    def test_rejects_invalid_values(self, kwargs: dict[str, Any]) -> None:
        """Out-of-range sizes and non-positive scales are rejected before reaching C#."""
        with pytest.raises(ValidationError):
            CaptureSettings(**kwargs)


class TestInfoOverlayPosition:
    """Tests for the :class:`InfoOverlayPosition` enum mirror."""

    def test_members_match_csharp(self) -> None:
        """Every member has the same name and value as the C# enum."""
        from FlaUI.Core.Capturing import InfoOverlayPosition as CSInfoOverlayPosition  # type: ignore

        for member in InfoOverlayPosition:
            assert int(getattr(CSInfoOverlayPosition, member.name)) == member.value
        assert len(InfoOverlayPosition) == 6


class TestVideoFormat:
    """Tests for the :class:`VideoFormat` enum mirror."""

    def test_members(self) -> None:
        """Both codecs are present with C#-matching ordering."""
        assert VideoFormat.x264.value == 0
        assert VideoFormat.xvid.value == 1


class TestVideoRecorderSettings:
    """Tests for :class:`VideoRecorderSettings`."""

    def test_defaults(self) -> None:
        """Defaults match FlaUI's C# defaults."""
        settings = VideoRecorderSettings()
        assert settings.frame_rate == 5
        assert settings.use_compressed_images is True
        assert settings.video_format is VideoFormat.x264
        assert settings.log_missing_frames is True

    def test_cs_object_round_trips_values(self) -> None:
        """``cs_object`` builds a C# ``VideoRecorderSettings`` carrying the model's values."""
        cs = VideoRecorderSettings(
            ffmpeg_path="C:/ffmpeg.exe",
            frame_rate=15,
            target_video_path="out.mp4",
            video_format=VideoFormat.xvid,
            video_quality=5,
        ).cs_object
        assert cs.ffmpegPath == "C:/ffmpeg.exe"
        assert cs.FrameRate == 15
        assert cs.TargetVideoPath == "out.mp4"
        assert cs.VideoQuality == 5
        assert str(cs.VideoFormat) == "xvid"

    def test_cs_object_skips_unset_optional_paths(self) -> None:
        """With ``ffmpeg_path``/``target_video_path`` unset, ``cs_object`` leaves the C# defaults."""
        cs = VideoRecorderSettings().cs_object
        assert cs.FrameRate == 5
        assert cs.UseCompressedImages is True

    def test_defaults_match_csharp_defaults(self) -> None:
        """A default model equals one read back from a freshly constructed C# settings object."""
        from FlaUI.Core.Capturing import VideoRecorderSettings as CSVideoRecorderSettings  # type: ignore

        assert VideoRecorderSettings.from_cs(CSVideoRecorderSettings()) == VideoRecorderSettings()

    def test_from_cs_round_trips_every_field(self) -> None:
        """``from_cs`` reads back every field that ``cs_object`` wrote."""
        settings = VideoRecorderSettings(
            ffmpeg_path="C:/tools/ffmpeg.exe",
            frame_rate=12,
            target_video_path="C:/out/run.mp4",
            use_compressed_images=False,
            video_format=VideoFormat.xvid,
            video_quality=4,
            encode_with_low_priority=True,
            log_missing_frames=False,
        )
        assert VideoRecorderSettings.from_cs(settings.cs_object) == settings

    def test_rejects_non_positive_frame_rate(self) -> None:
        """``frame_rate`` maps to a C# ``uint`` and must be at least 1."""
        with pytest.raises(ValidationError):
            VideoRecorderSettings(frame_rate=0)


class TestCaptureImage:
    """Tests for :class:`CaptureImage`, driven by a real primary-screen capture."""

    def test_properties(self) -> None:
        """``bitmap`` and ``original_bounds`` expose the native image data."""
        with Capture.main_screen() as image:
            assert image.bitmap is not None
            assert isinstance(image.original_bounds, Rectangle)

    def test_to_file_writes_image(self, tmp_path: Path) -> None:
        """``to_file`` persists the image to disk."""
        destination = tmp_path / "capture.png"
        with Capture.main_screen() as image:
            image.to_file(str(destination))
        assert destination.exists() and destination.stat().st_size > 0

    def test_apply_overlays_returns_self(self) -> None:
        """``apply_overlays`` with no overlays is a no-op that returns the image for chaining."""
        with Capture.main_screen() as image:
            assert image.apply_overlays() is image

    def test_apply_overlays_accepts_python_and_raw_overlays(self, tmp_path: Path) -> None:
        """Python overlay wrappers and raw C# overlays can be mixed in one call."""
        destination = tmp_path / "overlaid.png"
        with Capture.main_screen(CaptureSettings(output_scale=0.25)) as image:
            result = image.apply_overlays(
                MouseOverlay(image),
                InfoOverlay(image, overlay_position=InfoOverlayPosition.BottomCenter),
                CSMouseOverlay(image.raw_image),
            )
            assert result is image
            image.to_file(str(destination))
        assert destination.stat().st_size > 0

    def test_settings_none_without_settings(self) -> None:
        """``settings`` is ``None`` when the capture was taken without settings."""
        with Capture.main_screen() as image:
            assert image.settings is None

    def test_settings_reflect_capture_settings(self) -> None:
        """``settings`` returns the typed model the capture was taken with."""
        requested = CaptureSettings(output_scale=0.5)
        with Capture.main_screen(requested) as image:
            assert image.settings == requested

    def test_bitmap_image(self) -> None:
        """``bitmap_image`` returns a WPF ``BitmapImage`` of the capture."""
        with Capture.rectangle(Rectangle(raw_value=CSRectangle(0, 0, 20, 20))) as image:
            bitmap_image = image.bitmap_image
            assert bitmap_image.GetType().FullName == "System.Windows.Media.Imaging.BitmapImage"
            assert bitmap_image.PixelWidth == 20

    def test_context_manager_returns_self_and_disposes(self) -> None:
        """The context manager yields the same image and disposes it on exit without error."""
        image = Capture.main_screen()
        with image as entered:
            assert entered is image


class TestCaptureStatics:
    """Tests for the :class:`Capture` static helpers using real captures."""

    def test_main_screen_with_and_without_settings(self) -> None:
        """``main_screen`` works with default and explicit settings (covers both ``_cs_settings`` paths)."""
        with Capture.main_screen() as plain:
            assert isinstance(plain, CaptureImage)
        with Capture.main_screen(CaptureSettings(output_scale=0.5)) as scaled:
            assert isinstance(scaled, CaptureImage)

    def test_screen(self) -> None:
        """``screen`` captures the whole virtual desktop when the index is out of range."""
        with Capture.screen(-1) as image:
            assert isinstance(image, CaptureImage)

    def test_rectangle(self) -> None:
        """``rectangle`` captures a desktop-relative region."""
        with Capture.rectangle(Rectangle(raw_value=CSRectangle(0, 0, 40, 40))) as image:
            assert isinstance(image, CaptureImage)

    def test_element(self, desktop: AutomationElement) -> None:
        """``element`` captures a single automation element."""
        with Capture.element(desktop) as image:
            assert isinstance(image, CaptureImage)

    def test_element_rectangle(self, desktop: AutomationElement) -> None:
        """``element_rectangle`` captures a region relative to an element."""
        with Capture.element_rectangle(desktop, Rectangle(raw_value=CSRectangle(0, 0, 10, 10))) as image:
            assert isinstance(image, CaptureImage)

    def test_screens_with_element(self, desktop: AutomationElement) -> None:
        """``screens_with_element`` captures every screen the element overlaps."""
        with Capture.screens_with_element(desktop) as image:
            assert isinstance(image, CaptureImage)


class TestVideoRecorder:
    """Tests for :class:`VideoRecorder` lifecycle, driven by a stub C# recorder.

    ``start`` and ``download_ffmpeg`` require ffmpeg/network and are covered by the UI suite.
    """

    def test_target_video_path(self) -> None:
        """``target_video_path`` forwards to the native recorder."""
        raw = MagicMock()
        raw.TargetVideoPath = "out.mp4"
        assert VideoRecorder(raw_recorder=raw).target_video_path == "out.mp4"

    def test_record_time_span_is_timedelta(self) -> None:
        """``record_time_span`` converts the native ``TimeSpan`` to a :class:`~datetime.timedelta`."""
        raw = MagicMock()
        raw.RecordTimeSpan = TimeSpan.FromMilliseconds(1500)
        assert VideoRecorder(raw_recorder=raw).record_time_span == timedelta(seconds=1.5)

    def test_stop(self) -> None:
        """``stop`` calls the native ``Stop``."""
        raw = MagicMock()
        VideoRecorder(raw_recorder=raw).stop()
        raw.Stop.assert_called_once_with()

    def test_dispose(self) -> None:
        """``dispose`` calls the native ``Dispose``."""
        raw = MagicMock()
        VideoRecorder(raw_recorder=raw).dispose()
        raw.Dispose.assert_called_once_with()

    def test_context_manager_disposes(self) -> None:
        """The context manager returns the recorder and disposes it on exit."""
        raw = MagicMock()
        recorder = VideoRecorder(raw_recorder=raw)
        with recorder as entered:
            assert entered is recorder
        raw.Dispose.assert_called_once_with()


class _StubCapturing:
    """Stand-in for the C# ``FlaUI.Core.Capturing`` module used by ``VideoRecorder.start``.

    Captures the frame delegate that ``start`` builds so the test can invoke it directly and verify
    both the default (whole-desktop) and custom-callback frame sources without any native calls.
    """

    def __init__(self) -> None:
        """Initialise the stub recorder/capture surfaces and delegate capture slot."""
        self.captured_delegate: Any = None
        screen_marker = self
        self.screen_sentinel = object()

        class Capture:
            """Stub for ``Capture`` whose ``Screen`` returns a recognisable sentinel."""

            @staticmethod
            def Screen() -> object:
                """Return the stub's screen-capture sentinel."""
                return screen_marker.screen_sentinel

        class CaptureImage:
            """Marker type for the ``Func`` generic; never instantiated here."""

        recorder_self = self

        class VideoRecorder:  # noqa: N801 - mirrors the C# type name
            """Stub C# recorder that records the constructor's delegate argument."""

            def __init__(self, _settings: Any, delegate: Any) -> None:
                """Store the delegate so the test can drive it."""
                recorder_self.captured_delegate = delegate

        self.Capture = Capture
        self.CaptureImage = CaptureImage
        self.VideoRecorder = VideoRecorder


def _stub_func_module() -> Any:
    """Return a ``System`` module stub whose ``Func[...]`` just wraps the Python callable."""
    system = MagicMock()

    class _Func:
        """Mimic ``System.Func`` generic subscription: ``Func[A, B](fn)`` returns ``fn``."""

        def __getitem__(self, _types: Any) -> Any:
            """Return a constructor that hands the Python callable straight back."""
            return lambda fn: fn

    system.Func = _Func()
    return system


class TestVideoRecorderStart:
    """Cover ``VideoRecorder.start`` and ``download_ffmpeg`` with stubbed C# capturing types."""

    def test_start_default_frame_source_captures_desktop(self) -> None:
        """With no ``capture_method``, the frame delegate captures the whole desktop screen."""
        capturing = _StubCapturing()
        # A stub settings object: ``start`` only needs ``cs_object`` from it, so avoid touching the
        # real C# ``VideoRecorderSettings`` (whose ``cs_object`` would import the stubbed module).
        settings = MagicMock(cs_object=object())
        with patch.dict(
            "sys.modules",
            {"System": _stub_func_module(), "FlaUI.Core.Capturing": capturing},
        ):
            recorder = VideoRecorder.start(settings)

        assert isinstance(recorder, VideoRecorder)
        # Invoke the captured delegate to exercise the default ``_frame`` body.
        assert capturing.captured_delegate(MagicMock()) is capturing.screen_sentinel

    def test_start_custom_capture_method_unwraps_capture_image(self) -> None:
        """A custom callback returning a ``CaptureImage`` has its ``raw_image`` forwarded."""
        capturing = _StubCapturing()
        raw_image = object()
        capture_image = CaptureImage(raw_image=raw_image)
        settings = MagicMock(cs_object=object())

        def _capture(_recorder: VideoRecorder) -> CaptureImage:
            """Return a wrapped capture image to exercise the unwrap branch."""
            return capture_image

        with patch.dict(
            "sys.modules",
            {"System": _stub_func_module(), "FlaUI.Core.Capturing": capturing},
        ):
            VideoRecorder.start(settings, capture_method=_capture)
            assert capturing.captured_delegate(MagicMock()) is raw_image

    def test_start_custom_capture_method_passes_through_raw(self) -> None:
        """A custom callback returning a raw (non-CaptureImage) value is forwarded unchanged."""
        capturing = _StubCapturing()
        raw_frame = object()
        settings = MagicMock(cs_object=object())

        with patch.dict(
            "sys.modules",
            {"System": _stub_func_module(), "FlaUI.Core.Capturing": capturing},
        ):
            VideoRecorder.start(settings, capture_method=lambda _recorder: raw_frame)
            assert capturing.captured_delegate(MagicMock()) is raw_frame

    def test_download_ffmpeg_delegates_to_cs(self) -> None:
        """``download_ffmpeg`` returns the path produced by the C# task result."""
        capturing = MagicMock()
        capturing.VideoRecorder.DownloadFFMpeg.return_value.Result = "C:/ffmpeg/ffmpeg.exe"
        with patch.dict("sys.modules", {"FlaUI.Core.Capturing": capturing}):
            assert VideoRecorder.download_ffmpeg("C:/ffmpeg") == "C:/ffmpeg/ffmpeg.exe"
        capturing.VideoRecorder.DownloadFFMpeg.assert_called_once_with("C:/ffmpeg")


@pytest.fixture
def small_capture() -> Generator[CaptureImage, None, None]:
    """Yield a small desktop-region capture, disposing it afterwards."""
    with Capture.rectangle(Rectangle(raw_value=CSRectangle(0, 0, 64, 32))) as image:
        yield image


class TestOverlays:
    """Tests for :class:`ICaptureOverlay`, :class:`MouseOverlay` and :class:`InfoOverlay`."""

    def test_mouse_overlay_wraps_csharp_overlay(self, small_capture: CaptureImage) -> None:
        """``MouseOverlay(image)`` creates the C# overlay bound to that image."""
        overlay = MouseOverlay(small_capture)
        assert isinstance(overlay, ICaptureOverlay)
        assert overlay.raw_overlay.GetType().FullName == "FlaUI.Core.Capturing.MouseOverlay"
        assert overlay.capture_image.raw_image.Equals(small_capture.raw_image)

    def test_wraps_existing_raw_overlay(self, small_capture: CaptureImage) -> None:
        """``raw_overlay=`` wraps an existing C# overlay instead of creating a new one."""
        raw = CSMouseOverlay(small_capture.raw_image)
        assert MouseOverlay(raw_overlay=raw).raw_overlay is raw

    def test_requires_image_or_raw_overlay(self) -> None:
        """Constructing without an image or a raw overlay raises a clear error."""
        with pytest.raises(ValueError, match="needs a CaptureImage"):
            MouseOverlay()

    def test_overlay_base_is_abstract(self, small_capture: CaptureImage) -> None:
        """``OverlayBase`` itself cannot create a C# overlay."""
        with pytest.raises(TypeError, match="abstract"):
            OverlayBase(small_capture)

    def test_info_overlay_defaults(self, small_capture: CaptureImage) -> None:
        """A new ``InfoOverlay`` exposes FlaUI's defaults through typed properties."""
        overlay = InfoOverlay(small_capture)
        assert overlay.overlay_position == InfoOverlayPosition.TopLeft
        assert overlay.record_time_span == timedelta(0)
        assert "{dt" in overlay.overlay_string_format
        assert overlay.overlay_text_color.name == "White"
        assert overlay.overlay_text_font.Name == "Consolas"

    def test_info_overlay_keyword_options(self, small_capture: CaptureImage) -> None:
        """Option keyword arguments are applied to the C# overlay at construction."""
        overlay = InfoOverlay(
            small_capture,
            overlay_string_format="{rt}",
            overlay_position=InfoOverlayPosition.BottomRight,
            overlay_background_color=Color.Black,
            overlay_text_color=Color.Yellow,
            record_time_span=timedelta(minutes=1, microseconds=5),
        )
        assert overlay.overlay_string_format == "{rt}"
        assert overlay.overlay_position == InfoOverlayPosition.BottomRight
        assert overlay.overlay_background_color.name == "Black"
        assert overlay.overlay_text_color.name == "Yellow"
        assert overlay.record_time_span == timedelta(minutes=1, microseconds=5)

    def test_info_overlay_setters_accept_csharp_values(self, small_capture: CaptureImage) -> None:
        """Setters also accept raw C# ``Color``, ``Font`` and ``TimeSpan`` values."""
        overlay = InfoOverlay(small_capture)
        overlay.overlay_text_color = Color.Red.cs_object
        overlay.overlay_text_font = Font("Arial", 12.0)
        overlay.record_time_span = TimeSpan.FromSeconds(2)
        assert overlay.overlay_text_color.name == "Red"
        assert overlay.overlay_text_font.Name == "Arial"
        assert overlay.record_time_span == timedelta(seconds=2)

    def test_draw_forwards_to_csharp(self) -> None:
        """``draw`` hands the graphics surface to the C# overlay."""
        raw, graphics = MagicMock(), object()
        ICaptureOverlay(raw_overlay=raw).draw(graphics)
        raw.Draw.assert_called_once_with(graphics)


class TestCaptureUtilities:
    """Tests for :class:`CaptureUtilities`."""

    bounds = Rectangle(raw_value=[0, 0, 100, 100])

    def test_get_scale(self) -> None:
        """Without settings the scale is 1; a fixed output width scales proportionally."""
        assert CaptureUtilities.get_scale(self.bounds) == 1.0
        assert CaptureUtilities.get_scale(self.bounds, CaptureSettings(output_width=50)) == 0.5

    def test_scale_rectangle(self) -> None:
        """A rectangle is scaled against itself."""
        scaled = CaptureUtilities.scale_according_to_settings(self.bounds, CaptureSettings(output_scale=0.5))
        assert isinstance(scaled, Rectangle)
        assert (scaled.width, scaled.height) == (50, 50)

    @pytest.mark.parametrize("point", [(10, 20), Point(raw_value=(10, 20))])
    def test_scale_point(self, point: Any) -> None:
        """Points (``Point`` or ``(x, y)``) are scaled relative to the capture bounds."""
        scaled = CaptureUtilities.scale_according_to_settings(point, CaptureSettings(output_width=50), self.bounds)
        assert isinstance(scaled, Point)
        assert (scaled.x, scaled.y) == (5, 10)

    def test_scale_point_requires_bounds(self) -> None:
        """Scaling a point without ``original_bounds`` is rejected."""
        with pytest.raises(ValueError, match="original_bounds"):
            CaptureUtilities.scale_according_to_settings((1, 1), CaptureSettings())

    def test_capture_cursor(self) -> None:
        """``capture_cursor`` returns the cursor bitmap and a typed position."""
        bitmap, position = CaptureUtilities.capture_cursor()
        assert isinstance(position, Point)
        if bitmap is not None:  # no cursor is shown on some headless sessions
            bitmap.Dispose()

    def test_delete_object_with_null_handle(self) -> None:
        """Deleting the null GDI handle fails cleanly instead of raising."""
        assert CaptureUtilities.delete_object(0) is False


FFMPEG = shutil.which("ffmpeg")


@pytest.mark.skipif(FFMPEG is None, reason="ffmpeg is not on PATH; VideoRecorder needs it")
class TestVideoRecorderWithFfmpeg:
    """A short real recording, run only where ffmpeg is installed."""

    def test_records_with_info_overlay(self, tmp_path: Path) -> None:
        """A recording with per-frame overlays produces a file and a growing ``record_time_span``."""
        target = tmp_path / "recording.mp4"
        settings = VideoRecorderSettings(ffmpeg_path=FFMPEG, target_video_path=str(target), frame_rate=5)

        def frame(recorder: VideoRecorder) -> CaptureImage:
            """Capture the main screen with the mouse and a recording-time bar drawn on it."""
            image = Capture.main_screen(CaptureSettings(output_scale=0.25))
            return image.apply_overlays(
                InfoOverlay(image, record_time_span=recorder.record_time_span), MouseOverlay(image)
            )

        with VideoRecorder.start(settings, frame) as recorder:  # exiting stops and finishes encoding
            time.sleep(1.5)
            assert recorder.record_time_span > timedelta(0)
        assert target.stat().st_size > 0
