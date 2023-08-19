"""This module contains unit tests for the Automation module."""
from typing import Any

from FlaUI.Core import ITreeWalker  # pyright: ignore
from flaui.core.condition_factory import ConditionFactory
from flaui.modules.automation import Automation

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
