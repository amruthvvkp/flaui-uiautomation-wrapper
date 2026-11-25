# Logging examples

Each script sets up logging one way, then runs the same short FlaUI session (`_demo.py`): launch
the bundled WPF app, set a text box, close the app. That makes it easy to compare what each sink
records. FlaUI's Python-side messages arrive on `flaui.*` loggers, and its C# messages on
`flaui.csharp`.

| Script | Logging library | Run it |
|--------|-----------------|--------|
| `stdlib_sink.py` | standard `logging` (`dictConfig`): console plus a C#-only file | `uv run python examples/logging/stdlib_sink.py` |
| `loguru_sink.py` | loguru via an intercept handler; C# messages to JSON lines | `uv run --with loguru python examples/logging/loguru_sink.py` |
| `structlog_sink.py` | structlog `ProcessorFormatter`; one JSON stream | `uv run --with structlog python examples/logging/structlog_sink.py` |

The scripts write `flaui-csharp.log` / `flaui-csharp.jsonl` to the current directory; both are
git-ignored. The docs' **Guide → Configuration & logging** page includes the setup sections of these
scripts directly.
