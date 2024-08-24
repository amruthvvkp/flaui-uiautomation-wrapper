"""This module maps up all the elements in Simple Controls tab for the WPF application."""

from flaui.core.automation_elements import (
    AutomationElement,
    Button,
    CheckBox,
    ComboBox,
    Label,
    ListBox,
    ProgressBar,
    RadioButton,
    Slider,
    Tab,
    TabItem,
    TextBox,
)
from flaui.core.input import Wait

from tests.test_utilities.elements.wpf_application.common import AbtstractControlCollection
from tests.test_utilities.elements.wpf_application.constants import ApplicationTabIndex


class SimpleControlsElements(AbtstractControlCollection):
    """This class is used to store the Simple Controls element locators for the WPF application."""

    tab: Tab

    @property
    def parent_element(self) -> TabItem:
        """Returns the Simple Controls element.

        :return: The Simple Controls element.
        """
        element = self.tab.find_first_child(condition=self._cf.by_name("Simple Controls")).as_tab_item()

        if not element.is_selected:
            self.tab.select_tab_item(ApplicationTabIndex.SIMPLE_CONTROLS.value)
            Wait.until_input_is_processed()
        return element

    @property
    def test_label(self) -> Label:
        """Returns the Test Label element.

        :return: The Test Label element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_text("Test Label")).as_label()

    @property
    def test_text_box(self) -> TextBox:
        """Returns the Test TextBox element.

        :return: The Test TextBox element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("TextBox")).as_text_box()

    @property
    def password_box(self) -> TextBox:
        """Returns the password box element.

        :return: The password box element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("PasswordBox")).as_text_box()

    @property
    def editable_combo_box(self) -> ComboBox:
        """Returns the Editable ComboBox element.

        :return: The Editable ComboBox element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("EditableCombo")).as_combo_box()

    @property
    def non_editable_combo_box(self) -> ComboBox:
        """Returns the Non-Editable ComboBox element.

        :return: The Non-Editable ComboBox element.
        """
        return self.parent_element.find_first_child(
            condition=self._cf.by_automation_id("NonEditableCombo")
        ).as_combo_box()

    @property
    def list_box(self) -> ListBox:
        """Returns the List Box element.

        :return: The List Box element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("ListBox")).as_list_box()

    @property
    def test_check_box(self) -> CheckBox:
        """Returns the Test CheckBox element.

        :return: The Test CheckBox element.
        """
        return self.parent_element.find_first_child(
            condition=self._cf.by_automation_id("SimpleCheckBox")
        ).as_check_box()

    @property
    def three_way_check_box(self) -> CheckBox:
        """Returns the Three Way CheckBox element.

        :return: The Three Way CheckBox element.
        """
        return self.parent_element.find_first_child(
            condition=self._cf.by_automation_id("ThreeStateCheckBox")
        ).as_check_box()

    @property
    def radio_button_1(self) -> RadioButton:
        """Returns the Radio Button 1 element.

        :return: The Radio Button 1 element.
        """
        return self.parent_element.find_first_child(
            condition=self._cf.by_automation_id("RadioButton1")
        ).as_radio_button()

    @property
    def radio_button_2(self) -> RadioButton:
        """Returns the Radio Button 2 element.

        :return: The Radio Button 2 element.
        """
        return self.parent_element.find_first_child(
            condition=self._cf.by_automation_id("RadioButton2")
        ).as_radio_button()

    @property
    def progress_bar(self) -> ProgressBar:
        """Returns the Progress Bar element.

        :return: The Progress Bar element.
        """
        return self.parent_element.find_first_child(
            condition=self._cf.by_automation_id("ProgressBar")
        ).as_progress_bar()

    @property
    def slider(self) -> Slider:
        """Returns the Slider element.

        :return: The Slider element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("Slider")).as_slider()

    @property
    def context_menu_button(self) -> Button:
        """Returns the Context Menu Button element.

        :return: The Context Menu Button element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("ContextMenu")).as_button()

    @property
    def invoke_me_button(self) -> Button:
        """Returns the Invoke Me Button element.

        :return: The Invoke Me Button element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("InvokableButton")).as_button()

    @property
    def big_button(self) -> AutomationElement:
        """Returns the Big Button element.

        :return: The Big Button element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_name("BigButton")).as_button()

    @property
    def popup_toggle_button1(self) -> Button:
        """Returns the Popup Toggle Button 1 element.

        :return: The Popup Toggle Button 1 element.
        """
        return self.parent_element.find_first_child(
            condition=self._cf.by_automation_id("PopupToggleButton1")
        ).as_button()

    @property
    def popup_toggle_button2(self) -> Button:
        """Returns the Popup Toggle Button 2 element.

        :return: The Popup Toggle Button 2 element.
        """
        return self.parent_element.find_first_child(
            condition=self._cf.by_automation_id("PopupToggleButton2")
        ).as_button()

    @property
    def menu_item_checked_text_box(self) -> Label:
        """Returns the Menu Item Checked Label element.

        :return: The Menu Item Checked Label element.
        """
        return self.parent_element.find_first_child(condition=self._cf.by_automation_id("lblMenuChk")).as_label()
