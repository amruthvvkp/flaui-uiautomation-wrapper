"""Fixtures for the end-to-end integration journeys.

``tests/ui`` shares one long-lived instance of each test application across the whole session, which
keeps per-method checks fast. Integration journeys change a lot of state (they fill forms, toggle
menus, close the app), so every journey gets its **own fresh application process** instead. The
process is launched before the test and killed afterwards, so journeys never depend on each other
or leak state into ``tests/ui``.

The matrix ids (``UIA2_WinForms``, ``UIA2_WPF``, ``UIA3_WinForms``, ``UIA3_WPF``) match the ones in
``tests/conftest.py``, so ``-k UIA3_WPF`` and the ``skip_if_matrix`` marker work the same way here.
"""

from dataclasses import dataclass, field
import faulthandler
import gc
import logging
import sys
import time
from typing import Any, Generator

from flaui.core.application import Application
from flaui.core.automation_elements import Menu, Window
from flaui.core.input import Keyboard, Wait
from flaui.core.windows_api import VirtualKeyShort
from flaui.lib.enums import UIAutomationTypes
from flaui.lib.exceptions import ElementNotFound, NoClickablePointException
from flaui.modules.automation import Automation
import pytest

from tests.test_utilities.base import FlaUITestBase
from tests.test_utilities.elements.winforms_application import (
    WinFormsApplicationElements,
    get_winforms_application_elements,
)
from tests.test_utilities.elements.wpf_application import WPFApplicationElements, get_wpf_application_elements

logger = logging.getLogger(__name__)

ApplicationElements = WinFormsApplicationElements | WPFApplicationElements


@pytest.fixture(autouse=True)
def _suspend_faulthandler() -> Generator[None, Any, None]:
    """Turn off Python's ``faulthandler`` while a journey runs, and restore it afterwards.

    Journeys kill and close real app processes, so the UIA client (UIA2 and UIA3) keeps hitting
    ``RPC_S_SERVER_UNAVAILABLE`` and other first-chance SEH exceptions that the .NET runtime
    normally handles. With pytest's ``faulthandler`` plugin installed, one of these intermittently
    turned into ``Windows fatal exception: access violation`` / ``Fatal Python error: Aborted``,
    killing the whole pytest process mid-run (2 of 3 local runs). With it suspended, runs were clean.
    ``tests/ui`` does not need this because its apps stay alive for the whole session.

    :yield: Control to the journey.
    """
    was_enabled = faulthandler.is_enabled()
    faulthandler.disable()
    try:
        yield
    finally:
        if was_enabled:
            faulthandler.enable(file=sys.__stderr__ or sys.stderr)


@dataclass
class JourneyApp:
    """A freshly launched test application plus everything a journey needs to drive it."""

    test_base: FlaUITestBase
    elements: ApplicationElements = field(init=False)

    def __post_init__(self) -> None:
        """Resolve the main window and build the element map."""
        self.refresh()

    @property
    def ui_automation_type(self) -> UIAutomationTypes:
        """Return the UI Automation type (UIA2 or UIA3) driving this app."""
        return self.test_base.ui_automation_type

    @property
    def app_type(self) -> str:
        """Return the test application type, ``"WinForms"`` or ``"WPF"``."""
        return self.test_base.app_type

    @property
    def automation(self) -> Automation:
        """Return the high-level ``Automation`` that launched the app."""
        return self.test_base.automation

    @property
    def application(self) -> Application:
        """Return the launched ``Application``."""
        return self.test_base.automation.application

    @property
    def main_window(self) -> Window:
        """Return the main window from the current element map."""
        return self.elements.main_window

    @property
    def menu(self) -> Menu:
        """Return the main menu bar, located the same way on both apps and both UIA versions."""
        return self.main_window.find_first_child(condition=self.elements._cf.menu()).as_menu()

    def refresh(self) -> ApplicationElements:
        """Re-resolve the main window and rebuild the element map.

        :return: The rebuilt element map.
        """
        window = self.application.get_main_window(self.automation)
        self.elements = (
            get_winforms_application_elements(window)
            if self.app_type == "WinForms"
            else get_wpf_application_elements(window)
        )
        return self.elements

    def bring_to_front(self) -> None:
        """Make this app the foreground window so real mouse and keyboard input reaches it.

        Several test-app processes can be on the desktop at once (for example when ``tests/ui`` runs
        in the same session), so every journey that sends physical input calls this first.
        """
        self.main_window.set_foreground()
        Wait.until_input_is_processed()

    def dismiss_popups(self) -> None:
        """Press Escape a few times to close any open menu, submenu or context menu."""
        for _ in range(3):
            Keyboard.type_key(VirtualKeyShort.ESCAPE)
            Wait.until_input_is_processed()


def _open_simple_controls_tab(app: JourneyApp) -> None:
    """Select the Simple Controls tab, retrying the transient lookup and click errors seen on CI.

    :param app: The freshly launched app.
    """
    last_error: Exception | None = None
    for _ in range(5):
        try:
            app.elements.tab.select_tab_item(0, post_wait=True)
            return
        except (ElementNotFound, NoClickablePointException) as e:
            last_error = e
            time.sleep(0.5)
    logger.warning("Could not select the Simple Controls tab: %s", last_error)


@pytest.fixture(
    params=[
        pytest.param((UIAutomationTypes.UIA2, "WinForms"), id="UIA2_WinForms"),
        pytest.param((UIAutomationTypes.UIA2, "WPF"), id="UIA2_WPF"),
        pytest.param((UIAutomationTypes.UIA3, "WinForms"), id="UIA3_WinForms"),
        pytest.param((UIAutomationTypes.UIA3, "WPF"), id="UIA3_WPF"),
    ],
)
def journey_app(request: pytest.FixtureRequest) -> Generator[JourneyApp, Any, None]:
    """Launch a fresh test application for one journey and kill it afterwards.

    :param request: Supplies the ``(UIAutomationTypes, app type)`` matrix parameter.
    :yield: The launched app, on the Simple Controls tab and in the foreground.
    """
    ui_automation_type, app_type = request.param
    test_base = FlaUITestBase(ui_automation_type, app_type)
    test_base.launch_test_app()
    try:
        app = JourneyApp(test_base=test_base)
        _open_simple_controls_tab(app)
        app.bring_to_front()
        yield app
    finally:
        _close_quietly(test_base)
        # Release COM references to the dead process now, not on a later finalizer pass.
        gc.collect()


def _close_quietly(test_base: FlaUITestBase) -> None:
    """Kill the journey's process unless the journey already closed it.

    :param test_base: The test base that launched the process.
    """
    try:
        if not test_base.automation.application.has_exited:
            test_base.close_test_app()
            return
    except Exception as e:  # The process may already be gone, which is fine here.
        logger.debug("Ignoring error while closing the journey app: %s", e)
    try:
        test_base.automation.application.dispose()
    except Exception as e:
        logger.debug("Ignoring error while disposing the journey app: %s", e)


@pytest.fixture
def ui_automation_type(journey_app: JourneyApp) -> UIAutomationTypes:
    """Return the UI Automation type of the current journey (overrides the ``tests/ui`` fixture).

    :param journey_app: The current journey app.
    :return: UIA2 or UIA3.
    """
    return journey_app.ui_automation_type


@pytest.fixture
def test_application_type(journey_app: JourneyApp) -> str:
    """Return the application type of the current journey (overrides the ``tests/ui`` fixture).

    Overriding this keeps the shared ``skip_on_winforms`` / ``skip_on_uia3_winforms`` fixtures from
    ``tests/conftest.py`` working without launching the session-wide ``tests/ui`` applications.

    :param journey_app: The current journey app.
    :return: ``"WinForms"`` or ``"WPF"``.
    """
    return journey_app.app_type
