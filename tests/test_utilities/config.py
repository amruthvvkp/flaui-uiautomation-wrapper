"""Holds all settings for the unit test usages"""

from enum import Enum
from pathlib import Path

from pydantic import FilePath
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    """Holds all settings for the unit test usages"""

    WPF_TEST_APP_EXE: FilePath = Path(__file__).parent.parent.parent.joinpath(
        "test_applications", "WPFApplication", "WpfApplication.exe"
    )
    WPF_TEST_APP_PROCESS: str = "WpfApplication.exe"
    WINFORMS_TEST_APP_EXE: FilePath = Path(__file__).parent.parent.parent.joinpath(
        "test_applications", "WinFormsApplication", "WinFormsApplication.exe"
    )
    WINFORMS_TEST_APP_PROCESS: str = "WinFormsApplication.exe"


test_settings = TestSettings()


class ApplicationType(Enum):
    """Test Application Type"""

    WinForms = "WinForms"
    Wpf = "Wpf"
