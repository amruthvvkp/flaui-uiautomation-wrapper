"""UI integration tests for ScrollBar elements (GH-99)."""

from typing import Any, Generator, List, Optional

from flaui.core.automation_elements import AutomationElement, HorizontalScrollBar, VerticalScrollBar
from flaui.core.definitions import ControlType
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestScrollBar:
    """Tests for HorizontalScrollBar/VerticalScrollBar wrappers on a scrollable list view."""

    @pytest.fixture(name="scroll_bars")
    def get_scroll_bars(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: Any,
    ) -> Generator[List[AutomationElement], Any, None]:
        """Fixture to get all ScrollBars within the LargeListView, or skip if none present.

        :param test_application: Test application elements.
        :param condition_factory: Condition factory for building search conditions.
        :yield: The list of ScrollBar automation elements.
        """
        large_list_view = test_application.complex_controls_tab.large_list_view
        scroll_bars = large_list_view.find_all_descendants(
            condition=condition_factory.by_control_type(ControlType.ScrollBar)
        )
        if not scroll_bars:
            pytest.skip("No ScrollBar present in the LargeListView for this runtime")
        yield scroll_bars

    @pytest.fixture(name="scroll_bar")
    def get_scroll_bar(self, scroll_bars: List[AutomationElement]) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the first ScrollBar within the LargeListView.

        :param scroll_bars: All scroll bars in the list view.
        :yield: A ScrollBar automation element.
        """
        yield scroll_bars[0]

    @staticmethod
    def _by_orientation(scroll_bars: List[AutomationElement], horizontal: bool) -> Optional[AutomationElement]:
        """Return the first scroll bar matching the requested orientation, or ``None``.

        Orientation is inferred from the bounding rectangle: a horizontal scroll bar is wider than
        it is tall, and vice versa.

        :param scroll_bars: All scroll bars to choose from.
        :param horizontal: ``True`` to find a horizontal bar, ``False`` for a vertical one.
        :return: The first matching scroll bar, or ``None`` if there is none.
        """
        for bar in scroll_bars:
            rectangle = bar.bounding_rectangle
            is_horizontal = rectangle.width > rectangle.height
            if is_horizontal == horizontal:
                return bar
        return None

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

    def test_vertical_scroll_actions(self, scroll_bars: List[AutomationElement]) -> None:
        """Drive the vertical line/page scroll methods and keep the value within range."""
        element = self._by_orientation(scroll_bars, horizontal=False)
        if element is None:
            pytest.skip("No vertical ScrollBar present in the LargeListView for this runtime")
        bar = element.as_vertical_scroll_bar()
        if bar.maximum_value <= bar.minimum_value:
            pytest.skip("Vertical ScrollBar is not scrollable on this runtime")

        # Each action must leave the value within the reported range.
        for action in (bar.scroll_down, bar.scroll_down_large, bar.scroll_up_large, bar.scroll_up):
            action()
            assert bar.minimum_value <= bar.value <= bar.maximum_value

    def test_horizontal_scroll_actions(self, scroll_bars: List[AutomationElement]) -> None:
        """Drive the horizontal line/page scroll methods and keep the value within range."""
        element = self._by_orientation(scroll_bars, horizontal=True)
        if element is None:
            pytest.skip("No horizontal ScrollBar present in the LargeListView for this runtime")
        bar = element.as_horizontal_scroll_bar()
        if bar.maximum_value <= bar.minimum_value:
            pytest.skip("Horizontal ScrollBar is not scrollable on this runtime")

        # Each action must leave the value within the reported range.
        for action in (bar.scroll_right, bar.scroll_right_large, bar.scroll_left_large, bar.scroll_left):
            action()
            assert bar.minimum_value <= bar.value <= bar.maximum_value
