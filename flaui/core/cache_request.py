"""
Python wrapper for the C# FlaUI.Core.CacheRequest class.
Mirrors the C# API and exposes a high-level interface for cache requests.
"""

# Untested code may not work as expected.
# This code is a direct translation of the C# API and may require adjustments.

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Optional

# Import the C# CacheRequest class via PythonNet
from FlaUI.Core import CacheRequest as CSCacheRequest  # pyright: ignore

from flaui.core.definitions import TreeScope
from flaui.modules.automation import Automation


class CacheRequest:
    """
    Python wrapper for FlaUI.Core.CacheRequest.
    """

    def __init__(self, _cs_instance: Optional[Any] = None) -> None:
        """Initialize CacheRequest.

        Accepts either:
        - None: constructs a new C# CacheRequest()
        - A C# CacheRequest instance
        - An Automation wrapper: constructs C# CacheRequest(automation.cs_automation)
        """
        if _cs_instance is None:
            self._cs_instance = CSCacheRequest()
        elif isinstance(_cs_instance, Automation):
            # Some FlaUI versions expose only the parameterless constructor.
            # When an Automation wrapper is provided, fall back to a default CacheRequest.
            self._cs_instance = CSCacheRequest()
        else:
            # Assume it's already a C# CacheRequest instance
            self._cs_instance = _cs_instance

    @property
    def automation_element_mode(self) -> Any:
        """Get or set the automation element mode."""
        return self._cs_instance.AutomationElementMode

    @automation_element_mode.setter
    def automation_element_mode(self, value: Any) -> None:
        """Get or set the automation element mode."""
        self._cs_instance.AutomationElementMode = value

    @property
    def tree_filter(self) -> Any:
        """Get or set the tree filter."""
        return self._cs_instance.TreeFilter

    @tree_filter.setter
    def tree_filter(self, value: Any) -> None:
        """Get or set the tree filter."""
        self._cs_instance.TreeFilter = value

    @property
    def tree_scope(self) -> TreeScope:
        """Get or set the tree scope."""
        return self._cs_instance.TreeScope

    @tree_scope.setter
    def tree_scope(self, value: TreeScope) -> None:
        """Get or set the tree scope."""
        self._cs_instance.TreeScope = value.value

    @property
    def patterns(self) -> Any:
        """Get or set the patterns."""
        return self._cs_instance.Patterns

    @property
    def properties(self) -> Any:
        """Get or set the properties."""
        return self._cs_instance.Properties

    def add_pattern(self, pattern: Any) -> None:
        """Add a pattern to the cache request."""
        self._cs_instance.Add(pattern)

    def add_property(self, property_: Any) -> None:
        """Add a property to the cache request."""
        self._cs_instance.Add(property_)

    @contextmanager
    def activate(self) -> Any:
        """Activate the cache request. Returns a context manager/disposable."""
        disposable = self._cs_instance.Activate()
        try:
            yield
        finally:
            # C# IDisposable typically exposes Dispose()
            try:
                disposable.Dispose()
            except Exception:
                # Fallback if pythonnet provides lowercase method
                try:
                    disposable.dispose()
                except Exception:
                    pass

    @classmethod
    def is_caching_active(cls) -> bool:
        """Check if caching is currently active."""
        return CSCacheRequest.IsCachingActive

    @classmethod
    def current(cls) -> Optional[CacheRequest]:
        """Get the current active CacheRequest, if any."""
        cs_current = CSCacheRequest.Current
        if cs_current is not None:
            return CacheRequest(_cs_instance=cs_current)
        return None

    @classmethod
    def push(cls, cache_request: "CacheRequest") -> None:
        """Push a CacheRequest onto the stack."""
        CSCacheRequest.Push(cache_request._cs_instance)

    @classmethod
    def pop(cls) -> None:
        """Pop the top CacheRequest from the stack."""
        CSCacheRequest.Pop()

    @classmethod
    def force_no_cache(cls) -> Any:
        """Force no cache."""
        return CSCacheRequest.ForceNoCache()
