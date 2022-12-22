import os
from pathlib import Path
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    BIN_HOME: str = os.path.join(Path(__file__).parent.resolve(), "flaui", "bin")
    WRAPPERS_HOME: str = os.path.join(Path(__file__).parent.resolve(), "flaui", "wrappers_temp")
    FLAUI_HOME: str = str(Path(r"C:\Users\Amruth.Vithala\Projects\FlaUI\src"))


settings = Settings()
