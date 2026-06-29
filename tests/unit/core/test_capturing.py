"""Unit tests for the capturing/video wrappers (GH-95).

Settings objects and enums only need the PythonNet bridge (set up by the global conftest). Real
screen/element captures are cheap and run here too; only ``VideoRecorder.start`` /
``download_ffmpeg`` (which need ffmpeg or network access) are deferred to the UI suite.
"""

from pathlib import Path
from typing import Any, Generator
from unittest.mock import MagicMock, patch

from System.Drawing import Rectangle as CSRectangle  # type: ignore
import pytest

from flaui.core.automation_elements import AutomationElement
from flaui.core.capturing import (
    Capture,
    CaptureImage,
    CaptureSettings,
    VideoFormat,
    VideoRecorder,
    VideoRecorderSettings,
)
from flaui.lib.enums import UIAutomationTypes
from flaui.lib.system.drawing import Rectangle
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
