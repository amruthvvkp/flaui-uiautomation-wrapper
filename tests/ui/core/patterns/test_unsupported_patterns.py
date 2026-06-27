"""UI integration tests asserting the pattern facade reports unsupported patterns (GH-91).

Several UIA patterns have no suitable control in the WinForms/WPF test applications (Dock,
Annotation, Drag, DropTarget, ObjectModel, Spreadsheet, SpreadsheetItem, SynchronizedInput). Rather
than fabricate coverage, these tests exercise the facade plumbing end-to-end by confirming that the
``is_supported`` accessor resolves for each pattern on a plain control.
"""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestUnsupportedPatterns:
    """Facade plumbing tests for patterns with no exercisable control in the test apps."""

    @pytest.fixture(name="element")
    def get_element(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get a plain control that resolves on both WinForms and WPF.

        :param test_application: Test application elements.
        :yield: CheckBox automation element.
        """
        yield test_application.simple_controls_tab.test_check_box

    @pytest.mark.parametrize(
        "pattern_name",
        [
            "dock",
            "annotation",
            "drag",
            "drop_target",
            "object_model",
            "spreadsheet",
            "spreadsheet_item",
        ],
    )
    def test_pattern_reports_unsupported(
        self,
        element: AutomationElement,
        pattern_name: str,
        is_pattern_supported: object,
    ) -> None:
        """A plain control should not support these specialised patterns on any UIA framework.

        The helper treats both ``is_supported == False`` and a framework-level
        ``NotSupportedByFrameworkException`` (raised under UIA2 for patterns absent from that
        framework) as "not supported".

        :param element: A standard control automation element.
        :param pattern_name: Name of the pattern accessor on ``element.patterns``.
        :param is_pattern_supported: Helper that safely reports pattern support.
        """
        assert_that(element, not_none())
        assert is_pattern_supported(element.patterns, pattern_name) is False  # type: ignore[operator]

    def test_synchronized_input_accessor_resolves(
        self,
        element: AutomationElement,
        is_pattern_supported: object,
    ) -> None:
        """The SynchronizedInput accessor should resolve and report support as a boolean.

        Support varies by control and runtime, so this only asserts the plumbing works.

        :param element: A standard control automation element.
        :param is_pattern_supported: Helper that safely reports pattern support.
        """
        assert isinstance(is_pattern_supported(element.patterns, "synchronized_input"), bool)  # type: ignore[operator]
