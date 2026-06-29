"""Hermetic unit tests for the pure-Python :class:`flaui.core.tools.Retry` helpers (GH-88).

These exercise every retry variant and its timeout branches (``throw_on_timeout``,
``last_value_on_timeout``, ``default_on_timeout``, ``ignore_exception``) without touching C# or a
live UIA tree. Timeouts are kept tiny (0 ms) so failing paths resolve instantly, and ``_sleep_ms``
is patched out where a loop would otherwise iterate, so the suite stays fast and deterministic.

``ItemRealizer.realize_items`` and the ``AccessibilityTextResolver`` state-bit delegation are also
covered here by mocking their late-imported C# classes.
"""

from unittest.mock import MagicMock, patch

import pytest

from flaui.core.tools import AccessibilityTextResolver, ItemRealizer, Retry


class _Counter:
    """Callable returning a queued sequence of values/exceptions across successive calls."""

    def __init__(self, values: list) -> None:
        """Store the sequence to replay.

        :param values: Values to return in order; an ``Exception`` instance is raised instead.
        """
        self._values = list(values)
        self.calls = 0

    def __call__(self):  # type: ignore[no-untyped-def]
        """Return (or raise) the next queued item, repeating the last item once exhausted."""
        self.calls += 1
        item = self._values[min(self.calls - 1, len(self._values) - 1)]
        if isinstance(item, Exception):
            raise item
        return item


class TestRetryWhile:
    """Tests for :meth:`Retry.While` (retry until the value is truthy)."""

    def test_returns_first_truthy_value(self) -> None:
        """A truthy value is returned immediately."""
        assert Retry.While(retry_method=lambda: "ready", timeout=0) == "ready"

    def test_returns_truthy_after_falsey(self) -> None:
        """The loop keeps polling until a truthy value appears."""
        counter = _Counter([0, 0, 5])
        with patch.object(Retry, "_sleep_ms"):
            assert Retry.While(retry_method=counter, timeout=1000, interval=0) == 5

    def test_throw_on_timeout_raises_timeout_error(self) -> None:
        """``throw_on_timeout`` raises a :class:`TimeoutError` with the custom message."""
        with pytest.raises(TimeoutError, match="nope"):
            Retry.While(retry_method=lambda: False, timeout=0, throw_on_timeout=True, timeout_message="nope")

    def test_default_timeout_raises_timeout_error(self) -> None:
        """With no timeout flags set, a timeout raises :class:`TimeoutError`."""
        with pytest.raises(TimeoutError):
            Retry.While(retry_method=lambda: None, timeout=0)

    def test_last_value_on_timeout_returns_last_value(self) -> None:
        """``last_value_on_timeout`` returns the most recent (falsey) value on timeout."""
        assert Retry.While(retry_method=lambda: 0, timeout=0, last_value_on_timeout=True) == 0

    def test_default_on_timeout_returns_default(self) -> None:
        """``default_on_timeout`` returns the configured default on timeout."""
        assert Retry.While(retry_method=lambda: None, timeout=0, default_on_timeout="fallback") == "fallback"

    def test_ignore_exception_keeps_retrying(self) -> None:
        """When ``ignore_exception`` is set, a raised error becomes the last value and polling continues."""
        with pytest.raises(TimeoutError):
            Retry.While(retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0, ignore_exception=True)

    def test_exception_propagates_when_not_ignored(self) -> None:
        """A raised error propagates unchanged when ``ignore_exception`` is False."""
        with pytest.raises(AssertionError):
            Retry.While(retry_method=lambda: (_ for _ in ()).throw(AssertionError("x")), timeout=0)


class TestRetryWhileNot:
    """Tests for :meth:`Retry.WhileNot` (retry until the value is falsey)."""

    def test_returns_first_falsey_value(self) -> None:
        """A falsey value is returned immediately."""
        assert Retry.WhileNot(retry_method=lambda: 0, timeout=0) == 0

    def test_returns_falsey_after_truthy(self) -> None:
        """The loop keeps polling until a falsey value appears."""
        counter = _Counter([1, 1, 0])
        with patch.object(Retry, "_sleep_ms"):
            assert Retry.WhileNot(retry_method=counter, timeout=1000, interval=0) == 0

    def test_throw_on_timeout_raises(self) -> None:
        """``throw_on_timeout`` raises a :class:`TimeoutError`."""
        with pytest.raises(TimeoutError):
            Retry.WhileNot(retry_method=lambda: True, timeout=0, throw_on_timeout=True)

    def test_last_value_on_timeout(self) -> None:
        """``last_value_on_timeout`` returns the most recent truthy value on timeout."""
        assert Retry.WhileNot(retry_method=lambda: 7, timeout=0, last_value_on_timeout=True) == 7

    def test_default_on_timeout(self) -> None:
        """``default_on_timeout`` returns the configured default on timeout."""
        assert Retry.WhileNot(retry_method=lambda: True, timeout=0, default_on_timeout="d") == "d"

    def test_default_timeout_raises(self) -> None:
        """With no timeout flags, timing out raises :class:`TimeoutError`."""
        with pytest.raises(TimeoutError):
            Retry.WhileNot(retry_method=lambda: True, timeout=0)

    def test_ignore_exception_records_and_times_out(self) -> None:
        """An ignored exception lets the loop continue to its timeout."""
        with pytest.raises(TimeoutError):
            Retry.WhileNot(
                retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0, ignore_exception=True
            )

    def test_exception_propagates_when_not_ignored(self) -> None:
        """A raised error propagates when not ignored."""
        with pytest.raises(ValueError):
            Retry.WhileNot(retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0)


class TestRetryWhileTrue:
    """Tests for :meth:`Retry.WhileTrue` (succeeds when predicate becomes False)."""

    def test_returns_true_when_predicate_false(self) -> None:
        """Returns True as soon as the predicate is falsey."""
        assert Retry.WhileTrue(retry_method=lambda: False, timeout=0) is True

    def test_returns_false_on_timeout(self) -> None:
        """Returns False when the predicate stays truthy past the timeout."""
        assert Retry.WhileTrue(retry_method=lambda: True, timeout=0) is False

    def test_throw_on_timeout_raises(self) -> None:
        """``throw_on_timeout`` raises instead of returning False."""
        with pytest.raises(TimeoutError):
            Retry.WhileTrue(retry_method=lambda: True, timeout=0, throw_on_timeout=True)

    def test_ignore_exception_returns_false(self) -> None:
        """An ignored exception lets the loop run out and return False."""
        assert (
            Retry.WhileTrue(
                retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0, ignore_exception=True
            )
            is False
        )

    def test_exception_propagates_when_not_ignored(self) -> None:
        """A raised error propagates when not ignored."""
        with pytest.raises(ValueError):
            Retry.WhileTrue(retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0)


class TestRetryWhileFalse:
    """Tests for :meth:`Retry.WhileFalse` (succeeds when predicate becomes True)."""

    def test_returns_true_when_predicate_true(self) -> None:
        """Returns True as soon as the predicate is truthy."""
        assert Retry.WhileFalse(retry_method=lambda: True, timeout=0) is True

    def test_returns_false_on_timeout(self) -> None:
        """Returns False when the predicate stays falsey past the timeout."""
        assert Retry.WhileFalse(retry_method=lambda: False, timeout=0) is False

    def test_throw_on_timeout_raises(self) -> None:
        """``throw_on_timeout`` raises instead of returning False."""
        with pytest.raises(TimeoutError):
            Retry.WhileFalse(retry_method=lambda: False, timeout=0, throw_on_timeout=True)

    def test_ignore_exception_returns_false(self) -> None:
        """An ignored exception lets the loop run out and return False."""
        assert (
            Retry.WhileFalse(
                retry_method=lambda: (_ for _ in ()).throw(AssertionError("x")), timeout=0, ignore_exception=True
            )
            is False
        )

    def test_exception_propagates_when_not_ignored(self) -> None:
        """A raised error propagates when not ignored."""
        with pytest.raises(AssertionError):
            Retry.WhileFalse(retry_method=lambda: (_ for _ in ()).throw(AssertionError("x")), timeout=0)


class TestRetryWhileNull:
    """Tests for :meth:`Retry.WhileNull` (returns first non-None value)."""

    def test_returns_first_non_none(self) -> None:
        """A non-None value is returned immediately."""
        assert Retry.WhileNull(retry_method=lambda: 42, timeout=0) == 42

    def test_returns_none_on_timeout(self) -> None:
        """Returns None when the value stays None past the timeout."""
        assert Retry.WhileNull(retry_method=lambda: None, timeout=0) is None

    def test_throw_on_timeout_raises(self) -> None:
        """``throw_on_timeout`` raises instead of returning None."""
        with pytest.raises(TimeoutError):
            Retry.WhileNull(retry_method=lambda: None, timeout=0, throw_on_timeout=True)

    def test_ignore_exception_returns_none(self) -> None:
        """An ignored exception lets the loop run out and return None."""
        assert (
            Retry.WhileNull(
                retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0, ignore_exception=True
            )
            is None
        )

    def test_exception_propagates_when_not_ignored(self) -> None:
        """A raised error propagates when not ignored."""
        with pytest.raises(ValueError):
            Retry.WhileNull(retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0)


class TestRetryWhileNotNull:
    """Tests for :meth:`Retry.WhileNotNull` (returns once value becomes None)."""

    def test_returns_none_when_value_none(self) -> None:
        """Returns None as soon as the value is None."""
        assert Retry.WhileNotNull(retry_method=lambda: None, timeout=0) is None

    def test_returns_last_value_on_timeout(self) -> None:
        """Returns the last non-None value when it never becomes None."""
        assert Retry.WhileNotNull(retry_method=lambda: "stays", timeout=0) == "stays"

    def test_throw_on_timeout_raises(self) -> None:
        """``throw_on_timeout`` raises a :class:`TimeoutError`."""
        with pytest.raises(TimeoutError):
            Retry.WhileNotNull(retry_method=lambda: "stays", timeout=0, throw_on_timeout=True)

    def test_ignore_exception_records_and_returns_last(self) -> None:
        """An ignored exception is stored as the last value and returned on timeout."""
        result = Retry.WhileNotNull(
            retry_method=lambda: (_ for _ in ()).throw(ValueError("boom")), timeout=0, ignore_exception=True
        )
        assert isinstance(result, ValueError)

    def test_exception_propagates_when_not_ignored(self) -> None:
        """A raised error propagates when not ignored."""
        with pytest.raises(ValueError):
            Retry.WhileNotNull(retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0)


class TestRetryWhileEmpty:
    """Tests for :meth:`Retry.WhileEmpty` (retries while result is an empty iterable)."""

    def test_returns_non_empty_iterable(self) -> None:
        """A non-empty iterable is returned immediately."""
        assert Retry.WhileEmpty(retry_method=lambda: [1, 2], timeout=0) == [1, 2]

    def test_returns_non_iterable_value(self) -> None:
        """A non-iterable value is treated as 'not empty' and returned."""
        assert Retry.WhileEmpty(retry_method=lambda: 5, timeout=0) == 5

    def test_returns_non_empty_after_empty(self) -> None:
        """The loop sleeps and retries while the result stays empty, then returns the filled value."""
        counter = _Counter([[], [], [1]])
        with patch.object(Retry, "_sleep_ms") as sleep:
            assert Retry.WhileEmpty(retry_method=counter, timeout=1000, interval=0) == [1]
        assert sleep.called

    def test_throw_on_timeout_raises(self) -> None:
        """An always-empty result times out and raises with ``throw_on_timeout``."""
        with pytest.raises(TimeoutError):
            Retry.WhileEmpty(retry_method=lambda: [], timeout=0, throw_on_timeout=True)

    def test_last_value_on_timeout(self) -> None:
        """``last_value_on_timeout`` returns the last empty value on timeout."""
        assert Retry.WhileEmpty(retry_method=lambda: [], timeout=0, last_value_on_timeout=True) == []

    def test_default_on_timeout(self) -> None:
        """``default_on_timeout`` returns the configured default on timeout."""
        assert Retry.WhileEmpty(retry_method=lambda: [], timeout=0, default_on_timeout=["d"]) == ["d"]

    def test_default_timeout_raises(self) -> None:
        """With no timeout flags, an always-empty result raises :class:`TimeoutError`."""
        with pytest.raises(TimeoutError):
            Retry.WhileEmpty(retry_method=lambda: [], timeout=0)

    def test_ignore_exception_records_and_times_out(self) -> None:
        """An ignored exception lets the loop continue to its timeout."""
        with pytest.raises(TimeoutError):
            Retry.WhileEmpty(
                retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0, ignore_exception=True
            )

    def test_exception_propagates_when_not_ignored(self) -> None:
        """A raised error propagates when not ignored."""
        with pytest.raises(ValueError):
            Retry.WhileEmpty(retry_method=lambda: (_ for _ in ()).throw(ValueError("x")), timeout=0)


class TestRetryWhileException:
    """Tests for :meth:`Retry.WhileException` (returns first successful result)."""

    def test_returns_first_success(self) -> None:
        """A successful call returns its result immediately."""
        assert Retry.WhileException(retry_method=lambda: "ok", timeout=0) == "ok"

    def test_succeeds_after_failures(self) -> None:
        """The loop retries through failures until a call succeeds."""
        counter = _Counter([RuntimeError("a"), RuntimeError("b"), "done"])
        with patch.object(Retry, "_sleep_ms"):
            assert Retry.WhileException(retry_method=counter, timeout=1000, interval=0) == "done"

    def test_propagates_last_exception_on_timeout(self) -> None:
        """On timeout the last exception is re-raised when not configured to ignore."""
        with pytest.raises(RuntimeError, match="boom"):
            Retry.WhileException(retry_method=lambda: (_ for _ in ()).throw(RuntimeError("boom")), timeout=0)

    def test_throw_on_timeout_raises_timeout_error(self) -> None:
        """``throw_on_timeout`` raises a :class:`TimeoutError` instead of the last exception."""
        with pytest.raises(TimeoutError):
            Retry.WhileException(
                retry_method=lambda: (_ for _ in ()).throw(RuntimeError("boom")), timeout=0, throw_on_timeout=True
            )

    def test_ignore_exception_raises_timeout_error(self) -> None:
        """With ``ignore_exception`` the timeout path raises :class:`TimeoutError`, not the cause."""
        with pytest.raises(TimeoutError):
            Retry.WhileException(
                retry_method=lambda: (_ for _ in ()).throw(RuntimeError("boom")), timeout=0, ignore_exception=True
            )


class TestRetryHelpers:
    """Tests for the small private/static helpers on :class:`Retry`."""

    def test_now_ms_is_float(self) -> None:
        """``_now_ms`` returns a float millisecond clock reading."""
        assert isinstance(Retry._now_ms(), float)

    def test_sleep_ms_invokes_time_sleep(self) -> None:
        """``_sleep_ms`` converts milliseconds to seconds for ``time.sleep``."""
        with patch("flaui.core.tools.time.sleep") as sleep:
            Retry._sleep_ms(250)
        sleep.assert_called_once_with(0.25)

    def test_is_timeout_reached(self) -> None:
        """``IsTimeOutReached`` compares elapsed time against the timeout in milliseconds."""
        with patch("flaui.core.tools.time.monotonic", return_value=10.0):
            assert Retry.IsTimeOutReached(start_time=0.0, timeout=1000) is True
            assert Retry.IsTimeOutReached(start_time=9.999, timeout=1000) is False


class TestItemRealizer:
    """Tests for :class:`ItemRealizer`, mocking the late-imported C# class."""

    def test_realize_items_delegates_to_cs(self) -> None:
        """``realize_items`` forwards the element's ``raw_element`` to the C# realizer."""
        element = MagicMock()
        cs_module = MagicMock()
        with patch.dict(
            "sys.modules", {"FlaUI.Core.Tools": MagicMock(ItemRealizer=cs_module.ItemRealizer)}
        ):
            ItemRealizer.realize_items(element)
        cs_module.ItemRealizer.RealizeItems.assert_called_once_with(element.raw_element)


class TestAccessibilityStateBitText:
    """Cover the ``get_state_bit_text`` delegation, mocking the C# resolver."""

    def test_get_state_bit_text_delegates_to_cs(self) -> None:
        """``get_state_bit_text`` forwards the state to the C# resolver and returns its text."""
        resolver = MagicMock()
        resolver.GetStateBitText.return_value = "focused"
        with patch.dict("sys.modules", {"FlaUI.Core.Tools": MagicMock(AccessibilityTextResolver=resolver)}):
            assert AccessibilityTextResolver.get_state_bit_text("state") == "focused"
        resolver.GetStateBitText.assert_called_once_with("state")
