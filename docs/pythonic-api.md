# Pythonic API

Beyond the 1:1 FlaUI surface, the wrapper adds a few ergonomic, Python-native conveniences so tests
read naturally and clean up after themselves. These are additive — the underlying FlaUI methods are
unchanged.

## Context managers

`Application` and the high-level `Automation` both support the `with` statement and dispose
themselves on exit (graceful close, then dispose), so you never leak processes or COM objects:

```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
setup_pythonnet_bridge()

from flaui.modules.automation import Automation
from flaui.lib.enums import UIAutomationTypes

with Automation(UIAutomationTypes.UIA3) as automation:
    app = automation.application.launch("notepad.exe")
    main_window = app.get_main_window(automation)
    ...
# automation is disposed and the app is closed automatically here
```

`__exit__` never raises: cleanup failures are swallowed so they cannot mask an error from inside the
block.

## Element collections

The `find_all_*` methods return an `AutomationElementCollection`. It **is** a `list` (indexing,
slicing, `len`, iteration all work exactly as before), with a few helpers added:

```python
buttons = main_window.find_all_descendants()

buttons.first              # first element, or None if empty
buttons.filter(lambda e: e.is_enabled)        # -> AutomationElementCollection
buttons.where(name="OK")                       # match by attribute equality
for element in buttons:                          # still a plain list under the hood
    print(element)
```

`where(...)` treats a missing/unreadable attribute as a non-match (it never raises), so it is safe
across heterogeneous results.

## Fluent assertions: `expect(...)`

`expect(element)` provides Playwright-style, auto-waiting assertions. Each matcher polls the element
until the condition holds or the timeout elapses, then raises `AssertionError` with a clear message:

```python
from flaui.core.expectations import expect

expect(ok_button).to_be_visible()
expect(ok_button).to_be_enabled(timeout=2000)   # per-call timeout (ms)
expect(checkbox).to_be_checked()
expect(label).to_have_text("Done")
expect(field).to_have_value("42")

expect(spinner).not_.to_be_visible(timeout=2000)  # negate any matcher with .not_
```

Available matchers: `to_be_visible`, `to_be_enabled`, `to_be_offscreen`, `to_be_checked`,
`to_have_name`, `to_have_text`, `to_have_value` — each with an optional `timeout` (milliseconds) and
a `.not_` negation. Polling is built on the existing [`Retry`](api/retry.md) helper, so timeouts and
intervals behave consistently with the rest of the library (`expect(el, timeout=5000, interval=100)`).
