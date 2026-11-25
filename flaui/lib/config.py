"""Library settings, read once at import time from ``FLAUI_*`` environment variables.

Every setting can be overridden with an environment variable carrying the ``FLAUI_`` prefix (names
are case-insensitive). Set them **before** the first ``flaui`` import, because :data:`settings` is
created when this module is imported. See the *Configuration & logging* guide for the full list.

| Environment variable | Setting | Default |
|----------------------|---------|---------|
| ``FLAUI_LOG_CSHARP`` | :attr:`Settings.LOG_CSHARP` | ``False`` |
| ``FLAUI_LOG_CSHARP_LEVEL`` | :attr:`Settings.LOG_CSHARP_LEVEL` | unset |
| ``FLAUI_MAIN_WINDOW_TIMEOUT`` | :attr:`Settings.MAIN_WINDOW_TIMEOUT` | unset (7 s, or 20 s when ``CI`` is set) |
| ``FLAUI_BIN_HOME`` | :attr:`Settings.BIN_HOME` | the package's bundled ``flaui/bin`` |
"""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

#: Directory holding the FlaUI assemblies that ship inside the wheel.
DEFAULT_BIN_HOME: Path = Path(__file__).parent.parent.parent.joinpath("flaui", "bin")


class Settings(BaseSettings):
    """Holds all user-controllable settings for the library.

    Every field reads the matching ``FLAUI_<NAME>`` environment variable. The ``FLAUI_`` prefix
    keeps the library from picking up unrelated variables (a generic ``BIN_HOME`` is ignored).
    """

    model_config = SettingsConfigDict(env_prefix="FLAUI_", case_sensitive=False, extra="ignore")

    BIN_HOME: Path = Field(
        default=DEFAULT_BIN_HOME,
        description=(
            "Directory the PythonNet bridge loads the FlaUI assemblies from (env FLAUI_BIN_HOME). "
            "Override only to test a different FlaUI build; the bundled DLLs are the supported set."
        ),
    )
    LOG_CSHARP: bool = Field(
        default=False,
        validation_alias="FLAUI_LOG_CSHARP",
        description="Route FlaUI C# log output into Python logging when True (env FLAUI_LOG_CSHARP).",
    )
    LOG_CSHARP_LEVEL: Optional[str] = Field(
        default=None,
        validation_alias="FLAUI_LOG_CSHARP_LEVEL",
        description=(
            "Python logging level name (e.g. DEBUG, INFO) applied to the C# log sink when LOG_CSHARP is "
            "True (env FLAUI_LOG_CSHARP_LEVEL)."
        ),
    )
    MAIN_WINDOW_TIMEOUT: Optional[int] = Field(
        default=None,
        ge=0,
        description=(
            "Milliseconds Application.get_main_window waits for the main window (env "
            "FLAUI_MAIN_WINDOW_TIMEOUT). Unset means 7000, or 20000 when the CI variable is set. An "
            "explicit Automation(timeout=...) takes precedence."
        ),
    )


settings = Settings()


class VideoRecordingMode(Enum):
    """Defines how videos should be recorded for the tests."""

    NONE = None
    ONEPERTEST = "OnePerTest"
    ONEPERFIXTURE = "OnePerFixture"
