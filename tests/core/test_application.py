from time import sleep
from typing import Any
from typing import Generator
from typing import List
from typing import Optional

from flaui.core.application import Application
from flaui.core.automation_elements import AutomationElement
from flaui.modules.automation import Automation
import pytest
from System import InvalidOperationException  # pyright: ignore


@pytest.fixture(scope="module")
def wordpad_application(wordpad: Automation) -> Generator[Application, None, None]:
    yield wordpad.application


class TestApplication:
    def test_class_properties(self, wordpad_application: Application):
        assert wordpad_application.process_id is not None
        assert wordpad_application.name == "wordpad"
        assert wordpad_application.has_exited is False
        assert wordpad_application.main_window_handle is not None
        with pytest.raises(Exception):
            wordpad_application.exit_code
        assert wordpad_application.close_timeout is not None

    def test_get_all_top_level_windows(self, wordpad_application: Application, automation: Any):
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
        window = wordpad_application.get_main_window(automation)
        assert window is not None

    def test_launch(self):
        app = Application()
        app.launch("wordpad.exe")

        assert app.name == "wordpad"
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is False

        app.kill()

    def test_launch_store_app(self):
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
        app = Application()
        for _ in [f"{wordpad_application.name}.exe", wordpad_application.process_id]:
            app.attach(_)

            assert wordpad_application.name == app.name
            assert wordpad_application.process_id == app.process_id

    def test_attach_or_launch(self, wordpad_application: Application):
        app = Application()
        app.attach_or_launch(f"{wordpad_application.name}.exe")

        assert wordpad_application.name == app.name
        assert wordpad_application.process_id == app.process_id

    def test_kill(self):
        app = Application()
        app.launch("wordpad.exe")
        app.kill()

        with pytest.raises(InvalidOperationException):
            app.name
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is True
        assert app.exit_code == -1

    def test_dispose(self, wordpad_application: Application):
        app = Application()
        app.attach(wordpad_application.process_id)
        app.dispose()

        attrs = ["name", "exit_code", "has_exited", "main_window_handle", "process_id"]
        for _ in attrs:
            with pytest.raises(InvalidOperationException):
                getattr(app, _)

        assert app.is_store_app is False

    def test_close(self):
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
        app = Application()
        app.launch("wordpad.exe")

        app.wait_while_busy()

        assert app.name == "wordpad"
        assert app.process_id is not None
        assert app.is_store_app is False
        assert app.has_exited is False

        app.kill()
