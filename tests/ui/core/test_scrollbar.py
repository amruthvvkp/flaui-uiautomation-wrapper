"""UI integration tests for ScrollBar elements (GH-99)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement, HorizontalScrollBar, VerticalScrollBar
from flaui.core.definitions import ControlType
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestScrollBar:
    """Tests for HorizontalScrollBar/VerticalScrollBar wrappers on a scrollable list view."""

    @pytest.fixture(name="scroll_bar")
    def get_scroll_bar(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: Any,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the first ScrollBar within the LargeListView, or skip if none present.

        :param test_application: Test application elements.
        :param condition_factory: Condition factory for building search conditions.
        :yield: A ScrollBar automation element.
        """
        large_list_view = test_application.complex_controls_tab.large_list_view
        scroll_bars = large_list_view.find_all_descendants(
            condition=condition_factory.by_control_type(ControlType.ScrollBar)
        )
        if not scroll_bars:
            pytest.skip("No ScrollBar present in the LargeListView for this runtime")
        yield scroll_bars[0]

    def test_scroll_bar_range_properties(self, scroll_bar: AutomationElement) -> None:
        """Read the shared RangeValue properties through the scroll-bar wrapper."""
        bar = scroll_bar.as_vertical_scroll_bar()
        assert isinstance(bar, VerticalScrollBar)
        assert bar.minimum_value <= bar.value <= bar.maximum_value
        assert isinstance(bar.is_read_only, bool)
        assert bar.small_change >= 0
        assert bar.large_change >= 0

    def test_scroll_bar_converters(self, scroll_bar: AutomationElement) -> None:
        """Both scroll-bar converters return the correctly typed wrapper."""
        assert isinstance(scroll_bar.as_horizontal_scroll_bar(), HorizontalScrollBar)
        assert isinstance(scroll_bar.as_vertical_scroll_bar(), VerticalScrollBar)
