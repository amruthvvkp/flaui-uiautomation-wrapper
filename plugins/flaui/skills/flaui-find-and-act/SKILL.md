---
name: flaui-find-and-act
description: Find Windows UI elements and act on them with FlaUI for Python. Covers the ConditionFactory, find scopes, XPath, typed as_* conversion, UIA patterns versus real mouse input, post_wait and Retry. Use when locating a control, clicking, typing, toggling or selecting in a desktop app, or waiting for UI to appear.
---

# FlaUI for Python: find elements and act on them

This skill assumes the bridge is initialised and you hold a `window` and `cf = automation.cf`
(see the `flaui-setup` skill).

## 1. Find

Build conditions with the `ConditionFactory` (`automation.cf`, or `window.condition_factory`).
Prefer them in this order:

1. `cf.by_automation_id("...")`: stable and not localised. **Use it whenever the control has one.**
2. `cf.by_name("...")`: the visible text, which changes with the UI language.
3. `cf.by_control_type(ControlType.X)`: usually combined with another condition.

Others: `by_class_name`, `by_text`, `by_value`, `by_help_text`, `by_framework_id`, `by_process_id`.

```python
text_box = window.find_first_descendant(cf.by_automation_id("TextBox"))  # by AutomationId (preferred)
checkbox = window.find_first_descendant(cf.by_name("Test Checkbox"))  # by Name (visible text)
buttons = window.find_all_descendants(cf.by_control_type(ControlType.Button))  # by ControlType
```

Combine conditions with `And`, `Or` and `Not` (capitalised, as in C#):

```python
# AND: a Button whose AutomationId is "InvokableButton"
invoke = cf.by_control_type(ControlType.Button).And(cf.by_automation_id("InvokableButton"))

# OR: either radio button
radios = cf.by_automation_id("RadioButton1").Or(cf.by_automation_id("RadioButton2"))

# NOT: "x.Not(y)" means x AND NOT y -- every check box except the three-state one
two_state = cf.by_control_type(ControlType.CheckBox).Not(cf.by_automation_id("ThreeStateCheckBox"))
```

### Scope

| Method | Searches |
|--------|----------|
| `find_first_child` / `find_all_children` | Direct children only (cheap). |
| `find_first_descendant` / `find_all_descendants` | The whole subtree (slow from a big window or the desktop). |
| `find_first_by_x_path` / `find_all_by_x_path` | XPath over control types and properties. |
| `find_first(tree_scope, condition)` / `find_all(...)` | An explicit `TreeScope`. |

- Narrow the search: find a container first, then search inside it. Descendant searches from the
  desktop or a large window are the main cause of slow tests.
- `find_first_*` raises `flaui.lib.exceptions.ElementNotFound` when nothing matches. It never
  returns `None`. `find_all_*` returns an empty collection.

XPath helps with hierarchies that conditions express badly:

```python
button = window.find_first_by_x_path("//Button[@AutomationId='InvokableButton']").as_button()
tabs = window.find_all_by_x_path("//Tab/TabItem")  # every tab page
checkbox = window.find_first_by_x_path("//CheckBox[@Name='Test Checkbox']").as_check_box()
```

## 2. Convert to the typed element

`find_*` returns a generic `AutomationElement`. Convert it with an `as_*` helper (`as_button`,
`as_check_box`, `as_text_box`, `as_combo_box`, `as_list_box`, `as_tree`, `as_grid`, `as_tab`,
`as_slider`, `as_window`, ...) to reach that control's API.

## 3. Act: prefer patterns over the mouse

Pattern calls (`invoke()`, `toggle()`, `select()`, `text = ...`) talk to UI Automation directly.
They are fast, leave the cursor alone and work while the window is in the background. Use real
mouse input (`click()`, `flaui.core.input.Mouse`) only when no pattern fits.

```python
button = window.find_first_descendant(cf.by_automation_id("InvokableButton")).as_button()
button.invoke()  # Invoke pattern: no mouse movement, works when the window is in the background
```

```python
text_box = window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
text_box.text = "hello"  # Value pattern: sets the text directly
text_box.enter(" world")  # Keyboard: types into the focused box
```

```python
combo = window.find_first_descendant(cf.by_automation_id("NonEditableCombo")).as_combo_box()
combo.select("Item 2")  # or combo.select(1)
selected = combo.selected_item.text
```

## 4. post_wait after real input

Input methods (every `Mouse` method, `AutomationElement.click`, `TextBox.enter`,
`Tab.select_tab_item`) accept `post_wait`. `True` waits about 100 ms for input to be processed, a
float waits that many **seconds**, and a callable is called. Use it instead of `time.sleep()`.

```python
from flaui.core.input import Mouse

text_box = window.find_first_descendant(cf.by_automation_id("TextBox"))
Mouse.click(text_box.get_clickable_point(), post_wait=True)  # ~100 ms
text_box.as_text_box().enter("typed", post_wait=0.25)  # 250 ms
```

## 5. Wait for UI with Retry

`flaui.core.tools.Retry` polls, with C#-style method names. Timeouts and intervals are in
**milliseconds**. Use `WhileException` for lookups, because they raise until the element exists.

```python
from flaui.core.tools import Retry

# Keep trying while the lookup raises ElementNotFound; give up after 5 s.
button = Retry.WhileException(
    lambda: window.find_first_descendant(cf.by_automation_id("InvokableButton")),
    timeout=5000,
    interval=100,
    throw_on_timeout=True,
).as_button()

# Or wait for a predicate to become true.
ready = Retry.WhileFalse(lambda: button.is_enabled, timeout=2000)
```

Also available: `While`, `WhileNot`, `WhileTrue`, `WhileNull`, `WhileNotNull`, `WhileEmpty`.

## Unknown apps

Read AutomationIds, names and control types with FlaUInspect or Accessibility Insights for Windows
before writing locators. Do not guess them.

One recipe per control: https://amruthvvkp.github.io/flaui-uiautomation-wrapper/latest/examples/element-cookbook/
