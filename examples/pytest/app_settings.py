"""Test-suite settings with pydantic-settings: one typed, validated place for everything configurable.

The *Test design tips* guide includes this file. Values come from (highest priority first) keyword
arguments, ``EXAMPLE_*`` environment variables, a ``.env`` file, then the defaults below, so the
same suite runs locally and in CI without code changes::

    $env:EXAMPLE_AUTOMATION_TYPE = "UIA2"
    $env:EXAMPLE_LAUNCH_TIMEOUT_MS = "20000"
    uv run pytest examples/pytest
"""

from pathlib import Path

# --8<-- [start:settings]
from flaui.lib.enums import UIAutomationTypes
from pydantic import Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class ExampleSettings(BaseSettings):
    """Everything a run might change, validated once at start-up."""

    # A prefix keeps unrelated environment variables (PATH, APP_PATH, ...) from leaking in.
    model_config = SettingsConfigDict(env_prefix="EXAMPLE_", env_file=".env", extra="ignore")

    # FilePath fails fast at start-up if the executable is missing, not mid-test.
    app_path: FilePath = REPO_ROOT / "test_applications" / "WPFApplication" / "WpfApplication.exe"
    app_title: str = "FlaUI WPF Test App"
    # "UIA2" / "UIA3" strings from the environment are converted to the enum for you.
    automation_type: UIAutomationTypes = UIAutomationTypes.UIA3
    launch_timeout_ms: int = Field(default=10_000, ge=1_000)
    artifacts_dir: Path = REPO_ROOT / "artifacts"


settings = ExampleSettings()  # created once at import; tests import this instance
# --8<-- [end:settings]
