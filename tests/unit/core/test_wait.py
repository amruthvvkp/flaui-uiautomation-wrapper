"""Unit tests for Wait helpers that don't need a running application (GH-68)."""

import time

from flaui.core.input import Wait


class TestWhileCursorIsBusy:
    """Tests for :meth:`Wait.while_cursor_is_busy`."""

    def test_returns_true_when_cursor_idle(self) -> None:
        """With no busy cursor showing, it returns True promptly."""
        start = time.monotonic()
        result = Wait.while_cursor_is_busy(timeout_in_secs=2.0)
        elapsed = time.monotonic() - start
        assert result is True
        assert elapsed < 2.0  # returned before the timeout because the cursor is idle

    def test_returns_bool(self) -> None:
        """The helper always returns a boolean."""
        assert isinstance(Wait.while_cursor_is_busy(timeout_in_secs=0.5), bool)
