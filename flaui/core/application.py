"""
This module provides a wrapper for the Application class from the object <class 'FlaUI.Core.Application'> from the module - FlaUI.Core.
It contains methods to launch, attach, kill, dispose, and close an application. It also provides properties to get the name, process ID, exit code, and main window handle of the application.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, List, Optional, Union

from flaui.core.automation_elements import Window

# isort: off
from FlaUI.Core import Application as CSApplication  # pyright: ignore
from FlaUI.Core import AutomationBase as CSAutomationBase  # pyright: ignore
# isort: on

from flaui.core.automation_base import AutomationBase as PyAutomationBase
from flaui.lib.collections import TypeCast


def _coerce_cs_automation(automation: Any) -> Any:
    """Resolve a C# FlaUI.Core.AutomationBase from common Python wrapper shapes."""
    if isinstance(automation, CSAutomationBase):
        return automation
    if isinstance(automation, PyAutomationBase):
        return automation.raw_automation
    if hasattr(automation, "cs_automation"):
        return automation.cs_automation
    raise AttributeError(
        "Invalid automation object: expected C# AutomationBase, flaui.core.automation_base.AutomationBase, "
        "or an object with attribute cs_automation"
    )


class Application:
    """
    Wrapper for an application which should be automated
    """

    _application = CSApplication

    def __enter__(self) -> "Application":
        """Enter the runtime context and return the application instance.

        Enables ``with Application() as app:`` usage. Launch or attach to a process inside the
        ``with`` block; the application is closed and disposed automatically on exit.

        :return: This application instance.
        """
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Exit the runtime context, gracefully closing then disposing the application.

        Mirrors the C# ``IDisposable`` contract: attempts a graceful ``close`` first, then falls
        back to ``dispose``. Never raises — cleanup failures are swallowed so they cannot mask an
        exception raised inside the ``with`` block.

        :param exc_type: The exception type raised in the context, if any.
        :param exc_value: The exception instance raised in the context, if any.
        :param traceback: The traceback for the exception, if any.
        """
        # Nothing was launched/attached, so there is no live process to clean up.
        if self._application is CSApplication:
            return
        try:
            self.close()
        except Exception:
            try:
                self.dispose()
            except Exception:
                logging.debug("Application cleanup failed during context exit", exc_info=True)

    @property
    def name(self) -> str:
        """The name of the application's process.

        :return: Application process name
        """
        return self._application.Name

    @property
    def process_id(self) -> int:
        """The process id of the application

        :return: Application Process ID
        """
        return self._application.ProcessId

    @property
    def is_store_app(self) -> bool:
        """Flag to indicate, if the application is a windows store app.

        :return: True if app is a Windows Store App else False
        """
        return self._application.IsStoreApp

    @property
    def has_exited(self) -> bool:
        """Gets a value indicating whether the associated process has been terminated.

        :return: Exit flag
        """
        return self._application.HasExited

    @property
    def main_window_handle(self) -> int:
        """The current handle (Win32) of the application's main window. Can be IntPtr.Zero if no main window is currently available.

        :return: Main handle ID
        """
        return self._application.MainWindowHandle

    @property
    def exit_code(self) -> int:
        """
        Fetches Exit code of the application.
        Exit code is only available once the application is closed/terminated.

        :return: Exit code
        """
        return self._application.ExitCode

    @property
    def close_timeout(self) -> int:
        """The timeout to wait to close an application gracefully.

        :return: Timeout value
        """
        return self._application.CloseTimeout

    @close_timeout.setter
    def close_timeout(self, value: int) -> None:
        """The timeout to wait to close an application gracefully.

        :param value: Timeout value
        """
        self._application.CloseTimeout = value

    def get_all_top_level_windows(self, automation: Any) -> List[Window]:
        """Gets all top level windows from the application.

        :param automation: The automation object to use.
        :return: Get's all top level windows form the application
        """
        parsed = self._application.GetAllTopLevelWindows(_coerce_cs_automation(automation))
        return [Window(raw_element=element) for element in parsed]

    def get_main_window(self, automation: Any) -> Window:
        """Gets the main window of the applications process.

        :param automation: The automation object to use.
        :return: The main window object as Window element or null if no main window was found within the timeout.
        """
        _automation = _coerce_cs_automation(automation)
        # Robust retrieval with retries and process checks
        # CI hosts (AppVeyor, etc.) often need longer than local desktops for main window.
        total_timeout_ms = 20000 if os.environ.get("CI") else 7000
        poll_interval_ms = 200
        deadline = time.time() + (total_timeout_ms / 1000.0)

        # Initial wait for main handle
        try:
            self.wait_while_main_handle_is_missing(time_out=3000)
        except Exception:
            pass

        last_err: Optional[Exception] = None
        while time.time() < deadline:
            # If process exited or no process associated, break out with error
            try:
                if self.has_exited:
                    last_err = RuntimeError("Application process has exited before main window was available")
                    break
                # ProcessId can be 0 when not yet associated
                if not self.process_id:
                    # small sleep and continue until association is ready
                    time.sleep(poll_interval_ms / 1000.0)
                    continue
            except Exception as proc_err:
                last_err = proc_err  # store and try once more

            # Try to get the main window
            try:
                win = self._application.GetMainWindow(_automation, TypeCast.cs_timespan(poll_interval_ms))
                if win is not None:
                    return Window(raw_element=win)
            except Exception as e:
                last_err = e

            # If main handle still missing, wait a bit and retry
            try:
                if not self.main_window_handle:
                    self.wait_while_main_handle_is_missing(time_out=poll_interval_ms)
            except Exception:
                # swallow and retry
                pass
            time.sleep(poll_interval_ms / 1000.0)

        # Final attempt before giving up
        try:
            win = self._application.GetMainWindow(_automation, TypeCast.cs_timespan(1000))
            if win is not None:
                return Window(raw_element=win)
        except Exception as e:
            last_err = e

        logging.exception("Failed to get main window after retries: %s", last_err)
        if last_err:
            raise last_err
        raise RuntimeError("Failed to get main window: unknown error")

    def launch(self, executable: str, arguments: Optional[str] = None) -> None:
        """Launches the given executable.

        :param executable: The executable to launch.
        :param arguments: Arguments to executable, defaults to None
        """
        self._application = self._application.Launch(executable, arguments)
        # Allow process association and main handle to stabilize for simple apps like Notepad
        try:
            self.wait_while_main_handle_is_missing(2000)
        except Exception:
            pass
        # Fallback: Some modern Windows apps may require AttachOrLaunch to bind process
        try:
            pid = self.process_id
        except Exception:
            pid = 0
        if not pid:
            try:
                self.attach_or_launch(executable)
                self.wait_while_main_handle_is_missing(2000)
            except Exception:
                pass

    def launch_store_app(self, app_user_model_ltd: str, arguments: Optional[str] = None) -> None:
        """Launches a store application.

        :param app_user_model_ltd: The app id of the application to launch.
        :param arguments: The arguments to pass to the application., defaults to None
        """
        self._application = self._application.LaunchStoreApp(app_user_model_ltd, arguments)

    def attach(self, process: Union[str, int]) -> None:
        """Attaches to a given process id.

        :param process: The id/process/path of executable of the process to attach to.
        """
        self._application = self._application.Attach(process)

    def attach_or_launch(self, process: Union[str, int]) -> None:
        """Attaches or launches the given process.

        :param process: The id/process/path of executable of the process to attach to.
        """
        from System.Diagnostics import ProcessStartInfo  # pyright: ignore

        _process = ProcessStartInfo(process)
        self._application = self._application.AttachOrLaunch(_process)

    def kill(self) -> None:
        """Kills the applications and waits until it is closed."""
        self._application.Kill()

    def dispose(self) -> None:
        """Disposes the application."""
        self._application.Dispose()

    def close(self, kill_if_close_fails: bool = True) -> bool:
        """Closes the application. Force-closes it after a small timeout.

        :param kill_if_close_fails: A flag to indicate if the process should be killed if closing fails within the timeout, defaults to True
        :return: Returns true if the application was closed normally and false if it could not be closed gracefully.
        """
        return self._application.Close(kill_if_close_fails)

    def wait_while_main_handle_is_missing(self, time_out: Optional[int] = None) -> bool:
        """Waits until the main handle is set.

        :param time_out: An optional timeout in milliseconds. If null is passed, the timeout is infinite., defaults to None
        :return: True if a main window handle is found, else False.
        """
        return self._application.WaitWhileMainHandleIsMissing(TypeCast.cs_timespan(time_out) if time_out else time_out)

    def wait_while_busy(self, time_out: Optional[int] = None) -> bool:
        """Waits as long as the application is busy.

        :param time_out: An optional timeout in milliseconds. If null is passed, the timeout is infinite., defaults to None
        :return: True if the application is idle, else False.
        """
        return self._application.WaitWhileBusy(TypeCast.cs_timespan(time_out) if time_out else time_out)
