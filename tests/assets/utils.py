# Utilities for unit or example tests


import psutil

from tests.assets.config import test_settings


def force_close_test_application_process():
    """Close the test application process."""
    for process in (
        process
        for process in psutil.process_iter()
        if process.name() == test_settings.WPF_TEST_APP_PROCESS
        or process.name() == test_settings.WINFORMS_TEST_APP_PROCESS
    ):
        process.terminate()
