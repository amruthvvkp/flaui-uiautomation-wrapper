"""UI integration test for the VirtualizedItem pattern (GH-91)."""

from flaui.core.definitions import ControlType
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestVirtualizedItemPattern:
    """Tests for the VirtualizedItem pattern on list items that may be virtualized."""

    def test_virtualized_item_pattern(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        condition_factory: object,
        is_pattern_supported: object,
    ) -> None:
        """Realize the first virtualized item found, or skip when none are virtualized."""
        large_list_view = test_application.complex_controls_tab.large_list_view
        items = large_list_view.find_all_descendants(
            condition=condition_factory.by_control_type(ControlType.ListItem)  # type: ignore[attr-defined]
        )
        target = next(
            (item for item in items if is_pattern_supported(item.patterns, "virtualized_item")),  # type: ignore[operator]
            None,
        )
        if target is None:
            pytest.skip("No virtualized items are present in the available controls")
        # Realizing a virtualized item must not raise.
        target.patterns.virtualized_item.pattern.realize()
