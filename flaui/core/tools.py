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

import arrow

T = TypeVar("T")


class Retry:
    """This class contains methods for retrying actions.

    :raises TimeoutError: If the timeout has been reached.
    :return: The result of the retry method.
    """

    @staticmethod
    def _execute(
        retry_method: Callable[[], T],
        check_method: Callable[[T], bool],
        timeout: int = 1,
        interval: float = 0.1,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Executes the retry method.

        :param retry_method: The method to retry.
        :param check_method: The method to check the result.
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
        start_time = arrow.now()
        result = None

        while True:
            try:
                result = retry_method()
                if check_method(result):
                    return result
            except (ValueError, AssertionError):
                if not ignore_exception:
                    raise
            if arrow.now() > start_time.shift(seconds=timeout):
                if throw_on_timeout:
                    raise TimeoutError(timeout_message or f"Timeout of {timeout} seconds exceeded.")
                if last_value_on_timeout:
                    return result
                if default_on_timeout is not None:
                    return default_on_timeout
                raise TimeoutError(timeout_message or f"Timeout of {timeout} seconds exceeded.")
            time.sleep(interval)

    @staticmethod
    def While(
        retry_method: Callable[[], T],
        timeout: int = 1,
        interval: float = 0.1,
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
        return Retry._execute(
            retry_method,
            lambda x: x,  # pyright: ignore
            timeout,
            interval,
            throw_on_timeout,
            ignore_exception,
            timeout_message,
            last_value_on_timeout,
            default_on_timeout,
        )

    @staticmethod
    def WhileNot(
        retry_method: Callable[[], T],
        timeout: int = 1,
        interval: float = 0.1,
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
        return Retry._execute(
            retry_method,
            lambda x: not x,
            timeout,
            interval,
            throw_on_timeout,
            ignore_exception,
            timeout_message,
            last_value_on_timeout,
            default_on_timeout,
        )

    @staticmethod
    def WhileTrue(
        retry_method: Callable[[], T],
        timeout: int = 1,
        interval: float = 0.1,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries the method until the check method returns True.

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
        return Retry._execute(
            retry_method,
            lambda x: x is True,
            timeout,
            interval,
            throw_on_timeout,
            ignore_exception,
            timeout_message,
            last_value_on_timeout,
            default_on_timeout,
        )

    @staticmethod
    def WhileFalse(
        retry_method: Callable[[], T],
        timeout: int = 1,
        interval: float = 0.1,
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
        return Retry._execute(
            retry_method,
            lambda x: x is False,
            timeout,
            interval,
            throw_on_timeout,
            ignore_exception,
            timeout_message,
            last_value_on_timeout,
            default_on_timeout,
        )

    @staticmethod
    def WhileNull(
        retry_method: Callable[[], T],
        timeout: int = 1,
        interval: float = 0.1,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries the method until the check method returns None.

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
        return Retry._execute(
            retry_method,
            lambda x: x is None,
            timeout,
            interval,
            throw_on_timeout,
            ignore_exception,
            timeout_message,
            last_value_on_timeout,
            default_on_timeout,
        )

    @staticmethod
    def WhileNotNull(
        retry_method: Callable[[], T],
        timeout: int = 1,
        interval: float = 0.1,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries the method until the check method returns not None.

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
        return Retry._execute(
            retry_method,
            lambda x: x is not None,
            timeout,
            interval,
            throw_on_timeout,
            ignore_exception,
            timeout_message,
            last_value_on_timeout,
            default_on_timeout,
        )

    @staticmethod
    def WhileEmpty(
        retry_method: Callable[[], T],
        timeout: int = 1,
        interval: float = 0.1,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries the method until the check method returns an empty value.

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
        return Retry._execute(
            retry_method,
            lambda x: isinstance(x, Iterable) and not x,
            timeout,
            interval,
            throw_on_timeout,
            ignore_exception,
            timeout_message,
            last_value_on_timeout,
            default_on_timeout,
        )

    @staticmethod
    def WhileException(
        retry_method: Callable[[], T],
        timeout: int = 1,
        interval: float = 0.1,
        throw_on_timeout: bool = False,
        ignore_exception: bool = False,
        timeout_message: Optional[str] = None,
        last_value_on_timeout: bool = False,
        default_on_timeout: Optional[T] = None,
    ) -> T:
        """Retries the method until the check method returns an exception.

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
        return Retry._execute(
            retry_method,
            lambda x: isinstance(x, Exception),
            timeout,
            interval,
            throw_on_timeout,
            ignore_exception,
            timeout_message,
            last_value_on_timeout,
            default_on_timeout,
        )

    @staticmethod
    def IsTimeOutReached(start_time: float, timeout: int) -> bool:
        """Checks if the timeout has been reached.

        :param start_time: The start time.
        :param timeout: The timeout.
        :return: True if the timeout has been reached, False otherwise.
        """
        return time.time() - start_time > timeout

    # @staticmethod
    # def
