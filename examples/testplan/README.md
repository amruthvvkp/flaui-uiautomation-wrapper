# Testplan example (#49)

A [Testplan](https://testplan.readthedocs.io/) example that automates the bundled WPF test
application with a `MultiTest` / `@testsuite` / `@testcase` structure.

## Install + run

`testplan` is not a project dependency — install it first:

```bash
uv pip install testplan
uv run python examples/testplan/test_plan.py
```

Testplan writes a structured report to the console (and can emit PDF/JSON reports with extra flags —
see the Testplan docs).

## What's here

| Piece | Purpose |
|-------|---------|
| `_find_test_app()` | Locates the bundled `WpfApplication.exe`. |
| `SimpleControlsSuite.setup` / `teardown` | Launch and dispose the application around the test cases. |
| `@testcase` methods | `window_title`, `enter_text`, `toggle_checkbox` — using `result.equal` / `result.not_equal` assertions. |
| `@test_plan main(plan)` | Assembles a single `MultiTest` and is the script entry point. |

## Key ideas

- **Bridge first.** The script calls `setup_pythonnet_bridge()` at import time, before any C#-backed
  FlaUI type is used.
- **Launch in `setup`, dispose in `teardown`.** The application lifecycle is tied to the suite, and
  the checkbox case restores its original state.
- **Testplan assertions.** Interactions use the same Find → wrap → act pattern; results are recorded
  via the `result` collector rather than bare `assert`.
