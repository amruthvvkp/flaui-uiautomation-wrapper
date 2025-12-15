"""
Test for Invoke pattern, ported from C# InvokePatternTests.cs.

C# InvokePatternTests only runs on WPF (2 fixtures):
[TestFixture(AutomationType.UIA2, TestApplicationType.Wpf)]
[TestFixture(AutomationType.UIA3, TestApplicationType.Wpf)]

TODO: Update this test once RegisterAutomationEvent is ported to Python wrapper.
Currently simplified without event handling.
"""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from flaui.core.definitions import ControlType
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

    @pytest.mark.bug(
        id="GH-77",
        url="https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/77",
        reason="RegisterAutomationEvent not yet ported to Python wrapper",
    )
    @pytest.mark.skip(reason="TODO: Implement once RegisterAutomationEvent is ported to Python wrapper")
    def test_invoke_with_event(
        self,
        invokable_button: AutomationElement,
    ) -> None:
        """Test invoke pattern and event on InvokableButton control.

        This is a simplified version that will be enhanced once event handling is available.
        """
        assert_that(invokable_button, not_none())
        orig_button_text = invokable_button.properties.name  # noqa: F841
        invoke_pattern = (
            invokable_button.patterns.Invoke.Pattern
        )  # TODO: Move Patterns to Py-wrapper once it is created
        assert_that(invoke_pattern, not_none())

        # TODO: Add event registration when RegisterAutomationEvent is ported
        # For now, just test basic invoke without event verification
        invoke_pattern.Invoke()
        # Button text should change after invoke (verification without event handler)
        # This may need refinement based on actual behavior


#         orig_button_text = invokable_button.properties.name
#         invoke_pattern = (
#             invokable_button.patterns.Invoke.Pattern
#         )  # TODO: Move Patterns to Py-wrapper once it is created
#         assert_that(invoke_pattern, not_none())
#         invoke_fired = threading.Event()

#         # Register event handler (PythonNet interop, may need adjustment for your wrapper)
#         def on_invoked(element, event_id):
#             invoke_fired.set()

#         # This assumes RegisterAutomationEvent is exposed and works as in C#
#         registered_event = invokable_button.register_automation_event(
#             invoke_pattern.EventIds.InvokedEvent,
#             0,
#             on_invoked,  # 0 = TreeScope.Element
#         )
#         invoke_pattern.Invoke()
#         event_received = invoke_fired.wait(timeout=1.0)
#         assert event_received, "Invoke event was not received within timeout"
#         assert invokable_button.properties.name != orig_button_text, "Button text should change after invoke"
#         # Clean up event handler if needed
#         if hasattr(registered_event, "dispose"):
#             registered_event.dispose()
