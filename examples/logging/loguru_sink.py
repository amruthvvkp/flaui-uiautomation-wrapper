"""Logging example: send everything FlaUI logs (Python and C#) to loguru.

Run it from the project root (loguru is not a project dependency)::

    uv run --with loguru python examples/logging/loguru_sink.py

FlaUI logs through the standard library, so the usual loguru "intercept handler" bridges it: one
``logging.Handler`` on the ``flaui`` logger that re-emits each record through loguru.
"""

import _demo

# --8<-- [start:loguru]
import inspect
import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    """Re-emit standard-library log records through loguru (the pattern from loguru's docs)."""

    def emit(self, record: logging.LogRecord) -> None:
        """Forward one record, keeping its level and the caller's location."""
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame, depth = frame.f_back, depth + 1
        logger.opt(depth=depth, exception=record.exc_info).bind(source=record.name).log(level, record.getMessage())


# Route the whole "flaui" hierarchy (Python modules + "flaui.csharp") into loguru only.
flaui_logger = logging.getLogger("flaui")
flaui_logger.handlers = [InterceptHandler()]
flaui_logger.setLevel(logging.DEBUG)
flaui_logger.propagate = False

# loguru sinks: a readable console, and a JSON file holding only the C# messages.
logger.remove()
logger.add(sys.stderr, level="INFO", format="{time:HH:mm:ss} {level:<7} {extra[source]}: {message}")
logger.add(
    "flaui-csharp.jsonl", level="DEBUG", serialize=True, filter=lambda r: r["extra"].get("source") == "flaui.csharp"
)
# --8<-- [end:loguru]

if __name__ == "__main__":
    _demo.run()
    logger.complete()
    print(open("flaui-csharp.jsonl", encoding="utf-8").read()[:600])
