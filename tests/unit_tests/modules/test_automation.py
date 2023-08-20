"""This module contains unit tests for the Automation module."""
from typing import Any

import pytest

from FlaUI.Core import ITreeWalker  # pyright: ignore
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


@pytest.fixture
def wordpad(ui_automation_type: UIAutomationTypes):
    """Generates FlaUI Automation class with the Wordpad application.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: FlaUI Automation class with the wordpad application.
    """
    wordpad = Automation(ui_automation_type)
    wordpad.application.launch("wordpad.exe")
    yield wordpad

    wordpad.application.kill()


class TestAutomation:
    """
    This class contains unit tests for the Automation module of FlaUI.
    """

    def test_class_properties(self, wordpad: Automation, automation: Any):
        """
        This method tests the properties of the Automation class.

        Args:
            wordpad (Automation): An instance of the Automation class.
            automation (Any): An instance of the automation module.
        """
        assert wordpad.application.process_id is not None
        isinstance(wordpad.automation, type(automation))
        assert isinstance(wordpad.cf, ConditionFactory)
        assert isinstance(wordpad.tree_walker, ITreeWalker)
