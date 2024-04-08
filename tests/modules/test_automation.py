"""Test cases for the automation module."""

from typing import Any

from FlaUI.Core import ITreeWalker  # pyright: ignore
from flaui.core.condition_factory import ConditionFactory
from FlaUI.Core.Conditions import ConditionFactory as CSConditionFactory  # pyright: ignore
from flaui.modules.automation import Automation

class TestAutomation:
    """Test cases for the Automation class."""

    def test_class_properties(self, wordpad: Automation, automation: Any):
        """Test the class properties.

        :param wordpad: Wordpad application
        :param automation: Automation object
        """
        assert wordpad.application.process_id is not None
        isinstance(wordpad.automation, type(automation))
        assert isinstance(wordpad.cf, ConditionFactory)
        assert isinstance(wordpad.cf.raw_cf, CSConditionFactory)
        assert isinstance(wordpad.tree_walker, ITreeWalker)
