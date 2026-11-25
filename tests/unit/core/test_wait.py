"""Unit tests for Wait helpers that don't need a running application (GH-68)."""

import ctypes
import time

import pytest

from flaui.core.input import Wait


class TestWhileCursorIsBusy:
    """Tests for :meth:`Wait.while_cursor_is_busy`."""

    def test_returns_true_when_cursor_idle(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """With no busy cursor showing, it returns True promptly.

        The real desktop cursor is shared with other tests and the CI host (an app launched just
        before may still show the app-starting cursor), so stub ``GetCursorInfo`` to report a
        cursor that cannot be read, which the helper treats as idle.
        """
        monkeypatch.setattr(ctypes.windll.user32, "GetCursorInfo", lambda _info: 0)
        start = time.monotonic()
        result = Wait.while_cursor_is_busy(timeout_in_secs=2.0)
        elapsed = time.monotonic() - start
        assert result is True
        assert elapsed < 2.0  # returned before the timeout because the cursor is idle

    def test_returns_bool(self) -> None:
        """The helper always returns a boolean."""
        assert isinstance(Wait.while_cursor_is_busy(timeout_in_secs=0.5), bool)
