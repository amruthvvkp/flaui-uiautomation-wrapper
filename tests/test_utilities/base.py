# Utilities for unit or example tests


import psutil

from tests.test_utilities.config import test_settings


def force_close_test_application_process():
    """Close the test application process."""
    target_processes = {test_settings.WPF_TEST_APP_PROCESS, test_settings.WINFORMS_TEST_APP_PROCESS}

    for process in psutil.process_iter(["name"]):
        try:
            if process.info["name"] in target_processes:
                process.terminate()
                process.wait(timeout=5)  # Wait for the process to terminate
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            # Handle exceptions if the process disappears or can't be accessed
            continue

    # Check if any processes are still running and force kill them
    for process in psutil.process_iter(["name"]):
        if process.info["name"] in target_processes:
            try:
                process.kill()  # Force kill if terminate didn't work
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
