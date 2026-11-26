---
name: flaui-setup
description: Install FlaUI for Python (flaui-uiautomation-wrapper), initialise the PythonNet bridge in the right order, and choose UIA2 or UIA3. Use when starting Windows desktop UI automation in Python, when imports of FlaUI or C# types fail, or when deciding between the UIA2 and UIA3 backends.
---

# FlaUI for Python: setup

FlaUI for Python is a 1:1 PythonNet port of the C# FlaUI library for Windows UI Automation.
Python API names are the C# names in snake_case (`FindFirstDescendant` -> `find_first_descendant`).

## Requirements

- Windows with .NET Framework 4.8. UI Automation only exists on Windows.
- 64-bit CPython 3.11 to 3.15.

## Install

```bash
pip install flaui-uiautomation-wrapper
# or
uv add flaui-uiautomation-wrapper
```

The FlaUI DLLs ship inside the wheel (`flaui/bin/`). You do not install FlaUI separately.

## Rule 1: initialise the bridge before anything else

`setup_pythonnet_bridge()` loads the bundled FlaUI assemblies into the .NET runtime. Call it once,
at the top of your script or `conftest.py`, **before** importing any other `flaui` module or any
C# namespace (`FlaUI.*`, `System.*`). Otherwise those imports fail, typically with
`FileNotFoundException`, `TypeInitializationException` or `No module named 'FlaUI'`.

```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()  # must run before any C#-backed FlaUI import

from flaui.core.definitions import ControlType, ToggleState
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
```

Import sorters (isort, Ruff) will move the imports above the call and break this order. Fence the
block with `# isort: off` / `# isort: on`, as `examples/pytest/conftest.py` does.

## Launch, attach, dispose

`Automation` is the entry point. It owns the C# automation object, a condition factory (`cf`) and an
`Application` (`automation.application`). Used as a context manager, it disposes the automation and
closes the application on exit.

```python
# `with` disposes the automation and closes the application on exit.
with Automation(uia) as automation:
    automation.application.launch(executable)
    automation.application.wait_while_main_handle_is_missing(3000)
    window = automation.application.get_main_window(automation)
    cf = automation.cf
    print(f"Launched: {window.title}")
```

To drive an app that is already running, call `automation.application.attach("app.exe")` with a
process name or PID. `attach_or_launch()` attaches when the process exists and launches it
otherwise. For several copies of one app, give each its own `flaui.core.application.Application`
object (see `examples/pytest/test_multi_instance.py`).

## UIA2 or UIA3

Pick the backend with `UIAutomationTypes` when constructing `Automation`.

| Backend | Use it for |
|---------|------------|
| `UIAutomationTypes.UIA3` | The default. WPF, Store/UWP apps, modern Win32. Faster, richer patterns. |
| `UIAutomationTypes.UIA2` | Legacy WinForms apps where UIA3 misreports the tree. |

- One `Automation` instance uses one backend. Do not mix UIA2 and UIA3 in one process; use separate
  processes if you need both.
- `automation.automation_base` is the typed Python facade (`UIA2Automation` / `UIA3Automation`).
  `automation.cs_automation` is the raw C# object, for interop only.

## Units

FlaUI timeouts are in **milliseconds**, as in C#: `Retry.*(timeout=...)`,
`Automation(timeout=...)`, `wait_while_main_handle_is_missing(...)`. The one exception is
`post_wait`, where a float means **seconds**.

## Next

- Finding and driving controls: the `flaui-find-and-act` skill.
- Writing tests: the `flaui-write-tests` skill.
- Guide: https://amruthvvkp.github.io/flaui-uiautomation-wrapper/latest/basics/
- Runnable script: `examples/scripts/quickstart.py` in the repository.
