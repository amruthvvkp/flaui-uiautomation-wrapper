"""Utilities for unit or example tests"""

from pathlib import Path
import time
from typing import Optional

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
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


class FlaUITestBase:
    def __init__(
        self,
        ui_automation_type: UIAutomationTypes,
        app_type: str,
        automation: Optional[Automation] = None,
        executable: Optional[Path] = None,
    ) -> None:
        """Initialize FlaUITestBase."""
        self.ui_automation_type = ui_automation_type
        self.app_type = app_type
        self.automation = Automation(ui_automation_type) or automation
        self.executable_path = (
            str(test_settings.WPF_TEST_APP_EXE if app_type == "WPF" else test_settings.WINFORMS_TEST_APP_EXE)
            or executable
        )

    def launch_test_app(self) -> None:
        """Launch the test application."""
        self.automation.application.launch(str(self.executable_path))
        time.sleep(0.5)  # Wait for the application to start
        self.automation.application.wait_while_main_handle_is_missing(2000)

    def restart_test_app(self) -> None:
        """Restart the test application."""
        self.close_test_app()
        self.launch_test_app()

    def close_test_app(self) -> None:
        """Close the test application."""
        self.automation.application.kill()
        timeout = 2  # seconds
        start_time = time.time()

        try:
            while not self.automation.application.has_exited:
                if time.time() - start_time > timeout:
                    break
                time.sleep(0.1)
        except Exception:
            pass
        self.automation.application.dispose()
