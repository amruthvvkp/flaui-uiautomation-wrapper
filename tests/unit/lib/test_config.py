"""Unit tests for flaui.lib.config settings and enums."""

from pathlib import Path

import pytest

from flaui.lib.config import Settings, VideoRecordingMode, settings


def test_settings_bin_home_points_to_bundled_dlls() -> None:
    """BIN_HOME resolves to the existing flaui/bin directory."""
    assert isinstance(settings.BIN_HOME, Path)
    assert settings.BIN_HOME.name == "bin"
    assert settings.BIN_HOME.exists()


def test_log_csharp_defaults() -> None:
    """LOG_CSHARP defaults to False and LOG_CSHARP_LEVEL to None."""
    fresh = Settings()
    assert fresh.LOG_CSHARP is False
    assert fresh.LOG_CSHARP_LEVEL is None


def test_log_csharp_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """LOG_CSHARP and its level are read from FLAUI_LOG_CSHARP* env vars."""
    monkeypatch.setenv("FLAUI_LOG_CSHARP", "1")
    monkeypatch.setenv("FLAUI_LOG_CSHARP_LEVEL", "DEBUG")
    fresh = Settings()
    assert fresh.LOG_CSHARP is True
    assert fresh.LOG_CSHARP_LEVEL == "DEBUG"


def test_video_recording_mode_members() -> None:
    """VideoRecordingMode exposes the expected members and values."""
    assert VideoRecordingMode.NONE.value is None
    assert VideoRecordingMode.ONEPERTEST.value == "OnePerTest"
    assert VideoRecordingMode.ONEPERFIXTURE.value == "OnePerFixture"
