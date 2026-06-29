# FlaUI for Python — runnable examples

This directory holds **self-contained, runnable** example suites that automate the bundled WPF test
application (`test_applications/WPFApplication/WpfApplication.exe`) with three popular Python test
frameworks. They are intentionally kept **outside** the main `tests/` tree, so they are never picked
up by the project's own test run (`testpaths = ["tests/"]`).

Each suite drives the same handful of controls on the **Simple Controls** tab, so you can compare
the frameworks side by side:

| Framework | Folder | Run it | When to reach for it |
|-----------|--------|--------|----------------------|
| **pytest** | [`pytest/`](pytest/) | `uv run pytest examples/pytest` | The default. Fixtures, parametrization, the richest plugin ecosystem. |
| **behave** | [`behave/`](behave/) | `uv run behave examples/behave/features` | BDD / Gherkin — when non-engineers read or own the specs. |
| **Testplan** | [`testplan/`](testplan/) | `uv run python examples/testplan/test_plan.py` | Large, structured test campaigns with rich reporting. |

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
