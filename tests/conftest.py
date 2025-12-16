"""Fixtures for the test suite."""

import sys
from typing import Any, Generator

# isort: on
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
import pytest

# isort: off

setup_pythonnet_bridge()

from loguru import logger
from _pytest.logging import LogCaptureFixture

import gc
import time

from flaui.lib.enums import UIAutomationTypes
from flaui.lib.exceptions import ElementNotFound

from tests.test_utilities.base import FlaUITestBase
from tests.test_utilities.elements.winforms_application import (
    WinFormsApplicationElements,
    get_winforms_application_elements,
)
from tests.test_utilities.elements.wpf_application import WPFApplicationElements, get_wpf_application_elements


@pytest.fixture
def caplog(caplog: LogCaptureFixture) -> Generator[LogCaptureFixture, Any, None]:
    """Replaces caplog fixture from Pytest to Loguru

    :param caplog: Pytest Caplog fixture
    :yield: Caplog fixture
    """
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)


# =============================================================================
# Custom marker: skip_if_matrix
# =============================================================================
def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers used in this test suite."""
    config.addinivalue_line(
        "markers",
        "skip_if_matrix(matrix, reason=None): Skip test for specific combinations of UIA type and app type.\n"
        '  Example: @pytest.mark.skip_if_matrix({"ui_automation_type": [UIAutomationTypes.UIA2], "test_app_type": ["WinForms"]})',
    )
    config.addinivalue_line(
        "markers",
        "skip_notepad_on_win11(reason=None): Skip tests that launch Notepad on Windows 11 where Notepad is a Store app.",
    )


def _extract_matrix_context(item: pytest.Item) -> tuple[str | None, str | None]:
    """Best-effort extraction of (uia_label, app_label) from parametrized test id.

    Expected ids look like: UIA2_WinForms, UIA3_WPF, etc. We parse from either
    item.callspec.id (if present) or fallback to the nodeid string.
    """
    ident = getattr(getattr(item, "callspec", None), "id", "") or item.nodeid
    uia_label: str | None = None
    app_label: str | None = None

    # Common id format: "... [UIA2_WinForms]" or just "UIA2_WinForms"
    for token in ("UIA2_WinForms", "UIA2_WPF", "UIA3_WinForms", "UIA3_WPF"):
        if token in ident:
            uia_label, app_label = token.split("_", 1)
            break

    # Fallback heuristics if id format differs
    if uia_label is None:
        if "UIA2" in ident:
            uia_label = "UIA2"
        elif "UIA3" in ident:
            uia_label = "UIA3"
    if app_label is None:
        if "WinForms" in ident:
            app_label = "WinForms"
        elif "WPF" in ident:
            app_label = "WPF"
    return uia_label, app_label


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Evaluate custom skip markers before test setup proceeds."""
    # First: skip Notepad-based tests on Windows 11
    notepad_marker = item.get_closest_marker("skip_notepad_on_win11")
    if notepad_marker:
        try:
            is_win11 = sys.getwindowsversion().build >= 22000  # type: ignore[attr-defined]
        except Exception:
            is_win11 = False
        if is_win11:
            pytest.skip(notepad_marker.kwargs.get("reason") or "Windows 11 Store Notepad - see issue #89")

    # Second: matrix-based skipping
    marker = item.get_closest_marker("skip_if_matrix")
    if not marker:
        return

    matrix = marker.args[0] if marker.args else {}
    reason = marker.kwargs.get("reason", "Skipped by matrix")

    uia_wanted = matrix.get("ui_automation_type")
    app_wanted = matrix.get("test_app_type")

    uia_label, app_label = _extract_matrix_context(item)

    def _match_uia() -> bool:
        """Check if the UI Automation type matches the desired matrix criteria."""
        if not uia_wanted:
            return True
        # Accept enums (UIAutomationTypes.UIA2/UIA3) or strings ("UIA2"/"UIA3")
        wanted_labels: list[str] = []
        for u in uia_wanted:
            try:
                wanted_labels.append(getattr(u, "name", str(u)))
            except Exception:
                wanted_labels.append(str(u))
        return uia_label is not None and any(w in uia_label for w in wanted_labels)

    def _match_app() -> bool:
        """Check if the application type matches the desired matrix criteria."""
        if not app_wanted:
            return True
        wanted_apps = [str(a) for a in app_wanted]
        return app_label is not None and any(a == app_label for a in wanted_apps)

    if _match_uia() and _match_app():
        pytest.skip(reason)


@pytest.fixture(scope="session")
def launch_all_test_applications() -> Generator[dict[UIAutomationTypes, dict[str, FlaUITestBase]], Any, None]:
    """Fixture to launch all test applications for the UIAutomation tests."""
    result = {UIAutomationTypes.UIA2: {}, UIAutomationTypes.UIA3: {}}

    for app_type in ["WinForms", "WPF"]:
        for ui_automation_type in [UIAutomationTypes.UIA2, UIAutomationTypes.UIA3]:
            test_base = FlaUITestBase(ui_automation_type, app_type)
            try:
                logger.debug(f"Launching test application: {app_type} with {ui_automation_type}")
                test_base.launch_test_app()
                time.sleep(1)  # Give time for UI to initialize
                assert test_base.automation.application, "Application did not start correctly!"
            except Exception as e:
                logger.error(f"Error launching test app: {e}")
                pytest.exit("Test application failed to launch!")
            else:
                result[ui_automation_type][app_type] = test_base
    yield result
    for ui_automation_type in [UIAutomationTypes.UIA2, UIAutomationTypes.UIA3]:
        for app_type in ["WinForms", "WPF"]:
            test_base = result[ui_automation_type][app_type]
            test_base.close_test_app()
            gc.collect()


@pytest.fixture(
    scope="session",
    params=[
        pytest.param((UIAutomationTypes.UIA2, "WinForms"), id="UIA2_WinForms"),
        pytest.param((UIAutomationTypes.UIA2, "WPF"), id="UIA2_WPF"),
        pytest.param((UIAutomationTypes.UIA3, "WinForms"), id="UIA3_WinForms"),
        pytest.param((UIAutomationTypes.UIA3, "WPF"), id="UIA3_WPF"),
    ],
)
def setup_ui_testing_environment(
    request: pytest.FixtureRequest, launch_all_test_applications: dict[UIAutomationTypes, dict[str, FlaUITestBase]]
) -> Generator[FlaUITestBase, Any, None]:
    """Fixture to launch the test application for the UIAutomation tests."""
    ui_automation_type, test_application_type = request.param

    yield launch_all_test_applications[ui_automation_type][test_application_type]


@pytest.fixture(scope="class", name="test_application")
def get_ui_test_application(
    setup_ui_testing_environment: FlaUITestBase,
) -> Generator[WinFormsApplicationElements | WPFApplicationElements, Any, None]:
    """Fixture to get the test application for the UIAutomation tests.

    :param setup_ui_testing_environment: Application object.
    :yield: Application object.
    """
    application = setup_ui_testing_environment.automation.application
    automation = setup_ui_testing_environment.automation.cs_automation
    test_application_type = setup_ui_testing_environment.app_type
    elements = (
        get_winforms_application_elements(application.get_main_window(automation))
        if test_application_type == "WinForms"
        else get_wpf_application_elements(application.get_main_window(automation))
    )
    try:
        elements.main_window.find_first_descendant(
            condition=elements._cf.by_name("Simple Controls")
        ).as_tab_item().click()
    except ElementNotFound as e:
        logger.error(f"Error: {e}")
    yield elements


@pytest.fixture()
def ui_automation_type(setup_ui_testing_environment: FlaUITestBase) -> Generator[UIAutomationTypes, None, None]:
    """Fixture to get the UIAutomation type for the UIAutomation tests.

    :param setup_ui_testing_environment: Application object.
    :yield: UIAutomation type.
    """
    yield setup_ui_testing_environment.ui_automation_type


@pytest.fixture()
def test_application_type(setup_ui_testing_environment: FlaUITestBase) -> Generator[str, None, None]:
    """Fixture to get the test application type for the UIAutomation tests.

    :param setup_ui_testing_environment: Application object.
    :yield: Test application type.
    """
    yield setup_ui_testing_environment.app_type


@pytest.fixture()
def condition_factory(test_application: WinFormsApplicationElements | WPFApplicationElements) -> Generator:
    """Fixture to get the condition factory for the UIAutomation tests.

    :param test_application: Application object.
    :yield: Condition factory.
    """
    yield test_application._cf


# ============================================================================
# Platform-Specific Skip Fixtures
# ============================================================================
# These fixtures implement C# FlaUI skip patterns for platform limitations


@pytest.fixture
def skip_on_winforms(test_application_type: str) -> None:
    """Skip test if running on WinForms application.

    Equivalent to C# TestFixture exclusions for WinForms.
    Used for tests that only work on WPF (e.g., most pattern tests).

    :param test_application_type: Application type ("WinForms" or "WPF").
    """
    if test_application_type == "WinForms":
        pytest.skip("Not supported on WinForms")


@pytest.fixture
def skip_on_wpf(test_application_type: str) -> None:
    """Skip test if running on WPF application.

    Used for tests that only work on WinForms.

    :param test_application_type: Application type ("WinForms" or "WPF").
    """
    if test_application_type == "WPF":
        pytest.skip("Not supported on WPF")


@pytest.fixture
def skip_on_uia2(ui_automation_type: UIAutomationTypes) -> None:
    """Skip test if running on UIA2.

    Equivalent to C# UtilityMethods.IgnoreOnUIA2().
    Used for tests requiring UIA3-specific features.

    :param ui_automation_type: UI Automation type (UIA2 or UIA3).
    """
    if ui_automation_type == UIAutomationTypes.UIA2:
        pytest.skip("Only run test in UIA3 context")


@pytest.fixture
def skip_on_uia3(ui_automation_type: UIAutomationTypes) -> None:
    """Skip test if running on UIA3.

    Used for tests requiring UIA2-specific features.

    :param ui_automation_type: UI Automation type (UIA2 or UIA3).
    """
    if ui_automation_type == UIAutomationTypes.UIA3:
        pytest.skip("Only run test in UIA2 context")


@pytest.fixture
def require_uia3_winforms(ui_automation_type: UIAutomationTypes, test_application_type: str) -> None:
    """Skip test unless running on UIA3 + WinForms combination.

    Matches C# SpinnerTests which only has:
    [TestFixture(AutomationType.UIA3, TestApplicationType.WinForms)]

    :param ui_automation_type: UI Automation type (UIA2 or UIA3).
    :param test_application_type: Application type ("WinForms" or "WPF").
    """
    if not (ui_automation_type == UIAutomationTypes.UIA3 and test_application_type == "WinForms"):
        pytest.skip("Only runs on UIA3 + WinForms (spinner control limitation)")


@pytest.fixture
def skip_on_uia3_winforms(ui_automation_type: UIAutomationTypes, test_application_type: str) -> None:
    """Skip test if running on UIA3 + WinForms combination.

    Matches C# WindowTests which excludes:
    [TestFixture(AutomationType.UIA3, TestApplicationType.WinForms)]
    Used for context menu tests that fail on this combination.

    :param ui_automation_type: UI Automation type (UIA2 or UIA3).
    :param test_application_type: Application type ("WinForms" or "WPF").
    """
    if ui_automation_type == UIAutomationTypes.UIA3 and test_application_type == "WinForms":
        pytest.skip("Context menu of WinForms is not working with UIA3 on newer .NET versions")
