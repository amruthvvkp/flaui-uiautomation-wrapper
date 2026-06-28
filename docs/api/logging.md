# Logging

Route FlaUI's C# logging into Python's standard ``logging`` for unified telemetry. The bridge
installs FlaUI's ``EventLogger`` as ``Logger.Default`` and forwards its events into a Python logger,
so C# and Python log output land in one configurable destination.

It is **opt-in**: call ``enable_csharp_logging()``, or set the environment variable
``FLAUI_LOG_CSHARP=1`` (optionally ``FLAUI_LOG_CSHARP_LEVEL=DEBUG``) before
``setup_pythonnet_bridge()`` runs.

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from flaui.core.logging import enable_csharp_logging
enable_csharp_logging()  # FlaUI C# logs now flow through Python logging
```

::: flaui.core.logging
