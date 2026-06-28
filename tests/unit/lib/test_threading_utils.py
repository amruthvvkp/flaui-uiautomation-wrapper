"""Unit tests for the STA threading executor utilities."""

import pytest

from flaui.lib.threading_utils import _Result, STAThreadExecutor, get_sta_executor


class TestResult:
    """Validate the ``_Result`` future-like holder directly (on the main thread)."""

    def test_result_returns_value(self) -> None:
        """``result`` returns the value set by ``set_result``."""
        result = _Result()
        result.set_result(99)

        assert result.result() == 99

    def test_result_raises_set_exception(self) -> None:
        """``result`` re-raises the exception set by ``set_exception``."""
        result = _Result()
        result.set_exception(ValueError("boom"))

        with pytest.raises(ValueError, match="boom"):
            result.result()


class TestSTAThreadExecutor:
    """Validate that callables run on the dedicated STA thread and results/exceptions propagate."""

    def test_run_returns_value(self) -> None:
        """``run`` returns the callable's value."""
        executor = STAThreadExecutor()

        assert executor.run(lambda: 21 * 2) == 42

    def test_run_forwards_args_and_kwargs(self) -> None:
        """Positional and keyword arguments are forwarded to the callable."""
        executor = STAThreadExecutor()

        def add(a: int, b: int, c: int = 0) -> int:
            """Sum the three operands."""
            return a + b + c

        assert executor.run(add, 1, 2, c=3) == 6

    def test_run_propagates_exception(self) -> None:
        """An exception raised by the callable is re-raised to the caller."""
        executor = STAThreadExecutor()

        def boom() -> None:
            """Raise a ValueError."""
            raise ValueError("kaboom")

        with pytest.raises(ValueError, match="kaboom"):
            executor.run(boom)

    def test_runs_on_dedicated_sta_thread(self) -> None:
        """The callable executes on a thread distinct from the caller's."""
        import threading

        from System.Threading import ApartmentState, Thread  # type: ignore

        executor = STAThreadExecutor()
        caller_thread_id = threading.get_ident()

        worker_thread_id = executor.run(threading.get_ident)
        apartment = executor.run(lambda: Thread.CurrentThread.GetApartmentState())

        assert worker_thread_id != caller_thread_id
        assert apartment == ApartmentState.STA


class TestGetSTAExecutor:
    """Validate the lazily-created singleton executor."""

    def test_returns_same_instance(self) -> None:
        """Repeated calls return the same shared executor."""
        assert get_sta_executor() is get_sta_executor()

    def test_singleton_is_executor(self) -> None:
        """The singleton is a working ``STAThreadExecutor``."""
        assert isinstance(get_sta_executor(), STAThreadExecutor)
        assert get_sta_executor().run(lambda: "ok") == "ok"
