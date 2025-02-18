# """Tests for the Application class in the core module."""

# from time import sleep
# from typing import Any, Generator

# from flaui.core.application import Application
# from flaui.lib.enums import UIAutomationTypes
# from flaui.modules.automation import Automation
# import pytest
# from System import InvalidOperationException  # pyright: ignore

# from tests.test_utilities.config import test_settings


# @pytest.fixture()
# def application_object(test_application: Automation) -> Generator[Application, None, None]:
#     """Returns the Application object from the Automation object

#     :param test_application: Test Automaiton object
#     :raises ValueError: On error
#     :yield: Application object
#     """
#     yield test_application.application


# class TestApplication:
#     """Tests for the Application class in the core module."""

#     def test_class_properties(self, ui_automation_type: UIAutomationTypes, application_object: Application):
#         """Test the class properties.

#         :param application_object: Test application
#         """
#         assert application_object.process_id is not None
#         if ui_automation_type == UIAutomationTypes.UIA3:
#             assert application_object.name == str(test_settings.WPF_TEST_APP_PROCESS).split(".")[0]
#         else:
#             assert application_object.name == str(test_settings.WINFORMS_TEST_APP_PROCESS).split(".")[0]
#         assert application_object.has_exited is False
#         assert application_object.main_window_handle is not None

#         with pytest.raises(InvalidOperationException):
#             assert application_object.exit_code
#         assert application_object.close_timeout is not None

#     # TODO: Somehow recent tests on Windows 11 have begun failing fetching all top windows, needs investigation and a GitHub Issue to track the fix
#     # def test_get_all_top_level_windows(self, application_object: Application, automation: Any):
#     #     """Test the get_all_top_level_windows method.

#     #     :param application_object: Test application
#     #     :param automation: Automation object
#     #     """
#     #     timeout = 30
#     #     timer = 0
#     #     windows: Optional[List[Window]] = []
#     #     while timer != timeout and windows == []:
#     #         windows = application_object.get_all_top_level_windows(automation)
#     #         if windows != []:
#     #             break
#     #         timer = timer + 10
#     #         sleep(10)
#     #     assert len(windows) == 1  # type: ignore
#     #     assert all([isinstance(_, Window) for _ in windows])

#     def test_get_main_window(self, application_object: Application, automation: Any):
#         """Test the get_main_window method.

#         :param application_object: Test application
#         :param automation: Automation object
#         """
#         window = application_object.get_main_window(automation)
#         assert window is not None

#     def test_launch(self):
#         """Test the launch method."""
#         app = Application()
#         app.launch("wordpad.exe")

#         assert app.name == "wordpad"
#         assert app.process_id is not None
#         assert app.is_store_app is False
#         assert app.has_exited is False

#         app.kill()

#     def test_launch_store_app(self):
#         """Test the launch_store_app method.

#         :raises ValueError: If the OS is not Windows 10 or Windows 11
#         """
#         from FlaUI.Core.Tools import OperatingSystem  # pyright: ignore

#         if OperatingSystem.IsWindows10() or OperatingSystem.IsWindows11():
#             name = "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
#         else:
#             raise ValueError("Cannot launch Windows Store App on existing OS, need Windows 10 or Windows 11 host OS")

#         app = Application()
#         app.launch_store_app(name)

#         assert app.name == "CalculatorApp"
#         assert app.process_id is not None
#         assert app.is_store_app is True
#         assert app.has_exited is False

#         app.kill()

#     def test_attach(self, application_object: Application):
#         """Test the attach method.

#         :param application_object: Test application
#         """
#         app = Application()
#         for _ in [f"{application_object.name}.exe", application_object.process_id]:
#             app.attach(_)

#             assert application_object.name == app.name
#             assert application_object.process_id == app.process_id

#     def test_attach_or_launch(self, application_object: Application):
#         """Test the attach_or_launch method.

#         :param application_object: Test application
#         """
#         app = Application()
#         app.attach_or_launch(f"{application_object.name}.exe")

#         assert application_object.name == app.name
#         assert application_object.process_id == app.process_id

#     def test_kill(self):
#         """Test the kill method."""
#         app = Application()
#         app.launch("wordpad.exe")
#         app.kill()

#         with pytest.raises(InvalidOperationException):
#             assert app.name
#         assert app.process_id is not None
#         assert app.is_store_app is False
#         assert app.has_exited is True
#         assert app.exit_code == -1

#     def test_dispose(self, application_object: Application):
#         """Test the dispose method.

#         :param application_object: Test application
#         """
#         app = Application()
#         app.attach(application_object.process_id)
#         app.dispose()

#         attrs = ["name", "exit_code", "has_exited", "main_window_handle", "process_id"]
#         for _ in attrs:
#             with pytest.raises(InvalidOperationException):
#                 getattr(app, _)

#         assert app.is_store_app is False

#     def test_close(self):
#         """Test the close method."""
#         app = Application()
#         app.launch("wordpad.exe")
#         app.close()

#         timer = 0
#         while app.has_exited is False or timer != 10:
#             sleep(10)
#             timer = timer + 10

#         assert app.has_exited is True
#         assert app.exit_code in [0, -1]

#     def test_wait_while_main_handle_is_missing(self):
#         """Test the wait_while_main_handle_is_missing method."""
#         app = Application()
#         app.launch("wordpad.exe")

#         app.wait_while_main_handle_is_missing()

#         assert app.name == "wordpad"
#         assert app.process_id is not None
#         assert app.is_store_app is False
#         assert app.has_exited is False
#         assert app.main_window_handle is not None

#         app.kill()

#     def test_wait_while_busy(self):
#         """Test the wait_while_busy method."""
#         app = Application()
#         app.launch("wordpad.exe")

#         app.wait_while_busy()

#         assert app.name == "wordpad"
#         assert app.process_id is not None
#         assert app.is_store_app is False
#         assert app.has_exited is False

#         app.kill()
