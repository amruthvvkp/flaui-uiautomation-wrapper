"""This module contains unit tests for the Automation module."""

from FlaUI.Core import ITreeWalker  # pyright: ignore
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from FlaUI.UIA3 import UIA3Automation  # pyright: ignore
import pytest


@pytest.fixture
def wordpad():
    """Generates FlaUI Automation class with the Wordpad application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the wordpad application.
    """
    wordpad = Automation(UIAutomationTypes.UIA3)
    wordpad.application.launch("wordpad.exe")
    yield wordpad

    wordpad.application.kill()


class TestAutomation:
    """
    This class contains unit tests for the Automation module of FlaUI.
    """

    def test_class_properties(self, wordpad: Automation):
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
