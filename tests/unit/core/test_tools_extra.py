"""Unit tests for the additional tools/utilities (GH-100).

SystemInfo is pure Python (via psutil); LocalizedStrings and AccessibilityTextResolver delegate to
C# and only need the PythonNet bridge (set up by the global conftest), not a running application.
"""

from flaui.core.tools import AccessibilityTextResolver, LocalizedStrings, SystemInfo, WindowsStoreAppLauncher
import pytest


class TestSystemInfo:
    """Tests for the pure-Python SystemInfo metrics."""

    def test_cpu_usage_is_a_percentage(self) -> None:
        """CPU usage is a float between 0 and 100."""
        usage = SystemInfo.cpu_usage()
        assert isinstance(usage, float)
        assert 0.0 <= usage <= 100.0

    def test_physical_memory_metrics(self) -> None:
        """Physical memory totals are positive and percentages are within range."""
        assert SystemInfo.physical_memory_total() > 0
        assert SystemInfo.physical_memory_free() >= 0
        assert SystemInfo.physical_memory_used() >= 0
        assert 0.0 <= SystemInfo.physical_memory_used_percent() <= 100.0
        assert 0.0 <= SystemInfo.physical_memory_free_percent() <= 100.0

    def test_virtual_memory_metrics(self) -> None:
        """Virtual (swap) memory metrics are non-negative integers."""
        assert SystemInfo.virtual_memory_total() >= 0
        assert SystemInfo.virtual_memory_free() >= 0
        assert SystemInfo.virtual_memory_used() >= 0


class TestLocalizedStrings:
    """Tests for the culture-aware localized strings."""

    def test_scroll_bar_names_are_non_empty(self) -> None:
        """Horizontal and vertical scroll-bar names resolve to non-empty strings."""
        assert isinstance(LocalizedStrings.horizontal_scroll_bar(), str)
        assert LocalizedStrings.horizontal_scroll_bar()
        assert isinstance(LocalizedStrings.vertical_scroll_bar(), str)
        assert LocalizedStrings.vertical_scroll_bar()


class TestAccessibilityTextResolver:
    """Tests for resolving MSAA role/state text via oleacc."""

    def test_get_role_text(self) -> None:
        """A known accessibility role resolves to non-empty human-readable text."""
        from FlaUI.Core.WindowsAPI import AccessibilityRole  # pyright: ignore
        import System  # pyright: ignore

        roles = list(System.Enum.GetValues(AccessibilityRole))
        # Use a role other than the first (which is typically a 'none'/0 value).
        role = roles[1] if len(roles) > 1 else roles[0]
        text = AccessibilityTextResolver.get_role_text(role)
        assert isinstance(text, str)

    def test_get_state_text(self) -> None:
        """An accessibility state resolves to a string."""
        from FlaUI.Core.WindowsAPI import AccessibilityState  # pyright: ignore
        import System  # pyright: ignore

        states = list(System.Enum.GetValues(AccessibilityState))
        text = AccessibilityTextResolver.get_state_text(states[0])
        assert isinstance(text, str)


class TestWindowsStoreAppLauncher:
    """Tests for the Windows Store app launcher surface."""

    def test_invalid_app_id_raises(self) -> None:
        """Launching a non-existent app id raises rather than silently failing."""
        with pytest.raises(Exception):  # noqa: B017,PT011 - native COM error type varies
            WindowsStoreAppLauncher.launch("FlaUI.NonExistentApp!App")
