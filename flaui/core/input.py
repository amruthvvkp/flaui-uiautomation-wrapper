"""This module acts as a wrapper for classes listed in FlaUI.Core.Input namespace. It provides methods to interact with the keyboard and mouse."""

import time
from typing import Any, Optional

from FlaUI.Core.Input import Wait as CSWait  # pyright: ignore

from flaui.core.automation_elements import AutomationElement


class Wait:
    """Various helper tools used in various places, wrapper over Wait class in FlaUI.Core.Input namespace"""

    DEFAULT_TIMEOUT = 1  # in seconds

    @staticmethod
    def until_input_is_processed(wait_timeout_in_secs: Optional[float] = None):
        """
        Waits a little to allow inputs (mouse, keyboard, ...) to be processed.

        :param wait_timeout_in_secs: An optional timeout. If no value or None is passed, the timeout is 100ms.
        """
        wait_time = wait_timeout_in_secs if wait_timeout_in_secs is not None else 0.1  # default to 100ms
        time.sleep(wait_time)

    @staticmethod
    def until_responsive(automation_element: AutomationElement, timeout_in_secs: Optional[float] = None):
        """
        Waits until the given element is responsive.

        :param automation_element: The element that should be waited for.
        :param timeout_in_secs: The timeout of the waiting.
        :return: True if the element was responsive, false otherwise.
        """
        return CSWait.UntilResponsive(
            automation_element, timeout_in_secs if timeout_in_secs is not None else Wait.DEFAULT_TIMEOUT
        )

    @staticmethod
    def until_responsive_hwnd(hWnd: Any, timeout: Optional[float] = None):
        """
        Waits until the given hwnd is responsive.

        :param hWnd: The hwnd that should be waited for.
        :param timeout: The timeout of the waiting.
        :return: True if the hwnd was responsive, false otherwise.
        """
        return CSWait.UntilResponsiveHwnd(hWnd, timeout if timeout is not None else Wait.DEFAULT_TIMEOUT)


class Keyboard:
    """Simulates Key input, wrapper over Wait class in FlaUI.Core.Input namespace"""

    @staticmethod
    def type(text: str):
        pass
