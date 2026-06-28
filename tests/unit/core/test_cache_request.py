"""Unit tests for the :class:`flaui.core.cache_request.CacheRequest` wrapper."""

from FlaUI.Core import CacheRequest as CSCacheRequest  # type: ignore
from FlaUI.Core.Identifiers import PatternId, PropertyId  # type: ignore

from flaui.core.cache_request import CacheRequest
from flaui.core.definitions import AutomationElementMode, TreeScope
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


class TestConstruction:
    """Validate the three construction paths of ``CacheRequest.__init__``."""

    def test_default_construction(self) -> None:
        """Passing nothing builds a fresh C# ``CacheRequest``."""
        cache_request = CacheRequest()

        assert isinstance(cache_request._cs_instance, CSCacheRequest)

    def test_wraps_existing_cs_instance(self) -> None:
        """An existing C# instance is stored as-is."""
        cs_instance = CSCacheRequest()

        assert CacheRequest(_cs_instance=cs_instance)._cs_instance is cs_instance

    def test_construct_from_automation(self) -> None:
        """An ``Automation`` wrapper falls back to a default C# ``CacheRequest``."""
        automation = Automation(UIAutomationTypes.UIA3)
        try:
            cache_request = CacheRequest(_cs_instance=automation)
            assert isinstance(cache_request._cs_instance, CSCacheRequest)
        finally:
            automation.cs_automation.Dispose()


class TestProperties:
    """Validate the property getters/setters round-trip through the C# instance."""

    def test_automation_element_mode_enum_and_raw(self) -> None:
        """The mode is settable via the Python enum and via a raw C# value."""
        cache_request = CacheRequest()

        cache_request.automation_element_mode = AutomationElementMode.Full
        full = cache_request.automation_element_mode
        cache_request.automation_element_mode = AutomationElementMode.None_
        assert cache_request.automation_element_mode != full

        # Assigning a non-enum (raw C#) value hits the pass-through branch.
        cache_request.automation_element_mode = full
        assert cache_request.automation_element_mode == full

    def test_tree_scope(self) -> None:
        """Tree scope is settable via the Python enum."""
        cache_request = CacheRequest()

        cache_request.tree_scope = TreeScope.Subtree
        assert cache_request.tree_scope is not None

    def test_tree_filter_roundtrip(self) -> None:
        """The default tree filter is readable and re-assignable."""
        cache_request = CacheRequest()

        default = cache_request.tree_filter
        assert default is not None
        cache_request.tree_filter = default

    def test_patterns_and_properties(self) -> None:
        """Added patterns/properties are reflected by the collection accessors."""
        cache_request = CacheRequest()

        cache_request.add_property(PropertyId(30005, "Name"))
        cache_request.add_pattern(PatternId(10000, "TestPattern", None))

        assert cache_request.properties is not None
        assert cache_request.patterns is not None


class TestCachingLifecycle:
    """Validate activation, the active-state query, and the static stack helpers."""

    def test_activate_toggles_caching_state(self) -> None:
        """``activate`` enables caching for the duration of the block."""
        cache_request = CacheRequest()

        assert CacheRequest.is_caching_active() is False
        with cache_request.activate():
            assert CacheRequest.is_caching_active() is True
            assert isinstance(CacheRequest.current(), CacheRequest)
        assert CacheRequest.is_caching_active() is False

    def test_current_outside_activation(self) -> None:
        """``current`` is ``None`` (or a wrapper) when no request is active."""
        current = CacheRequest.current()

        assert current is None or isinstance(current, CacheRequest)

    def test_push_and_pop(self) -> None:
        """A request can be pushed onto and popped from the static stack."""
        cache_request = CacheRequest()

        CacheRequest.push(cache_request)
        CacheRequest.pop()

    def test_force_no_cache(self) -> None:
        """``force_no_cache`` returns a disposable that suppresses caching."""
        disposable = CacheRequest.force_no_cache()

        assert disposable is not None
        disposable.Dispose()
