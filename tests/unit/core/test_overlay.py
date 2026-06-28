"""Unit tests for the overlay manager wrapper (GH-103).

Backed by C# ``NullOverlayManager`` (a no-op), so these run without a display or running app — they
only need the PythonNet bridge (set up by the global conftest).
"""

from FlaUI.Core.Overlay import NullOverlayManager  # type: ignore

from flaui.core.overlay import OverlayManager
from flaui.lib.system.drawing import Color, Rectangle


def _manager() -> OverlayManager:
    """Return an OverlayManager backed by a C# NullOverlayManager."""
    return OverlayManager(raw_overlay_manager=NullOverlayManager())


class TestOverlayManager:
    """Tests for :class:`OverlayManager`."""

    def test_size_round_trips(self) -> None:
        """The ``size`` property reads and writes through to C#."""
        manager = _manager()
        manager.size = 7
        assert manager.size == 7

    def test_margin_round_trips(self) -> None:
        """The ``margin`` property reads and writes through to C# (negatives allowed)."""
        manager = _manager()
        manager.margin = -3
        assert manager.margin == -3

    def test_show_is_noop_on_null_manager(self) -> None:
        """``show`` forwards without error against the no-op manager."""
        manager = _manager()
        manager.show(Rectangle(raw_value=[0, 0, 10, 10]), Color.Red, 1)

    def test_show_blocking_forwards(self) -> None:
        """``show_blocking`` forwards without error (sleeps for the duration)."""
        manager = _manager()
        manager.show_blocking(Rectangle(raw_value=[0, 0, 10, 10]), Color.Blue, 1)

    def test_dispose_is_safe(self) -> None:
        """``dispose`` forwards to the C# manager without error."""
        _manager().dispose()
