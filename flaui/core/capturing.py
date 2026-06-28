"""Python wrappers for ``FlaUI.Core.Capturing`` — screen/element capture and video recording.

This mirrors the C# ``Capture`` static helpers, the ``CaptureImage`` result object, and the
``VideoRecorder``. Coordinates and bitmaps stay as C# objects (per the project's
prefer-C#-for-UI-primitives guidance); file paths and settings are plain Python.

.. note::
   :class:`VideoRecorder` requires ``ffmpeg``. Provide a path via
   :attr:`VideoRecorderSettings.ffmpeg_path` or download one with
   :meth:`VideoRecorder.download_ffmpeg`.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Optional

from pydantic import BaseModel, ConfigDict, Field

from flaui.lib.exceptions import handle_csharp_exceptions
from flaui.lib.system.drawing import Rectangle

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement


class VideoFormat(Enum):
    """Video codec used by :class:`VideoRecorder` (mirrors ``FlaUI.Core.Capturing.VideoFormat``)."""

    x264 = 0  # Small file size, high CPU usage.
    xvid = 1  # Medium file size, low CPU usage.


class CaptureSettings(BaseModel):
    """Output sizing options for a capture (mirrors ``FlaUI.Core.Capturing.CaptureSettings``)."""

    output_width: int = Field(default=-1, description="Output width; -1 keeps aspect ratio to height.")
    output_height: int = Field(default=-1, description="Output height; -1 keeps aspect ratio to width.")
    output_scale: float = Field(default=1.0, description="Output scale (1.0 == 100%).")

    @property
    def cs_object(self) -> Any:
        """Return the underlying C# ``CaptureSettings`` built from this model."""
        from FlaUI.Core.Capturing import CaptureSettings as CSCaptureSettings  # pyright: ignore

        settings = CSCaptureSettings()
        settings.OutputWidth = self.output_width
        settings.OutputHeight = self.output_height
        settings.OutputScale = self.output_scale
        return settings


def _cs_settings(settings: Optional[CaptureSettings]) -> Any:
    """Return the C# settings object for an optional :class:`CaptureSettings`, or ``None``."""
    return settings.cs_object if settings is not None else None


class CaptureImage(BaseModel):
    """A captured image (mirrors ``FlaUI.Core.Capturing.CaptureImage``).

    Wraps the C# result of a :class:`Capture` call. Use :meth:`to_file` to persist it, or use it as a
    context manager to dispose the underlying bitmap automatically.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_image: Any = Field(..., description="Underlying C# CaptureImage instance")

    @property
    @handle_csharp_exceptions
    def bitmap(self) -> Any:
        """Return the underlying C# ``Bitmap``."""
        return self.raw_image.Bitmap

    @property
    @handle_csharp_exceptions
    def original_bounds(self) -> Rectangle:
        """Return the desktop-relative bounding rectangle this image was captured from."""
        return Rectangle(raw_value=self.raw_image.OriginalBounds)

    @handle_csharp_exceptions
    def to_file(self, file_path: str) -> None:
        """Save the image to a file; the extension selects the format (defaults to PNG).

        :param file_path: Destination path (``.png``, ``.jpg``, ``.gif``, ``.tif``, ``.bmp``).
        """
        self.raw_image.ToFile(file_path)

    @handle_csharp_exceptions
    def apply_overlays(self, *overlays: Any) -> "CaptureImage":
        """Draw the given C# ``ICaptureOverlay`` objects onto the image.

        :param overlays: Raw C# overlay instances (e.g. ``MouseOverlay``, ``InfoOverlay``).
        :return: This :class:`CaptureImage` (for chaining).
        """
        self.raw_image.ApplyOverlays(*overlays)
        return self

    @handle_csharp_exceptions
    def dispose(self) -> None:
        """Dispose the underlying bitmap and release its memory."""
        self.raw_image.Dispose()

    def __enter__(self) -> "CaptureImage":
        """Enter the context manager.

        :return: This :class:`CaptureImage`.
        """
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Dispose the image on context-manager exit.

        :param exc_info: Standard ``(exc_type, exc, tb)`` tuple (unused).
        """
        self.dispose()


class Capture:
    """Static screen/element capture helpers (mirrors ``FlaUI.Core.Capturing.Capture``)."""

    @staticmethod
    @handle_csharp_exceptions
    def main_screen(settings: Optional[CaptureSettings] = None) -> CaptureImage:
        """Capture the primary screen.

        :param settings: Optional output sizing settings.
        :return: The captured image.
        """
        from FlaUI.Core.Capturing import Capture as CSCapture  # pyright: ignore

        return CaptureImage(raw_image=CSCapture.MainScreen(_cs_settings(settings)))

    @staticmethod
    @handle_csharp_exceptions
    def screen(screen_index: int = -1, settings: Optional[CaptureSettings] = None) -> CaptureImage:
        """Capture a screen (or the whole virtual desktop when ``screen_index`` is out of range).

        :param screen_index: Zero-based monitor index; ``-1`` captures all monitors.
        :param settings: Optional output sizing settings.
        :return: The captured image.
        """
        from FlaUI.Core.Capturing import Capture as CSCapture  # pyright: ignore

        return CaptureImage(raw_image=CSCapture.Screen(screen_index, _cs_settings(settings)))

    @staticmethod
    @handle_csharp_exceptions
    def element(element: "AutomationElement", settings: Optional[CaptureSettings] = None) -> CaptureImage:
        """Capture a single automation element.

        :param element: The element to capture.
        :param settings: Optional output sizing settings.
        :return: The captured image.
        """
        from FlaUI.Core.Capturing import Capture as CSCapture  # pyright: ignore

        return CaptureImage(raw_image=CSCapture.Element(element.raw_element, _cs_settings(settings)))

    @staticmethod
    @handle_csharp_exceptions
    def element_rectangle(
        element: "AutomationElement", rectangle: Rectangle, settings: Optional[CaptureSettings] = None
    ) -> CaptureImage:
        """Capture a rectangle (relative to the element) inside an element.

        :param element: The element whose region to capture.
        :param rectangle: The rectangle relative to the element's top-left corner.
        :param settings: Optional output sizing settings.
        :return: The captured image.
        """
        from FlaUI.Core.Capturing import Capture as CSCapture  # pyright: ignore

        return CaptureImage(
            raw_image=CSCapture.ElementRectangle(element.raw_element, rectangle.raw_value, _cs_settings(settings))
        )

    @staticmethod
    @handle_csharp_exceptions
    def screens_with_element(element: "AutomationElement", settings: Optional[CaptureSettings] = None) -> CaptureImage:
        """Capture every screen the given element overlaps.

        :param element: The element to locate across screens.
        :param settings: Optional output sizing settings.
        :return: The captured image.
        """
        from FlaUI.Core.Capturing import Capture as CSCapture  # pyright: ignore

        return CaptureImage(raw_image=CSCapture.ScreensWithElement(element.raw_element, _cs_settings(settings)))

    @staticmethod
    @handle_csharp_exceptions
    def rectangle(bounds: Rectangle, settings: Optional[CaptureSettings] = None) -> CaptureImage:
        """Capture a desktop-relative rectangle.

        :param bounds: The screen region to capture.
        :param settings: Optional output sizing settings.
        :return: The captured image.
        """
        from FlaUI.Core.Capturing import Capture as CSCapture  # pyright: ignore

        return CaptureImage(raw_image=CSCapture.Rectangle(bounds.raw_value, _cs_settings(settings)))


class VideoRecorderSettings(BaseModel):
    """Settings for :class:`VideoRecorder` (mirrors ``FlaUI.Core.Capturing.VideoRecorderSettings``)."""

    ffmpeg_path: Optional[str] = Field(default=None, description="Path to ffmpeg.exe.")
    frame_rate: int = Field(default=5, description="Capture/playback framerate.")
    target_video_path: Optional[str] = Field(default=None, description="Path to the output video file.")
    use_compressed_images: bool = Field(default=True, description="Capture compressed images (saves memory).")
    video_format: VideoFormat = Field(default=VideoFormat.x264, description="Video codec.")
    video_quality: int = Field(default=0, description="Codec-dependent quality value.")
    encode_with_low_priority: bool = Field(default=False, description="Run encoding at low process priority.")
    log_missing_frames: bool = Field(default=True, description="Warn when frames are dropped.")

    @property
    def cs_object(self) -> Any:
        """Return the underlying C# ``VideoRecorderSettings`` built from this model."""
        from FlaUI.Core.Capturing import (  # pyright: ignore
            VideoFormat as CSVideoFormat,
            VideoRecorderSettings as CSVideoRecorderSettings,
        )

        settings = CSVideoRecorderSettings()
        if self.ffmpeg_path is not None:
            settings.ffmpegPath = self.ffmpeg_path
        settings.FrameRate = self.frame_rate
        if self.target_video_path is not None:
            settings.TargetVideoPath = self.target_video_path
        settings.UseCompressedImages = self.use_compressed_images
        settings.VideoFormat = CSVideoFormat(self.video_format.value)
        settings.VideoQuality = self.video_quality
        settings.EncodeWithLowPriority = self.encode_with_low_priority
        settings.LogMissingFrames = self.log_missing_frames
        return settings


class VideoRecorder(BaseModel):
    """Records the screen (or a custom frame source) to a video file.

    Mirrors ``FlaUI.Core.Capturing.VideoRecorder``. Start a recording with :meth:`start`, then call
    :meth:`stop` (or use it as a context manager). Requires ffmpeg — see the module note.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_recorder: Any = Field(..., description="Underlying C# VideoRecorder instance")
    # Keep the C# delegate (and its Python target) alive for the recorder's lifetime; the recorder
    # invokes it on a background thread, so it must survive Python GC.
    keep_alive: Any = Field(default=None, repr=False, description="Internal delegate keep-alive handle")

    @classmethod
    @handle_csharp_exceptions
    def start(
        cls,
        settings: VideoRecorderSettings,
        capture_method: Optional[Callable[["VideoRecorder"], CaptureImage]] = None,
    ) -> "VideoRecorder":
        """Start recording.

        :param settings: Recorder settings (must include ``target_video_path``).
        :param capture_method: Optional callback ``(recorder) -> CaptureImage`` producing each frame.
            Defaults to capturing the whole virtual desktop.
        :return: The running :class:`VideoRecorder`.
        """
        from System import Func  # pyright: ignore
        from FlaUI.Core.Capturing import (  # pyright: ignore
            Capture as CSCapture,
            CaptureImage as CSCaptureImage,
            VideoRecorder as CSVideoRecorder,
        )

        if capture_method is None:

            def _frame(_recorder: Any) -> Any:
                """Default frame source: capture the whole desktop."""
                return CSCapture.Screen()
        else:

            def _frame(recorder: Any) -> Any:
                """Bridge the C# frame request to the user's Python capture callback."""
                result = capture_method(cls(raw_recorder=recorder))
                return result.raw_image if isinstance(result, CaptureImage) else result

        delegate = Func[CSVideoRecorder, CSCaptureImage](_frame)
        raw = CSVideoRecorder(settings.cs_object, delegate)
        return cls(raw_recorder=raw, keep_alive=(_frame, delegate))

    @property
    @handle_csharp_exceptions
    def target_video_path(self) -> str:
        """Return the output video file path."""
        return self.raw_recorder.TargetVideoPath

    @handle_csharp_exceptions
    def stop(self) -> None:
        """Stop recording and finish encoding the output file."""
        self.raw_recorder.Stop()

    @handle_csharp_exceptions
    def dispose(self) -> None:
        """Dispose the recorder (stops it if still running)."""
        self.raw_recorder.Dispose()

    @staticmethod
    @handle_csharp_exceptions
    def download_ffmpeg(target_folder: str) -> str:
        """Download a static ffmpeg build into ``target_folder`` (blocking).

        :param target_folder: Folder to download ffmpeg into.
        :return: The path to the downloaded ffmpeg executable.
        """
        from FlaUI.Core.Capturing import VideoRecorder as CSVideoRecorder  # pyright: ignore

        return CSVideoRecorder.DownloadFFMpeg(target_folder).Result

    def __enter__(self) -> "VideoRecorder":
        """Enter the context manager.

        :return: This :class:`VideoRecorder`.
        """
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Stop and dispose the recorder on context-manager exit.

        :param exc_info: Standard ``(exc_type, exc, tb)`` tuple (unused).
        """
        self.dispose()
