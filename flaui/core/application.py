"""
This module provides a wrapper for the Application class from the object <class 'FlaUI.Core.Application'> from the module - FlaUI.Core.
It contains methods to launch, attach, kill, dispose, and close an application. It also provides properties to get the name, process ID, exit code, and main window handle of the application.
"""

from __future__ import annotations

from typing import Any, List, Optional, Union

from flaui.core.automation_elements import Window
from flaui.lib.collections import TypeCast

# isort: off
from FlaUI.Core import Application as CSApplication  # pyright: ignore
# isort: on


class Application:
    """
    Wrapper for an application which should be automated
    """

    _application = CSApplication

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
        parsed = TypeCast.py_list(self._application.GetAllTopLevelWindows(automation))
        return [Window(raw_element=element) for element in parsed]

    def get_main_window(self, automation: Any) -> Window:
        """Gets the main window of the applications process.

        :param automation: The automation object to use.
        :return: The main window object as Window element or null if no main window was found within the timeout.
        """
        return Window(raw_element=self._application.GetMainWindow(automation))

    def launch(self, executable: str, arguments: Optional[str] = None) -> None:
        """Launches the given executable.

        :param executable: The executable to launch.
        :param arguments: Arguments to executable, defaults to None
        """
        self._application = self._application.Launch(executable, arguments)

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

        :param time_out: An optional timeout. If null is passed, the timeout is infinite., defaults to None
        :return: True if a main window handle is found, else False.
        """
        return self._application.WaitWhileMainHandleIsMissing(time_out)

    def wait_while_busy(self, time_out: Optional[int] = None) -> bool:
        """Waits as long as the application is busy.

        :param time_out: An optional timeout. If null is passed, the timeout is infinite., defaults to None
        :return: True if the application is idle, else False.
        """
        return self._application.WaitWhileBusy(time_out)
