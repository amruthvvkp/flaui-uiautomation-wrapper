"""Unit tests pinning C# properties that must stay Python properties (not methods).

``TitleBar.MinimizeButton``, ``Window.ModalWindows`` and ``Tab.SelectedTabItem`` are C# properties.
The wrappers used to call them like methods (``raw.MinimizeButton()``), which raised ``TypeError`` on
every use. A mock stands in for the C# element so these run without a UI.
"""

from unittest.mock import MagicMock

from flaui.core.automation_elements import Button, Tab, TabItem, TitleBar, Window
import pytest


@pytest.mark.parametrize(
    ("attribute", "cs_property"),
    [
        ("minimize_button", "MinimizeButton"),
        ("maximize_button", "MaximizeButton"),
        ("restore_button", "RestoreButton"),
        ("close_button", "CloseButton"),
    ],
)
def test_title_bar_buttons_are_properties(attribute: str, cs_property: str) -> None:
    """Each title bar button is read from the C# property and wrapped as a Button."""
    raw = MagicMock()
    raw_button = MagicMock()
    setattr(raw, cs_property, raw_button)

    button = getattr(TitleBar(raw_element=raw), attribute)

    assert isinstance(button, Button)
    assert button.raw_element is raw_button


def test_modal_windows_is_a_property() -> None:
    """``modal_windows`` iterates the C# ``ModalWindows`` array and wraps each entry as a Window."""
    raw = MagicMock()
    raw.ModalWindows = [MagicMock(), MagicMock()]

    windows = Window(raw_element=raw).modal_windows

    assert [w.raw_element for w in windows] == raw.ModalWindows
    assert all(isinstance(w, Window) for w in windows)


def test_selected_tab_item_is_a_property() -> None:
    """``selected_tab_item`` wraps the C# ``SelectedTabItem`` property as a TabItem."""
    raw = MagicMock()

    item = Tab(raw_element=raw).selected_tab_item

    assert isinstance(item, TabItem)
    assert item.raw_element is raw.SelectedTabItem


def test_draw_highlight_passes_duration_as_int_milliseconds() -> None:
    """``draw_highlight`` must call ``OverlayManager.Show(Rectangle, Color, int ms)``, not a TimeSpan."""
    from flaui.core.automation_elements import AutomationElement
    from flaui.lib.system.drawing import Color

    raw = MagicMock()
    AutomationElement(raw_element=raw).draw_highlight(Color.Blue, duration=750)

    rect, color, duration = raw.Automation.OverlayManager.Show.call_args.args
    assert rect is raw.Properties.BoundingRectangle.Value
    assert duration == 750 and isinstance(duration, int)
