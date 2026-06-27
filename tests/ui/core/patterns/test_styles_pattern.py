"""UI integration test for the Styles pattern on a DataGrid cell (GH-91)."""

from typing import Any, Generator

from flaui.core.automation_elements import AutomationElement
from hamcrest import assert_that, not_none
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.wpf_only
class TestStylesPattern:
    """Tests for the Styles pattern on a WPF DataGrid cell."""

    @pytest.fixture(name="data_grid")
    def get_data_grid(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        skip_on_winforms: None,
    ) -> Generator[AutomationElement, Any, None]:
        """Fixture to get the DataGrid element from the Complex Controls tab.

        :param test_application: Test application elements.
        :param skip_on_winforms: Fixture that skips WinForms tests.
        :yield: DataGrid automation element.
        """
        yield test_application.complex_controls_tab.data_grid_view

    def test_styles_pattern(self, data_grid: AutomationElement, is_pattern_supported: object) -> None:
        """Read the style identifier of a cell through the Styles pattern when supported."""
        cell = data_grid.patterns.grid.pattern.get_item(1, 1)
        assert_that(cell, not_none())
        if not is_pattern_supported(cell.patterns, "styles"):  # type: ignore[operator]
            pytest.skip("Styles pattern is not supported on this cell/runtime")
        assert cell.patterns.styles.pattern.style.value is not None
