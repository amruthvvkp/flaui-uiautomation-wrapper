"""Threading utilities to ensure UIAutomation calls run on an STA thread.

This module provides a lightweight single-threaded apartment (STA) executor
that marshals callable execution onto a dedicated .NET STA thread. This avoids
COM threading violations (e.g., 0x8001010d) when UIAutomation objects are
accessed from background or async threads.

The executor is intentionally minimal and synchronous. It is used by core API
entrypoints and proxies that expose C# FrameworkAutomationElement members.
"""

from __future__ import annotations

from queue import Queue
import threading
from typing import Any, Callable, Optional, Tuple

from System.Threading import ApartmentState, Thread, ThreadStart  # type: ignore


class _Result:
    """Hold the outcome of a scheduled callable.

    Stores either a returned value or an exception and allows the caller to
    wait synchronously for completion.
    """

    def __init__(self) -> None:
        self._event = threading.Event()
        self._value: Any = None
        self._exc: Optional[BaseException] = None

    def set_result(self, value: Any) -> None:
        """Set the successful result value.

        :param value: Value produced by the callable.
        :return: None
        """
        self._value = value
        self._event.set()

    def set_exception(self, exc: BaseException) -> None:
        """Set the exception raised by the callable.

        :param exc: Exception raised during execution.
        :return: None
        """
        self._exc = exc
        self._event.set()

    def result(self) -> Any:
        """Return the result or raise the captured exception.

        :return: The value produced by the callable when successful.
        :raises BaseException: Re-raises the exception captured from the callable.
        """
        self._event.wait()
        if self._exc is not None:
            raise self._exc
        return self._value


class STAThreadExecutor:
    """Provide a dedicated STA thread to synchronously run callables.

    All UIA/COM-bound calls should be executed via this executor to avoid
    apartment/thread affinity issues.
    """

    def __init__(self) -> None:
        self._queue: "Queue[Tuple[Callable[..., Any], Tuple[Any, ...], dict, _Result]]" = Queue()
        self._ready = threading.Event()

        def _worker() -> None:
            # Signal ready as soon as we enter the thread
            self._ready.set()
            while True:
                func, args, kwargs, res = self._queue.get()
                try:
                    value = func(*args, **kwargs)
                except BaseException as exc:  # noqa: BLE001
                    res.set_exception(exc)
                else:
                    res.set_result(value)

        # Start a .NET Thread with STA apartment state
        self._thread = Thread(ThreadStart(_worker))
        self._thread.IsBackground = True
        self._thread.SetApartmentState(ApartmentState.STA)
        self._thread.Start()
        # Wait until the thread signals readiness
        self._ready.wait()

    def run(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute the callable on the STA thread and return its result.

        :param func: Callable to execute on the STA thread.
        :param args: Positional arguments forwarded to the callable.
        :param kwargs: Keyword arguments forwarded to the callable.
        :return: The callable's return value.
        :raises BaseException: Any exception raised by the callable.
        """
        res = _Result()
        self._queue.put((func, args, kwargs, res))
        return res.result()


_executor_lock = threading.Lock()
_executor_singleton: Optional[STAThreadExecutor] = None


def get_sta_executor() -> STAThreadExecutor:
    """Return the singleton STA executor instance.

    Lazily creates the executor on first use and reuses it for all
    subsequent calls to ensure a single STA thread is used.

    :return: Shared `STAThreadExecutor` instance.
    """
    global _executor_singleton
    if _executor_singleton is None:
        with _executor_lock:
            if _executor_singleton is None:
                _executor_singleton = STAThreadExecutor()
    return _executor_singleton
