from typing import Any

from FlaUI.Core import ITreeWalker  # pyright: ignore
from flaui.core.condition_factory import ConditionFactory
from flaui.modules.automation import Automation

class TestAutomation:
    def test_class_properties(self, wordpad: Automation, automation: Any):
        assert wordpad.application.process_id is not None
        isinstance(wordpad.automation, type(automation))
        assert isinstance(wordpad.cf, ConditionFactory)
        assert isinstance(wordpad.tree_walker, ITreeWalker)
