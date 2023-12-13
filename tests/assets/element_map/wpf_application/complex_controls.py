"""This contains element map for the tab Complex Controls for the WPF test application."""

from flaui.core.automation_elements import Button, DataGridView, Grid, TabItem, Tree
from flaui.core.definitions import ControlType

from tests.assets.element_map.wpf_application.common import AbtstractControlCollection
from tests.assets.element_map.wpf_application.constants import ApplicationTabIndex


class ComplexControlsElements(AbtstractControlCollection):
    """This class is used to store the Complex Controls element locators for the WPF application."""

    @property
    def parent_element(self) -> TabItem:
        """Returns the Simple Controls element.

        :return: The Simple Controls element.
        """
        tab = self.main_window.find_first_child(
            condition=self._condition_factory.by_control_type(ControlType.Tab)
        ).as_tab()
        element = tab.find_first_child(condition=self._condition_factory.by_name("Complex Controls")).as_tab_item()

        if not element.is_selected:
            tab.select_tab_item(ApplicationTabIndex.COMPLEX_CONTROLS.value)
        return element

    @property
    def data_grid_view(self) -> DataGridView:
        """Returns the Data Grid View element.

        :return: The Data Grid View element.
        """
        return self.parent_element.find_first_descendant(
            condition=self._condition_factory.by_automation_id("dataGridView")
        ).as_data_grid_view()

    @property
    def large_list_view(self) -> DataGridView:
        """Returns the Large List View element.

        :return: The Large List View element.
        """
        return self.parent_element.find_first_descendant(
            condition=self._condition_factory.by_automation_id("LargeListView")
        ).as_data_grid_view()

    @property
    def list_view_grid(self) -> Grid:
        """Returns the List View 1 element.

        :return: The List View 1 element.
        """
        return self.parent_element.find_first_descendant(
            condition=self._condition_factory.by_automation_id("listView1")
        ).as_grid()

    @property
    def more_options_button(self) -> Button:
        """Returns the More Options Button element.

        :return: The More Options Button element.
        """
        return self.parent_element.find_first_descendant(
            condition=self._condition_factory.by_automation_id("HeaderSite")
        ).as_button()

    @property
    def tree_elements(self) -> Tree:
        """Returns the Tree Elements element.

        :return: The Tree Elements element.
        """
        return self.parent_element.find_first_descendant(
            condition=self._condition_factory.by_automation_id("treeView1")
        ).as_tree()
