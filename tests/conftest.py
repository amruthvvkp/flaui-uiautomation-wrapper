import pytest

from config import settings
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()


def close_wpf_application_process():
    import os

    import psutil

    for process in (process for process in psutil.process_iter() if process.name() == "WpfApplication.exe"):
        process.terminate()


@pytest.fixture()
def wpf_application():
    from FlaUI.Core import Application  # pyright: ignore

    close_wpf_application_process()
    application = Application.Launch(settings.WPF_TEST_APP)
    return application


@pytest.fixture()
def uia2_wpf_app(wpf_application):
    from FlaUI.UIA2 import UIA2Automation  # pyright: ignore

    automation = UIA2Automation()
    main_window = wpf_application.GetMainWindow(automation)
    yield main_window

    main_window.Close()


@pytest.fixture()
def uia3_wpf_app(wpf_application):
    from FlaUI.UIA3 import UIA3Automation  # pyright: ignore

    automation = UIA3Automation()
    main_window = wpf_application.GetMainWindow(automation)
    yield main_window

    main_window.Close()
