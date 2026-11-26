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

    def test_navigator_node_properties(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """``local_name``, ``has_attributes``, ``is_empty_element`` and ``underlying_object`` describe the node."""
        navigator = test_application.main_window.get_x_path_navigator()
        assert navigator.local_name == navigator.name
        assert navigator.has_attributes is True
        assert navigator.is_empty_element is False
        assert navigator.underlying_object.automation_id == test_application.main_window.automation_id

    def test_navigator_position_comparison(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """``is_same_position`` compares positions and ``move_to`` copies another navigator's position."""
        navigator = test_application.main_window.get_x_path_navigator()
        root = navigator.clone()
        assert navigator.is_same_position(root)
        if not navigator.move_to_first_child():
            pytest.skip("Root element has no children to navigate to")
        assert not navigator.is_same_position(root)
        assert navigator.move_to(root)
        assert navigator.is_same_position(root)

    def test_navigator_attribute_axis(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """The attribute axis can be walked and a named attribute selected, then left via ``move_to_parent``."""
        navigator = test_application.main_window.get_x_path_navigator()
        assert navigator.move_to_first_attribute()
        assert navigator.has_attributes is False
        names = [navigator.name]
        while navigator.move_to_next_attribute():
            names.append(navigator.name)
        assert {"AutomationId", "Name", "ProcessId"} <= set(names)
        assert navigator.move_to_parent()
        assert navigator.move_to_attribute("ProcessId")
        assert navigator.value == str(test_application.main_window.properties.process_id.value)
        assert navigator.move_to_parent()
        assert not navigator.move_to_attribute("NoSuchAttribute")
