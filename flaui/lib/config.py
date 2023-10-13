"""This module holds all settings for the tool."""
from pathlib import Path

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Holds all common settings for the tool"""
    BIN_HOME: Path = Path(__file__).parent.parent.parent.joinpath("flaui", "bin")


settings = Settings()
