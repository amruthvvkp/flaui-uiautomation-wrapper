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


class CacheRequest:
    """
    Python wrapper for FlaUI.Core.CacheRequest.
    """

    def __init__(self, _cs_instance: Optional[Any] = None) -> None:
        if _cs_instance is not None:
            self._cs_instance = _cs_instance
        else:
            self._cs_instance = CSCacheRequest()

    @property
    def automation_element_mode(self) -> Any:
        return self._cs_instance.AutomationElementMode

    @automation_element_mode.setter
    def automation_element_mode(self, value: Any) -> None:
        self._cs_instance.AutomationElementMode = value

    @property
    def tree_filter(self) -> Any:
        return self._cs_instance.TreeFilter

    @tree_filter.setter
    def tree_filter(self, value: Any) -> None:
        self._cs_instance.TreeFilter = value

    @property
    def tree_scope(self) -> TreeScope:
        return self._cs_instance.TreeScope

    @tree_scope.setter
    def tree_scope(self, value: TreeScope) -> None:
        self._cs_instance.TreeScope = value.value

    @property
    def patterns(self) -> Any:
        return self._cs_instance.Patterns

    @property
    def properties(self) -> Any:
        return self._cs_instance.Properties

    def add_pattern(self, pattern: Any) -> None:
        self._cs_instance.Add(pattern)

    def add_property(self, property_: Any) -> None:
        self._cs_instance.Add(property_)

    @contextmanager
    def activate(self) -> Any:
        """Activate the cache request. Returns a context manager/disposable."""
        disposable = self._cs_instance.Activate()
        try:
            yield
        finally:
            disposable.dispose()

    @classmethod
    def is_caching_active(cls) -> bool:
        return CSCacheRequest.IsCachingActive

    @classmethod
    def current(cls) -> Optional[CacheRequest]:
        cs_current = CSCacheRequest.Current
        if cs_current is not None:
            return CacheRequest(_cs_instance=cs_current)
        return None

    @classmethod
    def push(cls, cache_request: "CacheRequest") -> None:
        CSCacheRequest.Push(cache_request._cs_instance)

    @classmethod
    def pop(cls) -> None:
        CSCacheRequest.Pop()

    @classmethod
    def force_no_cache(cls) -> Any:
        return CSCacheRequest.ForceNoCache()
