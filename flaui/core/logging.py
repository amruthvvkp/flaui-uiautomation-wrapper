"""Route FlaUI's C# logging into Python's standard :mod:`logging` for unified telemetry.

FlaUI (C#) logs through ``FlaUI.Core.Logging.Logger.Default`` (an ``ILogger``). This module installs
FlaUI's own ``EventLogger`` as that default and subscribes to its ``OnLog`` event, forwarding every
C# log message into a Python :class:`logging.Logger`. The result: C# and Python log output land in
**one** destination that you configure with the stdlib ``logging`` module.

(We use ``EventLogger`` + event subscription rather than subclassing ``LoggerBase`` because its log
hooks are ``protected abstract`` and cannot be overridden across the pythonnet boundary.)

The bridge is **opt-in**. Enable it explicitly with :func:`enable_csharp_logging`, or set the
environment variable ``FLAUI_LOG_CSHARP=1`` before :func:`~flaui.lib.pythonnet_bridge.setup_pythonnet_bridge`
runs (see :data:`flaui.lib.config.settings`).

.. note::
   ``setup_pythonnet_bridge()`` must have run before importing/using this module, because the C#
   logging types are only available after the FlaUI DLLs are loaded.

Example::

    import logging
    logging.basicConfig(level=logging.DEBUG)
    from flaui.core.logging import enable_csharp_logging
    enable_csharp_logging()  # FlaUI C# logs now flow through Python logging
"""

from __future__ import annotations

import logging
from typing import Any, Optional, Tuple

#: Name of the default Python logger the C# sink writes to.
CSHARP_LOGGER_NAME = "flaui.csharp"

#: Maps the integer value of ``FlaUI.Core.Logging.LogLevel`` to a Python logging level.
_LEVEL_MAP = {
    0: logging.DEBUG,  # Trace
    1: logging.DEBUG,  # Debug
    2: logging.INFO,  # Info
    3: logging.WARNING,  # Warn
    4: logging.ERROR,  # Error
    5: logging.CRITICAL,  # Fatal
}

#: Holds the active ``(event_logger, delegate, callback)`` so the C# delegate is kept alive (the
#: event may fire from a background thread, so its Python target must survive GC).
_active_sink: Optional[Tuple[Any, Any, Any]] = None


def enable_csharp_logging(logger: Optional[logging.Logger] = None, level: Optional[str] = None) -> Any:
    """Install FlaUI's ``EventLogger`` as the default and forward its events into Python logging.

    All FlaUI C# log output is emitted at every level (the C# side gates nothing); the Python
    ``logging`` configuration decides what is actually recorded, giving you a single place to control
    verbosity and destinations. Calling this again replaces any previously installed sink.

    :param logger: Python logger to forward into; defaults to ``logging.getLogger("flaui.csharp")``.
    :param level: Optional Python level name (e.g. ``"DEBUG"``) applied to ``logger``.
    :return: The installed C# ``EventLogger`` instance (also set as ``Logger.Default``).
    """
    from System import Action  # pyright: ignore
    from FlaUI.Core.Logging import EventLogger, LogLevel as CSLogLevel, Logger as CSLogger  # pyright: ignore

    disable_csharp_logging()  # remove any previous subscription first

    py_logger = logger if logger is not None else logging.getLogger(CSHARP_LOGGER_NAME)
    if level is not None:
        py_logger.setLevel(level)

    def _on_log(cs_level: Any, message: str) -> None:
        """Forward a single C# log entry into the Python logger."""
        py_logger.log(_LEVEL_MAP.get(int(cs_level), logging.INFO), message)

    event_logger = EventLogger()
    # Emit everything from C#; Python logging handles filtering for a single, unified control point.
    event_logger.SetLevel(CSLogLevel.Trace)
    delegate = Action[CSLogLevel, str](_on_log)
    event_logger.OnLog += delegate
    CSLogger.Default = event_logger

    global _active_sink
    _active_sink = (event_logger, delegate, _on_log)
    return event_logger


def disable_csharp_logging() -> None:
    """Stop routing C# logs into Python and restore a silent (``NullLogger``) default."""
    from FlaUI.Core.Logging import Logger as CSLogger, NullLogger  # pyright: ignore

    global _active_sink
    if _active_sink is not None:
        event_logger, delegate, _callback = _active_sink
        try:
            event_logger.OnLog -= delegate
        except Exception:  # pragma: no cover - best-effort detach
            pass
        _active_sink = None
    CSLogger.Default = NullLogger()


def maybe_enable_from_settings() -> None:
    """Enable the C# log sink if ``FLAUI_LOG_CSHARP`` is set (called during bridge setup).

    No-op when the flag is off. Failures are swallowed (logging must never break automation setup).
    """
    from flaui.lib.config import settings

    if not settings.LOG_CSHARP:
        return
    try:
        enable_csharp_logging(level=settings.LOG_CSHARP_LEVEL)
    except Exception:  # pragma: no cover - logging must never break setup
        logging.getLogger(__name__).exception("Failed to enable C# logging sink")
