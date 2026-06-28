"""This module holds all settings for the tool."""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Holds all common settings for the tool"""

    BIN_HOME: Path = Path(__file__).parent.parent.parent.joinpath("flaui", "bin")

    # Opt-in: route FlaUI's C# logging into Python's ``logging`` for unified telemetry.
    # Enable by setting the environment variable ``FLAUI_LOG_CSHARP=1``.
    LOG_CSHARP: bool = Field(
        default=False,
        validation_alias="FLAUI_LOG_CSHARP",
        description="Route FlaUI C# log output into Python logging when True.",
    )
    # Optional level name (e.g. ``DEBUG``, ``INFO``) for the Python logger the C# sink writes to.
    LOG_CSHARP_LEVEL: Optional[str] = Field(
        default=None,
        validation_alias="FLAUI_LOG_CSHARP_LEVEL",
        description="Python logging level name applied to the C# log sink when LOG_CSHARP is True.",
    )


settings = Settings()


class VideoRecordingMode(Enum):
    """Defines how videos should be recorded for the tests."""

    NONE = None
    ONEPERTEST = "OnePerTest"
    ONEPERFIXTURE = "OnePerFixture"
