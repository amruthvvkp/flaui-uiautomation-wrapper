"""UI tests for the ``FlaUI.Core.Debug`` wrapper (GH-159), on the UIA2/UIA3 x WinForms/WPF matrix."""

import logging

from flaui.core import debug
from flaui.core.automation_elements import AutomationElement, Window
from flaui.core.condition_factory import ConditionFactory
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.fixture
def window(test_application: WinFormsApplicationElements | WPFApplicationElements) -> Window:
    """Return the test application's main window."""
    return test_application.main_window


@pytest.fixture
def radio_button(window: Window, condition_factory: ConditionFactory) -> AutomationElement:
    """Return the Simple Controls ``RadioButton1``, present in both test applications."""
    return window.find_first_descendant(condition_factory.by_automation_id("RadioButton1"))


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestDebug:
    """Tests for ``details()`` and ``get_xpath_to_element()``."""

    # FlaUI's Debug.Details caches a fixed property set over the subtree and returns "" if any
    # read fails. The WinForms MSAA proxy intermittently rejects the cached HelpText/AutomationId,
    # so the full content check runs on WPF only; WinForms is covered by the "never raises" test.
    @pytest.mark.platform_limitation
    @pytest.mark.usefixtures("skip_on_winforms")
    def test_details_describes_element(self, radio_button: AutomationElement) -> None:
        """``details()`` returns a multi-line dump naming the element and its patterns."""
        text = debug.details(radio_button)
        assert len(text.splitlines()) > 1
        assert "AutomationId: RadioButton1" in text
        assert "ControlType: RadioButton" in text
        assert "SelectionItem" in text

    @pytest.mark.usefixtures("skip_on_wpf")
    def test_details_on_winforms_never_raises(
        self, radio_button: AutomationElement, caplog: pytest.LogCaptureFixture
    ) -> None:
        """On WinForms ``details()`` returns a real dump, or "" with FlaUI's error logged."""
        with caplog.at_level(logging.WARNING, logger="flaui.core.debug"):
            text = radio_button.details()
        if text:
            assert "AutomationId: RadioButton1" in text
        else:
            assert "Failed to dump info" in caplog.text

    @pytest.mark.usefixtures("skip_on_winforms")
    def test_details_method_matches_module(self, radio_button: AutomationElement) -> None:
        """``AutomationElement.details()`` delegates to the module function."""
        text = radio_button.details()
        assert text
        assert text == debug.details(radio_button)

    def test_xpath_from_desktop_root_finds_same_element(self, window: Window, radio_button: AutomationElement) -> None:
        """Rooted at the desktop, the path is window-relative and finds the same element again."""
        desktop = radio_button.automation.get_desktop()
        xpath = debug.get_xpath_to_element(radio_button, desktop)
        assert xpath.startswith("/") and not xpath.startswith("/Window")
        assert xpath.split("/")[-1].startswith("RadioButton")
        assert window.find_first_by_x_path(xpath).equals(radio_button)

    # Without a root FlaUI indexes the window among every top-level window on the desktop, which
    # is slow on a busy desktop.
    @pytest.mark.timeout(120)
    def test_xpath_without_root_starts_at_window(self, radio_button: AutomationElement) -> None:
        """Without a root the path starts at the top-level window under the desktop."""
        desktop = radio_button.automation.get_desktop()
        full = radio_button.get_xpath_to_element()
        relative = radio_button.get_xpath_to_element(desktop)
        assert full.startswith("/Window")
        assert full.endswith(relative)

    def test_xpath_with_ancestor_root_drops_its_child_step(
        self, window: Window, radio_button: AutomationElement
    ) -> None:
        """Like FlaUI C#, a root leaves out the step for the root's direct child."""
        desktop = radio_button.automation.get_desktop()
        from_desktop = debug.get_xpath_to_element(radio_button, desktop)
        from_window = debug.get_xpath_to_element(radio_button, window)
        assert from_window == "/" + from_desktop.split("/", 2)[2]

    def test_xpath_method_matches_module(self, window: Window, radio_button: AutomationElement) -> None:
        """``AutomationElement.get_xpath_to_element()`` delegates to the module function."""
        assert radio_button.get_xpath_to_element(window) == debug.get_xpath_to_element(radio_button, window)
