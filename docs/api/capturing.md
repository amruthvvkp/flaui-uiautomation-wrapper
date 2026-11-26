# Capturing & Video

Screen/element capture and video recording, ported from ``FlaUI.Core.Capturing``. ``Capture``
provides static helpers that return a ``CaptureImage`` (savable via ``to_file`` and usable as a
context manager). ``VideoRecorder`` records the screen to a file and requires ffmpeg
(see ``VideoRecorder.download_ffmpeg``).

## Settings

``CaptureSettings`` and ``VideoRecorderSettings`` are Pydantic models: values are validated in
Python (for example ``output_scale`` must be positive and ``frame_rate`` at least 1) before they
reach FlaUI. ``cs_object`` builds the C# settings object and ``from_cs`` reads one back, so
``CaptureImage.settings`` returns the typed model the image was captured with.

| C# property | Python field | Default |
|-------------|--------------|---------|
| `CaptureSettings.OutputWidth` | `output_width` | `-1` (keep aspect ratio) |
| `CaptureSettings.OutputHeight` | `output_height` | `-1` (keep aspect ratio) |
| `CaptureSettings.OutputScale` | `output_scale` | `1.0` |
| `VideoRecorderSettings.ffmpegPath` | `ffmpeg_path` | `None` |
| `VideoRecorderSettings.FrameRate` | `frame_rate` | `5` |
| `VideoRecorderSettings.TargetVideoPath` | `target_video_path` | `None` |
| `VideoRecorderSettings.UseCompressedImages` | `use_compressed_images` | `True` |
| `VideoRecorderSettings.VideoFormat` | `video_format` | `VideoFormat.x264` |
| `VideoRecorderSettings.VideoQuality` | `video_quality` | `0` |
| `VideoRecorderSettings.EncodeWithLowPriority` | `encode_with_low_priority` | `False` |
| `VideoRecorderSettings.LogMissingFrames` | `log_missing_frames` | `True` |

## Overlays

``MouseOverlay`` and ``InfoOverlay`` are built from the image they draw on and passed straight to
``CaptureImage.apply_overlays``. Raw C# ``ICaptureOverlay`` objects are still accepted, and the two
can be mixed in one call.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:capture_overlays"
    ```

=== "C#"

    ```csharp
    using (var image = Capture.Element(window))
    {
        var info = new InfoOverlay(image)
        {
            OverlayStringFormat = "{dt:HH:mm:ss} / {name}",
            OverlayPosition = InfoOverlayPosition.BottomRight,
            OverlayTextColor = Color.Yellow,
        };
        image.ApplyOverlays(new MouseOverlay(image), info).ToFile(@"C:\temp\annotated.png");
    }
    ```

Durations are `datetime.timedelta` on the Python side: ``VideoRecorder.record_time_span`` and
``InfoOverlay.record_time_span`` (the ``{rt}`` placeholder) both use it. The overlay's font stays a
C# ``System.Drawing.Font``.

## Recording video

The frame callback receives the running recorder, so each frame can stamp the elapsed time:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:video_recorder"
    ```

=== "C#"

    ```csharp
    var settings = new VideoRecorderSettings
    {
        ffmpegPath = @"C:\tools\ffmpeg.exe",
        TargetVideoPath = @"C:\temp\run.mp4",
        FrameRate = 10,
        VideoFormat = VideoFormat.xvid,
    };
    using (var recorder = new VideoRecorder(settings, r =>
    {
        var image = Capture.MainScreen(new CaptureSettings { OutputScale = 0.5 });
        var info = new InfoOverlay(image) { OverlayStringFormat = @"{rt:hh\:mm\:ss}", RecordTimeSpan = r.RecordTimeSpan };
        return image.ApplyOverlays(info, new MouseOverlay(image));
    }))
    {
        // drive the application
    }
    ```

## Reference

::: flaui.core.capturing.Capture

::: flaui.core.capturing.CaptureImage

::: flaui.core.capturing.CaptureSettings

::: flaui.core.capturing.ICaptureOverlay

::: flaui.core.capturing.OverlayBase

::: flaui.core.capturing.MouseOverlay

::: flaui.core.capturing.InfoOverlay

::: flaui.core.capturing.InfoOverlayPosition

::: flaui.core.capturing.CaptureUtilities

::: flaui.core.capturing.VideoRecorder

::: flaui.core.capturing.VideoRecorderSettings

::: flaui.core.capturing.VideoFormat
