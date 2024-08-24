import time

from flaui.core.automation_elements import Window
from flaui.core.automation_type import AutomationType
from flaui.core.definitions import ControlType
from flaui.core.tools import Retry
import pytest
from pytest_check import equal, is_false, is_true

from tests.test_utilities.config import ApplicationType


@pytest.mark.parametrize(
    "automation_type,application_type",
    [
        (AutomationType.UIA2, ApplicationType.WinForms),
        (AutomationType.UIA2, ApplicationType.Wpf),
        (AutomationType.UIA3, ApplicationType.WinForms),
        (AutomationType.UIA3, ApplicationType.Wpf),
    ],
    scope="class",
)
class TestAutomationElement:
    @pytest.fixture(autouse=True)
    def setup_method(self, ui_test_base):
        app, automation = ui_test_base
        self.app = app
        self.main_window: Window = app.get_main_window(automation)
        self.automation = automation

    def test_parent(self):
        window = self.main_window
        child = window.find_first_child()
        equal(child.parent.control_type, ControlType.Window)

    def test_is_available(self):
        window = self.main_window
        is_true(window.is_available)
        window.close()
        Retry.WhileTrue(lambda: window.is_available, timeout=5)
        time.sleep(2)  # Adding a 2 second delay for Window to close properly
        is_false(window.is_available, "Window should be closed")
