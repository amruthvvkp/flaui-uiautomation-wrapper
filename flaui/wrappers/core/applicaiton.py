# Auto-Generated wrapper for Application class from the object <class 'FlaUI.Core.Application'> from the module - FlaUI.Core

from __future__ import annotations

from typing import Any, Optional, Union

from FlaUI.Core import Application as CSApplication  # pyright: ignore  # type: ignore  # noqa: E402
from flaui.lib.cast_type_converter import TypeConverter


class Application:
    """
    Wrapper for an application which should be automated
    """

    def __init__(self, application: Optional[Any] = None):
        self.application = application if application else CSApplication()

        self.name: str = self.application.Name  # The name of the application's process.
        self.process_id: int = self.application.ProcessId  # The process id of the application.
        self.is_store_app: bool = (
            self.application.IsStoreApp
        )  # Flag to indicate, if the application is a windows store app.
        self.close_timeout: int = (
            self.application.CloseTimeout
        )  # The timeout to wait to close an application gracefully.
        self.has_exited: bool = (
            self.application.HasExited
        )  # Gets a value indicating whether the associated process has been terminated.
        self.main_window_handle: int = (
            self.application.MainWindowHandle
        )  # The current handle (Win32) of the application's main window. Can be IntPtr.Zero if no main window is currently available.
        self.exit_code: int = (
            self.application.ExitCode
        )  # Gets the value that the associated process specified when it terminated.

    @classmethod
    def return_application(cls, application: Any) -> Application:
        """Returns an instance of the Application class

        :param cls: Reference to the class itself
        :param application: Application object
        :return: New Application class
        """
        return Application(application)

    def launch(self, executable: str, arguments: Optional[str] = None) -> Application:
        """Launches the given executable.

        :param executable: The executable to launch.
        :param arguments: Arguments to executable, defaults to None
        :return: An application instance which is launched to the process.
        """
        return self.return_application(self.application.Launch(executable, arguments))

    def get_all_top_level_windows(self) -> Any:  # TODO: Update this to return Element object
        """Gets all top level windows from the application.

        :param automation: The automation object to use.
        :return: Get's all top level windows form the application
        """
        # return element
        return TypeConverter.cast_to_py_list(self.application.GetAllTopLevelWindows())

    def launch_store_app(self, app_user_model_ltd: str, arguments: Optional[str] = None) -> Application:
        """Launches a store application.

        :param app_user_model_ltd: The app id of the application to launch.
        :param arguments: The arguments to pass to the application., defaults to None
        :return: An application instance which is launched to the process.
        """
        return self.application.LaunchStoreApp(app_user_model_ltd, arguments)

    def get_main_window(self) -> Any:  # TODO: Update this to return Element object
        """Gets the main window of the applications process.

        :param automation: The automation object to use.
        :return: The main window object as Window element or null if no main window was found within the timeout.
        """

        # return element
        return self.application.GetMainWindow()

    def attach(self, process: Union[str, int]) -> Application:
        """Attaches to a given process id.

        :param process: The id/process/path of executable of the process to attach to.
        :return: An application instance which is attached to the process.
        """
        return self.return_application(self.application.Attach(process))

    def attach_or_launch(self, process: Union[str, int]) -> Application:
        """Attaches or launches the given process.

        :param process: The id/process/path of executable of the process to attach to.
        :return: An application instance which is attached to the process.
        """
        return self.return_application(self.application.AttachOrLaunch(process))

    def kill(self) -> None:
        """Kills the applications and waits until it is closed."""
        return self.application.Kill()

    def dispose(self) -> None:
        """Disposes the application."""
        return self.application.Dispose()

    def close(self, kill_if_close_fails: bool = True) -> bool:
        """Closes the application. Force-closes it after a small timeout.

        :param kill_if_close_fails: A flag to indicate if the process should be killed if closing fails within the timeout, defaults to True
        :return: Returns true if the application was closed normally and false if it could not be closed gracefully.
        """
        return self.application.Close(kill_if_close_fails)

    def wait_while_main_handle_is_missing(self, time_out: Optional[int] = None) -> bool:
        """Waits until the main handle is set.

        :param time_out: An optional timeout. If null is passed, the timeout is infinite., defaults to None
        :return: True a main window handle was found, false otherwise.
        """
        return self.application.WaitWhileMainHandleIsMissing(time_out)

    def wait_while_busy(self, time_out: Optional[int] = None) -> bool:
        """Waits as long as the application is busy.

        :param time_out: An optional timeout. If null is passed, the timeout is infinite., defaults to None
        :return: True if the application is idle, false otherwise.
        """
        return self.application.WaitWhileBusy(time_out)
