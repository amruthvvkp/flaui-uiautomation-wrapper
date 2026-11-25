# Configuration & logging

This page covers everything you can configure in FlaUI for Python: logging (both the library's own
Python messages and the C# messages from FlaUI itself), the `FLAUI_*` environment variables,
timeouts, and mouse speed.

!!! success "Every Python snippet on this page runs"
    The snippets come from
    [`examples/pytest/test_configuration.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/examples/pytest/test_configuration.py)
    and the scripts in
    [`examples/logging/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples/logging):

    ```bash
    uv run pytest examples/pytest/test_configuration.py -v
    uv run python examples/logging/stdlib_sink.py
    uv run --with loguru python examples/logging/loguru_sink.py
    uv run --with structlog python examples/logging/structlog_sink.py
    ```

## Logging

### How FlaUI logs

FlaUI for Python logs through the standard library `logging` module, using named loggers under
`flaui`:

| Logger | What it records |
|--------|-----------------|
| `flaui.lib.pythonnet_bridge` | Loading the FlaUI assemblies (DEBUG, one line per DLL), plus one INFO line when setup completes |
| `flaui.core.application` | Main-window lookups and cleanup problems (DEBUG) |
| `flaui.modules.automation` | Cleanup problems when an `Automation` exits (DEBUG) |
| `flaui.core.event_handlers` | Errors inside your UI Automation event callbacks |
| `flaui.csharp` | Messages from FlaUI's **C#** code, once you [enable them](#c-logging) |

The `flaui` logger has a `NullHandler`, so **FlaUI prints nothing and never changes your logging
setup** until you configure logging yourself. Because these are ordinary loggers, everything you
already do with `logging` works: levels, handlers, filters, `dictConfig`, pytest's `caplog`.

```python
--8<-- "examples/pytest/test_configuration.py:hierarchy"
```

### C# logging

FlaUI's C# code has its own logger (`FlaUI.Core.Logging.Logger.Default`), which records things like
process launches and application shutdown. It is **off by default**. Turning it on forwards every C#
message to the Python logger `flaui.csharp`, so C# and Python messages end up in the same place and
you control both from Python.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_configuration.py:enable_csharp"
    ```

=== "C#"

    ```csharp
    using FlaUI.Core.Logging;

    // FlaUI ships ConsoleLogger, DebugLogger, TraceLogger, EventLogger and NullLogger.
    Logger.Default = new ConsoleLogger();
    Logger.Default.SetLevel(LogLevel.Debug);
    ```

You can also turn it on without changing any code. Set these environment variables **before**
`setup_pythonnet_bridge()` runs:

```powershell
$env:FLAUI_LOG_CSHARP = "1"
$env:FLAUI_LOG_CSHARP_LEVEL = "DEBUG"   # optional: level for the flaui.csharp logger
```

`disable_csharp_logging()` turns it off again. C# log levels map to Python levels as follows: Trace
and Debug become `DEBUG`, Info becomes `INFO`, Warn becomes `WARNING`, Error becomes `ERROR`, and
Fatal becomes `CRITICAL`.

A typical C# message looks like this:

```text
DEBUG flaui.csharp: [Launching process:C:\...\WpfApplication.exe] [Working directory:C:\...] ...
DEBUG flaui.csharp: Closing application
```

### Sending logs to a sink

Each example below sends both the Python-side `flaui.*` messages and the `flaui.csharp` messages to
one place. Pick the logging library you already use.

=== "logging (stdlib)"

    Console at INFO, plus every C# message in its own file:

    ```python
    --8<-- "examples/logging/stdlib_sink.py:stdlib"
    ```

=== "loguru"

    FlaUI logs through the standard library, so loguru's usual intercept handler bridges it. This
    sends everything to loguru, then writes the C# messages to a separate JSON-lines file:

    ```python
    --8<-- "examples/logging/loguru_sink.py:loguru"
    ```

=== "structlog"

    structlog's `ProcessorFormatter` formats FlaUI's standard-library records, so FlaUI messages
    (Python and C#) and your own structlog events come out as one JSON stream:

    ```python
    --8<-- "examples/logging/structlog_sink.py:structlog"
    ```

    Sample output:

    ```json
    {"event": "Python.NET bridge setup complete (FlaUI 5.0.0.0)", "logger": "flaui.lib.pythonnet_bridge", "level": "info", "timestamp": "..."}
    {"event": "Closing application", "logger": "flaui.csharp", "level": "debug", "timestamp": "..."}
    ```

!!! tip "In pytest"
    pytest captures `logging` records by default, and they show up in failure reports. To watch them
    live, run `uv run pytest -o log_cli=true --log-cli-level=DEBUG`, or set `log_cli = true` and
    `log_cli_level = "INFO"` under `[tool.pytest.ini_options]`. Use `caplog` to assert on them, as
    `test_enable_csharp_logging` in the example file does.

!!! warning "Logs can contain sensitive data"
    C# messages include full process paths and working directories. Your own logging of element
    values can capture whatever is on screen. Treat log files like any other test artifact before
    uploading them from CI. See the [Security Policy](security.md#safe-usage-notes).

## Environment variables

FlaUI reads these settings **once, when it is first imported**, so set them before your first
`flaui` import. The `FLAUI_` prefix is required: a plain `BIN_HOME`, for example, is ignored.

| Variable | Default | What it does |
|----------|---------|--------------|
| `FLAUI_LOG_CSHARP` | off | Send C# FlaUI messages to the `flaui.csharp` logger (`1`, `true`, `yes`). |
| `FLAUI_LOG_CSHARP_LEVEL` | unset | Level for the `flaui.csharp` logger (`DEBUG`, `INFO`, ...). |
| `FLAUI_MAIN_WINDOW_TIMEOUT` | unset | How many milliseconds `get_main_window` waits (see [Timeouts](#timeouts)). |
| `FLAUI_BIN_HOME` | bundled `flaui/bin` | Load the FlaUI DLLs from another folder. Only use this to test a different FlaUI build; the bridge logs a warning when it is set. |
| `CI` | unset | When set (most CI services set it), the default main-window wait grows from 7 s to 20 s. |

In code, the same values are available as `flaui.lib.config.settings`.

## Timeouts

### Main-window wait

`automation.application.get_main_window(automation)` keeps polling until the application's main
window appears. It uses the first of these that is set:

1. `Automation(timeout=...)`, in milliseconds.
2. The `FLAUI_MAIN_WINDOW_TIMEOUT` environment variable, in milliseconds.
3. 7000 ms, or 20000 ms when `CI` is set.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_configuration.py:main_window_timeout"
    ```

=== "C#"

    ```csharp
    using var automation = new UIA3Automation();
    using var app = Application.Launch(path);
    var window = app.GetMainWindow(automation, TimeSpan.FromSeconds(15));
    ```

### UI Automation transaction and connection timeouts

The UIA3 automation object has two timeouts of its own. The **transaction** timeout limits how long
a single call to the target app may take; the default is 20 s. The **connection** timeout limits how
long connecting to the app may take; the default is 2 s. Both are .NET `TimeSpan` values. UIA2 does
not support them.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_configuration.py:uia_timeouts"
    ```

=== "C#"

    ```csharp
    var automation = new UIA3Automation();
    Console.WriteLine($"{automation.TransactionTimeout} {automation.ConnectionTimeout}");
    automation.TransactionTimeout = TimeSpan.FromSeconds(30);
    ```

### Units at a glance

Different APIs use different units, and C# uses `TimeSpan` everywhere:

| API | Unit |
|-----|------|
| `Retry.*(timeout=, interval=)` | milliseconds (int) |
| `Automation(timeout=)`, `FLAUI_MAIN_WINDOW_TIMEOUT`, `wait_while_main_handle_is_missing(time_out=)` | milliseconds (int) |
| `expect(el).to_*(timeout=)` | milliseconds (int) |
| `Wait.until_input_is_processed(...)`, `Wait.until_responsive(...)`, `Wait.while_cursor_is_busy(...)` | seconds (float) |
| `post_wait=` on input methods | `True` (~100 ms) or seconds (float) |
| `automation_base.transaction_timeout` / `connection_timeout` | .NET `TimeSpan` |

## Mouse speed

Real mouse movement (`Mouse.move_to`, `click(move_mouse=True)`, drag) is animated. These two class
settings are FlaUI's C# `Mouse` settings, so changing them takes effect immediately for every
following movement.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_configuration.py:mouse_speed"
    ```

=== "C#"

    ```csharp
    Mouse.MovePixelsPerMillisecond = 2.0;
    Mouse.MovePixelsPerStep = 10;
    ```
