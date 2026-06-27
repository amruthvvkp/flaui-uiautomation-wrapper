"""UI integration test for the ItemRealizer tool (GH-100)."""

import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestItemRealizer:
    """Tests for realizing virtualized items in a container."""

    def test_realize_items_on_large_list_view(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """Realizing the items of the LargeListView completes without raising."""
        from flaui.core.tools import ItemRealizer

        large_list_view = test_application.complex_controls_tab.large_list_view
        # Should walk and realize all (virtualized) items without error.
        ItemRealizer.realize_items(large_list_view)
