"""Element name map (page objects) for the bundled WPF test app, built on pydantic models.

The *Test design tips* guide includes this file. A name map gives every element your tests touch a
readable name and keeps each locator in exactly one place, so a changed AutomationId is a one-line
fix instead of a search-and-replace across the suite.

It follows the same shape as the project's own maps in ``tests/test_utilities/elements/``.
"""

# --8<-- [start:map]
from flaui.core.automation_elements import Button, CheckBox, Grid, Tab, TabItem, TextBox, Tree, Window
from flaui.core.condition_factory import ConditionFactory
from flaui.core.definitions import ControlType
from pydantic import BaseModel, ConfigDict


class PageMap(BaseModel):
    """Base for every page: holds the window and finds elements *when they are used*."""

    # FlaUI elements are pydantic models wrapping C# objects; allow them as fields.
    model_config = ConfigDict(arbitrary_types_allowed=True)

    window: Window

    @property
    def cf(self) -> ConditionFactory:
        """The condition factory, shared by every locator on the page."""
        return self.window.condition_factory

    def _tab(self, name: str) -> TabItem:
        """Select a tab page by name (if it isn't already) and return it."""
        tab = self.window.find_first_descendant(self.cf.by_control_type(ControlType.Tab)).as_tab()
        item = tab.find_first_child(self.cf.by_name(name)).as_tab_item()
        if not item.is_selected:
            item.select()
        return item


class SimpleControlsPage(PageMap):
    """The "Simple Controls" tab."""

    @property
    def page(self) -> TabItem:
        """The tab page itself; selecting it is part of finding it."""
        return self._tab("Simple Controls")

    @property
    def name_box(self) -> TextBox:
        """Free-text input."""
        return self.page.find_first_descendant(self.cf.by_automation_id("TextBox")).as_text_box()

    @property
    def accept_terms(self) -> CheckBox:
        """Two-state checkbox (found by its label, as it has no AutomationId)."""
        return self.page.find_first_descendant(self.cf.by_name("Test Checkbox")).as_check_box()

    @property
    def invoke_button(self) -> Button:
        """Button that renames itself to "Invoked!" when invoked."""
        return self.page.find_first_descendant(self.cf.by_automation_id("InvokableButton")).as_button()


class ComplexControlsPage(PageMap):
    """The "Complex Controls" tab."""

    @property
    def page(self) -> TabItem:
        """The tab page itself; selecting it is part of finding it."""
        return self._tab("Complex Controls")

    @property
    def tree(self) -> Tree:
        """Three-level tree."""
        return self.page.find_first_descendant(self.cf.by_automation_id("treeView1")).as_tree()

    @property
    def key_value_grid(self) -> Grid:
        """Two-column grid ("Key", "Value")."""
        return self.page.find_first_descendant(self.cf.by_automation_id("listView1")).as_grid()


class TestAppMap(PageMap):
    """Root of the map: one attribute per page."""

    __test__ = False  # not a pytest test class, despite the name

    @property
    def tabs(self) -> Tab:
        """The tab control that hosts every page."""
        return self.window.find_first_descendant(self.cf.by_control_type(ControlType.Tab)).as_tab()

    @property
    def simple(self) -> SimpleControlsPage:
        """Simple Controls page."""
        return SimpleControlsPage(window=self.window)

    @property
    def complex(self) -> ComplexControlsPage:
        """Complex Controls page."""
        return ComplexControlsPage(window=self.window)


# --8<-- [end:map]
