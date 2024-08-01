"""Tests for the Checkbox class."""

from flaui.core.definitions import ToggleState

from tests.assets.elements.wpf_application.base import WPFApplicationElements


class TestCalendarElements:
    """Tests for the Checkbox class."""

    # TODO: Use this Restart application test elsewhere to test the restart functionality
    # def restart_application(
    #     self, wpf_application: Automation, automation: Any, ui_automation_type: UIAutomationTypes
    # ) -> WPFApplicationElements:
    #     """Restarts the test application.

    #     :param wpf_application: Test application to restart.
    #     :param automation: Automation class to use for the tests.
    #     :param ui_automation_type: UIAutomation type to use for the tests.
    #     :return: WPF application element map.
    #     """
    #     wpf_application.application.close()
    #     # TODO: Add Retry.WhileFalse(() => Application.HasExited, TimeSpan.FromSeconds(2), ignoreException: true) method here once the tools namespace is implemented
    #     wpf_application.application.dispose()

    #     wpf_application = Automation(ui_automation_type)
    #     wpf_application.application.launch(
    #         test_settings.WPF_TEST_APP_EXE.as_posix()
    #         if ui_automation_type == UIAutomationTypes.UIA3
    #         else test_settings.WINFORMS_TEST_APP_EXE.as_posix()
    #     )
    #     main_window = wpf_application.application.get_main_window(automation)
    #     return WPFApplicationElements(main_window=main_window)

    def test_toggle_element(self, test_elements: WPFApplicationElements):
        """Tests the toggle method of the Checkbox class.

        :param wpf_elements: The WPF application element map.
        """
        checkbox = test_elements.simple_controls_tab.test_check_box
        assert checkbox.toggle_state == ToggleState.Off
        checkbox.toggle()
        assert checkbox.toggle_state == ToggleState.On

    def test_set_state(self, test_elements: WPFApplicationElements):
        """Tests the set_state method of the Checkbox class.

        :param wpf_elements: The WPF application element map.
        """
        checkbox = test_elements.simple_controls_tab.test_check_box
        checkbox.toggle_state = ToggleState.On
        assert checkbox.toggle_state == ToggleState.On
        checkbox.toggle_state = ToggleState.Off
        assert checkbox.toggle_state == ToggleState.Off
        checkbox.toggle_state = ToggleState.On
        assert checkbox.toggle_state == ToggleState.On

    def test_three_way_toggle(self, test_elements: WPFApplicationElements):
        """Tests the three_way_toggle method of the Checkbox class.

        :param wpf_elements: The WPF application element map.
        """
        checkbox = test_elements.simple_controls_tab.three_way_check_box
        assert checkbox.toggle_state == ToggleState.Off
        checkbox.toggle()
        assert checkbox.toggle_state == ToggleState.On
        checkbox.toggle()
        assert checkbox.toggle_state == ToggleState.Indeterminate

    def test_three_way_set_state(self, test_elements: WPFApplicationElements):
        """Tests the three_way_set_state method of the Checkbox class.

        :param wpf_elements: The WPF application element map.
        """
        checkbox = test_elements.simple_controls_tab.three_way_check_box
        checkbox.toggle_state = ToggleState.On
        assert checkbox.toggle_state == ToggleState.On
        checkbox.toggle_state = ToggleState.Off
        assert checkbox.toggle_state == ToggleState.Off
        checkbox.toggle_state = ToggleState.Indeterminate
        assert checkbox.toggle_state == ToggleState.Indeterminate
