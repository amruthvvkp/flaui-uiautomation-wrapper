# FlaUI for Python — runnable examples

This directory holds **self-contained, runnable** examples. They are intentionally kept **outside**
the main `tests/` tree, so the project's own test run (`testpaths = ["tests/"]`) never picks them up.
The documentation site includes its Python snippets **directly from these files**, so every
snippet in the docs is code that runs.

| Folder | What it is | Run it |
|--------|------------|--------|
| [`pytest/`](pytest/) | pytest suite, plus the *Element Cookbook* and *Advanced* recipes | `uv run pytest examples/pytest` |
| [`unittest/`](unittest/) | Standard-library `unittest` suite | `uv run python -m unittest discover -s examples/unittest` |
| [`behave/`](behave/) | BDD / Gherkin suite | `uv run behave examples/behave/features` |
| [`testplan/`](testplan/) | Testplan multitest | `uv run python examples/testplan/test_plan.py` |
| [`logging/`](logging/) | Sending FlaUI's Python and C# logs to stdlib `logging`, loguru or structlog | `uv run --with loguru python examples/logging/loguru_sink.py` |
| [`scripts/`](scripts/) | Gallery: plain scripts for the bundled apps, Calculator and Notepad | `uv run python examples/scripts/quickstart.py` |

The framework suites all drive the same controls on the **Simple Controls** tab of the bundled WPF
test application (`test_applications/WPFApplication/WpfApplication.exe`), so you can compare the
frameworks side by side.

> **Snippet markers.** The `# --8<-- [start:name]` / `# --8<-- [end:name]` comments mark the sections the docs include.
> Keep them when you edit a file. The strict docs build fails if a referenced section disappears.

## Prerequisites

- **Windows** (UI Automation is a Windows technology).
- The bundled WPF test application, which ships in this repository under `test_applications/`. The
  helpers in each suite locate it automatically by walking up from the example file.
- [`uv`](https://docs.astral.sh/uv/) for running commands in the project environment.

`pytest` is already a project dependency. `behave` and `testplan` are **not** — install them into the
environment before running those suites:

```bash
uv pip install behave      # for examples/behave
uv pip install testplan    # for examples/testplan
```

## The one rule that matters

Always call `setup_pythonnet_bridge()` **before** importing or using any C#-backed FlaUI type. Each
suite does this at import time in its setup module (`conftest.py`, `environment.py`, or the script
entry point). See the [project docs](https://amruthvvkp.github.io/flaui-uiautomation-wrapper/) for
the full API reference.
