"""Unit tests for flaui.lib.config settings and enums."""

from pathlib import Path

import pytest

from flaui.lib.config import DEFAULT_BIN_HOME, Settings, VideoRecordingMode, settings


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


def test_generic_bin_home_env_var_is_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    """An unprefixed BIN_HOME must not redirect where the FlaUI DLLs are loaded from."""
    monkeypatch.setenv("BIN_HOME", r"C:\somewhere-else")
    monkeypatch.delenv("FLAUI_BIN_HOME", raising=False)
    assert Settings().BIN_HOME == DEFAULT_BIN_HOME


def test_flaui_bin_home_overrides_dll_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    """FLAUI_BIN_HOME is the one supported way to point the bridge at other DLLs."""
    monkeypatch.setenv("FLAUI_BIN_HOME", r"C:\custom-flaui")
    assert Settings().BIN_HOME == Path(r"C:\custom-flaui")


def test_main_window_timeout_setting(monkeypatch: pytest.MonkeyPatch) -> None:
    """MAIN_WINDOW_TIMEOUT defaults to None and reads FLAUI_MAIN_WINDOW_TIMEOUT (ms)."""
    monkeypatch.delenv("FLAUI_MAIN_WINDOW_TIMEOUT", raising=False)
    assert Settings().MAIN_WINDOW_TIMEOUT is None
    monkeypatch.setenv("FLAUI_MAIN_WINDOW_TIMEOUT", "15000")
    assert Settings().MAIN_WINDOW_TIMEOUT == 15000


def test_main_window_timeout_rejects_negative(monkeypatch: pytest.MonkeyPatch) -> None:
    """A negative timeout is a configuration error, reported when settings load."""
    monkeypatch.setenv("FLAUI_MAIN_WINDOW_TIMEOUT", "-1")
    with pytest.raises(ValueError):
        Settings()


def test_video_recording_mode_members() -> None:
    """VideoRecordingMode exposes the expected members and values."""
    assert VideoRecordingMode.NONE.value is None
    assert VideoRecordingMode.ONEPERTEST.value == "OnePerTest"
    assert VideoRecordingMode.ONEPERFIXTURE.value == "OnePerFixture"
