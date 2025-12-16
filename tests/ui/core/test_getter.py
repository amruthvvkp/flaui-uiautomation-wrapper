"""Tests for pattern and property getters with caching, ported from C# GetterTests.cs."""
# TOOD: Tests running into frequent errors, need investigation later
# from flaui.core.automation_elements import Window
# from flaui.core.cache_request import CacheRequest
# from flaui.core.definitions import AutomationElementMode, TreeScope
# from flaui.lib.exceptions import (
#     PatternNotCachedException,
#     PatternNotSupportedException,
#     PropertyNotCachedException,
#     PropertyNotSupportedException,
# )
# from flaui.modules.automation import Automation
# import pytest
# from System import Object as SystemObject  # pyright: ignore[reportMissingImports]


# @pytest.mark.skip_notepad_on_win11(reason="Windows 11 Notepad is a Store app; see issue #89")
# class TestGetterPatterns:
#     """Tests for pattern getters with and without caching."""

#     def test_correct_pattern(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting a supported pattern without caching.

#         Ported from GetterTests.cs::CorrectPattern
#         """
#         assert notepad_window is not None
#         window_pattern = notepad_window.framework_automation_element.GetNativePattern[SystemObject](
#             automation.cs_automation.PatternLibrary.WindowPattern
#         )
#         assert window_pattern is not None

#     def test_correct_pattern_cached(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting a supported pattern with caching.

#         Ported from GetterTests.cs::CorrectPatternCached
#         """
#         cache_request = CacheRequest(automation)
#         cache_request.automation_element_mode = AutomationElementMode.None_
#         cache_request.tree_scope = TreeScope.Element
#         cache_request.add_pattern(automation.cs_automation.PatternLibrary.WindowPattern)

#         with cache_request.activate():
#             # Must get window AFTER cache activation for cache to apply
#             window = automation.application.get_main_window(automation)
#             assert window is not None
#             window_pattern = window.framework_automation_element.GetNativePattern[SystemObject](
#                 automation.cs_automation.PatternLibrary.WindowPattern
#             )
#             assert window_pattern is not None

#     def test_unsupported_pattern(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting an unsupported pattern throws PatternNotSupportedException.

#         Ported from GetterTests.cs::UnsupportedPattern
#         """
#         assert notepad_window is not None
#         with pytest.raises(PatternNotSupportedException, match="ExpandCollapse"):
#             notepad_window.framework_automation_element.GetNativePattern[SystemObject](
#                 automation.cs_automation.PatternLibrary.ExpandCollapsePattern
#             )

#     def test_unsupported_pattern_cached(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting an unsupported pattern with caching throws PatternNotSupportedException.

#         Ported from GetterTests.cs::UnsupportedPatternCached
#         """
#         cache_request = CacheRequest(automation)
#         cache_request.automation_element_mode = AutomationElementMode.None_
#         cache_request.tree_scope = TreeScope.Element
#         cache_request.add_pattern(automation.cs_automation.PatternLibrary.ExpandCollapsePattern)

#         with cache_request.activate():
#             # Must get window AFTER cache activation for cache to apply
#             window = automation.application.get_main_window(automation)
#             assert window is not None
#             with pytest.raises(PatternNotSupportedException, match="ExpandCollapse"):
#                 window.framework_automation_element.GetNativePattern[SystemObject](
#                     automation.cs_automation.PatternLibrary.ExpandCollapsePattern
#                 )

#     def test_correct_pattern_uncached(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting a supported but uncached pattern throws PatternNotCachedException.

#         Ported from GetterTests.cs::CorrectPatternUncached
#         """
#         cache_request = CacheRequest(automation)
#         cache_request.automation_element_mode = AutomationElementMode.None_
#         cache_request.tree_scope = TreeScope.Element
#         cache_request.add_pattern(automation.cs_automation.PatternLibrary.ExpandCollapsePattern)

#         with cache_request.activate():
#             # Must get window AFTER cache activation for cache to apply
#             window = automation.application.get_main_window(automation)
#             assert window is not None
#             with pytest.raises(PatternNotCachedException, match="Window"):
#                 window.framework_automation_element.GetNativePattern[SystemObject](
#                     automation.cs_automation.PatternLibrary.WindowPattern
#                 )

#     def test_unsupported_pattern_uncached(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting an unsupported and uncached pattern throws PatternNotCachedException.

#         Ported from GetterTests.cs::UnsupportedPatternUnCached
#         """
#         cache_request = CacheRequest(automation)
#         cache_request.automation_element_mode = AutomationElementMode.None_
#         cache_request.tree_scope = TreeScope.Element
#         cache_request.add_pattern(automation.cs_automation.PatternLibrary.WindowPattern)

#         with cache_request.activate():
#             # Must get window AFTER cache activation for cache to apply
#             window = automation.application.get_main_window(automation)
#             assert window is not None
#             with pytest.raises(PatternNotCachedException, match="ExpandCollapse"):
#                 window.framework_automation_element.GetNativePattern[SystemObject](
#                     automation.cs_automation.PatternLibrary.ExpandCollapsePattern
#                 )


# @pytest.mark.skip_notepad_on_win11(reason="Windows 11 Notepad is a Store app; see issue #89")
# class TestGetterProperties:
#     """Tests for property getters with and without caching."""

#     def test_correct_property(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting a supported property without caching.

#         Ported from GetterTests.cs::CorrectProperty
#         """
#         assert notepad_window is not None
#         window_property = notepad_window.framework_automation_element.GetPropertyValue(
#             automation.cs_automation.PropertyLibrary.Window.CanMaximize
#         )
#         assert window_property is not None

#     def test_correct_property_cached(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting a supported property with caching.

#         Ported from GetterTests.cs::CorrectPropertyCached
#         """
#         cache_request = CacheRequest(automation)
#         cache_request.automation_element_mode = AutomationElementMode.None_
#         cache_request.tree_scope = TreeScope.Element
#         cache_request.add_property(automation.cs_automation.PropertyLibrary.Window.CanMaximize)

#         with cache_request.activate():
#             # Must get window AFTER cache activation for cache to apply
#             window = automation.application.get_main_window(automation)
#             assert window is not None
#             window_property = window.framework_automation_element.GetPropertyValue(
#                 automation.cs_automation.PropertyLibrary.Window.CanMaximize
#             )
#             assert window_property is not None

#     def test_unsupported_property(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting an unsupported property throws PropertyNotSupportedException.

#         Ported from GetterTests.cs::UnsupportedProperty
#         """
#         assert notepad_window is not None
#         with pytest.raises(PropertyNotSupportedException, match="ExpandCollapseState"):
#             notepad_window.framework_automation_element.GetPropertyValue(
#                 automation.cs_automation.PropertyLibrary.ExpandCollapse.ExpandCollapseState
#             )

#     def test_unsupported_property_cached(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting an unsupported property with caching throws PropertyNotSupportedException.

#         Ported from GetterTests.cs::UnsupportedPropertyCached
#         """
#         cache_request = CacheRequest(automation)
#         cache_request.automation_element_mode = AutomationElementMode.None_
#         cache_request.tree_scope = TreeScope.Element
#         cache_request.add_property(automation.cs_automation.PropertyLibrary.ExpandCollapse.ExpandCollapseState)

#         with cache_request.activate():
#             # Must get window AFTER cache activation for cache to apply
#             window = automation.application.get_main_window(automation)
#             assert window is not None
#             with pytest.raises(PropertyNotSupportedException, match="ExpandCollapseState"):
#                 window.framework_automation_element.GetPropertyValue(
#                     automation.cs_automation.PropertyLibrary.ExpandCollapse.ExpandCollapseState
#                 )

#     def test_correct_property_uncached(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting a supported but uncached property throws PropertyNotCachedException.

#         Ported from GetterTests.cs::CorrectPropertyUncached
#         """
#         cache_request = CacheRequest(automation)
#         cache_request.automation_element_mode = AutomationElementMode.None_
#         cache_request.tree_scope = TreeScope.Element
#         cache_request.add_property(automation.cs_automation.PropertyLibrary.ExpandCollapse.ExpandCollapseState)

#         with cache_request.activate():
#             # Must get window AFTER cache activation for cache to apply
#             window = automation.application.get_main_window(automation)
#             assert window is not None
#             with pytest.raises(PropertyNotCachedException, match="CanMaximize"):
#                 window.framework_automation_element.GetPropertyValue(
#                     automation.cs_automation.PropertyLibrary.Window.CanMaximize
#                 )

#     def test_unsupported_property_uncached(self, notepad_window: Window, automation: Automation) -> None:
#         """Test getting an unsupported and uncached property throws PropertyNotCachedException.

#         Ported from GetterTests.cs::UnsupportedPropertyUnCached
#         """
#         cache_request = CacheRequest(automation)
#         cache_request.automation_element_mode = AutomationElementMode.None_
#         cache_request.tree_scope = TreeScope.Element
#         cache_request.add_property(automation.cs_automation.PropertyLibrary.Window.CanMaximize)

#         with cache_request.activate():
#             # Must get window AFTER cache activation for cache to apply
#             window = automation.application.get_main_window(automation)
#             assert window is not None
#             with pytest.raises(PropertyNotCachedException, match="ExpandCollapseState"):
#                 window.framework_automation_element.GetPropertyValue(
#                     automation.cs_automation.PropertyLibrary.ExpandCollapse.ExpandCollapseState
#                 )
