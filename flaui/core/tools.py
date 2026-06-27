"""
This module contains classes and methods for retrying actions.
Although the retry methods are not used in the library, they are still useful for the end user.
FlaUI.Core.Tools do have some useful methods for retrying actions, but translations between Python and C# for these classes has been quite complex.
These custom retry methods are written in Python and can be used directly in the library.
These can be actively used during test automation for reliability and improved performance.
"""

from collections.abc import Iterable
import time
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar

import psutil

if TYPE_CHECKING:
    from flaui.core.automation_elements import AutomationElement

T = TypeVar("T")


class Retry:
    """This class contains methods for retrying actions.

    :raises TimeoutError: If the timeout has been reached.
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


class ItemRealizer:
    """Realizes virtualized items in a container so they become full members of the automation tree.

    Mirrors C# ``FlaUI.Core.Tools.ItemRealizer``; delegates to the native implementation, which uses
    the Scroll and ItemContainer patterns to walk and realize each item.
    """

    @staticmethod
    def realize_items(item_container_element: "AutomationElement") -> None:
        """Realize all virtualized items in the given container element.

        :param item_container_element: The container whose items should be realized.
        """
        from FlaUI.Core.Tools import ItemRealizer as CSItemRealizer  # pyright: ignore

        CSItemRealizer.RealizeItems(item_container_element.raw_element)


class AccessibilityTextResolver:
    """Resolves human-readable text for MSAA accessibility roles and states.

    Mirrors C# ``FlaUI.Core.Tools.AccessibilityTextResolver`` (a thin wrapper over ``oleacc``).
    Roles/states are the C# ``AccessibilityRole`` / ``AccessibilityState`` values, e.g. those
    returned by ``element.patterns.legacy_i_accessible.pattern.role.value``.
    """

    @staticmethod
    def get_role_text(role: Any) -> str:
        """Return the localized text for an accessibility role.

        :param role: The C# ``AccessibilityRole`` value.
        :return: Human-readable role text (e.g. ``"push button"``).
        """
        from FlaUI.Core.Tools import AccessibilityTextResolver as CSResolver  # pyright: ignore

        return CSResolver.GetRoleText(role)

    @staticmethod
    def get_state_bit_text(state: Any) -> str:
        """Return the localized text for a single accessibility state bit.

        :param state: The C# ``AccessibilityState`` value (single bit).
        :return: Human-readable state text (e.g. ``"focused"``).
        """
        from FlaUI.Core.Tools import AccessibilityTextResolver as CSResolver  # pyright: ignore

        return CSResolver.GetStateBitText(state)

    @staticmethod
    def get_state_text(state: Any) -> str:
        """Return the comma-separated localized text for all set accessibility state flags.

        :param state: The C# ``AccessibilityState`` value (possibly multiple flags).
        :return: Comma-separated human-readable state text.
        """
        from FlaUI.Core.Tools import AccessibilityTextResolver as CSResolver  # pyright: ignore

        return CSResolver.GetStateText(state)


class WindowsStoreAppLauncher:
    """Launches Windows Store (UWP) apps by their Application User Model ID.

    Mirrors C# ``FlaUI.Core.Tools.WindowsStoreAppLauncher``, which uses the COM
    ``IApplicationActivationManager`` to activate the app.
    """

    @staticmethod
    def launch(app_user_model_id: str, arguments: str = "") -> int:
        """Launch a Windows Store app and return its process id.

        :param app_user_model_id: The Application User Model ID of the app to launch.
        :param arguments: Arguments to pass to the app, defaults to an empty string.
        :return: The process id of the launched app.
        """
        from FlaUI.Core.Tools import WindowsStoreAppLauncher as CSLauncher  # pyright: ignore

        return int(CSLauncher.Launch(app_user_model_id, arguments).Id)


class LocalizedStrings:
    """Culture-aware UI strings used by FlaUI (e.g. scroll-bar names per framework/locale).

    Mirrors C# ``FlaUI.Core.Tools.LocalizedStrings``; values are read from the native class, which
    selects strings based on the current OS culture.
    """

    @staticmethod
    def _get(name: str) -> str:
        """Return a named localized string from the C# ``LocalizedStrings`` class.

        :param name: The C# property name (PascalCase).
        :return: The localized string value.
        """
        from FlaUI.Core.Tools import LocalizedStrings as CSLocalizedStrings  # pyright: ignore

        return getattr(CSLocalizedStrings, name)

    @classmethod
    def horizontal_scroll_bar(cls) -> str:
        """Return the localized name of a horizontal scroll bar.

        :return: Localized horizontal scroll-bar name.
        """
        return cls._get("HorizontalScrollBar")

    @classmethod
    def vertical_scroll_bar(cls) -> str:
        """Return the localized name of a vertical scroll bar.

        :return: Localized vertical scroll-bar name.
        """
        return cls._get("VerticalScrollBar")


class SystemInfo:
    """System CPU and memory metrics, implemented in pure Python via :mod:`psutil`.

    Python-native equivalent of C# ``FlaUI.Core.Tools.SystemInfo`` (the C# version uses
    ``PerformanceCounter`` / WMI). Memory values are bytes; percentages are 0-100 floats.
    """

    @staticmethod
    def cpu_usage() -> float:
        """Return the current system-wide CPU utilization as a percentage (0-100).

        :return: CPU usage percentage.
        """
        return psutil.cpu_percent()

    @staticmethod
    def physical_memory_total() -> int:
        """Return the total physical memory in bytes.

        :return: Total physical memory (bytes).
        """
        return psutil.virtual_memory().total

    @staticmethod
    def physical_memory_free() -> int:
        """Return the available physical memory in bytes.

        :return: Available physical memory (bytes).
        """
        return psutil.virtual_memory().available

    @staticmethod
    def physical_memory_used() -> int:
        """Return the used physical memory in bytes.

        :return: Used physical memory (bytes).
        """
        return psutil.virtual_memory().used

    @staticmethod
    def physical_memory_used_percent() -> float:
        """Return the used physical memory as a percentage (0-100).

        :return: Used physical memory percentage.
        """
        return psutil.virtual_memory().percent

    @staticmethod
    def physical_memory_free_percent() -> float:
        """Return the free physical memory as a percentage (0-100).

        :return: Free physical memory percentage.
        """
        return 100.0 - psutil.virtual_memory().percent

    @staticmethod
    def virtual_memory_total() -> int:
        """Return the total virtual (swap/page-file) memory in bytes.

        :return: Total virtual memory (bytes).
        """
        return psutil.swap_memory().total

    @staticmethod
    def virtual_memory_free() -> int:
        """Return the free virtual (swap/page-file) memory in bytes.

        :return: Free virtual memory (bytes).
        """
        return psutil.swap_memory().free

    @staticmethod
    def virtual_memory_used() -> int:
        """Return the used virtual (swap/page-file) memory in bytes.

        :return: Used virtual memory (bytes).
        """
        return psutil.swap_memory().used

    # @staticmethod
    # def
