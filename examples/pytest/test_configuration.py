"""Runnable recipes for the *Configuration & logging* guide.

Run it from the project root::

    uv run pytest examples/pytest/test_configuration.py -v

The guide includes the Python tab of each recipe straight from this file via the
``# --8<-- [start:name]`` / ``# --8<-- [end:name]`` section markers.
"""

import logging
from typing import Generator

from flaui.core.automation_elements import Window
import flaui.core.input as flaui_input
from flaui.core.logging import disable_csharp_logging
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from conftest import find_test_app


@pytest.fixture
def csharp_logging() -> Generator[None, None, None]:
    """Make sure every test starts and ends with the C# sink switched off."""
    disable_csharp_logging()
    yield
    disable_csharp_logging()


@pytest.mark.usefixtures("csharp_logging")
def test_enable_csharp_logging(caplog: pytest.LogCaptureFixture) -> None:
    """C# FlaUI messages arrive on the ``flaui.csharp`` Python logger."""
    caplog.set_level(logging.DEBUG, logger="flaui")
    # --8<-- [start:enable_csharp]
    from flaui.core.logging import enable_csharp_logging

    enable_csharp_logging()  # C# FlaUI -> logging.getLogger("flaui.csharp")
    # or forward into a logger of your own, at a level of your choosing:
    enable_csharp_logging(logger=logging.getLogger("myapp.flaui"), level="INFO")
    # --8<-- [end:enable_csharp]

    enable_csharp_logging()
    with Automation(UIAutomationTypes.UIA3) as automation:
        automation.application.launch(str(find_test_app()))
        automation.application.get_main_window(automation)
    assert any(r.name == "flaui.csharp" and "Launching process" in r.getMessage() for r in caplog.records)


def test_logger_hierarchy() -> None:
    """Library loggers live under ``flaui`` and print nothing until you configure logging."""
    # --8<-- [start:hierarchy]
    import logging

    logging.basicConfig(level=logging.INFO)  # your app's normal setup is all FlaUI needs
    logging.getLogger("flaui").setLevel(logging.WARNING)  # quieter FlaUI...
    logging.getLogger("flaui.csharp").setLevel(logging.DEBUG)  # ...except the C# messages
    # --8<-- [end:hierarchy]
    assert logging.getLogger("flaui.csharp").getEffectiveLevel() == logging.DEBUG
    logging.getLogger("flaui").setLevel(logging.NOTSET)
    logging.getLogger("flaui.csharp").setLevel(logging.NOTSET)


def test_main_window_timeout() -> None:
    """``Automation(timeout=...)`` sets how long ``get_main_window`` waits (milliseconds)."""
    # --8<-- [start:main_window_timeout]
    with Automation(UIAutomationTypes.UIA3, timeout=15000) as automation:  # wait up to 15 s
        automation.application.launch(str(find_test_app()))
        window = automation.application.get_main_window(automation)
    # --8<-- [end:main_window_timeout]
    assert isinstance(window, Window)


def test_uia3_timeouts(automation: Automation) -> None:
    """Read and change the C# UIA3 transaction and connection timeouts."""
    # --8<-- [start:uia_timeouts]
    from System import TimeSpan

    base = automation.automation_base  # UIA3 only: UIA2 raises NotSupportedByFrameworkException
    print(base.transaction_timeout, base.connection_timeout)  # 00:00:20 00:00:02 by default
    base.transaction_timeout = TimeSpan.FromSeconds(30)
    # --8<-- [end:uia_timeouts]
    assert base.transaction_timeout.TotalSeconds == 30
    base.transaction_timeout = TimeSpan.FromSeconds(20)


def test_mouse_speed() -> None:
    """Mouse movement speed is a class-level setting shared with C#."""
    original = flaui_input.Mouse.move_pixels_per_millisecond
    # --8<-- [start:mouse_speed]
    from flaui.core.input import Mouse

    Mouse.move_pixels_per_millisecond = 2.0  # default 0.5; higher moves faster
    Mouse.move_pixels_per_step = 10  # default 10; larger steps, fewer intermediate points
    # --8<-- [end:mouse_speed]
    try:
        assert Mouse.move_pixels_per_millisecond == 2.0
    finally:
        Mouse.move_pixels_per_millisecond = original
