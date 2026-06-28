"""UI integration tests for capturing, overlay, and element repr (GH-95 / GH-103 / GH-87).

Runs across the UIA2/UIA3 x WinForms/WPF matrix via the shared ``test_application`` fixture. Video
recording (which needs ffmpeg) is covered by unit tests only.
"""

from pathlib import Path
from typing import Any

from flaui.core.capturing import Capture, CaptureImage, CaptureSettings
from flaui.core.overlay import OverlayManager
from flaui.lib.system.drawing import Color
import pytest

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestCapture:
    """Screen/element capture against the live test application window."""

    def test_main_screen_capture(self) -> None:
        """Capturing the primary screen yields a non-empty image."""
        with Capture.main_screen() as image:
            assert isinstance(image, CaptureImage)
            assert image.bitmap is not None
            assert image.original_bounds.width > 0
            assert image.original_bounds.height > 0

    def test_element_capture(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Capturing the main window yields an image sized to the window."""
        window = test_application.main_window
        with Capture.element(window) as image:
            assert image.bitmap is not None
            assert image.original_bounds.width > 0
            assert image.original_bounds.height > 0

    def test_capture_to_file(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, tmp_path: Path
    ) -> None:
        """An element capture can be written to a PNG file on disk."""
        window = test_application.main_window
        out = tmp_path / "window.png"
        with Capture.element(window, CaptureSettings(output_scale=0.5)) as image:
            image.to_file(str(out))
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestOverlay:
    """Overlay manager exposed by the automation behind the live window."""

    def test_overlay_manager_is_typed_facade(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """``automation.overlay_manager`` returns the Python facade with readable settings."""
        manager = test_application.main_window.automation.overlay_manager
        assert isinstance(manager, OverlayManager)
        assert isinstance(manager.size, int)

    def test_overlay_show_does_not_raise(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """Showing a short, non-blocking overlay around the window completes without error."""
        window = test_application.main_window
        window.automation.overlay_manager.show(window.bounding_rectangle, Color.Red, 1)


@pytest.mark.usefixtures("test_application", "ui_automation_type", "test_application_type")
class TestElementRepr:
    """The debug ``repr`` is safe and informative on live elements (GH-87)."""

    def test_repr_includes_type_and_is_safe(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """``repr`` contains the class name and never raises."""
        window: Any = test_application.main_window
        text = repr(window)
        assert text.startswith("<")
        assert type(window).__name__ in text
