# pytest example (#50)

A small, realistic pytest suite that automates the bundled WPF test application.

## Run it

```bash
uv run pytest examples/pytest -v
```

(`pytest` ships with the project, so there is nothing extra to install.)

## What's here

| File | Purpose |
|------|---------|
| `conftest.py` | Initialises the PythonNet bridge, then provides session/function fixtures: `automation` (launches the app once), `main_window`, and `condition_factory`. |
| `test_simple_controls.py` | Five tests: window title, text entry, button invoke, checkbox toggle (with restore), and reading the slider value. |

## Key ideas

- **Initialise the bridge first.** `conftest.py` calls `setup_pythonnet_bridge()` before importing
  any C#-backed FlaUI type.
- **Launch once per session.** The `automation` fixture is `scope="session"` and kills/disposes the
  app in its teardown.
- **Find → wrap → act.** Locate an element with the `condition_factory`, convert it with an `as_*`
  helper (`as_text_box()`, `as_button()`, …), then call typed methods/properties.
- **Leave shared state clean.** Because the app is shared, the checkbox test restores the original
  state in a `finally` block.
