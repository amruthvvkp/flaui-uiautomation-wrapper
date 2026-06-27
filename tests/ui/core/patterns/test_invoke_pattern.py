"""
Test for Invoke pattern, ported from C# InvokePatternTests.cs.

C# InvokePatternTests only runs on WPF (2 fixtures):
[TestFixture(AutomationType.UIA2, TestApplicationType.Wpf)]
[TestFixture(AutomationType.UIA3, TestApplicationType.Wpf)]

TODO: Update this test once RegisterAutomationEvent is ported to Python wrapper.
Currently simplified without event handling.
"""

import threading
from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from flaui.core.definitions import ControlType, TreeScope
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.wpf_only
class TestInvokePattern:
    """Tests for Invoke pattern on WPF InvokableButton control."""

    @pytest.fixture(name="invokable_button")
    def get_invokable_button(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        skip_on_winforms: None,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the InvokableButton element from the first tab.

        :param test_application: Test application elements.
        :param skip_on_winforms: Fixture that skips WinForms tests.
        :yield: InvokableButton automation element.
        """
        tab_control = test_application.main_window.find_first_descendant(
            condition=test_application._cf.by_control_type(ControlType.Tab)
        ).as_tab()
        tab_item = tab_control.tab_items[0]
        button = tab_item.find_first_descendant(condition=test_application._cf.by_automation_id("InvokableButton"))
        yield button

    def test_invoke_with_event(
        self,
        invokable_button: AutomationElement,
    ) -> None:
        """Invoke the button and verify the registered automation event fires (GH-77)."""
        assert_that(invokable_button, not_none())
        invoke_pattern = invokable_button.patterns.invoke.pattern
        assert_that(invoke_pattern, not_none())

        invoke_fired = threading.Event()

        def on_invoked(element: AutomationElement, event_id: Any) -> None:
            """Set the threading event when the Invoked event fires."""
            invoke_fired.set()

        # EventIds is exposed on the raw C# pattern (Automation.EventLibrary.Invoke).
        invoked_event_id = invoke_pattern.raw_pattern.EventIds.InvokedEvent
        registration = invokable_button.register_automation_event(
            invoked_event_id, TreeScope.Element, on_invoked
        )
        try:
            invoke_pattern.invoke()
            assert invoke_fired.wait(timeout=5.0), "Invoke event was not received within timeout"
        finally:
            registration.unregister()
        assert registration.is_active is False
