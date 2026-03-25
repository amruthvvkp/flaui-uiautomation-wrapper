"""Unit tests for Python AutomationBase / UIA2 / UIA3 facades."""

from FlaUI.UIA2 import UIA2Automation as CSUIA2Automation  # pyright: ignore
from FlaUI.UIA3 import UIA3Automation as CSUIA3Automation  # pyright: ignore

from flaui.core.automation_base import AutomationBase, wrap_cs_automation
from flaui.core.automation_elements import AutomationElement
from flaui.core.automation_type import AutomationType
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from flaui.uia2 import UIA2Automation
from flaui.uia3 import UIA3Automation


def test_uia3_automation_wrapper_properties() -> None:
    """UIA3Automation exposes libraries and condition factory via Python."""
    engine = UIA3Automation()
    assert engine.automation_type == AutomationType.UIA3
    assert isinstance(engine.raw_automation, CSUIA3Automation)
    assert isinstance(engine.condition_factory, ConditionFactory)
    assert engine.property_library is not None
    assert engine.pattern_library is not None


def test_uia2_automation_wrapper_properties() -> None:
    """UIA2Automation exposes automation type and raw C# instance."""
    engine = UIA2Automation()
    assert engine.automation_type == AutomationType.UIA2
    assert isinstance(engine.raw_automation, CSUIA2Automation)


def test_wrap_cs_automation_round_trip() -> None:
    """wrap_cs_automation returns the correct Python subtype for a C# instance."""
    cs_u3 = CSUIA3Automation()
    wrapped = wrap_cs_automation(cs_u3)
    assert isinstance(wrapped, UIA3Automation)
    assert wrapped.raw_automation is cs_u3

    cs_u2 = CSUIA2Automation()
    wrapped2 = wrap_cs_automation(cs_u2)
    assert isinstance(wrapped2, UIA2Automation)
    assert wrapped2.raw_automation is cs_u2


def test_get_desktop_returns_python_automation_element() -> None:
    """get_desktop wraps the C# root element in AutomationElement."""
    engine = UIA3Automation()
    desktop = engine.get_desktop()
    assert isinstance(desktop, AutomationElement)
    assert isinstance(desktop.automation, UIA3Automation)
    assert desktop.automation.automation_type == AutomationType.UIA3


def test_modules_automation_exposes_base_and_raw() -> None:
    """High-level Automation keeps cs_automation as C# and adds automation_base."""
    auto = Automation(UIAutomationTypes.UIA3)
    assert isinstance(auto.automation_base, UIA3Automation)
    assert isinstance(auto.automation_base, AutomationBase)
    assert isinstance(auto.cs_automation, CSUIA3Automation)
    assert auto.cs_automation is auto.automation_base.raw_automation
