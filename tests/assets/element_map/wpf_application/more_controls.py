"""This contains element map for the tab More Controls for the WPD test application."""

from flaui.core.automation_elements import Button, Calendar, DateTimePicker, ListBox, TabItem, TextBox
from flaui.core.definitions import ControlType
from tests.assets.element_map.wpf_application.common import AbtstractControlCollection
from tests.assets.element_map.wpf_application.constants import ApplicationTabIndex


class MoreControlsElements(AbtstractControlCollection):
    """This class is used to store the More Controls element locators for the WPF application."""

    @property
    def parent_element(self) -> TabItem:
        """Returns the Simple Controls element.

        :return: The Simple Controls element.
        """
        tab = self.main_window.find_first_child(condition=self._condition_factory().by_control_type(ControlType.Tab)).as_tab()
        element = tab.find_first_child(condition=self._condition_factory().by_name("More Controls")).as_tab_item()

        if not element.is_selected:
            tab.select_tab_item(ApplicationTabIndex.MORE_CONTROLS.value)
        return element

    @property
    def calender(self) -> Calendar:
        """Returns the Calender element.

        :return: The Calender element.
        """
        return self.parent_element.find_first_child(condition=self._condition_factory().by_automation_id("calendar")).as_calendar()


    @property
    def date_picker(self) -> DateTimePicker:
        """Returns the DatePicker element.

        :return: The DatePicker element.
        """
        return self.parent_element.find_first_child(condition=self._condition_factory().by_automation_id("datePicker")).as_date_time_picker()

    @property
    def date_picker_show_calendar_button(self) -> Button:
        """Returns the Show Calendar Button element, This is a child of the DatePicker element.

        :return: The Show Calendar Button element.
        """
        return self.date_picker.find_first_child(condition=self._condition_factory().by_name("Show Calendar")).as_button()

    @property
    def date_picker_edit_text_box(self) -> TextBox:
        """Returns the Edit TextBox element, This is a child of the DatePicker element.

        :return: The Edit TextBox element.
        """
        return self.date_picker.find_first_child(condition=self._condition_factory().by_name("PART_TextBox")).as_text_box()

    @property
    def large_list_box(self) -> ListBox:
        """Returns the Large ListBox element.

        :return: The Large ListBox element.
        """
        return self.parent_element.find_first_child(condition=self._condition_factory().by_automation_id("LargeListBox")).as_list_box()
