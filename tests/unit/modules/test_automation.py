"""This module contains unit tests for the Automation module."""

from typing import Any, Generator

from FlaUI.Core import ITreeWalker  # pyright: ignore
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from FlaUI.UIA3 import UIA3Automation  # pyright: ignore
import pytest

from tests.test_utilities.os_platform import is_windows_11


@pytest.fixture
def wordpad() -> Generator[Automation, Any, None]:
    """Generates FlaUI Automation class with the Wordpad application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the wordpad application.
    """
    wordpad = Automation(UIAutomationTypes.UIA3)
    try:
        wordpad.application.launch("wordpad.exe")
    except Exception as e:
        import pytest

        pytest.skip(f"Could not launch wordpad.exe: {e}")
    yield wordpad
    wordpad.application.kill()


class TestAutomation:
    """
    This class contains unit tests for the Automation module of FlaUI.
    """

    @pytest.mark.windows11
    @pytest.mark.xfail(
        is_windows_11,
        reason="WordPad has been removed or deprecated on Windows 11 (as of 2024). "
        "Use test applications (WinForms/WPF) for reliable automation testing.",
    )
    def test_class_properties(self, wordpad: Automation) -> None:
        """
        This method tests the properties of the Automation class.

        Args:
            wordpad (Automation): An instance of the Automation class.
            automation (Any): An instance of the automation module.
        """
        assert wordpad.application.process_id is not None
        isinstance(wordpad.cs_automation, UIA3Automation)
        assert isinstance(wordpad.cf, ConditionFactory)
        assert isinstance(wordpad.tree_walker, ITreeWalker)
