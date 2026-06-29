# Behave (BDD) example (#48)

A behavior-driven example that automates the bundled WPF test application with Gherkin scenarios.

## Install + run

`behave` is not a project dependency — install it first:

```bash
uv pip install behave
uv run behave examples/behave/features
```

## What's here

| File | Purpose |
|------|---------|
| `features/simple_controls.feature` | Three Gherkin scenarios: title check, text entry, checkbox toggle. |
| `features/environment.py` | `before_all` initialises the PythonNet bridge, launches the app, and stores `context.window` / `context.cf`; `after_all` disposes them. |
| `features/steps/simple_controls_steps.py` | The `@given` / `@when` / `@then` step implementations. |

## Key ideas

- **Bridge first.** `environment.py` calls `setup_pythonnet_bridge()` at import time, before any
  C#-backed FlaUI type is used and before behave loads the step modules.
- **Launch once.** The application is launched in `before_all` and shared across scenarios, so steps
  that change state (the checkbox) restore it afterwards.
- **Same Find → wrap → act pattern** as the pytest example, expressed through Gherkin steps.
