from pathlib import Path

from pydantic import FilePath
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Holds all common settings for the tool"""
    BIN_HOME: Path = Path(__file__).parent.joinpath("flaui", "bin")


class TestSettings(BaseSettings):
    """Holds all settings for the unit test usages"""
    WPF_TEST_APP_EXE: FilePath = Path(__file__).parent.joinpath("test_applications", "WPFApplication", "WpfApplication.exe")
    WPF_TEST_APP_PROCESS: str = "WpfApplication.exe"
    WINFORMS_TEST_APP_EXE: FilePath = Path(__file__).parent.joinpath("test_applications", "WINFORMSApplication", "WinFormsApplication.exe")
    WINFORMS_TEST_APP_PROCESS: str = "WinFormsApplication.exe"


settings = Settings()
test_settings = TestSettings()
