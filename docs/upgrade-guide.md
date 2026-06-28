# Upgrade guide

This guide is for anyone coming from the **old 0.x release on PyPI** (published several years ago)
to the modern **1.x** line.

!!! warning "0.x → 1.x is not a drop-in upgrade"
    The old 0.x package was a thin, experimental wrapper. The 1.x line is effectively a ground-up
    rewrite with a different, fully typed API surface. Treat this as **re-onboarding**, not a
    version bump. Read [Basics](basics.md) once after upgrading — it is short and covers the new
    canonical workflow end to end.

## What changed at a glance

| Area | 0.x (old) | 1.x (new) |
|------|-----------|-----------|
| Python support | 3.8-era | **3.10–3.14** |
| API surface | thin, partial | **1:1 FlaUI parity** (elements, patterns, events, capturing) |
| Types | minimal | **Pydantic models** end to end, IDE autocomplete |
| Methods | mixed | **snake_case**, mirroring the C# API |
| Returns | raw values | Python **enums**, wrapped types (`Rectangle`, `Point`, …) |
| Errors | raw .NET exceptions | translated **Python exception hierarchy** |
| UIA2/UIA3 | ad hoc | explicit `AutomationBase` facades |

## Before you upgrade

1. **Check your Python version.** 1.x requires Python **3.10+**. Upgrade your interpreter first if
   you are on 3.8/3.9.
2. **Pin your old version** while you migrate, so existing scripts keep working:
   ```bash
   pip install "flaui-uiautomation-wrapper<1"
   ```
3. Migrate in a branch/virtualenv, then switch over.

## Installing 1.x

=== "Stable"

    ```bash
    pip install --upgrade flaui-uiautomation-wrapper
    ```

=== "Beta (pre-release)"

    ```bash
    pip install --pre --upgrade flaui-uiautomation-wrapper
    ```

While 1.0 is in beta, use the pre-release channel — see [Road to v1.0](release-plan.md#testing-a-beta-release).

## The new canonical workflow

Initialize the PythonNet bridge **before** importing any C#-backed modules, then drive everything
through the high-level `Automation` entry point:

```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
setup_pythonnet_bridge()  # must run first

from flaui.modules.automation import Automation
from flaui.lib.enums import UIAutomationTypes

automation = Automation(UIAutomationTypes.UIA3)
app = automation.application.launch("notepad.exe")
main_window = app.get_main_window(automation)
main_window.find_first_by_x_path("//Button[@Name='OK']").as_button().invoke()
```

New in 1.x and worth adopting:

- **Context managers** — `with Automation(UIAutomationTypes.UIA3) as automation:` disposes the
  automation and closes the app automatically.
- **Typed results** — properties return enums (e.g. `ToggleState.On`) and wrapped geometry types,
  not bare strings/ints. Assert against enums, not strings.
- **Condition factory & XPath** — flexible search via `ConditionFactory` or `find_*_by_x_path`.

## Migration checklist

- [ ] Move to Python 3.10+.
- [ ] Add `setup_pythonnet_bridge()` as the first import-time call.
- [ ] Replace old entry points with `flaui.modules.automation.Automation`.
- [ ] Convert any PascalCase calls to **snake_case** (`Click()` → `click()`).
- [ ] Update assertions to compare against **enums** and wrapped types.
- [ ] Catch the new [Python exceptions](api/exceptions.md) instead of raw .NET errors.
- [ ] Re-run against [Basics](basics.md) to confirm the flow.

## Need the old docs?

Once documentation [versioning](release-plan.md#documentation-versioning) is live, pick the matching
version from the selector in the header. The **`stable`** alias always points at the latest
released version; **`latest`** tracks `master`.
