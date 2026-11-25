"""Unit tests for library logging hygiene and the main-window timeout resolution.

A library must log through its own named loggers and leave handler configuration to the application.
Logging through the root logger (``logging.info(...)``) silently installs a root ``StreamHandler`` via
``logging.basicConfig`` when the application has not configured logging yet.
"""

import logging
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

import flaui.core.application as application_module
from flaui.core.application import (
    DEFAULT_CI_MAIN_WINDOW_TIMEOUT_MS,
    DEFAULT_MAIN_WINDOW_TIMEOUT_MS,
    _main_window_timeout_ms,
)

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_flaui_logger_has_null_handler() -> None:
    """The package attaches a NullHandler to the ``flaui`` logger hierarchy."""
    assert any(isinstance(h, logging.NullHandler) for h in logging.getLogger("flaui").handlers)


def test_bridge_setup_leaves_root_logger_untouched() -> None:
    """Setting up the bridge in a fresh interpreter must not add handlers to the root logger."""
    script = (
        "import logging\n"
        "from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge\n"
        "setup_pythonnet_bridge()\n"
        "from flaui.modules.automation import Automation\n"
        "print(len(logging.getLogger().handlers))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", script], cwd=REPO_ROOT, capture_output=True, text=True, timeout=120, check=True
    )
    assert result.stdout.strip().splitlines()[-1] == "0", result.stderr


def test_no_root_logger_calls_in_library() -> None:
    """Library modules never call the module-level ``logging.<level>()`` helpers."""
    offenders = []
    for path in (REPO_ROOT / "flaui").rglob("*.py"):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for level in ("debug", "info", "warning", "error", "exception", "critical"):
                if f"logging.{level}(" in stripped:
                    offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}")
    assert offenders == []


class TestMainWindowTimeout:
    """Precedence: Automation(timeout=...) > FLAUI_MAIN_WINDOW_TIMEOUT > built-in default."""

    def test_explicit_automation_timeout_wins(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """An explicit ``timeout`` on the Automation object is used as-is."""
        monkeypatch.setattr(application_module.settings, "MAIN_WINDOW_TIMEOUT", 9999)
        assert _main_window_timeout_ms(SimpleNamespace(timeout=2500)) == 2500

    def test_setting_used_when_no_explicit_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Without an explicit timeout, the FLAUI_MAIN_WINDOW_TIMEOUT setting applies."""
        monkeypatch.setattr(application_module.settings, "MAIN_WINDOW_TIMEOUT", 12000)
        assert _main_window_timeout_ms(SimpleNamespace(timeout=None)) == 12000

    def test_default_local(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Locally (no CI variable) the default is 7 s; raw C# automations have no timeout attribute."""
        monkeypatch.setattr(application_module.settings, "MAIN_WINDOW_TIMEOUT", None)
        monkeypatch.delenv("CI", raising=False)
        assert _main_window_timeout_ms(object()) == DEFAULT_MAIN_WINDOW_TIMEOUT_MS == 7000

    def test_default_on_ci(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When the CI variable is set, the default is 20 s."""
        monkeypatch.setattr(application_module.settings, "MAIN_WINDOW_TIMEOUT", None)
        monkeypatch.setenv("CI", "true")
        assert _main_window_timeout_ms(SimpleNamespace(timeout=None)) == DEFAULT_CI_MAIN_WINDOW_TIMEOUT_MS == 20000
