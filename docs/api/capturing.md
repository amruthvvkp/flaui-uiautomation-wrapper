# Capturing & Video

Screen/element capture and video recording, ported from ``FlaUI.Core.Capturing``. ``Capture``
provides static helpers that return a ``CaptureImage`` (savable via ``to_file`` and usable as a
context manager). ``VideoRecorder`` records the screen to a file and requires ffmpeg
(see ``VideoRecorder.download_ffmpeg``).

::: flaui.core.capturing.Capture

::: flaui.core.capturing.CaptureImage

::: flaui.core.capturing.CaptureSettings

::: flaui.core.capturing.VideoRecorder

::: flaui.core.capturing.VideoRecorderSettings

::: flaui.core.capturing.VideoFormat
