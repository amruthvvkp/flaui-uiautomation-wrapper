"""This module maps up all the elements in Simple Controls tab for the WPF application."""

import time

from flaui.core.automation_elements import (
    AutomationElement,
    Button,
    CheckBox,
    ComboBox,
    DateTimePicker,
    Label,
    ListBox,
    ProgressBar,
    RadioButton,
    Slider,
    Spinner,
    Tab,
    TabItem,
    TextBox,
)
from flaui.core.definitions import ControlType
from flaui.lib.exceptions import ElementNotFound, FlaUIException, SystemException

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
        if self.tab.selected_tab_item_index != ApplicationTabIndex.SIMPLE_CONTROLS.value:
            self.tab.select_tab_item(index=ApplicationTabIndex.SIMPLE_CONTROLS.value, post_wait=True)
        return self.tab.tab_items[ApplicationTabIndex.SIMPLE_CONTROLS.value]

    @property
    def test_label(self) -> Label:
        """Returns the Test Label element.

        :return: The Test Label element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_text("Test Label")
        ).as_label()

    @property
    def test_text_box(self) -> TextBox:
        """Returns the Test TextBox element.

        :return: The Test TextBox element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("TextBox")
        ).as_text_box()

    @property
    def password_box(self) -> TextBox:
        """Returns the password box element.

        :return: The password box element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("PasswordBox")
        ).as_text_box()

    @property
    def editable_combo_box(self) -> ComboBox:
        """Returns the Editable ComboBox element.

        :return: The Editable ComboBox element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("EditableCombo")
        ).as_combo_box()

    @property
    def non_editable_combo_box(self) -> ComboBox:
        """Returns the Non-Editable ComboBox element.

        :return: The Non-Editable ComboBox element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("NonEditableCombo")
        ).as_combo_box()

    @property
    def list_box(self) -> ListBox:
        """Returns the List Box element.

        :return: The List Box element.
        """
        return self.main_window.find_first_descendant(
            condition=self._get_condition_factory.by_automation_id("ListBox")
        ).as_list_box()

    @property
    def test_check_box(self) -> CheckBox:
        """Returns the Test CheckBox element.

        :return: The Test CheckBox element.
        """
        return self.main_window.find_first_descendant(
            condition=self._get_condition_factory.by_name("Test Checkbox")
        ).as_check_box()

    @property
    def three_way_check_box(self) -> CheckBox:
        """Returns the Three Way CheckBox element.

        :return: The Three Way CheckBox element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("ThreeStateCheckBox")
        ).as_check_box()

    @property
    def radio_button_1(self) -> RadioButton:
        """Returns the Radio Button 1 element.

        :return: The Radio Button 1 element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("RadioButton1")
        ).as_radio_button()

    @property
    def radio_button_2(self) -> RadioButton:
        """Returns the Radio Button 2 element.

        :return: The Radio Button 2 element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("RadioButton2")
        ).as_radio_button()

    @property
    def progress_bar(self) -> ProgressBar:
        """Returns the Progress Bar element.

        :return: The Progress Bar element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("ProgressBar")
        ).as_progress_bar()

    @property
    def slider(self) -> Slider:
        """Returns the Slider element.

        :return: The Slider element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("Slider")
        ).as_slider()

    @property
    def context_menu_button(self) -> Button:
        """Returns the Context Menu Button element.

        :return: The Context Menu Button element.
        """
        return self.parent_element.find_first_descendant(
            condition=self._get_condition_factory.by_name("ContextMenu")
        ).as_button()

    @property
    def invoke_me_button(self) -> Button:
        """Returns the Invoke Me Button element.

        :return: The Invoke Me Button element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("InvokableButton")
        ).as_button()

    @property
    def big_button(self) -> AutomationElement:
        """Returns the Big Button element.

        :return: The Big Button element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_name("BigButton")
        ).as_button()

    @property
    def popup_toggle_button1(self) -> Button:
        """Returns the Popup Toggle Button 1 element.

        :return: The Popup Toggle Button 1 element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("PopupToggleButton1")
        ).as_button()

    @property
    def popup_toggle_button2(self) -> Button:
        """Returns the Popup Toggle Button 2 element.

        :return: The Popup Toggle Button 2 element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("PopupToggleButton2")
        ).as_button()

    @property
    def menu_item_checked_text_box(self) -> Label:
        """Returns the Menu Item Checked Label element.

        :return: The Menu Item Checked Label element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("lblMenuChk")
        ).as_label()

    @property
    def spinner(self) -> Spinner:
        """Returns Spinner control

        Note: Spinner control only works with UIA3 + WinForms due to platform limitations.
        This matches C# FlaUI SpinnerTests which only runs on that combination.

        The control is located by ``ControlType.Spinner`` + ``Name == "Spinner"`` rather than by
        AutomationID. The WinForms app exposes two ``Spinner`` controls (the labelled target named
        "Spinner" and an unlabelled one named "NumericUpDown"), and the target's AutomationID is
        unstable - it intermittently flips from ``numericUpDown1`` to a generated numeric value,
        which is the root cause of GH-74. ControlType + Name are stable across that instability.

        The lookup is retried a few times because in bulk runs the UIA tree can momentarily be
        incomplete. The decisive flakiness in GH-74 was a transient ``REGDB_E_IIDNOTREG`` COM hiccup
        raised during element discovery when the app is backgrounded behind the other matrix combos.
        That surfaces as a :class:`~flaui.lib.exceptions.SystemException` (a raw ``System.Exception``
        kept outside the ``FlaUIException`` tree), *not* an ``ElementNotFound`` - so an earlier
        ``except ElementNotFound`` retry let it escape and fail the test. The retry below therefore
        also swallows ``SystemException``/``FlaUIException`` between attempts and only raises a clean
        ``ElementNotFound`` once all attempts are exhausted.

        :return: Spinner element
        :raises ElementNotFound: If spinner control is not found (expected on non-UIA3+WinForms)
        """
        cf = self._get_condition_factory
        last_error: Exception | None = None
        for _ in range(5):
            try:
                # Ensure the Simple Controls tab is active before searching. In bulk runs another
                # test class sharing the session app may have left a different tab selected, and the
                # spinner lives on the Simple Controls page; parent_element selects it via the UIA
                # SelectionItem pattern (more reliable than a mouse click).
                _ = self.parent_element
                # Primary: stable ControlType.Spinner + Name match (independent of the unstable
                # AutomationID that is the root cause of GH-74).
                for element in self.main_window.find_all_descendants(
                    condition=cf.by_control_type(ControlType.Spinner)
                ):
                    if element.name == "Spinner":
                        return element.as_spinner()
                # Fallback: original AutomationID lookup, in case the control is ever renamed.
                return self.main_window.find_first_descendant(
                    condition=cf.by_automation_id("numericUpDown1")
                ).as_spinner()
            except (FlaUIException, SystemException) as error:
                # ElementNotFound (tab/control not ready) and the transient REGDB_E_IIDNOTREG COM
                # hiccup (-> SystemException) are both expected mid-bulk-run; retry after a short
                # settle. FlaUIException is the base of ElementNotFound, so it is covered here too.
                last_error = error
                time.sleep(0.5)
        raise ElementNotFound(
            "Spinner control not found after retries. Note: Spinner only works with UIA3 + WinForms "
            f"(C# platform limitation). Last error: {last_error}"
        )

    @property
    def date_picker(self) -> DateTimePicker:
        """Returns the DatePicker element.

        :return: The DatePicker element.
        """
        return self.parent_element.find_first_child(
            condition=self._get_condition_factory.by_automation_id("dateTimePicker1")
        ).as_date_time_picker()
