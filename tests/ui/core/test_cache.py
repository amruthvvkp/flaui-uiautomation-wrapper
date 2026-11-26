"""Tests for the cache request and caching, ported from C# CacheTests.cs."""

import time
from typing import Any, Generator, Optional

from dirty_equals import HasLen
from flaui.core.automation_elements import AutomationElement, Grid
from flaui.core.condition_factory import PropertyCondition
from flaui.core.cache_request import CacheRequest
from flaui.core.definitions import AutomationElementMode, TreeScope
from flaui.core.identifiers import PatternId, PropertyId
from flaui.lib.enums import UIAutomationTypes
from flaui.lib.exceptions import ElementNotFound, PropertyNotCachedException
from flaui.modules.automation import Automation
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


def _find_or_none(root: AutomationElement, condition: PropertyCondition) -> Optional[AutomationElement]:
    """Return the first child of ``root`` matching ``condition``, or ``None`` when absent.

    :param root: The live element to search under.
    :param condition: The search condition.
    :return: The matching child, or ``None``.
    """
    try:
        return root.find_first_child(condition)
    except ElementNotFound:
        return None


class TestCache:
    """Tests for the cache request and caching behavior."""

    @pytest.fixture(name="list_view_grid")
    def get_list_view_grid(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[Grid, Any, None]:
        """Returns the list view grid element.

        :param test_application: Test application elements.
        :yield: List view grid element.
        """
        yield test_application.complex_controls_tab.list_view_grid

    @pytest.mark.skip_if_matrix(
        {"ui_automation_type": [UIAutomationTypes.UIA2], "test_app_type": ["WinForms"]},
        reason="Tab element not exposed in UIA2_WinForms",
    )
    def test_rows_and_cells_cached(self, ui_automation_type: UIAutomationTypes, list_view_grid: Grid) -> None:
        """Tests that rows and cells are cached and have correct values using CacheRequest wrapper.

        Ported from CacheTests.cs::RowsAndCellsTest
        """
        expected_cell_values = [["1", "10"], ["2", "20"], ["3", "30"]]

        # Create cache request and configure it
        automation = Automation(ui_automation_type)
        cache_request = CacheRequest(automation)
        cache_request.tree_scope = TreeScope.Descendants
        cache_request.add_property(automation.cs_automation.PropertyLibrary.Element.Name)

        with cache_request.activate():
            rows = list_view_grid.rows
            assert rows == HasLen(3), "Grid should have 3 rows."

            for row_index, row in enumerate(rows):
                # Use cached_children property
                cells = row.cached_children
                assert cells == HasLen(2), "Each row should have 2 cells."

                for cell_index, cell in enumerate(cells):
                    # Convert to AutomationElement and get label
                    cell_element = AutomationElement(raw_element=cell)
                    cell_text = cell_element.as_label().text
                    assert cell_text == expected_cell_values[row_index][cell_index], (
                        f"Cell value mismatch at row {row_index}, cell {cell_index}."
                    )

    def test_add_identifiers_and_not_cached_property(
        self,
        ui_automation_type: UIAutomationTypes,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> None:
        """``CacheRequest.add`` caches raw and wrapped ids; reading an uncached one names it via ``.property``.

        Also exercises ``PropertyId.get_condition`` to locate the element on each matrix combination.
        """
        automation = Automation(ui_automation_type)
        library = automation.cs_automation.PropertyLibrary
        name_id = PropertyId(raw=library.Element.Name)
        automation_id = PropertyId(raw=library.Element.AutomationId)
        class_name_id = PropertyId(raw=library.Element.ClassName)

        cache_request = CacheRequest()
        cache_request.tree_scope = TreeScope.Element
        cache_request.automation_element_mode = AutomationElementMode.Full
        cache_request.add(name_id)
        cache_request.add(automation_id.raw)
        cache_request.add(PatternId(raw=automation.cs_automation.PatternLibrary.InvokePattern))
        assert {p.Id for p in cache_request.properties} == {name_id.id, automation_id.id}

        condition = automation_id.get_condition("ProgressBar")
        # Resolve the search root and wait for the target before activating: in ``None_`` mode every
        # element found under the request is cache-only, so the search root must be a live element.
        # WinForms only realises the tab page's children while its window is in front, and a moment
        # after the tab switch (the four matrix apps overlap on the desktop).
        test_application.main_window.set_foreground()
        root = test_application.simple_controls_tab.parent_element
        deadline = time.monotonic() + 5
        while _find_or_none(root, condition) is None:
            if time.monotonic() > deadline:
                pytest.fail("Progress bar never appeared on the simple controls tab")
            time.sleep(0.2)
        with cache_request.activate():
            # A cached search walks the raw view (the request's TrueCondition filter), where WinForms
            # nests the controls under an extra TabPage pane, so search descendants, not children.
            target = root.find_first_descendant(condition)
            assert target.properties.automation_id.value == "ProgressBar", "Cached AutomationId is readable."
            assert isinstance(target.properties.name.value, str), "Cached Name is readable."
            with pytest.raises(PropertyNotCachedException) as info:
                _ = target.properties.class_name.value
        assert info.value.property == class_name_id
        assert info.value.property.name == "ClassName"
