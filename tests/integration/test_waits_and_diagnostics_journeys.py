"""Journeys that wait on UI changes with ``expect()`` / ``Retry`` and capture evidence on failure."""

from contextlib import contextmanager
from pathlib import Path
import struct
from typing import Generator

from flaui.core.automation_elements import AutomationElement
from flaui.core.capturing import Capture
from flaui.core.expectations import expect
from flaui.core.tools import Retry
import pytest

from tests.integration.conftest import JourneyApp

pytestmark = pytest.mark.integration


@contextmanager
def capture_on_failure(element: AutomationElement, image_path: Path) -> Generator[None, None, None]:
    """Save a PNG of ``element`` if the block raises, then re-raise.

    This is the pattern a suite would use to attach a screenshot to a failing step.

    :param element: The element to photograph when the block fails.
    :param image_path: Where to write the PNG.
    :yield: Control to the guarded block.
    """
    try:
        yield
    except Exception:
        with Capture.element(element) as image:
            image.to_file(str(image_path))
        raise


def _png_size(image_path: Path) -> tuple[int, int]:
    """Read the pixel size from a PNG's IHDR chunk.

    :param image_path: Path to a PNG file.
    :return: ``(width, height)`` in pixels.
    """
    header = image_path.read_bytes()[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n", "Not a PNG file"
    width, height = struct.unpack(">II", header[16:24])
    return width, height


class TestWaitsAndDiagnosticsJourneys:
    """Auto-waiting assertions across UI changes, and screenshots on the failure path."""

    def test_expect_and_retry_across_page_change(self, journey_app: JourneyApp) -> None:
        """Wait for a check box, a text box and a whole tab page to change state."""
        page = journey_app.elements.simple_controls_tab

        check_box = page.test_check_box
        expect(check_box).not_.to_be_checked(timeout=1000)
        journey_app.bring_to_front()
        check_box.click(post_wait=True)
        expect(check_box).to_be_checked()

        text_box = page.test_text_box
        text_box.text = "Waited for"
        expect(text_box).to_have_text("Waited for")

        # Click the Complex Controls tab and wait for the tree to appear on the new page.
        journey_app.elements.tab.tab_items[1].click(post_wait=True)
        tree = Retry.WhileException(
            lambda: journey_app.elements.complex_controls_tab.tree_elements, timeout=5000, interval=200
        )
        expect(tree).to_be_visible()
        expect(tree).to_be_enabled()

        # Going back hides the tree again.
        journey_app.elements.tab.tab_items[0].click(post_wait=True)
        expect(tree).not_.to_be_visible()
        expect(page.test_check_box).to_be_checked()

    # The WinForms test app has no "Invoke me!" button, so this journey runs on WPF only.
    def test_expect_waits_for_caption_change_after_invoke(
        self, journey_app: JourneyApp, skip_on_winforms: None
    ) -> None:
        """Invoke a button whose caption changes, and let ``expect`` wait for the new caption."""
        button = journey_app.elements.simple_controls_tab.invoke_me_button
        expect(button).to_have_name("Invoke me!")
        button.invoke()
        expect(button).to_have_name("Invoked!")

    def test_capture_element_screenshot_when_a_step_fails(self, journey_app: JourneyApp, tmp_path: Path) -> None:
        """A failing ``expect`` inside ``capture_on_failure`` leaves a PNG of the element behind."""
        text_box = journey_app.elements.simple_controls_tab.test_text_box
        image_path = tmp_path / f"{journey_app.app_type}-text-box-failure.png"

        with pytest.raises(AssertionError, match="to have text 'not the real text'"):
            with capture_on_failure(text_box, image_path):
                expect(text_box, timeout=300).to_have_text("not the real text")

        assert image_path.exists() and image_path.stat().st_size > 0
        width, height = _png_size(image_path)
        bounds = text_box.bounding_rectangle
        # Capture uses physical pixels; allow for display scaling (up to 300 %) around the UIA bounds.
        assert bounds.width <= width <= bounds.width * 3 + 1
        assert bounds.height <= height <= bounds.height * 3 + 1

        # On the success path nothing is written.
        ok_path = tmp_path / "unused.png"
        with capture_on_failure(text_box, ok_path):
            expect(text_box).to_have_text("Test TextBox")
        assert not ok_path.exists()
