"""Unit tests for the capturing/video wrappers (GH-95).

Settings objects and enums only need the PythonNet bridge (set up by the global conftest); live
screen capture is exercised in the UI suite.
"""

from flaui.core.capturing import CaptureSettings, VideoFormat, VideoRecorderSettings


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
