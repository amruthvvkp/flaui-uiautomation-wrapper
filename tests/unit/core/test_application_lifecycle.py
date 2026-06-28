"""Unit tests for the Application context-manager lifecycle."""

from unittest.mock import MagicMock

from flaui.core.application import Application


def test_enter_returns_self() -> None:
    """__enter__ returns the application instance for use in a with-block."""
    app = Application()
    with app as entered:
        assert entered is app


def test_exit_is_a_noop_when_nothing_launched() -> None:
    """__exit__ does nothing (and does not raise) when no process was launched."""
    app = Application()
    assert app.__exit__(None, None, None) is None


def test_exit_closes_a_launched_application() -> None:
    """__exit__ gracefully closes the underlying application when one is bound."""
    app = Application()
    fake = MagicMock()
    app._application = fake
    app.__exit__(None, None, None)
    fake.Close.assert_called_once()


def test_exit_disposes_when_close_fails() -> None:
    """__exit__ falls back to dispose when graceful close raises."""
    app = Application()
    fake = MagicMock()
    fake.Close.side_effect = RuntimeError("close failed")
    app._application = fake
    app.__exit__(None, None, None)
    fake.Dispose.assert_called_once()


def test_exit_swallows_dispose_failure() -> None:
    """__exit__ never propagates cleanup errors, even if dispose also fails."""
    app = Application()
    fake = MagicMock()
    fake.Close.side_effect = RuntimeError("close failed")
    fake.Dispose.side_effect = RuntimeError("dispose failed")
    app._application = fake
    # Should not raise.
    assert app.__exit__(None, None, None) is None
