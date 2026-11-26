---
name: flaui-debug-flaky
description: Diagnose failing, flaky or slow FlaUI for Python automation on Windows. Covers bridge and DLL load errors, ElementNotFound, timing races, focus and foreground problems, known platform limitations (WinForms ComboBox, lazy tree items, Windows 11 Notepad and Paint), C# logging and failure screenshots. Use when a FlaUI script or test errors, passes only sometimes, or runs slowly.
---

# FlaUI for Python: debug failing and flaky automation

Work through the sections in order. Most failures are setup, locator or timing problems, not
FlaUI bugs.

## 1. Import and load errors

| Symptom | Cause and fix |
|---------|---------------|
| `FileNotFoundException`, `TypeInitializationException` or `No module named 'FlaUI'` on import | `setup_pythonnet_bridge()` did not run first. Call it before any other `flaui` or C# import, and stop import sorters from reordering it. |
| `No module named 'clr'` | `pythonnet` is missing from this interpreter. Install into the same environment you run. |
| `module 'clr' has no attribute 'AddReference'` | The unrelated PyPI package `clr` shadows PythonNet. Uninstall it, then reinstall `pythonnet`. |
| `Failed to create a .NET runtime (coreclr)` | `PYTHONNET_RUNTIME` is set to `coreclr` or `mono`. The bundled DLLs need .NET Framework 4.8: unset it. |
| `FileLoadException ... HRESULT: 0x80131515` | DLLs blocked by Mark of the Web, or the venv lives on a network drive. `Unblock-File` the `flaui/bin` folder, or reinstall with pip on a local disk. |
| A DLL missing from `flaui/bin` | Antivirus quarantine. Reinstall with `--force-reinstall --no-deps` and get the folder allow-listed. |

The quick environment check is in the troubleshooting guide (link at the end).

## 2. ElementNotFound

`find_first_*` raises `flaui.lib.exceptions.ElementNotFound` when nothing matches.

1. Check the locator with FlaUInspect or Accessibility Insights. AutomationIds are case-sensitive,
   and `Name` is localised.
2. Check the search root. A child search (`find_first_child`) does not see grandchildren, and a
   search from the wrong window or tab page finds nothing.
3. If the element appears later (a dialog, a lazily loaded page), wait for it with
   `Retry.WhileException(lambda: ..., timeout=5000, throw_on_timeout=True)` instead of searching
   once.
4. Check the backend. Some properties and controls differ between UIA2 and UIA3. For example,
   `IsPassword` is not exposed through XPath on UIA2 + WinForms.

## 3. Flaky: passes sometimes

- **Race with the UI.** Assert with `Retry.WhileFalse(lambda: ..., timeout=...)` or
  `expect(element).to_have_text(...)`, not a single read straight after an action.
- **Lazily realised items.** WPF creates tree, list and menu items only after their parent expands
  or scrolls into view. After `expand()`, wait for the children, for example
  `Retry.WhileFalse(lambda: len(item.items) >= count, timeout=5000, interval=100)`.
- **Focus and foreground.** Drop-downs, context menus and keyboard input go to the foreground
  window. Call `window.set_foreground()` before them, and do not run two UI suites on one desktop.
- **Leftover state.** A shared, session-scoped app keeps the last test's selection, text and toggles.
  Reset state at the start of each test or restore it in `finally`.
- **Real mouse input.** Prefer patterns (`invoke()`, `toggle()`, `select()`, `text = ...`). When the
  mouse is needed, pass `post_wait` (`True`, or a float of seconds). Mouse position reads can lag on
  CI runners.
- **Retry tuning.** Use small intervals (50 to 100 ms) with a bounded timeout. Timeouts are in
  milliseconds.

## 4. Known platform limitations

These are Windows or .NET limitations, not bugs to work around in your test:

- **WinForms ComboBox** is broken through UI Automation on both UIA2 and UIA3: `items` comes back
  empty and selecting raises. Upstream FlaUI skips these tests too. WPF ComboBox works.
- **Windows 11 Notepad** is a Store app with a different tree from classic Notepad.
- **Windows 11 Paint** changed its UI structure. Native UIA/COM failures there can abort the Python
  process outright.
- **Do not mix UIA2 and UIA3 in one process.** Use separate processes.
- **32-bit Python** is untested and cannot fully inspect 64-bit processes. Use 64-bit CPython.

## 5. See what FlaUI is doing

Send FlaUI's own C# log messages to Python logging, then show them live in pytest with
`-o log_cli=true --log-cli-level=DEBUG`. Setting `FLAUI_LOG_CSHARP=1` in the environment does the
same without code.

```python
from flaui.core.logging import enable_csharp_logging

enable_csharp_logging()  # C# FlaUI -> logging.getLogger("flaui.csharp")
# or forward into a logger of your own, at a level of your choosing:
enable_csharp_logging(logger=logging.getLogger("myapp.flaui"), level="INFO")
```

- `element.draw_highlight()` flashes a red frame around the element you actually found.
- `element.capture_to_file("found.png")` saves an image of one element. `Capture.main_screen()`
  (from `flaui.core.capturing`) grabs the whole screen. Hook it into pytest failures as in
  `examples/pytest/conftest.py`.
- If `get_main_window` gives up on a slow machine, raise its wait with `Automation(timeout=...)` or
  `FLAUI_MAIN_WINDOW_TIMEOUT` (milliseconds).

## 6. Slow

- Search from the nearest container, not the window or desktop. Prefer `find_first_child` when
  the element is a direct child.
- Prefer patterns to mouse clicks.
- Read many properties of many elements inside a `CacheRequest`, which fetches them in one round
  trip.

Full guide: https://amruthvvkp.github.io/flaui-uiautomation-wrapper/latest/troubleshooting/
