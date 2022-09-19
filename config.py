import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    BIN_HOME: str = os.path.join(Path(__file__).parent.resolve(), "flaui", "bin")


settings = Settings()
