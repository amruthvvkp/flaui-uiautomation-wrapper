"""
This module contains classes and methods for retrying actions.
Although the retry methods are not used in the library, they are still useful for the end user.
FlaUI.Core.Tools do have some useful methods for retrying actions, but translations between Python and C# for these classes has been quite complex.
These custom retry methods are written in Python and can be used directly in the library.
These can be actively used during test automation for reliability and improved performance.
"""

from collections.abc import Iterable
import time
from typing import Callable, Optional, TypeVar

T = TypeVar("T")


class Retry:
    """This class contains methods for retrying actions.

    :raises TimeoutError: If the timeout has been reached.
    :return: The result of the retry method.
    """

    @staticmethod
    def _now_ms() -> float:
        """Get the current time in milliseconds."""
        return time.monotonic() * 1000.0

    @staticmethod
    def _sleep_ms(ms: int) -> None:
        """Sleep for the specified number of milliseconds."""
        time.sleep(ms / 1000.0)

    @staticmethod
    def While(
        retry_method: Callable[[], T],
        timeout: int = 1000,
        interval: int = 100,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries the method until the check method returns True.

        Example:

        Retry.While(
            retry_method=lambda: main_window.find_first_descendant(condition=cf.by_class_name("#32770")).as_window(),
            timeout=5,
            interval=0.1,
        )

        :param retry_method: The method to retry.
        :param timeout: Timeout when the retry aborts, defaults to 1
        :param interval: Interval of retries, defaults to 0.1
        :param throw_on_timeout: Flag to indicate if exception is thrown on timeout, defaults to False
        :param ignore_exception: Flag to indicate that exceptions can be ignored, defaults to False
        :param timeout_message: Message that should be added to the timeout exception incase of a timeout, defaults to None
        :param last_value_on_timeout: Flag to indicate that last value should be returned on timeout, defaults to False
        :param default_on_timeout: Defines a default value in case of a timeout, defaults to None
        :raises TimeoutError: If the timeout has been reached
        :return: Result of the retry method
        """
        start = Retry._now_ms()
        last_value: Optional[T] = None
        while True:
            try:
                val = retry_method()
                last_value = val
                if val:
                    return val
            except (ValueError, AssertionError) as e:
                if not ignore_exception:
                    raise
                last_value = e  # type: ignore
            if Retry._now_ms() - start >= timeout:
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
                if last_value_on_timeout:
                    return last_value  # type: ignore
                if default_on_timeout is not None:
                    return default_on_timeout
                raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
            Retry._sleep_ms(interval)

    @staticmethod
    def WhileNot(
        retry_method: Callable[[], T],
        timeout: int = 1000,
        interval: int = 100,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries the method until the check method returns False.

        :param retry_method: The method to retry.
        :param timeout: Timeout when the retry aborts, defaults to 1
        :param interval: Interval of retries, defaults to 0.1
        :param throw_on_timeout: Flag to indicate if exception is thrown on timeout, defaults to False
        :param ignore_exception: Flag to indicate that exceptions can be ignored, defaults to False
        :param timeout_message: Message that should be added to the timeout exception incase of a timeout, defaults to None
        :param last_value_on_timeout: Flag to indicate that last value should be returned on timeout, defaults to False
        :param default_on_timeout: Defines a default value in case of a timeout, defaults to None
        :raises TimeoutError: If the timeout has been reached
        :return: Result of the retry method
        """
        start = Retry._now_ms()
        last_value: Optional[T] = None
        while True:
            try:
                val = retry_method()
                last_value = val
                if not val:
                    return val
            except (ValueError, AssertionError) as e:
                if not ignore_exception:
                    raise
                last_value = e  # type: ignore
            if Retry._now_ms() - start >= timeout:
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
                if last_value_on_timeout:
                    return last_value  # type: ignore
                if default_on_timeout is not None:
                    return default_on_timeout
                raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
            Retry._sleep_ms(interval)

    @staticmethod
    def WhileTrue(
        retry_method: Callable[[], T],
        timeout: int = 1000,
        interval: int = 100,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> bool:
        """Retries while the predicate returns True; succeeds when it becomes False.

        :param retry_method: The method to retry.
        :param timeout: Timeout when the retry aborts, defaults to 1
        :param interval: Interval of retries, defaults to 0.1
        :param throw_on_timeout: Flag to indicate if exception is thrown on timeout, defaults to False
        :param ignore_exception: Flag to indicate that exceptions can be ignored, defaults to False
        :param timeout_message: Message that should be added to the timeout exception incase of a timeout, defaults to None
        :param last_value_on_timeout: Flag to indicate that last value should be returned on timeout, defaults to False
        :param default_on_timeout: Defines a default value in case of a timeout, defaults to None
        :raises TimeoutError: If the timeout has been reached
        :return: True if the predicate became False before timeout, False otherwise
        """
        start = Retry._now_ms()
        while True:
            try:
                if not bool(retry_method()):
                    return True
            except (ValueError, AssertionError):
                if not ignore_exception:
                    raise
            if Retry._now_ms() - start >= timeout:
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
                return False
            Retry._sleep_ms(interval)

    @staticmethod
    def WhileFalse(
        retry_method: Callable[[], T],
        timeout: int = 1000,
        interval: int = 100,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> bool:
        """Retries while the predicate returns False; succeeds when it becomes True.

        :param retry_method: The method to retry.
        :param timeout: Timeout when the retry aborts, defaults to 1
        :param interval: Interval of retries, defaults to 0.1
        :param throw_on_timeout: Flag to indicate if exception is thrown on timeout, defaults to False
        :param ignore_exception: Flag to indicate that exceptions can be ignored, defaults to False
        :param timeout_message: Message that should be added to the timeout exception incase of a timeout, defaults to None
        :param last_value_on_timeout: Flag to indicate that last value should be returned on timeout, defaults to False
        :param default_on_timeout: Defines a default value in case of a timeout, defaults to None
        :raises TimeoutError: If the timeout has been reached
        :return: True if the predicate became True before timeout, False otherwise
        """
        start = Retry._now_ms()
        while True:
            try:
                if bool(retry_method()):
                    return True
            except (ValueError, AssertionError):
                if not ignore_exception:
                    raise
            if Retry._now_ms() - start >= timeout:
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
                return False
            Retry._sleep_ms(interval)

    @staticmethod
    def WhileNull(
        retry_method: Callable[[], T],
        timeout: int = 1000,
        interval: int = 100,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries while the result is None; returns first non-None value.

        :param retry_method: The method to retry.
        :param timeout: Timeout when the retry aborts, defaults to 1
        :param interval: Interval of retries, defaults to 0.1
        :param throw_on_timeout: Flag to indicate if exception is thrown on timeout, defaults to False
        :param ignore_exception: Flag to indicate that exceptions can be ignored, defaults to False
        :param timeout_message: Message that should be added to the timeout exception incase of a timeout, defaults to None
        :param last_value_on_timeout: Flag to indicate that last value should be returned on timeout, defaults to False
        :param default_on_timeout: Defines a default value in case of a timeout, defaults to None
        :raises TimeoutError: If the timeout has been reached
        :return: Result of the retry method
        """
        start = Retry._now_ms()
        while True:
            try:
                val = retry_method()
                if val is not None:
                    return val
            except (ValueError, AssertionError):
                if not ignore_exception:
                    raise
            if Retry._now_ms() - start >= timeout:
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
                return None  # type: ignore
            Retry._sleep_ms(interval)

    @staticmethod
    def WhileNotNull(
        retry_method: Callable[[], T],
        timeout: int = 1000,
        interval: int = 100,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries while the result is not None; returns None once it becomes None.

        :param retry_method: The method to retry.
        :param timeout: Timeout when the retry aborts, defaults to 1
        :param interval: Interval of retries, defaults to 0.1
        :param throw_on_timeout: Flag to indicate if exception is thrown on timeout, defaults to False
        :param ignore_exception: Flag to indicate that exceptions can be ignored, defaults to False
        :param timeout_message: Message that should be added to the timeout exception incase of a timeout, defaults to None
        :param last_value_on_timeout: Flag to indicate that last value should be returned on timeout, defaults to False
        :param default_on_timeout: Defines a default value in case of a timeout, defaults to None
        :raises TimeoutError: If the timeout has been reached
        :return: Result of the retry method
        """
        start = Retry._now_ms()
        last_value: Optional[T] = None
        while True:
            try:
                val = retry_method()
                last_value = val
                if val is None:
                    return None  # type: ignore
            except (ValueError, AssertionError) as e:
                if not ignore_exception:
                    raise
                last_value = e  # type: ignore
            if Retry._now_ms() - start >= timeout:
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
                return last_value  # type: ignore
            Retry._sleep_ms(interval)

    @staticmethod
    def WhileEmpty(
        retry_method: Callable[[], T],
        timeout: int = 1000,
        interval: int = 100,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries while the result is empty (iterable of length 0).

        :param retry_method: The method to retry.
        :param timeout: Timeout when the retry aborts, defaults to 1
        :param interval: Interval of retries, defaults to 0.1
        :param throw_on_timeout: Flag to indicate if exception is thrown on timeout, defaults to False
        :param ignore_exception: Flag to indicate that exceptions can be ignored, defaults to False
        :param timeout_message: Message that should be added to the timeout exception incase of a timeout, defaults to None
        :param last_value_on_timeout: Flag to indicate that last value should be returned on timeout, defaults to False
        :param default_on_timeout: Defines a default value in case of a timeout, defaults to None
        :raises TimeoutError: If the timeout has been reached
        :return: Result of the retry method
        """
        start = Retry._now_ms()
        last_value: Optional[T] = None
        while True:
            try:
                val = retry_method()
                last_value = val
                if not (isinstance(val, Iterable) and not val):
                    return val
            except (ValueError, AssertionError) as e:
                if not ignore_exception:
                    raise
                last_value = e  # type: ignore
            if Retry._now_ms() - start >= timeout:
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
                if last_value_on_timeout:
                    return last_value  # type: ignore
                if default_on_timeout is not None:
                    return default_on_timeout
                raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
            Retry._sleep_ms(interval)

    @staticmethod
    def WhileException(
        retry_method: Callable[[], T],
        timeout: int = 1000,
        interval: int = 100,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries while the function raises; returns first successful result.

        :param retry_method: The method to retry.
        :param timeout: Timeout when the retry aborts, defaults to 1
        :param interval: Interval of retries, defaults to 0.1
        :param throw_on_timeout: Flag to indicate if exception is thrown on timeout, defaults to False
        :param ignore_exception: Flag to indicate that exceptions can be ignored, defaults to False
        :param timeout_message: Message that should be added to the timeout exception incase of a timeout, defaults to None
        :param last_value_on_timeout: Flag to indicate that last value should be returned on timeout, defaults to False
        :param default_on_timeout: Defines a default value in case of a timeout, defaults to None
        :raises TimeoutError: If the timeout has been reached
        :return: Result of the retry method
        """
        start = Retry._now_ms()
        last_exc: Optional[Exception] = None
        while True:
            try:
                return retry_method()
            except Exception as e:  # Always ignore and retry until success
                last_exc = e
            if Retry._now_ms() - start >= timeout:
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
                if last_exc is not None and not ignore_exception:
                    # If not configured to ignore, propagate last exception
                    raise last_exc
                raise TimeoutError(timeout_message or f"Timeout of {timeout} ms exceeded.")
            Retry._sleep_ms(interval)

    @staticmethod
    def IsTimeOutReached(start_time: float, timeout: int) -> bool:
        """Checks if the timeout has been reached.

        :param start_time: The start time.
        :param timeout: The timeout.
        :return: True if the timeout has been reached, False otherwise.
        """
        return (time.monotonic() - start_time) * 1000.0 > timeout

    # @staticmethod
    # def
