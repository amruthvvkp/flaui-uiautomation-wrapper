# UIA2 vs UIA3

FlaUI targets two Windows UI Automation client stacks: **UIA2** (`System.Windows.Automation`) and **UIA3** (`IUIAutomation` via COM). This package ships both C# assemblies and exposes them through Python.

## Choosing a stack

Use the same entry point as today: construct [`flaui.modules.automation.Automation`](api/automation.md) with `UIAutomationTypes` from `flaui.lib.enums`.

```python
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation

auto_uia3 = Automation(UIAutomationTypes.UIA3)  # default-style modern stack
auto_uia2 = Automation(UIAutomationTypes.UIA2)  # legacy WPF/.NET scenarios
```

- **UIA3** is the usual choice on current Windows builds (richer patterns, better coverage for many apps).
- **UIA2** can behave differently for some WinForms/WPF trees; the pytest matrix still runs both because parity and bugs vary by combination.

## Python facades vs raw C#

Phase 1 adds Python types that mirror `FlaUI.Core.AutomationBase` and the concrete `FlaUI.UIA2` / `FlaUI.UIA3` automation classes:

| Attribute | Purpose |
|-----------|---------|
| `automation.automation_base` | Preferred typed API: [`AutomationBase`](api/automation_base.md) subclass (`UIA2Automation` or `UIA3Automation` from `flaui.uia2` / `flaui.uia3`). |
| `automation.cs_automation` | Raw C# instance for interop, libraries, and code that expects `FlaUI.UIA2.UIA2Automation` / `FlaUI.UIA3.UIA3Automation` (backward compatible). |

[`AutomationElement.automation`](api/automation_element.md) returns the same Python facade via `wrap_cs_automation`, so element trees and high-level `Automation` stay consistent.

## Process and mixing stacks

Upstream guidance: **do not mix UIA2 and UIA3 in one process** in unsupported ways. A single [`Automation`](api/automation.md) instance uses one stack; use separate OS processes if you truly need both stacks at once.

## Further reading

- API: [`AutomationBase`](api/automation_base.md), [`Automation`](api/automation.md)
- Tracking issue for this work: [GitHub #107](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/107)
