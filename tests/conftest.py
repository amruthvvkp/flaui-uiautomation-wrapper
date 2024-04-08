"""
This file contains fixtures that are used in the unit tests. The fixtures include:
- ui_automation_type: Sets the UIAutomation type to use for the tests.
- automation: Sets the Automation class to use for the tests.
This file consists of fixtures that are used in the unit tests."""

import os
from typing import Any, Generator, Literal

from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
import pytest

# # isort: off

setup_pythonnet_bridge()

from flaui.lib.enums import UIAutomationTypes

# # isort: on

@pytest.fixture(scope="package")
def ui_automation_type() -> Generator[Literal[UIAutomationTypes.UIA3, UIAutomationTypes.UIA2], None, None]:
    """Sets the UIAutomation type to use for the tests.

    :yield: UIAutomation type to use for the tests.
    """
    yield UIAutomationTypes.UIA3 if os.getenv(
        "DEFAULT_UIA_VERSION", "UIA3"
    ).upper() == "UIA3" else UIAutomationTypes.UIA2


@pytest.fixture(scope="package")
def automation(ui_automation_type: UIAutomationTypes) -> Generator[Any, None, None]:
    """Sets the Automation class to use for the tests.

    :param ui_automation_type: UIAutomation type to use for the tests.
    :yield: Automation class to use for the tests.
    """
    from FlaUI.UIA2 import UIA2Automation  # pyright: ignore
    from FlaUI.UIA3 import UIA3Automation  # pyright: ignore

    yield UIA3Automation() if ui_automation_type == UIAutomationTypes.UIA3 else UIA2Automation()
