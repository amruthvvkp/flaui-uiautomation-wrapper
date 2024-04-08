"""Test cases for the automation element class."""

import os
from pathlib import Path

from flaui.core.automation_elements import AutomationElement
from flaui.core.automation_type import AutomationType
from flaui.core.condition_factory import ConditionFactory
from FlaUI.Core.Definitions import (  # pyright: ignore
    TreeScope,  # pyright: ignore
    TreeTraversalOptions,  # pyright: ignore
)
from flaui.core.definitions import ControlType
import pytest

from tests.config import test_settings


@pytest.fixture(scope="module")
def condition_factory(test_app_main_window: AutomationElement):
    """Fixture to yield the condition factory.

    :param test_app_main_window: Test application main window
    :return: Condition factory
    """
    return test_app_main_window.condition_factory


@pytest.fixture(scope="module")
def generic_element(test_app_main_window: AutomationElement):
    """Fixture to yield the generic element.

    :param test_app_main_window: Test application main window
    :return: Generic element
    """
    return test_app_main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")


class TestAutomationElement:
    """Tests for the AutomationElement class."""

    def test_class_properties(self, test_app_main_window: AutomationElement, automation):
        """Test the class properties.

        :param test_app_main_window: Test application main window
        :param automation: Automation object
        """
        element = test_app_main_window

        assert element.actual_height != 0
        assert element.actual_width != 0
        assert isinstance(element.automation_type, AutomationType)
        assert element.bounding_rectangle is not None
        assert element.cached_children is not None
        assert element.cached_parent is None
        assert element.class_name is not None
        assert isinstance(element.condition_factory, ConditionFactory)
        assert element.control_type is not None
        isinstance(element.framework_automation_element, type(automation))
        assert element.framework_type is not None
        assert element.help_text == ""
        assert element.is_available
        assert element.is_enabled
        assert element.is_offscreen is False
        assert element.name == "FlaUI WPF Test App"
        assert element.parent is not None
        assert element.patterns is not None
        assert element.properties is not None

    def test_capture(self, generic_element: AutomationElement):
        """Test the capture method.

        :param generic_element: Generic element
        """
        from System.Drawing import Bitmap  # pyright: ignore

        isinstance(generic_element.capture(), Bitmap)

    def test_capture_to_file(self, generic_element: AutomationElement):
        """Test the capture_to_file method.

        :param generic_element: Generic element
        """
        file_path = Path(os.path.join(Path(test_settings.WPF_TEST_APP_EXE).parent.resolve(), "test_capture.png"))

        generic_element.capture_to_file(str(file_path))

        assert file_path.exists()
        file_path.unlink()

    def test_click(self, generic_element: AutomationElement):
        """Test the click method.

        :param generic_element: Generic element
        """
        for _ in [False, True]:
            try:
                generic_element.click(_)
            except Exception:
                pytest.fail("Unable to click on the test element")

    def test_double_click(self, generic_element: AutomationElement):
        """Test the double_click method.

        :param generic_element: Generic element
        """
        for _ in [False, True]:
            try:
                generic_element.double_click(_)
            except Exception:
                pytest.fail("Unable to click on the test element")

    def test_find_all(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_all method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        elements = test_app_main_window.find_all(
            TreeScope.Descendants, condition_factory.by_control_type(ControlType.TabItem)
        )
        for _ in elements:
            assert _.class_name == "TabItem"

    def test_find_all_by_x_path(self, test_app_main_window: AutomationElement):
        """Test the find_all_by_x_path method.

        :param test_app_main_window: Test application main window
        """
        elements = test_app_main_window.find_all_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        for _ in elements:
            assert _.class_name == "TabItem"

    def test_find_all_children(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_all_children method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        elements = test_app_main_window.find_all_children(condition_factory.by_class_name("TabControl"))
        assert len(elements) == 1
        assert elements[0].class_name == "TabControl"

    def test_find_all_descendants(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_all_descendants method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        elements = test_app_main_window.find_all_descendants(condition_factory.by_class_name("TabControl"))
        assert len(elements) == 1
        assert elements[0].class_name == "TabControl"

    def test_find_all_nested(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_all_nested method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        elements = test_app_main_window.find_all_nested(condition_factory.by_class_name("TabControl"))
        assert len(elements) == 1
        assert elements[0].class_name == "TabControl"

    def test_find_all_with_options(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_all_with_options method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        elements = test_app_main_window.find_all_with_options(
            TreeScope.Descendants,
            condition_factory.by_class_name("TabControl"),
            TreeTraversalOptions.Default,
            test_app_main_window.raw_element,
        )
        assert len(elements) == 1
        assert elements[0].class_name == "TabControl"

    def test_find_at(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_at method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        element = test_app_main_window.find_at(TreeScope.Descendants, 0, condition_factory.by_class_name("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_child_at(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_child_at method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        element = test_app_main_window.find_child_at(0, condition_factory.by_class_name("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_first method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        element = test_app_main_window.find_first(TreeScope.Descendants, condition_factory.by_class_name("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first_by_x_path(self, test_app_main_window: AutomationElement):
        """Test the find_first_by_x_path method.

        :param test_app_main_window: Test application main window
        """
        element = test_app_main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        assert element.class_name == "TabItem"

    def test_find_first_child(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_first_child method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        element = test_app_main_window.find_first_child(condition_factory.by_class_name("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first_descendant(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_first_descendant method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        element = test_app_main_window.find_first_descendant(condition_factory.by_class_name("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first_nested(self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory):
        """Test the find_first_nested method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        element = test_app_main_window.find_first_nested(condition_factory.by_class_name("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first_with_options(
        self, test_app_main_window: AutomationElement, condition_factory: ConditionFactory
    ):
        """Test the find_first_with_options method.

        :param test_app_main_window: Test application main window
        :param condition_factory: Condition factory
        """
        element = test_app_main_window.find_first_with_options(
            TreeScope.Descendants,
            condition_factory.by_class_name("TabControl"),
            TreeTraversalOptions.Default,
            test_app_main_window.raw_element,
        )
        assert element.class_name == "TabControl"

    def test_focus(self, generic_element: AutomationElement):
        """Test the focus method.

        :param generic_element: Generic element
        """
        generic_element.focus()

    def test_focus_native(self, generic_element: AutomationElement):
        """Test the focus_native method.

        :param generic_element: Generic element
        """
        generic_element.focus_native()

    def test_get_clickable_point(self, generic_element: AutomationElement):
        """Test the get_clickable_point method.

        :param generic_element: Generic element
        """
        point = generic_element.get_clickable_point()
        assert point is not None

    def test_get_current_metadata_value(self):
        """Test the get_current_metadata_value method."""
        pass

    def test_get_supported_patterns(self, generic_element: AutomationElement):
        """Test the get_supported_patterns method.

        :param generic_element: Generic element
        """
        patterns = generic_element.get_supported_patterns()
        assert patterns != []

    def test_get_supported_patterns_direct(self, generic_element: AutomationElement):
        """Test the get_supported_patterns_direct method.

        :param generic_element: Generic element
        """
        patterns = generic_element.get_supported_patterns_direct()
        assert patterns != []

    def test_get_supported_properties_direct(self, generic_element: AutomationElement):
        """Test the get_supported_properties_direct method.

        :param generic_element: Generic element
        """
        properties = generic_element.get_supported_properties_direct()
        assert properties != []

    def test_right_click(self, generic_element: AutomationElement):
        """Test the right_click method.

        :param generic_element: Generic element
        """
        for _ in [False, True]:
            generic_element.right_click(_)

    def test_right_double_click(self, generic_element: AutomationElement):
        """Test the right_double_click method.

        :param generic_element: Generic element
        """
        for _ in [False, True]:
            generic_element.right_double_click(_)

    def test_set_focus(self, generic_element: AutomationElement):
        """Test the set_focus method.

        :param generic_element: Generic element
        """
        generic_element.set_focus()

    def test_set_foreground(self, generic_element: AutomationElement):
        """Test the set_foreground method.

        :param generic_element: Generic element
        """
        generic_element.set_foreground()

    def test_to_string(self, generic_element: AutomationElement):
        """Test the to_string method.

        :param generic_element: Generic element
        """
        test_string = generic_element.to_string()
        assert test_string == "AutomationId:, Name:Simple Controls, ControlType:tab item, FrameworkId:WPF"
