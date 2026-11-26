"""Journeys through the main menu, a checkable menu item and the context menu."""

from flaui.core.input import Mouse, MouseButton, Wait
from flaui.core.tools import Retry
from flaui.lib.exceptions import ElementNotFound
import pytest

from tests.integration.conftest import JourneyApp

pytestmark = pytest.mark.integration


class TestMenuJourneys:
    """Drive menus the way a user does: by clicking through them."""

    def test_click_through_nested_menu(self, journey_app: JourneyApp) -> None:
        """Open ``Edit > Copy`` with the mouse, read the submenu, then close it with Escape."""
        journey_app.bring_to_front()
        try:
            edit = journey_app.menu.get_item_by_name("Edit")
            edit.click(post_wait=True)
            copy = edit.get_item_by_name("Copy")
            copy.click(post_wait=True)
            assert [item.name for item in copy.items] == ["Plain", "Fancy"]
            assert copy.get_item_by_name("Fancy").is_enabled
        finally:
            journey_app.dismiss_popups()

        # Closing the menus leaves the form as the main window, not a leftover dropdown (GH-82).
        assert journey_app.refresh().main_window.title == journey_app.elements.application_name
        assert journey_app.elements.simple_controls_tab.test_text_box.text == "Test TextBox"

    # GH-78: UI Automation exposes no Toggle pattern for WinForms menu items, and the WinForms app
    # has no "Show Label" item, so this journey runs on the two WPF combinations only.
    @pytest.mark.platform_limitation
    def test_checkable_menu_item_hides_and_shows_label(self, journey_app: JourneyApp, skip_on_winforms: None) -> None:
        """Untick ``Edit > Show Label`` to hide the label, then tick it again to bring it back."""
        page = journey_app.elements.simple_controls_tab
        assert page.menu_item_checked_text_box.name == "Menu Item Checked"

        def click_show_label() -> None:
            """Open the Edit menu and click its Show Label item."""
            journey_app.bring_to_front()
            edit = journey_app.menu.get_item_by_name("Edit")
            edit.click(post_wait=True)
            edit.get_item_by_name("Show Label").click(post_wait=True)

        def label_is_gone() -> bool:
            """Return True once the label has been removed from the UI tree."""
            try:
                _ = page.menu_item_checked_text_box
            except ElementNotFound:
                return True
            return False

        click_show_label()
        assert Retry.WhileFalse(label_is_gone, timeout=3000), "Label still shown after unticking Show Label"
        assert journey_app.menu.get_item_by_name("Edit").get_item_by_name("Show Label").is_checked is False
        journey_app.dismiss_popups()

        click_show_label()
        label = Retry.WhileException(lambda: page.menu_item_checked_text_box, timeout=3000)
        assert label.name == "Menu Item Checked"
        assert journey_app.menu.get_item_by_name("Edit").get_item_by_name("Show Label").is_checked is True
        journey_app.dismiss_popups()

    # GH-79: the WinForms context menu is not exposed through UIA3 on newer .NET versions, so this
    # journey is skipped on UIA3 + WinForms and runs on the other three combinations.
    @pytest.mark.platform_limitation
    def test_context_menu_open_submenu_and_dismiss(self, journey_app: JourneyApp, skip_on_uia3_winforms: None) -> None:
        """Right-click the ContextMenu button, open its submenu, then dismiss every level."""
        button = journey_app.elements.simple_controls_tab.context_menu_button
        journey_app.bring_to_front()
        Mouse.click(button.get_clickable_point(), mouse_button=MouseButton.Right, post_wait=True)
        try:
            context_menu = Retry.WhileException(lambda: journey_app.main_window.context_menu, timeout=3000)
            assert [item.name for item in context_menu.items] == ["Context 1", "Context 2"]

            submenu = context_menu.items[1]
            submenu.click(post_wait=True)
            assert [item.text for item in submenu.items] == ["Inner Context"]
        finally:
            journey_app.dismiss_popups()
        Wait.until_input_is_processed()

        # Every popup level is closed, so the form is the main window again (GH-82).
        assert journey_app.refresh().main_window.title == journey_app.elements.application_name
        assert journey_app.elements.simple_controls_tab.context_menu_button.name == "ContextMenu"
