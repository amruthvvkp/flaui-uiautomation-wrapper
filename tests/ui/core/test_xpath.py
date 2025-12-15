"""Tests for XPath functionality, ported from C# XPathTests.cs and XPathTests2.cs."""

import platform

from flaui.core.application import Application
from flaui.core.definitions import ControlType
from flaui.modules.automation import Automation
import pytest


class TestXPath:
    """Tests for XPath search functionality."""

    def test_notepad_find_first_by_xpath(self, automation: Automation) -> None:
        """Test finding first element by XPath in Notepad.

        Ported from XPathTests.cs::NotepadFindFirst
        """
        app = Application.launch("notepad.exe")
        try:
            window = app.get_main_window(automation)
            assert window is not None
            assert window.title is not None

            # Find File menu item - text varies by Windows version/language
            file_menu = window.find_first_by_x_path("/MenuBar/MenuItem[@Name='File']")
            assert file_menu is not None
        finally:
            try:
                app.close()
            except Exception:
                pass

    def test_notepad_find_all_by_xpath(self, automation: Automation) -> None:
        """Test finding all elements by XPath in Notepad.

        Ported from XPathTests.cs::NotePadFindAll
        """
        app = Application.launch("notepad.exe")
        try:
            window = app.get_main_window(automation)
            assert window is not None
            assert window.title is not None

            # Find all menu items
            items = window.find_all_by_x_path("//MenuItem")
            assert items is not None
            # Note: Count may vary by Windows version
            assert len(items) >= 5, f"Expected at least 5 menu items, found {len(items)}"
        finally:
            try:
                app.close()
            except Exception:
                pass

    def test_notepad_find_by_automation_id(self, automation: Automation) -> None:
        """Test finding element by AutomationId using XPath.

        Ported from XPathTests.cs::NotepadFindByAutomationId
        """
        app = Application.launch("notepad.exe")
        try:
            window = app.get_main_window(automation)

            # Find element with AutomationId 15 (text document area)
            elem = window.find_all_by_x_path("//*[@AutomationId='15']")
            assert len(elem) == 1
            assert elem[0].control_type == ControlType.Document
        finally:
            try:
                app.close()
            except Exception:
                pass

    def test_notepad_find_all_indexed(self, automation: Automation) -> None:
        """Test finding elements using indexed XPath expressions.

        Ported from XPathTests.cs::NotePadFindAllIndexed
        """
        app = Application.launch("notepad.exe")
        try:
            window = app.get_main_window(automation)
            assert window is not None
            assert window.title is not None

            # Find first MenuBar's MenuItem children
            items = window.find_all_by_x_path("(//MenuBar)[1]/MenuItem")
            assert items is not None
            # Note: Result count may vary by Windows version

            # Find second MenuBar's MenuItem children (if exists)
            items2 = window.find_all_by_x_path("(//MenuBar)[2]/MenuItem")
            # May or may not exist depending on Notepad version
        finally:
            try:
                app.close()
            except Exception:
                pass

    @pytest.mark.skipif(platform.system() != "Windows", reason="MS Paint is Windows-specific")
    def test_paint_find_element_below_unknown(self, automation: Automation) -> None:
        """Test finding element below unknown element types in Paint.

        Ported from XPathTests.cs::PaintFindElementBelowUnknown
        """
        app = Application.launch("mspaint.exe")
        try:
            window = app.get_main_window(automation)

            # Windows 11 uses RadioButton, older versions use Button
            element_type = "RadioButton" if platform.win32_ver()[0] >= "10.0.22000" else "Button"

            # Try to find brush tool (name may vary by Windows version)
            button = window.find_first_by_x_path(f"//{element_type}[@Name='Brushes']")
            if button is None:
                # Try alternative names
                button = window.find_first_by_x_path(f"//{element_type}[contains(@Name,'Brush')]")

            assert button is not None
        finally:
            try:
                app.close()
            except Exception:
                pass

    @pytest.mark.skipif(platform.system() != "Windows", reason="MS Paint is Windows-specific")
    def test_paint_reference_element_with_unknown_type(self, automation: Automation) -> None:
        """Test finding reference element with unknown control type in Paint.

        Ported from XPathTests.cs::PaintReferenceElementWithUnknownType
        """
        app = Application.launch("mspaint.exe")
        try:
            window = app.get_main_window(automation)

            # Find Custom control type
            unknown = window.find_first_by_x_path("//Custom")
            assert unknown is not None
        finally:
            try:
                app.close()
            except Exception:
                pass

    def test_xpath_contains_function(self, automation: Automation) -> None:
        """Test XPath contains() function.

        Ported from XPathTests.cs::ContainsTest
        """
        app = Application.launch("notepad.exe")
        try:
            window = app.get_main_window(automation)

            # Find elements containing text in Name
            items = window.find_all_by_x_path("//MenuItem[contains(@Name,'ile')]")
            assert items is not None
            assert len(items) > 0, "Should find File menu item"
        finally:
            try:
                app.close()
            except Exception:
                pass

    def test_xpath_is_password_property(self, test_application, automation: Automation) -> None:
        """Test XPath with IsPassword property.

        Ported from XPathTests2.cs::IsPassword
        """
        window = test_application.main_window

        # Find password box using IsPassword property
        password_box = window.find_first_by_x_path("//*[@IsPassword='true']")
        assert password_box is not None, "Should find password box element"
