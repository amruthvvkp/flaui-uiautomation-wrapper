"""This module holds all settings for the tool."""

from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Holds all common settings for the tool"""

    BIN_HOME: Path = Path(__file__).parent.parent.parent.joinpath("flaui", "bin")


settings = Settings()


class VideoRecordingMode(Enum):
    """Defines how videos should be recorded for the tests."""

    NONE = None
    ONEPERTEST = "OnePerTest"
    ONEPERFIXTURE = "OnePerFixture"
