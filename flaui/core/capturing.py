"""Python wrappers for ``FlaUI.Core.Capturing`` — screen/element capture and video recording.

This mirrors the C# ``Capture`` static helpers, the ``CaptureImage`` result object, the capture
overlays (``MouseOverlay`` / ``InfoOverlay``), ``CaptureUtilities``, and the ``VideoRecorder``.
Bitmaps and fonts stay as C# objects (per the project's prefer-C#-for-UI-primitives guidance);
file paths, durations (:class:`datetime.timedelta`) and settings are plain Python.

.. note::
   :class:`VideoRecorder` requires ``ffmpeg``. Provide a path via
   :attr:`VideoRecorderSettings.ffmpeg_path` or download one with
   :meth:`VideoRecorder.download_ffmpeg`.
"""

from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field

from flaui.lib.exceptions import handle_csharp_exceptions
from flaui.lib.system.drawing import ColorData, Point, Rectangle

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement


class VideoFormat(Enum):
    """Video codec used by :class:`VideoRecorder` (mirrors ``FlaUI.Core.Capturing.VideoFormat``)."""

    x264 = 0  # Small file size, high CPU usage.
    xvid = 1  # Medium file size, low CPU usage.


class InfoOverlayPosition(Enum):
    """Where :class:`InfoOverlay` draws its text bar (mirrors ``FlaUI.Core.Capturing.InfoOverlayPosition``)."""

    TopLeft = 0
    TopRight = 1
    TopCenter = 2
    BottomLeft = 3
    BottomRight = 4
    BottomCenter = 5


# One .NET tick is 100 ns, so a microsecond is 10 ticks.
_TICKS_PER_MICROSECOND = 10


def _to_timedelta(cs_timespan: Any) -> timedelta:
    """Convert a C# ``System.TimeSpan`` to a :class:`datetime.timedelta` (microsecond precision).

    :param cs_timespan: The C# ``TimeSpan`` value.
    :return: The equivalent :class:`~datetime.timedelta`.
    """
    return timedelta(microseconds=int(cs_timespan.Ticks) // _TICKS_PER_MICROSECOND)


def _to_cs_timespan(value: Union[timedelta, Any]) -> Any:
    """Convert a :class:`datetime.timedelta` to a C# ``System.TimeSpan`` (C# values pass through).

    :param value: A :class:`~datetime.timedelta` or an existing C# ``TimeSpan``.
    :return: The C# ``TimeSpan``.
    """
    if not isinstance(value, timedelta):
        return value
    from System import TimeSpan  # pyright: ignore

    return TimeSpan.FromTicks((value // timedelta(microseconds=1)) * _TICKS_PER_MICROSECOND)


class CaptureSettings(BaseModel):
    """Output sizing options for a capture (mirrors ``FlaUI.Core.Capturing.CaptureSettings``).

    ``output_width`` / ``output_height`` take precedence over ``output_scale``; leave one of them at
    ``-1`` to keep the aspect ratio.
    """

    output_width: int = Field(default=-1, ge=-1, description="Output width; -1 keeps aspect ratio to height.")
    output_height: int = Field(default=-1, ge=-1, description="Output height; -1 keeps aspect ratio to width.")
    output_scale: float = Field(default=1.0, gt=0, description="Output scale (1.0 == 100%).")

    @classmethod
    def from_cs(cls, cs_settings: Any) -> "CaptureSettings":
        """Build a model from a C# ``CaptureSettings`` instance.

        :param cs_settings: The C# ``FlaUI.Core.Capturing.CaptureSettings``.
        :return: The equivalent :class:`CaptureSettings`.
        """
        return cls(
            output_width=cs_settings.OutputWidth,
            output_height=cs_settings.OutputHeight,
            output_scale=cs_settings.OutputScale,
        )

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
    def bitmap_image(self) -> Any:
        """Return the image as a C# WPF ``System.Windows.Media.Imaging.BitmapImage``.

        Each access encodes the bitmap again, so keep the result if you need it more than once.
        """
        return self.raw_image.BitmapImage

    @property
    @handle_csharp_exceptions
    def original_bounds(self) -> Rectangle:
        """Return the desktop-relative bounding rectangle this image was captured from."""
        return Rectangle(raw_value=self.raw_image.OriginalBounds)

    @property
    @handle_csharp_exceptions
    def settings(self) -> Optional[CaptureSettings]:
        """Return the settings the image was captured with, or ``None`` when none were given."""
        raw_settings = self.raw_image.Settings
        return CaptureSettings.from_cs(raw_settings) if raw_settings is not None else None

    @handle_csharp_exceptions
    def to_file(self, file_path: str) -> None:
        """Save the image to a file; the extension selects the format (defaults to PNG).

        :param file_path: Destination path (``.png``, ``.jpg``, ``.gif``, ``.tif``, ``.bmp``).
        """
        self.raw_image.ToFile(file_path)

    @handle_csharp_exceptions
    def apply_overlays(self, *overlays: Union["ICaptureOverlay", Any]) -> "CaptureImage":
        """Draw the given overlays onto the image, in order.

        :param overlays: Python overlays (:class:`MouseOverlay`, :class:`InfoOverlay`, any
            :class:`ICaptureOverlay`) or raw C# ``ICaptureOverlay`` instances; both may be mixed.
        :return: This :class:`CaptureImage` (for chaining).
        """
        self.raw_image.ApplyOverlays(*map(_cs_overlay, overlays))
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
    frame_rate: int = Field(default=5, ge=1, description="Capture/playback framerate (frames per second).")
    target_video_path: Optional[str] = Field(default=None, description="Path to the output video file.")
    use_compressed_images: bool = Field(default=True, description="Capture compressed images (saves memory).")
    video_format: VideoFormat = Field(default=VideoFormat.x264, description="Video codec.")
    video_quality: int = Field(default=0, description="Codec-dependent quality value.")
    encode_with_low_priority: bool = Field(default=False, description="Run encoding at low process priority.")
    log_missing_frames: bool = Field(default=True, description="Warn when frames are dropped.")

    @classmethod
    def from_cs(cls, cs_settings: Any) -> "VideoRecorderSettings":
        """Build a model from a C# ``VideoRecorderSettings`` instance.

        :param cs_settings: The C# ``FlaUI.Core.Capturing.VideoRecorderSettings``.
        :return: The equivalent :class:`VideoRecorderSettings`.
        """
        return cls(
            ffmpeg_path=cs_settings.ffmpegPath,
            frame_rate=int(cs_settings.FrameRate),
            target_video_path=cs_settings.TargetVideoPath,
            use_compressed_images=cs_settings.UseCompressedImages,
            video_format=VideoFormat(int(cs_settings.VideoFormat)),
            video_quality=cs_settings.VideoQuality,
            encode_with_low_priority=cs_settings.EncodeWithLowPriority,
            log_missing_frames=cs_settings.LogMissingFrames,
        )

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
        # pylint: disable-next=too-many-function-args  # C# ctor; pylint resolves FlaUI.Core.Capturing to this module on case-insensitive file systems
        raw = CSVideoRecorder(settings.cs_object, delegate)
        return cls(raw_recorder=raw, keep_alive=(_frame, delegate))

    @property
    @handle_csharp_exceptions
    def target_video_path(self) -> str:
        """Return the output video file path."""
        return self.raw_recorder.TargetVideoPath

    @property
    @handle_csharp_exceptions
    def record_time_span(self) -> timedelta:
        """Return how long the recorder has been recording (feed it to :attr:`InfoOverlay.record_time_span`)."""
        return _to_timedelta(self.raw_recorder.RecordTimeSpan)

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


def _cs_overlay(overlay: Union["ICaptureOverlay", Any]) -> Any:
    """Return the C# overlay behind a Python :class:`ICaptureOverlay`; raw C# overlays pass through.

    :param overlay: A Python overlay wrapper or a raw C# ``ICaptureOverlay``.
    :return: The raw C# ``ICaptureOverlay``.
    """
    return overlay.raw_overlay if isinstance(overlay, ICaptureOverlay) else overlay


class ICaptureOverlay(BaseModel):
    """Wraps any C# ``FlaUI.Core.Capturing.ICaptureOverlay`` (something that draws onto a capture).

    Use it directly to pass a custom C# overlay through the typed API, or use the concrete
    :class:`MouseOverlay` / :class:`InfoOverlay`.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_overlay: Any = Field(..., description="Underlying C# ICaptureOverlay instance")

    @handle_csharp_exceptions
    def draw(self, graphics: Any) -> None:
        """Draw the overlay onto a C# ``System.Drawing.Graphics`` surface.

        :meth:`CaptureImage.apply_overlays` calls this for you; call it directly only when drawing
        onto your own ``Graphics``.

        :param graphics: The C# ``Graphics`` surface to draw on.
        """
        self.raw_overlay.Draw(graphics)


class OverlayBase(ICaptureOverlay):
    """Base for overlays bound to a :class:`CaptureImage` (mirrors ``FlaUI.Core.Capturing.OverlayBase``).

    Subclasses are constructed from the image they will be drawn on, e.g. ``MouseOverlay(image)``.
    An existing C# overlay can be wrapped with ``MouseOverlay(raw_overlay=cs_overlay)``.
    """

    def __init__(self, capture_image: Optional[CaptureImage] = None, /, **data: Any) -> None:
        """Create the C# overlay for ``capture_image``, or wrap ``raw_overlay`` when given.

        :param capture_image: The image the overlay will be drawn on.
        :param data: Model fields; pass ``raw_overlay`` to wrap an existing C# overlay instead.
        :raises ValueError: If neither ``capture_image`` nor ``raw_overlay`` is given.
        """
        if "raw_overlay" not in data:
            if capture_image is None:
                raise ValueError(f"{type(self).__name__} needs a CaptureImage (or raw_overlay=...)")
            data["raw_overlay"] = self._create_cs_overlay(capture_image.raw_image)
        super().__init__(**data)

    @classmethod
    def _create_cs_overlay(cls, raw_image: Any) -> Any:
        """Construct the C# overlay for a raw C# ``CaptureImage``; implemented by subclasses.

        :param raw_image: The raw C# ``CaptureImage``.
        :raises TypeError: Always, for the abstract base.
        """
        raise TypeError(f"{cls.__name__} is abstract; use MouseOverlay or InfoOverlay")

    @property
    @handle_csharp_exceptions
    def capture_image(self) -> CaptureImage:
        """Return the image this overlay draws on."""
        return CaptureImage(raw_image=self.raw_overlay.CaptureImage)


class MouseOverlay(OverlayBase):
    """Draws the mouse cursor onto a capture (mirrors ``FlaUI.Core.Capturing.MouseOverlay``).

    Example::

        with Capture.main_screen() as image:
            image.apply_overlays(MouseOverlay(image)).to_file("screen.png")
    """

    @classmethod
    @handle_csharp_exceptions
    def _create_cs_overlay(cls, raw_image: Any) -> Any:
        """Construct a C# ``MouseOverlay`` for the raw image.

        :param raw_image: The raw C# ``CaptureImage``.
        :return: The new C# ``MouseOverlay``.
        """
        from FlaUI.Core.Capturing import MouseOverlay as CSMouseOverlay  # pyright: ignore

        return CSMouseOverlay(raw_image)


_INFO_OVERLAY_OPTIONS = (
    "overlay_string_format",
    "overlay_position",
    "overlay_background_color",
    "overlay_text_color",
    "overlay_text_font",
    "record_time_span",
)


class InfoOverlay(OverlayBase):
    """Draws a text bar (time, machine name, CPU/RAM, ...) onto a capture.

    Mirrors ``FlaUI.Core.Capturing.InfoOverlay``. Options may be passed as keyword arguments, e.g.
    ``InfoOverlay(image, overlay_position=InfoOverlayPosition.BottomRight)``. The text comes from
    :attr:`overlay_string_format`; FlaUI fills placeholders such as ``{dt}`` (now), ``{rt}`` (the
    :attr:`record_time_span`), ``{name}`` (machine name), ``{cpu}`` and ``{mem.p.used}``.
    """

    def __init__(self, capture_image: Optional[CaptureImage] = None, /, **data: Any) -> None:
        """Create the overlay and apply any option keyword arguments.

        :param capture_image: The image the overlay will be drawn on.
        :param data: ``raw_overlay`` to wrap an existing C# overlay, plus any of
            ``overlay_string_format``, ``overlay_position``, ``overlay_background_color``,
            ``overlay_text_color``, ``overlay_text_font`` and ``record_time_span``.
        """
        options = {name: data.pop(name) for name in _INFO_OVERLAY_OPTIONS if name in data}
        super().__init__(capture_image, **data)
        for name, value in options.items():
            setattr(self, name, value)

    @classmethod
    @handle_csharp_exceptions
    def _create_cs_overlay(cls, raw_image: Any) -> Any:
        """Construct a C# ``InfoOverlay`` for the raw image.

        :param raw_image: The raw C# ``CaptureImage``.
        :return: The new C# ``InfoOverlay``.
        """
        from FlaUI.Core.Capturing import InfoOverlay as CSInfoOverlay  # pyright: ignore

        return CSInfoOverlay(raw_image)

    @property
    @handle_csharp_exceptions
    def overlay_string_format(self) -> str:
        """Get the text template drawn by the overlay."""
        return self.raw_overlay.OverlayStringFormat

    @overlay_string_format.setter
    @handle_csharp_exceptions
    def overlay_string_format(self, value: str) -> None:
        """Set the text template drawn by the overlay.

        :param value: Template with FlaUI placeholders (``{dt}``, ``{rt}``, ``{name}``, ...).
        """
        self.raw_overlay.OverlayStringFormat = value

    @property
    @handle_csharp_exceptions
    def overlay_position(self) -> InfoOverlayPosition:
        """Get where the text bar is drawn."""
        return InfoOverlayPosition(int(self.raw_overlay.OverlayPosition))

    @overlay_position.setter
    @handle_csharp_exceptions
    def overlay_position(self, value: InfoOverlayPosition) -> None:
        """Set where the text bar is drawn.

        :param value: The bar position.
        """
        from FlaUI.Core.Capturing import InfoOverlayPosition as CSInfoOverlayPosition  # pyright: ignore

        self.raw_overlay.OverlayPosition = CSInfoOverlayPosition(InfoOverlayPosition(value).value)

    @property
    @handle_csharp_exceptions
    def overlay_background_color(self) -> ColorData:
        """Get the background color of the text bar."""
        return ColorData(cs_object=self.raw_overlay.OverlayBackgroundColor)

    @overlay_background_color.setter
    @handle_csharp_exceptions
    def overlay_background_color(self, value: Union[ColorData, Any]) -> None:
        """Set the background color of the text bar.

        :param value: A :class:`~flaui.lib.system.drawing.ColorData` (e.g. ``Color.Black``) or a C# ``Color``.
        """
        self.raw_overlay.OverlayBackgroundColor = _cs_color(value)

    @property
    @handle_csharp_exceptions
    def overlay_text_color(self) -> ColorData:
        """Get the text color."""
        return ColorData(cs_object=self.raw_overlay.OverlayTextColor)

    @overlay_text_color.setter
    @handle_csharp_exceptions
    def overlay_text_color(self, value: Union[ColorData, Any]) -> None:
        """Set the text color.

        :param value: A :class:`~flaui.lib.system.drawing.ColorData` (e.g. ``Color.White``) or a C# ``Color``.
        """
        self.raw_overlay.OverlayTextColor = _cs_color(value)

    @property
    @handle_csharp_exceptions
    def overlay_text_font(self) -> Any:
        """Get the text font (a C# ``System.Drawing.Font``)."""
        return self.raw_overlay.OverlayTextFont

    @overlay_text_font.setter
    @handle_csharp_exceptions
    def overlay_text_font(self, value: Any) -> None:
        """Set the text font.

        :param value: A C# ``System.Drawing.Font``, e.g. ``Font("Consolas", 12)``.
        """
        self.raw_overlay.OverlayTextFont = value

    @property
    @handle_csharp_exceptions
    def record_time_span(self) -> timedelta:
        """Get the recording time shown by the ``{rt}`` placeholder."""
        return _to_timedelta(self.raw_overlay.RecordTimeSpan)

    @record_time_span.setter
    @handle_csharp_exceptions
    def record_time_span(self, value: Union[timedelta, Any]) -> None:
        """Set the recording time shown by the ``{rt}`` placeholder.

        :param value: A :class:`~datetime.timedelta` (e.g. :attr:`VideoRecorder.record_time_span`) or a C# ``TimeSpan``.
        """
        self.raw_overlay.RecordTimeSpan = _to_cs_timespan(value)


def _cs_color(value: Union[ColorData, Any]) -> Any:
    """Return the C# ``Color`` for a :class:`~flaui.lib.system.drawing.ColorData`; C# colors pass through.

    :param value: A Python color wrapper or a C# ``System.Drawing.Color``.
    :return: The C# ``Color``.
    """
    return value.cs_object if isinstance(value, ColorData) else value


class CaptureUtilities:
    """Scaling and cursor helpers used by captures (mirrors ``FlaUI.Core.Capturing.CaptureUtilities``)."""

    @staticmethod
    @handle_csharp_exceptions
    def get_scale(original_bounds: Rectangle, settings: Optional[CaptureSettings] = None) -> float:
        """Return the scale factor ``settings`` applies to a capture of ``original_bounds``.

        :param original_bounds: The bounds of the area being captured.
        :param settings: The capture settings; ``None`` means unscaled (``1.0``).
        :return: The scale factor.
        """
        from FlaUI.Core.Capturing import CaptureUtilities as CSCaptureUtilities  # pyright: ignore

        return float(CSCaptureUtilities.GetScale(original_bounds.raw_value, _cs_settings(settings)))

    @staticmethod
    @handle_csharp_exceptions
    def scale_according_to_settings(
        value: Union[Point, Rectangle, Tuple[int, int]],
        settings: Optional[CaptureSettings] = None,
        original_bounds: Optional[Rectangle] = None,
    ) -> Union[Point, Rectangle]:
        """Scale a point or rectangle the way ``settings`` scales a capture.

        A :class:`~flaui.lib.system.drawing.Rectangle` is scaled against itself. A point (a
        :class:`~flaui.lib.system.drawing.Point` or an ``(x, y)`` tuple) needs the
        ``original_bounds`` of the capture it belongs to.

        :param value: The point or rectangle to scale.
        :param settings: The capture settings; ``None`` leaves the value unscaled.
        :param original_bounds: Bounds of the captured area (required for points).
        :return: The scaled point or rectangle (same kind as ``value``; tuples come back as a Point).
        :raises ValueError: If a point is given without ``original_bounds``.
        """
        from FlaUI.Core.Capturing import CaptureUtilities as CSCaptureUtilities  # pyright: ignore

        cs_settings = _cs_settings(settings)
        if isinstance(value, Rectangle):
            return Rectangle(raw_value=CSCaptureUtilities.ScaleAccordingToSettings(value.raw_value, cs_settings))
        if original_bounds is None:
            raise ValueError("original_bounds is required when scaling a point")
        point = value if isinstance(value, Point) else Point(raw_value=value)
        scaled = CSCaptureUtilities.ScaleAccordingToSettings(point.raw_value, original_bounds.raw_value, cs_settings)
        return Point(raw_value=scaled)

    @staticmethod
    @handle_csharp_exceptions
    def capture_cursor() -> Tuple[Any, Point]:
        """Capture the current mouse cursor.

        :return: ``(bitmap, position)``: the cursor as a C# ``Bitmap`` (``None`` when no cursor is
            shown) and its top-left screen position.
        """
        from System.Drawing import Point as CSPoint  # pyright: ignore
        from FlaUI.Core.Capturing import CaptureUtilities as CSCaptureUtilities  # pyright: ignore

        bitmap, position = CSCaptureUtilities.CaptureCursor(CSPoint(0, 0))
        return bitmap, Point(raw_value=position)

    @staticmethod
    @handle_csharp_exceptions
    def delete_object(handle: int) -> bool:
        """Delete a GDI object handle (wraps the Win32 ``DeleteObject``).

        :param handle: The GDI handle (e.g. from ``Bitmap.GetHbitmap()``).
        :return: ``True`` if the handle was deleted.
        """
        from System import IntPtr  # pyright: ignore
        from FlaUI.Core.Capturing import CaptureUtilities as CSCaptureUtilities  # pyright: ignore

        return bool(CSCaptureUtilities.DeleteObject(IntPtr(handle)))
