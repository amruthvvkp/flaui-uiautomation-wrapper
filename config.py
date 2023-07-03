from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    BIN_HOME: Path = Path(__file__).parent.joinpath("flaui", "bin")
    WPF_TEST_APP: Path = Path(__file__).parent.joinpath("test_applications", "WpfApplication.exe")
    WPF_TEST_APP_PROCESS: str = "WpfApplication.exe"


settings = Settings()
