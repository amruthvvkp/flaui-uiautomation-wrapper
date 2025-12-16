"""Tests for Retry utility functionality, ported from C# RetryTests.cs."""

import time

from flaui.core.tools import Retry
import pytest


class TestRetry:
    """Tests for Retry utility methods."""

    def test_retry_while_true_succeeds(self) -> None:
        """Test Retry.while_true succeeds when condition becomes false.

        Ported from RetryTests.cs::RetryWhileTrue
        """
        start_time = time.time()

        # Condition is true for 1 second, then becomes false
        result = Retry.WhileTrue(
            lambda: time.time() - start_time < 1.0,
            timeout=2000,  # 2 seconds timeout
            throw_on_timeout=False,
        )

        elapsed = time.time() - start_time
        assert elapsed >= 1.0, "Should have waited at least 1 second"
        assert result is True, "Retry should succeed"

    def test_retry_while_true_timeout(self) -> None:
        """Test Retry.while_true times out when condition stays true.

        Ported from RetryTests.cs::RetryWhileTrueFails
        """
        start_time = time.time()

        # Condition is true for 4 seconds, but timeout is 1 second
        result = Retry.WhileTrue(
            lambda: time.time() - start_time < 4.0,
            timeout=1000,  # 1 second timeout
            throw_on_timeout=False,
        )

        elapsed = time.time() - start_time
        assert elapsed >= 1.0, "Should have waited at least 1 second"
        assert result is False, "Retry should timeout and return False"

    def test_retry_while_true_throws_on_timeout(self) -> None:
        """Test Retry.while_true throws exception on timeout.

        Ported from RetryTests.cs::RetryWhileTrueTimeouts
        """
        start_time = time.time()

        with pytest.raises(TimeoutError):
            Retry.WhileTrue(lambda: time.time() - start_time < 4.0, timeout=1000, throw_on_timeout=True)

    def test_retry_while_true_throws_on_exception(self) -> None:
        """Test Retry.while_true throws exceptions when not ignored.

        Ported from RetryTests.cs::RetryWhileTrueThrowsOnException
        """
        with pytest.raises(ValueError):
            Retry.WhileTrue(
                lambda: (_ for _ in ()).throw(ValueError("Test error")),
                timeout=1000,
                throw_on_timeout=True,
                ignore_exception=False,
            )

    def test_retry_while_true_ignores_exception(self) -> None:
        """Test Retry.while_true ignores exceptions and continues.

        Ported from RetryTests.cs::RetryWhileTrueIgnoresException
        """
        start_time = time.time()
        exception_count = [0]  # Use list for closure mutability

        def condition_with_exception():
            """Condition that raises exception for first second."""
            runtime = time.time() - start_time
            if runtime < 1.0:
                exception_count[0] += 1
                raise ValueError("Test exception")
            return False

        result = Retry.WhileTrue(condition_with_exception, timeout=2000, throw_on_timeout=True, ignore_exception=True)

        assert exception_count[0] > 0, "Should have encountered exceptions"
        elapsed = time.time() - start_time
        assert elapsed >= 1.0, "Should have waited at least 1 second"
        assert result is True, "Retry should eventually succeed"

    def test_retry_while_false_succeeds(self) -> None:
        """Test Retry.while_false succeeds when condition becomes true.

        Ported from RetryTests.cs::RetryWhileFalse
        """
        start_time = time.time()

        # Condition is false for 1 second, then becomes true
        result = Retry.WhileFalse(lambda: time.time() - start_time > 1.0, timeout=2000, throw_on_timeout=False)

        elapsed = time.time() - start_time
        assert elapsed >= 1.0, "Should have waited at least 1 second"
        assert result is True, "Retry should succeed"

    def test_retry_while_false_timeout(self) -> None:
        """Test Retry.while_false times out when condition stays false.

        Ported from RetryTests.cs::RetryWhileFalseFails
        """
        start_time = time.time()

        # Condition is false for 4 seconds, but timeout is 1 second
        result = Retry.WhileFalse(lambda: time.time() - start_time > 4.0, timeout=1000, throw_on_timeout=False)

        elapsed = time.time() - start_time
        assert elapsed >= 1.0, "Should have waited at least 1 second"
        assert result is False, "Retry should timeout"

    def test_retry_while_exception_succeeds(self) -> None:
        """Test Retry.while_exception succeeds when no exception thrown.

        Ported from RetryTests.cs::RetryWhileException (partial)
        """
        start_time = time.time()
        exception_count = [0]

        def func_with_temporary_exception():
            """Function that raises exception for first second."""
            runtime = time.time() - start_time
            if runtime < 1.0:
                exception_count[0] += 1
                raise ValueError("Temporary error")
            return "Success"

        result = Retry.WhileException(func_with_temporary_exception, timeout=2000)

        assert exception_count[0] > 0, "Should have encountered exceptions"
        elapsed = time.time() - start_time
        assert elapsed >= 1.0, "Should have waited at least 1 second"
        assert result == "Success", "Should return the function result"

    def test_retry_find_succeeds(self) -> None:
        """Test Retry.find succeeds when element is found.

        Simplified test - full test requires actual UI elements
        """
        start_time = time.time()
        counter = [0]

        def find_element():
            """Function that returns None for first second, then a mock element."""
            counter[0] += 1
            runtime = time.time() - start_time
            # Return None for first second, then return a mock element
            if runtime < 1.0:
                return None
            return "FoundElement"

        # Retry.find does not exist; emulate with WhileNotNull pattern
        result = Retry.WhileNull(find_element, timeout=2000, interval=100)

        assert result == "FoundElement"
        assert counter[0] > 5, "Should have retried multiple times"

    def test_retry_find_timeout(self) -> None:
        """Test Retry.find returns None on timeout."""

        def find_never_succeeds():
            """Function that always returns None."""
            return None

        result = Retry.WhileNull(
            find_never_succeeds,
            timeout=500,  # Short timeout
            interval=100,
        )

        assert result is None, "Should return None on timeout"

    def test_retry_with_custom_interval(self) -> None:
        """Test Retry with custom interval between attempts."""
        start_time = time.time()
        attempt_count = [0]

        def counting_condition():
            """Condition that counts attempts and returns True for 0.5 seconds."""
            attempt_count[0] += 1
            return time.time() - start_time < 0.5

        Retry.WhileTrue(
            counting_condition,
            timeout=1000,
            interval=200,  # 200ms between attempts
            throw_on_timeout=False,
        )

        # With 200ms interval over 500ms, should have ~2-3 attempts
        assert 2 <= attempt_count[0] <= 5, f"Expected 2-5 attempts, got {attempt_count[0]}"

    def test_retry_while_not_null(self) -> None:
        """Test Retry.while_not_null waits for None value."""
        start_time = time.time()

        def returns_none_after_delay():
            """Function that returns a non-None value for first 0.5 seconds, then None."""
            if time.time() - start_time < 0.5:
                return "NotNone"
            return None

        result = Retry.WhileNotNull(returns_none_after_delay, timeout=1000, throw_on_timeout=False)

        elapsed = time.time() - start_time
        assert elapsed >= 0.5, "Should have waited at least 0.5 seconds"
        assert result is None, "Should return None when condition met"

    def test_retry_while_null(self) -> None:
        """Test Retry.while_null waits for non-None value."""
        start_time = time.time()

        def returns_value_after_delay():
            """Function that returns None for first 0.5 seconds, then a non-None value."""
            if time.time() - start_time < 0.5:
                return None
            return "Found"

        result = Retry.WhileNull(returns_value_after_delay, timeout=1000, throw_on_timeout=False)

        elapsed = time.time() - start_time
        assert elapsed >= 0.5, "Should have waited at least 0.5 seconds"
        assert result == "Found", "Should return the found value"
