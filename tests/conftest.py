"""Fixtures for the test suite."""

from typing import Any, Generator, Literal

# isort: on
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
import pytest

# isort: off

setup_pythonnet_bridge()

from flaui.lib.enums import UIAutomationTypes


def pytest_addoption(parser):
    """Adds additional options for Pytest unit tests

    :param parser: Pytest Parser
    :yield: Updated options
    """
    parser.addoption(
        "--test-app-uia-version",
        action="store",
        default="UIA3",
        help="UIA version of the Test Application to load for this session",
    )


@pytest.fixture(scope="package")
def ui_automation_type(request) -> Generator[Literal[UIAutomationTypes.UIA3, UIAutomationTypes.UIA2], None, None]:
    """Fixture to yield the UI Automation type.

    :yield: UI Automation type
    """
    if str(request.config.getoption("--test-app-uia-version")).upper() == "UIA3":
        yield UIAutomationTypes.UIA3
    elif str(request.config.getoption("--test-app-uia-version")).upper() == "UIA2":
        yield UIAutomationTypes.UIA2
    else:
        raise ValueError(
            "Invalid value sent to the arguments `--test-app-uia-version`, supported values are UIA2 or UIA3"
        )


@pytest.fixture(scope="package")
def automation(ui_automation_type: UIAutomationTypes) -> Generator[Any, None, None]:
    """Fixture to yield the automation object.

    :param ui_automation_type: UI Automation type
    :yield: Automation object
    """
    from FlaUI.UIA2 import UIA2Automation  # pyright: ignore
    from FlaUI.UIA3 import UIA3Automation  # pyright: ignore

    yield UIA3Automation() if ui_automation_type == UIAutomationTypes.UIA3 else UIA2Automation()
