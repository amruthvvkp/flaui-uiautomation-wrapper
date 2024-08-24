"""This contains element map for the tab More Controls for the WPF test application."""

from flaui.core.automation_elements import Calendar, ListBox, Tab, TabItem
from flaui.core.input import Wait

from tests.test_utilities.elements.wpf_application.common import AbtstractControlCollection
from tests.test_utilities.elements.wpf_application.constants import ApplicationTabIndex


class MoreControlsElements(AbtstractControlCollection):
    """This class is used to store the More Controls element locators for the WPF application."""

    tab: Tab

    @property
    def parent_element(self) -> TabItem:
        """Returns the Simple Controls element.

        :return: The Simple Controls element.
        """
        element = self.tab.find_first_child(condition=self._cf.by_name("More Controls")).as_tab_item()

        if not element.is_selected:
            self.tab.select_tab_item(ApplicationTabIndex.MORE_CONTROLS.value)
            Wait.until_input_is_processed()
        return element

    @property
    def calender(self) -> Calendar:
        """Returns the Calender element.

        :return: The Calender element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("calendar")).as_calendar()

    # @property
    # def date_picker_show_calendar_button(self) -> Button:
    #     """Returns the Show Calendar Button element, This is a child of the DatePicker element.

    #     :return: The Show Calendar Button element.
    #     """
    #     return self.date_picker.find_first_child(condition=self._cf.by_name("Show Calendar")).as_button()

    # @property
    # def date_picker_edit_text_box(self) -> TextBox:
    #     """Returns the Edit TextBox element, This is a child of the DatePicker element.

    #     :return: The Edit TextBox element.
    #     """
    #     return self.date_picker.find_first_child(condition=self._cf.by_name("PART_TextBox")).as_text_box()

    @property
    def large_list_box(self) -> ListBox:
        """Returns the Large ListBox element.

        :return: The Large ListBox element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("LargeListBox")).as_list_box()
