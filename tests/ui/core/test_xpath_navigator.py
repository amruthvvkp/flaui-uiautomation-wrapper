"""UI integration tests for the AutomationElementXPathNavigator wrapper (GH-105)."""

from flaui.core.automation_elements import AutomationElement
from flaui.core.xpath_navigator import AutomationElementXPathNavigator
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestXPathNavigator:
    """Tests for navigating the UIA tree via the XPath navigator."""

    def test_navigator_starts_at_root(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """A fresh navigator is positioned at the root element (the window)."""
        navigator = test_application.main_window.get_x_path_navigator()
        assert isinstance(navigator, AutomationElementXPathNavigator)
        assert "Root" in navigator.node_type
        assert_that(navigator.current_element, not_none())
        assert isinstance(navigator.current_element, AutomationElement)

    def test_navigator_moves_through_tree(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """The navigator can move to a child and back to the root."""
        navigator = test_application.main_window.get_x_path_navigator()
        if not navigator.move_to_first_child():
            pytest.skip("Root element has no children to navigate to")
        # On a child node the name is the control type string; it should be non-empty.
        assert isinstance(navigator.name, str) and navigator.name
        navigator.move_to_root()
        assert "Root" in navigator.node_type

    def test_navigator_get_attribute(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """The navigator exposes element attributes by name."""
        navigator = test_application.main_window.get_x_path_navigator()
        # Name attribute should resolve to a string (possibly empty) without raising.
        assert isinstance(navigator.get_attribute("Name"), str)
