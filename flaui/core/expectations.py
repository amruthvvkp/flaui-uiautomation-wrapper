"""Playwright-style fluent assertions for FlaUI automation elements.

``expect(element).to_be_visible()`` auto-waits, polling the element until the expectation holds or a
timeout elapses, then raises :class:`AssertionError` with a helpful message if it never does. This
makes UI assertions resilient to the small delays inherent in desktop automation without scattering
manual ``sleep``/retry code through tests.

Polling reuses :class:`flaui.core.tools.Retry`; no new polling loop is introduced here.

Example::

    from flaui.core.expectations import expect

    expect(ok_button).to_be_visible()
    expect(ok_button).to_be_enabled()
    expect(checkbox).to_be_checked()
    expect(label).to_have_text("Done")
    expect(spinner).not_.to_be_visible(timeout=2000)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from flaui.core.tools import Retry

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement

#: Default time to wait for an expectation to hold, in milliseconds.
DEFAULT_TIMEOUT_MS = 5000
#: Default interval between expectation polls, in milliseconds.
DEFAULT_INTERVAL_MS = 100


def _safe_bool(getter: Callable[[], Any]) -> bool:
    """Evaluate ``getter`` and coerce to ``bool``, returning ``False`` on any error.

    :param getter: A zero-argument callable reading an element attribute.
    :return: The truthiness of the value, or ``False`` if reading it raised.
    """
    try:
        return bool(getter())
    except Exception:
        return False


class ElementAssertions:
    """Fluent expectation builder for a single :class:`AutomationElement`.

    Each ``to_*`` matcher polls until the condition holds (or, after :attr:`not_`, until it no longer
    holds) and raises :class:`AssertionError` on timeout. Create instances via :func:`expect`.
    """

    def __init__(
        self,
        element: "AutomationElement",
        timeout: int = DEFAULT_TIMEOUT_MS,
        interval: int = DEFAULT_INTERVAL_MS,
        is_negated: bool = False,
    ) -> None:
        """Initialise the assertion wrapper.

        :param element: The element under assertion.
        :param timeout: Maximum time to wait for the expectation, in milliseconds.
        :param interval: Polling interval, in milliseconds.
        :param is_negated: Whether matchers should assert the negated condition.
        """
        self._element = element
        self._timeout = timeout
        self._interval = interval
        self._is_negated = is_negated

    @property
    def not_(self) -> "ElementAssertions":
        """Return a negated view of these assertions.

        :return: A new :class:`ElementAssertions` whose matchers assert the opposite condition.
        """
        return ElementAssertions(self._element, self._timeout, self._interval, not self._is_negated)

    def _check(self, predicate: Callable[[], bool], description: str, timeout: int | None) -> None:
        """Poll ``predicate`` until it matches the desired polarity, else raise ``AssertionError``.

        :param predicate: A robust, non-raising callable returning the current condition state.
        :param description: Human-readable condition description for the failure message.
        :param timeout: Optional per-call timeout override, in milliseconds.
        :raises AssertionError: If the expectation is not met within the timeout.
        """
        want = not self._is_negated
        effective_timeout = self._timeout if timeout is None else timeout
        matched = Retry.While(
            retry_method=lambda: predicate() == want,
            timeout=effective_timeout,
            interval=self._interval,
            default_on_timeout=False,
        )
        if not matched:
            negate = "not " if self._is_negated else ""
            raise AssertionError(
                f"Expected {self._element!r} {negate}{description} within {effective_timeout}ms."
            )

    def to_be_visible(self, timeout: int | None = None) -> None:
        """Assert the element is available and on-screen.

        :param timeout: Optional per-call timeout override, in milliseconds.
        :raises AssertionError: If the expectation is not met within the timeout.
        """
        self._check(
            lambda: _safe_bool(lambda: self._element.is_available) and not _safe_bool(lambda: self._element.is_offscreen),
            "to be visible",
            timeout,
        )

    def to_be_enabled(self, timeout: int | None = None) -> None:
        """Assert the element is enabled.

        :param timeout: Optional per-call timeout override, in milliseconds.
        :raises AssertionError: If the expectation is not met within the timeout.
        """
        self._check(lambda: _safe_bool(lambda: self._element.is_enabled), "to be enabled", timeout)

    def to_be_offscreen(self, timeout: int | None = None) -> None:
        """Assert the element is off-screen.

        :param timeout: Optional per-call timeout override, in milliseconds.
        :raises AssertionError: If the expectation is not met within the timeout.
        """
        self._check(lambda: _safe_bool(lambda: self._element.is_offscreen), "to be offscreen", timeout)

    def to_be_checked(self, timeout: int | None = None) -> None:
        """Assert the element's ``is_checked`` state is truthy.

        :param timeout: Optional per-call timeout override, in milliseconds.
        :raises AssertionError: If the expectation is not met within the timeout.
        """
        self._check(lambda: _safe_bool(lambda: self._element.is_checked), "to be checked", timeout)

    def to_have_name(self, expected: str, timeout: int | None = None) -> None:
        """Assert the element's ``name`` equals ``expected``.

        :param expected: The expected name value.
        :param timeout: Optional per-call timeout override, in milliseconds.
        :raises AssertionError: If the expectation is not met within the timeout.
        """
        self._check(lambda: _read(self._element, "name") == expected, f"to have name {expected!r}", timeout)

    def to_have_text(self, expected: str, timeout: int | None = None) -> None:
        """Assert the element's ``text`` equals ``expected``.

        :param expected: The expected text value.
        :param timeout: Optional per-call timeout override, in milliseconds.
        :raises AssertionError: If the expectation is not met within the timeout.
        """
        self._check(lambda: _read(self._element, "text") == expected, f"to have text {expected!r}", timeout)

    def to_have_value(self, expected: Any, timeout: int | None = None) -> None:
        """Assert the element's ``value`` equals ``expected``.

        :param expected: The expected value.
        :param timeout: Optional per-call timeout override, in milliseconds.
        :raises AssertionError: If the expectation is not met within the timeout.
        """
        self._check(lambda: _read(self._element, "value") == expected, f"to have value {expected!r}", timeout)


def _read(element: "AutomationElement", attr: str) -> Any:
    """Read ``element.attr`` without raising, returning a sentinel object on failure.

    A unique sentinel is returned on error so that equality comparisons against any expected value
    are ``False`` (rather than accidentally matching ``None``).

    :param element: The element to read from.
    :param attr: The attribute name.
    :return: The attribute value, or a unique sentinel if reading raised.
    """
    try:
        return getattr(element, attr)
    except Exception:
        return object()


def expect(
    element: "AutomationElement",
    timeout: int = DEFAULT_TIMEOUT_MS,
    interval: int = DEFAULT_INTERVAL_MS,
) -> ElementAssertions:
    """Create a fluent, auto-waiting assertion for ``element``.

    :param element: The element to assert on.
    :param timeout: Default time to wait for each expectation, in milliseconds.
    :param interval: Polling interval, in milliseconds.
    :return: An :class:`ElementAssertions` builder (use ``.not_`` for negation).
    """
    return ElementAssertions(element, timeout=timeout, interval=interval)
