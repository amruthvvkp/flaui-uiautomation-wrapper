"""
This module contains unit tests for the Application class in the flaui.core.application module.
The Application class is responsible for launching, attaching, and interacting with applications.
It also provides methods for getting information about the application, such as its process ID and main window handle.
"""
from time import sleep
from typing import Any
from typing import List
from typing import Optional

from flaui.core.application import Application
from flaui.core.automation_elements import Window
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest
from System import InvalidOperationException  # pyright: ignore

@pytest.fixture(scope="package")
def wordpad(ui_automation_type: UIAutomationTypes):
    """Generates FlaUI Automation class with the Wordpad application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the wordpad application.
    """
    wordpad = Automation(ui_automation_type)
    wordpad.application.launch("wordpad.exe")
    yield wordpad

    wordpad.application.kill()

class TestApplication:
    """Tests for the Application class in the flaui.core.application module."""

    @pytest.fixture(autouse=True)
    def _wordpad_application(self, wordpad: Automation):
        """Fixture to launch wordpad application.

        :param wordpad: The wordpad automation instance.
        """
        self.application: Application = wordpad.application


    def test_class_properties(self):
        """Test the class properties of the Application class."""
        assert self.application.process_id is not None
        assert self.application.name == "wordpad"
        assert self.application.has_exited is False
        assert self.application.main_window_handle is not None
        assert self.application.close_timeout is not None

    def test_get_all_top_level_windows(self, automation: Any):
        """Test the get_all_top_level_windows method of the Application class.

        :param automation: The automation instance.
        """
        timeout = 30
        timer = 0
        windows: Optional[List[Window]] = []
        while timer != timeout and windows == []:
            windows = self.application.get_all_top_level_windows(automation)
            if windows != []:
                break
            timer = timer + 10
            sleep(10)
        assert len(windows) == 1  # type: ignore
        window = windows[0]
        assert window.title == "Document - WordPad"
        assert isinstance(window, Window)

    def test_get_main_window(self, automation: Any):
        """Test the get_main_window method of the Application class.

        :param automation: The automation instance.
        """
        window = self.application.get_main_window(automation)
        assert window is not None
        assert window.title == "Document - WordPad"
        assert window.class_name == "WordPadClass"
        assert window.name == "Document - WordPad"
        assert isinstance(window, Window)

    def test_launch(self):
        """Test the launch method of the Application class."""
        app = Application()
        app.launch("wordpad.exe")

        assert app.name == "wordpad"
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is False

        app.kill()

    def test_launch_store_app(self):
        """Test the launch_store_app method of the Application class.

        :raises ValueError: If the host OS is not Windows 10 or Windows 11.
        """
        from FlaUI.Core.Tools import OperatingSystem  # pyright: ignore

        if OperatingSystem.IsWindows10() or OperatingSystem.IsWindows11():
            name = "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
        else:
            raise ValueError("Cannot launch Windows Store App on existing OS, need Windows 10 or Windows 11 host OS")

        app = Application()
        app.launch_store_app(name)

        assert app.name == "CalculatorApp"
        assert app.process_id is not None
        assert app.is_store_app is True
        assert app.has_exited is False

        app.kill()

    def test_attach(self):
        """Test the attach method of the Application class."""
        app = Application()
        for _ in [f"{self.application.name}.exe", self.application.process_id]:
            app.attach(_)

            assert self.application.name == app.name
            assert self.application.process_id == app.process_id

    def test_attach_or_launch(self):
        """Test the attach_or_launch method of the Application class."""
        app = Application()
        app.attach_or_launch(f"{self.application.name}.exe")

        assert self.application.name == app.name
        assert self.application.process_id == app.process_id

    def test_kill(self):
        """Test the kill method of the Application class."""
        app = Application()
        app.launch("wordpad.exe")
        app.kill()

        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is True
        assert app.exit_code == -1

    def test_dispose(self):
        """Test the dispose method of the Application class."""
        app = Application()
        app.attach(self.application.process_id)
        app.dispose()

        attrs = ["name", "exit_code", "has_exited", "main_window_handle", "process_id"]
        for _ in attrs:
            with pytest.raises(InvalidOperationException):
                getattr(app, _)

        assert app.is_store_app is False

    def test_close(self):
        """Test the close method of the Application class."""
        app = Application()
        app.launch("wordpad.exe")
        app.close()

        timer = 0
        while app.has_exited is False or timer != 10:
            sleep(10)
            timer = timer + 10

        assert app.has_exited is True
        assert app.exit_code in [0, -1]

    def test_wait_while_main_handle_is_missing(self):
        """Test the wait_while_main_handle_is_missing method of the Application class."""
        app = Application()
        app.launch("wordpad.exe")

        app.wait_while_main_handle_is_missing()

        assert app.name == "wordpad"
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is False
        assert app.main_window_handle is not None

        app.kill()

    def test_wait_while_busy(self):
        """Test the wait_while_busy method of the Application class."""
        app = Application()
        app.launch("wordpad.exe")

        app.wait_while_busy()

        assert app.name == "wordpad"
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is False

        app.kill()
