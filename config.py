import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    BIN_HOME: str = os.path.join(Path(__file__).parent.resolve(), "flaui", "bin")
    WPF_TEST_APP: str = os.path.join(Path(__file__).parent.resolve(), "test_applications", "WpfApplication.exe")
    WPF_TEST_APP_PROCESS: str = "WpfApplication.exe"


settings = Settings()
