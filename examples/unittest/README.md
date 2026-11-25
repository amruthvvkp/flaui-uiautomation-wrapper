# unittest example

A standard-library-only example that automates the bundled WPF test application.

## Run

```bash
uv run python -m unittest discover -s examples/unittest -v
```

Nothing extra to install. `unittest` ships with Python.

## Key ideas

- **Bridge first.** `setup_pythonnet_bridge()` runs at import time, before any C#-backed FlaUI type.
- **Launch once per class.** `setUpClass` launches the app; `tearDownClass` kills it and disposes
  the automation.
- **Restore shared state** with `addCleanup`, because every test in the class uses the same app.
