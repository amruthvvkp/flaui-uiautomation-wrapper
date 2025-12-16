"""
Test for ExpandCollapse pattern, ported from C# ExpandCollapsePatternTests.cs.

C# ExpandCollapsePatternTests only runs on WPF (2 fixtures):
[TestFixture(AutomationType.UIA2, TestApplicationType.Wpf)]
[TestFixture(AutomationType.UIA3, TestApplicationType.Wpf)]
"""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from flaui.core.definitions import ControlType, ExpandCollapseState
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.wpf_only
class TestExpandCollapsePattern:
    """Tests for ExpandCollapse pattern on WPF Expander control."""

    @pytest.fixture(name="expander")
    def get_expander(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        skip_on_winforms: None,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the Expander element from the second tab.

        :param test_application: Test application elements.
        :param skip_on_winforms: Fixture that skips WinForms tests.
        :yield: Expander automation element.
        """
        # Select the second tab (index 1)
        tab_control = test_application.main_window.find_first_descendant(
            condition=test_application._cf.by_control_type(ControlType.Tab)
        ).as_tab()
        tab_control.select_tab_item(index=1)
        tab_item = tab_control.tab_items[1]
        # Find the Expander inside the tab (nested: Pane -> Expander)
        expander = tab_item.find_first_nested(
            [
                test_application._cf.by_control_type(ControlType.Pane),
                test_application._cf.by_automation_id("Expander"),
            ]
        )
        yield expander

    def test_expander_pattern(self, expander: AutomationElement) -> None:
        """Test expand/collapse pattern on Expander control."""
        assert_that(expander, not_none())
        ecp = expander.patterns.ExpandCollapse.Pattern  # TODO: Move Patterns to Py-wrapper once it is created
        assert_that(ecp, not_none())
        assert ecp.ExpandCollapseState.Value == ExpandCollapseState.Collapsed.value, "Initial state should be collapsed"
        ecp.Expand()
        assert ecp.ExpandCollapseState.Value == ExpandCollapseState.Expanded.value, (
            "State should be expanded after expand()"
        )
        ecp.Collapse()
        assert ecp.ExpandCollapseState.Value == ExpandCollapseState.Collapsed.value, (
            "State should be collapsed after collapse()"
        )
