"""UI integration test for the Scroll pattern on a scrollable list view (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestScrollPattern:
    """Tests for the Scroll pattern on the LargeListView control."""

    @pytest.fixture(name="large_list_view")
    def get_large_list_view(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the LargeListView element from the Complex Controls tab.

        :param test_application: Test application elements.
        :yield: LargeListView automation element.
        """
        yield test_application.complex_controls_tab.large_list_view

    def test_scroll_pattern(self, large_list_view: AutomationElement, is_pattern_supported: object) -> None:
        """Scroll the content vertically and verify the scroll percentage moves, then reset it."""
        assert_that(large_list_view, not_none())
        if not is_pattern_supported(large_list_view.patterns, "scroll"):  # type: ignore[operator]
            pytest.skip("Scroll pattern is not supported on this control/runtime")
        scroll_pattern = large_list_view.patterns.scroll.pattern
        if not scroll_pattern.vertically_scrollable.value:
            pytest.skip("Content is not vertically scrollable")
        try:
            scroll_pattern.set_scroll_percent(-1, 50)
            assert scroll_pattern.vertical_scroll_percent.value > 0
        finally:
            scroll_pattern.set_scroll_percent(-1, 0)
