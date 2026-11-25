"""Logging example: the standard library ``logging`` module, console plus a C#-only log file.

Run it from the project root::

    uv run python examples/logging/stdlib_sink.py

Everything from FlaUI goes through the ``flaui`` logger hierarchy, so you configure it like any other
library: Python-side messages on ``flaui.<module>`` loggers, C# messages on ``flaui.csharp``.
"""

from pathlib import Path

import _demo

# --8<-- [start:stdlib]
import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {"format": "%(asctime)s %(levelname)-7s %(name)s: %(message)s"},
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "plain", "level": "INFO"},
            "csharp_file": {
                "class": "logging.FileHandler",
                "filename": "flaui-csharp.log",
                "formatter": "plain",
                "level": "DEBUG",
            },
        },
        "loggers": {
            # Every Python-side FlaUI logger: INFO and above to the console.
            "flaui": {"handlers": ["console"], "level": "INFO"},
            # C# FlaUI messages: everything, into their own file (and up to "flaui" for the console).
            "flaui.csharp": {"handlers": ["csharp_file"], "level": "DEBUG"},
        },
    }
)
# --8<-- [end:stdlib]

if __name__ == "__main__":
    _demo.run()
    logging.shutdown()
    print("C# log file:", Path("flaui-csharp.log").resolve())
    print(Path("flaui-csharp.log").read_text(encoding="utf-8"))
