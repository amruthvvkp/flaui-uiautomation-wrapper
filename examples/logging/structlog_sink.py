"""Logging example: render everything FlaUI logs (Python and C#) as structlog JSON.

Run it from the project root (structlog is not a project dependency)::

    uv run --with structlog python examples/logging/structlog_sink.py

FlaUI logs through the standard library, so structlog's ``ProcessorFormatter`` formats its records:
attach a handler using that formatter to the ``flaui`` logger and every record, Python or C#, comes
out as one JSON object per line.
"""

import _demo

# --8<-- [start:structlog]
import logging
import sys

import structlog

shared_processors = [
    structlog.stdlib.add_logger_name,  # "logger": "flaui.csharp", "flaui.core.application", ...
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
]

# Your own structlog loggers and FlaUI's stdlib records share one pipeline and one output.
structlog.configure(
    processors=[*shared_processors, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,  # applied to FlaUI's (non-structlog) records
        processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, structlog.processors.JSONRenderer()],
    )
)

flaui_logger = logging.getLogger("flaui")
flaui_logger.handlers = [handler]
flaui_logger.setLevel(logging.DEBUG)
flaui_logger.propagate = False

log = structlog.get_logger("flaui.example")  # under "flaui", so it uses the same handler
# --8<-- [end:structlog]

if __name__ == "__main__":
    log.info("demo.start", app="WPF test app")
    _demo.run()
    log.info("demo.done")
