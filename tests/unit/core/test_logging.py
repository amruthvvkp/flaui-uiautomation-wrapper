"""Unit tests for the C#->Python logging bridge (GH-96).

These only need the PythonNet bridge (set up by the global conftest), not a running application.
"""

import logging
from typing import Generator

from FlaUI.Core.Logging import Logger as CSLogger  # type: ignore
import pytest

from flaui.core.logging import (
    CSHARP_LOGGER_NAME,
    disable_csharp_logging,
    enable_csharp_logging,
    maybe_enable_from_settings,
)


@pytest.fixture(autouse=True)
def _restore_default_logger() -> Generator[None, None, None]:
    """Ensure each test starts and ends without an installed sink."""
    disable_csharp_logging()
    yield
    disable_csharp_logging()


class TestEnableCsharpLogging:
    """Validate that C# log calls are forwarded into Python logging."""

    def test_routes_messages_with_levels(self, caplog: pytest.LogCaptureFixture) -> None:
        """C# Info/Warn/Error/Fatal map to the matching Python levels."""
        enable_csharp_logging()
        with caplog.at_level(logging.DEBUG, logger=CSHARP_LOGGER_NAME):
            CSLogger.Default.Info("info-msg")
            CSLogger.Default.Warn("warn-msg")
            CSLogger.Default.Error("error-msg")
            CSLogger.Default.Fatal("fatal-msg")

        by_message = {record.message: record.levelno for record in caplog.records}
        assert by_message["info-msg"] == logging.INFO
        assert by_message["warn-msg"] == logging.WARNING
        assert by_message["error-msg"] == logging.ERROR
        assert by_message["fatal-msg"] == logging.CRITICAL

    def test_forwards_to_custom_logger(self, caplog: pytest.LogCaptureFixture) -> None:
        """A caller-supplied logger receives the C# messages."""
        custom = logging.getLogger("flaui.csharp.custom")
        enable_csharp_logging(logger=custom)
        with caplog.at_level(logging.DEBUG, logger="flaui.csharp.custom"):
            CSLogger.Default.Info("custom-target")
        assert any(record.message == "custom-target" for record in caplog.records)

    def test_disable_stops_routing(self, caplog: pytest.LogCaptureFixture) -> None:
        """After ``disable_csharp_logging`` no further messages reach Python logging."""
        enable_csharp_logging()
        disable_csharp_logging()
        with caplog.at_level(logging.DEBUG, logger=CSHARP_LOGGER_NAME):
            CSLogger.Default.Info("should-not-appear")
        assert not any(record.message == "should-not-appear" for record in caplog.records)


class TestMaybeEnableFromSettings:
    """Validate the env-flag driven auto-enable used during bridge setup."""

    def test_noop_when_flag_off(self, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
        """With ``LOG_CSHARP`` off, nothing is installed."""
        from flaui.lib import config

        monkeypatch.setattr(config.settings, "LOG_CSHARP", False, raising=False)
        maybe_enable_from_settings()
        with caplog.at_level(logging.DEBUG, logger=CSHARP_LOGGER_NAME):
            CSLogger.Default.Info("flag-off")
        assert not any(record.message == "flag-off" for record in caplog.records)

    def test_enables_when_flag_on(self, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
        """With ``LOG_CSHARP`` on, the sink is installed and routes messages."""
        from flaui.lib import config

        monkeypatch.setattr(config.settings, "LOG_CSHARP", True, raising=False)
        monkeypatch.setattr(config.settings, "LOG_CSHARP_LEVEL", "DEBUG", raising=False)
        maybe_enable_from_settings()
        with caplog.at_level(logging.DEBUG, logger=CSHARP_LOGGER_NAME):
            CSLogger.Default.Info("flag-on")
        assert any(record.message == "flag-on" for record in caplog.records)
