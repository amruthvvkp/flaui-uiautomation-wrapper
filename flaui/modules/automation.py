from typing import Any, List, Optional, Union

from pydantic import validate_arguments

from FlaUI.Core import Application as CSApplication  # pyright: ignore
from flaui.lib.collections import TypeCast  # pyright: ignore
from flaui.lib.enums import UIAutomationTypes
from FlaUI.UIA2 import UIA2Automation  # pyright: ignore
from FlaUI.UIA3 import UIA3Automation  # pyright: ignore
from flaui.wrappers.core.application import Application
from flaui.wrappers.core.automation_elements import AutomationElement


class Automation:
    """UIAutomation constructed wrapper for FlaUI DLL

    FlaUI is written entirely on C# .Net, using it directly inside an IDE within a Python project
    would be painful since intellisense does not pick up the methods/typing hints.
    This class is designed to overcome those challenges by providing Python compatible workstream.
    """

    @validate_arguments
    def __init__(self, ui_automation_types: UIAutomationTypes, timeout: int = 1000) -> None:
        self._ui_automation_types = ui_automation_types
        self.timeout = timeout
        self.automation = UIA3Automation() if ui_automation_types == UIAutomationTypes.UIA3 else UIA2Automation()
        self.cf = self.automation.ConditionFactory
        self.tree_walker = self.automation.TreeWalkerFactory.GetRawViewWalker()
        self.application: Application
        self.main_window: AutomationElement  # TODO: Move this to window element type

    def _build_application(self, application) -> None:
        self.application = Application(application)
        self.main_window = self.application.get_main_window(self.automation)

    def launch(self, executable: str, arguments: Optional[str] = None) -> None:
        """Launches the given executable.

        :param executable: The executable to launch.
        :param arguments: Arguments to executable, defaults to None
        """
        self._build_application(CSApplication.Launch(executable, arguments))

    def launch_store_app(self, app_user_model_ltd: str, arguments: Optional[str] = None) -> None:
        """Launches a store application.

        :param app_user_model_ltd: The app id of the application to launch.
        :param arguments: The arguments to pass to the application., defaults to None
        """
        self._build_application(CSApplication.LaunchStoreApp(app_user_model_ltd, arguments))

    def attach(self, process: Union[str, int]) -> None:
        """Attaches to a given process id.

        :param process: The id/process/path of executable of the process to attach to.
        """
        self._build_application(CSApplication.Attach(process))

    def attach_or_launch(self, process: Union[str, int]) -> None:
        """Attaches or launches the given process.

        :param process: The id/process/path of executable of the process to attach to.
        """
        self._build_application(CSApplication.AttachOrLaunch(process))

    def get_all_top_level_windows(self) -> List[AutomationElement]:  # TODO: Update this to return Window Element object
        """Gets all top level windows from the application.

        :return: Get's all top level windows form the application
        """
        return TypeCast.py_list(self.application.get_all_top_level_windows(self.automation))

    def get_main_window(self) -> AutomationElement:
        """Gets the main window of the applications process.

        :return: The main window object as Window element or null if no main window was found within the timeout.
        """

        return self.application.get_main_window(self.automation)
