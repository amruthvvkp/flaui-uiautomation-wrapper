# Upgrade guide

This guide covers the two ways people arrive at **FlaUI for Python 1.x**:

- **[Upgrading from 0.x](#upgrading-from-0x)**: you used the old 0.x release on PyPI, published
  several years ago.
- **[Migrating from FlaUI C#](#migrating-from-flaui-c)**: you have FlaUI tests or tools in C# and
  want to move them, or write new ones, in Python.

## Upgrading from 0.x

!!! warning "0.x → 1.x is not a drop-in upgrade"
    The old 0.x package was a thin, experimental wrapper. The 1.x line is effectively a ground-up
    rewrite with a different, fully typed API surface. Treat this as **re-onboarding**, not a
    version bump. Read [Basics](basics.md) once after upgrading — it is short and covers the new
    canonical workflow end to end.

### What changed at a glance

| Area | 0.x (old) | 1.x (new) |
|------|-----------|-----------|
| Python support | 3.8-era | **3.11–3.15** |
| API surface | thin, partial | **1:1 FlaUI parity** (elements, patterns, events, capturing) |
| Types | minimal | **Pydantic models** end to end, IDE autocomplete |
| Methods | mixed | **snake_case**, mirroring the C# API |
| Returns | raw values | Python **enums**, wrapped types (`Rectangle`, `Point`, …) |
| Errors | raw .NET exceptions | translated **Python exception hierarchy** |
| UIA2/UIA3 | ad hoc | explicit `AutomationBase` facades |

### Before you upgrade

1. **Check your Python version.** 1.x requires Python **3.11+**. Upgrade your interpreter first if
   you are on 3.10 or older.
2. **Pin your old version** while you migrate, so existing scripts keep working:
   ```bash
   pip install "flaui-uiautomation-wrapper<1"
   ```
3. Migrate in a branch/virtualenv, then switch over.

### Installing 1.x

=== "Stable"

    ```bash
    pip install --upgrade flaui-uiautomation-wrapper
    ```

=== "Beta (pre-release)"

    ```bash
    pip install --pre --upgrade flaui-uiautomation-wrapper
    ```

While 1.0 is in beta, use the pre-release channel — see [Road to v1.0](release-plan.md#testing-a-beta-release).

### The new canonical workflow

Initialize the PythonNet bridge **before** importing any C#-backed modules, then drive everything
through the high-level `Automation` entry point:

```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
setup_pythonnet_bridge()  # must run first

from flaui.modules.automation import Automation
from flaui.lib.enums import UIAutomationTypes

with Automation(UIAutomationTypes.UIA3) as automation:
    automation.application.launch("notepad.exe")
    main_window = automation.application.get_main_window(automation)
    main_window.find_first_by_x_path("//Button[@Name='OK']").as_button().invoke()
```

New in 1.x and worth adopting:

- **Context managers** — `with Automation(UIAutomationTypes.UIA3) as automation:` disposes the
  automation and closes the app automatically.
- **Typed results** — properties return enums (e.g. `ToggleState.On`) and wrapped geometry types,
  not bare strings/ints. Assert against enums, not strings.
- **Condition factory & XPath** — flexible search via `ConditionFactory` or `find_*_by_x_path`.

### Migration checklist

- [ ] Move to Python 3.11+.
- [ ] Add `setup_pythonnet_bridge()` as the first import-time call.
- [ ] Replace old entry points with `flaui.modules.automation.Automation`.
- [ ] Convert any PascalCase calls to **snake_case** (`Click()` → `click()`).
- [ ] Update assertions to compare against **enums** and wrapped types.
- [ ] Catch the new [Python exceptions](api/exceptions.md) instead of raw .NET errors.
- [ ] Re-run against [Basics](basics.md) to confirm the flow.

## Migrating from FlaUI C#

The Python API is a **1:1 port** of FlaUI. Class names, the element hierarchy, and the
find → convert → act workflow are all the same, so most C# code translates line by line. The docs
show the C# next to the Python in tabs throughout. Start with [Basics](basics.md) and the
[Element Cookbook](examples/element-cookbook.md), and keep the
[C# Parity Map](parity.md) open for anything not covered here.

### Side by side

=== "Python"

    ```python
    from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

    setup_pythonnet_bridge()  # 1. load the FlaUI assemblies first

    from flaui.lib.enums import UIAutomationTypes
    from flaui.modules.automation import Automation

    with Automation(UIAutomationTypes.UIA3) as automation:  # 2. `with` replaces `using`
        automation.application.launch(r"C:\path\to\App.exe")
        window = automation.application.get_main_window(automation)
        cf = automation.cf

        text_box = window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
        text_box.text = "hello"  # 3. PascalCase -> snake_case, properties stay properties
    ```

=== "C#"

    ```csharp
    using FlaUI.Core;
    using FlaUI.UIA3;

    using var automation = new UIA3Automation();
    using var app = Application.Launch(@"C:\path\to\App.exe");
    var window = app.GetMainWindow(automation);
    var cf = automation.ConditionFactory;

    var textBox = window.FindFirstDescendant(cf.ByAutomationId("TextBox")).AsTextBox();
    textBox.Text = "hello";
    ```

### Translation table

| C# FlaUI | FlaUI for Python | Notes |
|----------|------------------|-------|
| `using FlaUI.UIA3;` | `setup_pythonnet_bridge()`, then `from flaui... import ...` | The bridge call must come before any C#-backed import. |
| `new UIA3Automation()` / `new UIA2Automation()` | `Automation(UIAutomationTypes.UIA3)` / `UIA2` | `automation.automation_base` is the typed facade; `automation.cs_automation` is the raw C# object. |
| `Application.Launch(path)` → `app` | `automation.application.launch(path)` | Returns `None`. The application lives on `automation.application`. |
| `Application.LaunchStoreApp(aumid)` | `automation.application.launch_store_app(aumid)` | |
| `Application.Attach(name)` | `automation.application.attach(name)` | |
| `app.GetMainWindow(automation)` | `automation.application.get_main_window(automation)` | |
| `automation.ConditionFactory` | `automation.cf` | |
| `FindFirstDescendant(cf => cf.ByName("OK"))` | `find_first_descendant(cf.by_name("OK"))` | Pass a condition, not a lambda. |
| `FindFirst…` returns `null` | raises `ElementNotFound` | Poll with `Retry.WhileException` instead of `Retry.WhileNull`. |
| `FindAll…` returns `AutomationElement[]` | returns `AutomationElementCollection` (a `list`) | Adds `.first`, `.filter`, `.where`. |
| `.AsButton()`, `.AsTextBox()`, … | `.as_button()`, `.as_text_box()`, … | |
| `element.Name`, `checkBox.ToggleState` | `element.name`, `check_box.toggle_state` | Properties stay properties, renamed to snake_case. |
| `button.Invoke()`, `tab.SelectTabItem(1)` | `button.invoke()`, `tab.select_tab_item(1)` | Methods stay methods, renamed to snake_case. |
| `a.And(b)`, `a.Or(b)`, `a.Not()` | `a & b`, `a \| b`, `~a` (or `a.and_(b)`, `a.or_(b)`, `a.not_()`) | The C# names still work as aliases. The legacy `a.Not(b)` means *a AND NOT b* (`a & ~b`). |
| `TrueCondition.Default`, `FalseCondition.Default` | `ConditionFactory.true_condition()`, `ConditionFactory.false_condition()` | Also `TrueCondition.default()` / `FalseCondition.default()`. |
| `TimeSpan.FromSeconds(5)` | `5000` (int milliseconds) | Applies to `Retry` and `timeout=` arguments. |
| `Retry.WhileNull(...).Result` | `Retry.WhileNull(...)` | Python returns the value directly. |
| `Click(); Wait.UntilInputIsProcessed();` | `click(post_wait=True)` | `post_wait` is a Python addition. |
| `ToggleState.On`, `ControlType.Button` | `ToggleState.On`, `ControlType.Button` | Same enum names, from `flaui.core.definitions`. |
| .NET exceptions | [Python exceptions](api/exceptions.md) | e.g. `PatternNotSupportedException`, `ElementNotFound`. |
| `using (cacheRequest.Activate())` | `with cache_request.activate():` | |

### What Python adds

These have no direct C# equivalent:

- **`post_wait=`** on input methods, so you don't need a separate wait call after a click.
- **`expect(element)`**: auto-waiting assertions, e.g. `expect(button).to_be_enabled()`. See
  [Pythonic API](pythonic-api.md#fluent-assertions-expect).
- **Collection helpers** on `find_all_*` results.
- **Pydantic models and type hints** throughout, so your IDE autocompletes the API.

### Escape hatch

Anything not yet wrapped is still reachable. Every Python element exposes the underlying C# object
as `.raw_element`, and `automation.cs_automation` is the C# automation. You can call FlaUI
directly through PythonNet, then wrap the result back with
`AutomationElement(raw_element=...)`. If you find yourself needing this, please
[open an issue](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues) so the gap can be
closed.

## Need the old docs?

Once documentation [versioning](release-plan.md#documentation-versioning) is live, pick the matching
version from the selector in the header. The **`stable`** alias always points at the latest
released version; **`latest`** tracks `master`.
