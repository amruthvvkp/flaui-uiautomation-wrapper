import os
from pathlib import Path
from typing import Any

import pytest
from System import InvalidOperationException  # pyright: ignore

from config import settings
from FlaUI.Core.Definitions import ControlType  # pyright: ignore
from FlaUI.Core.Definitions import TreeScope  # pyright: ignore
from FlaUI.Core.Definitions import TreeTraversalOptions  # pyright: ignore
from flaui.lib.collections import TypeCast  # pyright: ignore
from flaui.wrappers.core.automation_elements import AutomationElement


@pytest.fixture(scope="module")
def condition_factory(test_app_main_window: AutomationElement):
    return test_app_main_window.condition_factory


@pytest.fixture(scope="module")
def generic_element(test_app_main_window: AutomationElement, condition_factory: Any):
    return test_app_main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")


class TestAutomationElement:
    def test_class_properties(self, test_app_main_window: AutomationElement, automation):
        element = test_app_main_window
        from FlaUI.Core import AutomationType  # pyright: ignore
        from FlaUI.Core.Conditions import ConditionFactory  # pyright: ignore

        assert element.actual_height is not 0
        assert element.actual_width is not 0
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
        from System.Drawing import Bitmap  # pyright: ignore

        isinstance(generic_element.capture(), Bitmap)

    def test_capture_to_file(self, generic_element: AutomationElement):
        file_path = Path(os.path.join(Path(settings.WPF_TEST_APP).parent.resolve(), "test_capture.png"))

        generic_element.capture_to_file(str(file_path))

        assert file_path.exists()
        file_path.unlink()

    def test_click(self, generic_element: AutomationElement):
        for _ in [False, True]:
            try:
                generic_element.click(_)
            except Exception:
                pytest.fail("Unable to click on the test element")

    def test_double_click(self, generic_element: AutomationElement):
        for _ in [False, True]:
            try:
                generic_element.double_click(_)
            except Exception:
                pytest.fail("Unable to click on the test element")

    def test_find_all(self, test_app_main_window: AutomationElement, condition_factory: Any):
        elements = test_app_main_window.find_all(
            TreeScope.Descendants, condition_factory.ByControlType(ControlType.TabItem)
        )
        for _ in elements:
            assert _.class_name == "TabItem"

    def test_find_all_by_x_path(self, test_app_main_window: AutomationElement):
        elements = test_app_main_window.find_all_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        for _ in elements:
            assert _.class_name == "TabItem"

    def test_find_all_children(self, test_app_main_window: AutomationElement, condition_factory: Any):
        elements = test_app_main_window.find_all_children(condition_factory.ByClassName("TabControl"))
        assert len(elements) == 1
        assert elements[0].class_name == "TabControl"

    def test_find_all_descendants(self, test_app_main_window: AutomationElement, condition_factory: Any):
        elements = test_app_main_window.find_all_descendants(condition_factory.ByClassName("TabControl"))
        assert len(elements) == 1
        assert elements[0].class_name == "TabControl"

    def test_find_all_nested(self, test_app_main_window: AutomationElement, condition_factory: Any):
        elements = test_app_main_window.find_all_nested(condition_factory.ByClassName("TabControl"))
        assert len(elements) == 1
        assert elements[0].class_name == "TabControl"

    def test_find_all_with_options(self, test_app_main_window: AutomationElement, condition_factory: Any):
        elements = test_app_main_window.find_all_with_options(
            TreeScope.Descendants,
            condition_factory.ByClassName("TabControl"),
            TreeTraversalOptions.Default,
            test_app_main_window.raw_element,
        )
        assert len(elements) == 1
        assert elements[0].class_name == "TabControl"

    def test_find_at(self, test_app_main_window: AutomationElement, condition_factory: Any):
        element = test_app_main_window.find_at(TreeScope.Descendants, 0, condition_factory.ByClassName("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_child_at(self, test_app_main_window: AutomationElement, condition_factory: Any):
        element = test_app_main_window.find_child_at(0, condition_factory.ByClassName("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first(self, test_app_main_window: AutomationElement, condition_factory: Any):
        element = test_app_main_window.find_first(TreeScope.Descendants, condition_factory.ByClassName("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first_by_x_path(self, test_app_main_window: AutomationElement):
        element = test_app_main_window.find_first_by_x_path("/Tab/TabItem[@Name='Simple Controls']")
        assert element.class_name == "TabItem"

    def test_find_first_child(self, test_app_main_window: AutomationElement, condition_factory: Any):
        element = test_app_main_window.find_first_child(condition_factory.ByClassName("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first_descendant(self, test_app_main_window: AutomationElement, condition_factory: Any):
        element = test_app_main_window.find_first_descendant(condition_factory.ByClassName("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first_nested(self, test_app_main_window: AutomationElement, condition_factory: Any):
        element = test_app_main_window.find_first_nested(condition_factory.ByClassName("TabControl"))
        assert element.class_name == "TabControl"

    def test_find_first_with_options(self, test_app_main_window: AutomationElement, condition_factory: Any):
        element = test_app_main_window.find_first_with_options(
            TreeScope.Descendants,
            condition_factory.ByClassName("TabControl"),
            TreeTraversalOptions.Default,
            test_app_main_window.raw_element,
        )
        assert element.class_name == "TabControl"

    def test_focus(self, generic_element: AutomationElement):
        generic_element.focus()

    def test_focus_native(self, generic_element: AutomationElement):
        generic_element.focus_native()

    def test_get_clickable_point(self, generic_element: AutomationElement):
        point = generic_element.get_clickable_point()
        assert point is not None

    def test_get_current_metadata_value(self):
        pass

    def test_get_supported_patterns(self, generic_element: AutomationElement):
        patterns = generic_element.get_supported_patterns()
        assert patterns != []

    def test_get_supported_patterns_direct(self, generic_element: AutomationElement):
        patterns = generic_element.get_supported_patterns_direct()
        assert patterns != []

    def test_get_supported_properties_direct(self, generic_element: AutomationElement):
        properties = generic_element.get_supported_properties_direct()
        assert properties != []

    def test_right_click(self, generic_element: AutomationElement):
        for _ in [False, True]:
            generic_element.right_click(_)

    def test_right_double_click(self, generic_element: AutomationElement):
        for _ in [False, True]:
            generic_element.right_double_click(_)

    def test_set_focus(self, generic_element: AutomationElement):
        generic_element.set_focus()

    def test_set_foreground(self, generic_element: AutomationElement):
        generic_element.set_foreground()

    def test_to_string(self, generic_element: AutomationElement):
        test_string = generic_element.to_string()
        assert test_string == "AutomationId:, Name:Simple Controls, ControlType:tab item, FrameworkId:WPF"
