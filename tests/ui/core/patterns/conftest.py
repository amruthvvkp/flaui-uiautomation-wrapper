"""Shared fixtures for pattern UI integration tests."""

from typing import Any, Callable

import pytest


@pytest.fixture
def is_pattern_supported() -> Callable[[Any, str], bool]:
    """Return a helper that reports whether ``patterns.<name>`` is supported.

    Some patterns are absent from a UIA framework entirely (notably several patterns under UIA2).
    FlaUI surfaces that by raising ``NotSupportedByFrameworkException`` when the accessor is first
    materialised, rather than reporting ``is_supported == False``. The returned helper treats that
    case as "not supported" so tests can guard uniformly across the UIA2/UIA3 matrix.

    :return: A callable ``(patterns, name) -> bool``.
    """

    def _is_supported(patterns: Any, name: str) -> bool:
        """Check pattern support, treating framework-unsupported patterns as unsupported.

        :param patterns: The element's ``patterns`` facade.
        :param name: The snake_case pattern accessor name (e.g. ``"styles"``).
        :return: ``True`` if the pattern is supported, else ``False``.
        """
        from FlaUI.Core.Exceptions import NotSupportedByFrameworkException

        try:
            return bool(getattr(patterns, name).is_supported)
        except NotSupportedByFrameworkException:
            return False

    return _is_supported
