"""Tests for the Application class in the core module."""

from time import sleep
from typing import Any, Generator, List, Optional

from flaui.core.application import Application
from flaui.core.automation_elements import AutomationElement
from flaui.modules.automation import Automation
import pytest
from System import InvalidOperationException  # pyright: ignore


@pytest.fixture(scope="module")
def wordpad_application(wordpad: Automation) -> Generator[Application, None, None]:
    """Fixture to yield the wordpad application.

    :param wordpad: Wordpad automation object
    :yield: Wordpad application
    """
    yield wordpad.application


class TestApplication:
    """Tests for the Application class in the core module."""

    def test_class_properties(self, wordpad_application: Application):
        """Test the class properties.

        :param wordpad_application: Wordpad application
        """
        assert wordpad_application.process_id is not None
        assert wordpad_application.name == "wordpad"
        assert wordpad_application.has_exited is False
        assert wordpad_application.main_window_handle is not None
        with pytest.raises(Exception) as exc_info:
            assert wordpad_application.exit_code
        assert isinstance(exc_info.value, AttributeError)
        assert wordpad_application.close_timeout is not None

    def test_get_all_top_level_windows(self, wordpad_application: Application, automation: Any):
        """Test the get_all_top_level_windows method.

        :param wordpad_application: Wordpad application
        :param automation: Automation object
        """
        timeout = 30
        timer = 0
        windows: Optional[List[AutomationElement]] = []
        while timer != timeout and windows == []:
            windows = wordpad_application.get_all_top_level_windows(automation)
            if windows != []:
                break
            timer = timer + 10
            sleep(10)
        assert len(windows) == 1  # type: ignore
        # TODO: assert return type is window element and validate title

    def test_get_main_window(self, wordpad_application: Application, automation: Any):
        """Test the get_main_window method.

        :param wordpad_application: Wordpad application
        :param automation: Automation object
        """
        window = wordpad_application.get_main_window(automation)
        assert window is not None

    def test_launch(self):
        """Test the launch method."""
        app = Application()
        app.launch("wordpad.exe")

        assert app.name == "wordpad"
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is False

        app.kill()

    def test_launch_store_app(self):
        """Test the launch_store_app method.

        :raises ValueError: If the OS is not Windows 10 or Windows 11
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

    def test_attach(self, wordpad_application: Application):
        """Test the attach method.

        :param wordpad_application: Wordpad application
        """
        app = Application()
        for _ in [f"{wordpad_application.name}.exe", wordpad_application.process_id]:
            app.attach(_)

            assert wordpad_application.name == app.name
            assert wordpad_application.process_id == app.process_id

    def test_attach_or_launch(self, wordpad_application: Application):
        """Test the attach_or_launch method.

        :param wordpad_application: Wordpad application
        """
        app = Application()
        app.attach_or_launch(f"{wordpad_application.name}.exe")

        assert wordpad_application.name == app.name
        assert wordpad_application.process_id == app.process_id

    def test_kill(self):
        """Test the kill method."""
        app = Application()
        app.launch("wordpad.exe")
        app.kill()

        with pytest.raises(InvalidOperationException):
            assert app.name
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is True
        assert app.exit_code == -1

    def test_dispose(self, wordpad_application: Application):
        """Test the dispose method.

        :param wordpad_application: Wordpad application
        """
        app = Application()
        app.attach(wordpad_application.process_id)
        app.dispose()

        attrs = ["name", "exit_code", "has_exited", "main_window_handle", "process_id"]
        for _ in attrs:
            with pytest.raises(InvalidOperationException):
                getattr(app, _)

        assert app.is_store_app is False

    def test_close(self):
        """Test the close method."""
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
        """Test the wait_while_main_handle_is_missing method."""
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
        """Test the wait_while_busy method."""
        app = Application()
        app.launch("wordpad.exe")

        app.wait_while_busy()

        assert app.name == "wordpad"
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is False

        app.kill()
