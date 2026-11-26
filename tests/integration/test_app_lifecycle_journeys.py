"""Journeys covering an application's whole life: launch, attach from a second client, and close."""

from flaui.core.application import Application
from flaui.core.input import Wait
from flaui.core.tools import Retry
import pytest

from tests.integration.conftest import JourneyApp

pytestmark = pytest.mark.integration


class TestAppLifecycleJourneys:
    """Launch, attach and close the bundled test applications end to end."""

    def test_launch_attach_by_process_and_close(self, journey_app: JourneyApp) -> None:
        """Attach a second ``Application`` to the running process, drive it, then close it gracefully."""
        launched = journey_app.application
        process_id = launched.process_id
        assert process_id > 0

        attached = Application()
        attached.attach(process_id)
        try:
            assert attached.process_id == process_id
            assert attached.has_exited is False

            # The attached handle resolves the same main window and can drive the UI.
            window = attached.get_main_window(journey_app.automation)
            assert window.title == journey_app.elements.application_name
            assert journey_app.automation.automation_base.compare(window, journey_app.main_window)

            text_box = journey_app.refresh().simple_controls_tab.test_text_box
            text_box.text = "Typed through the attached app"
            assert text_box.text == "Typed through the attached app"

            # A graceful close (WM_CLOSE) works and the original launch handle sees the exit too.
            assert attached.close(kill_if_close_fails=False) is True
            assert Retry.WhileFalse(lambda: launched.has_exited, timeout=5000, interval=100)
        finally:
            attached.dispose()

    def test_close_through_title_bar_button(self, journey_app: JourneyApp) -> None:
        """Close the app the way a user would, with the title bar's Close button.

        (``File > Exit`` exists in both test apps but has no handler, so it cannot be used here.)
        """
        journey_app.bring_to_front()
        title_bar = journey_app.main_window.title_bar
        assert title_bar.close_button.is_enabled
        title_bar.close_button.click()
        Wait.until_input_is_processed()

        assert Retry.WhileFalse(lambda: journey_app.application.has_exited, timeout=5000, interval=100), (
            "The application did not exit after clicking the title bar Close button"
        )
