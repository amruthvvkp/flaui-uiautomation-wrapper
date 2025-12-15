# Advanced Usage Guide

This guide covers advanced scenarios for using the FlaUI Python port, including backend selection, element patterns, custom automation flows, and maintainable object mapping for tests.

## Choosing UIA2 vs UIA3

FlaUI supports two automation backends:
- **UIA2**: For legacy Windows applications.
- **UIA3**: For modern Windows applications.

**How to select backend:**
```python
from flaui.core.automation_type import AutomationType
from flaui.core.application import Application

# Choose UIA2 or UIA3
app = Application().launch("path/to/app.exe", automation_type=AutomationType.UIA3)
```

## Working with WinForms and WPF

- **WinForms**: Use for classic desktop apps.
- **WPF**: Use for modern desktop apps with rich UI.
- The Python port can automate both types using the same API.

## Element Patterns and Actions

Most UI elements expose patterns (Invoke, Toggle, Selection, etc.) for automation. Example:
```python
# Invoke a button
button = main_window.find_first_child(condition_factory.by_automation_id("submitBtn"))
button.as_button().invoke()

# Toggle a checkbox
checkbox = main_window.find_first_child(condition_factory.by_automation_id("acceptTerms"))
checkbox.as_check_box().toggle()

# Select an item in a ComboBox
combo = main_window.find_first_child(condition_factory.by_automation_id("countryList"))
combo.as_combo_box().select("India")
```

## Advanced Element Search

- Use XPath, property conditions, and tree traversal options to find elements:
```python
# Find by XPath
element = main_window.find_first_by_x_path("//Button[@Name='OK']")

# Find all descendants matching a condition
elements = main_window.find_all_descendants(condition_factory.by_control_type("Button"))
```

## Custom Automation Flows

- Chain actions, handle exceptions, and validate results:
```python
try:
    button.click()
    assert button.is_enabled
except Exception as e:
    print(f"Automation failed: {e}")
```

## Placeholder: UIA2 and UIA3 Port Details

- The backend implementation is based on `flaui.core` and supports switching between UIA2 and UIA3. More details will be added as the port matures.

## Maintainable Object Mapping with pydantic-settings

For scalable and maintainable test automation, you can use `pydantic-settings` to create nested classes that represent your application's UI structure. This allows centralized, importable object management, making it easy to use in fixtures for PyTest or other frameworks.

**Example:**
```python
from pydantic_settings import BaseSettings
from flaui.core.automation_elements import Button, TextBox, Window

class MainWindowMap(BaseSettings):
    submit_button: Button
    username_textbox: TextBox
    main_window: Window

class AppMap(BaseSettings):
    main: MainWindowMap

# Usage in tests
app_map = AppMap(
    main=MainWindowMap(
        submit_button=main_window.find_first_child(condition_factory.by_automation_id("submitBtn")).as_button(),
        username_textbox=main_window.find_first_child(condition_factory.by_automation_id("username")).as_text_box(),
        main_window=main_window
    )
)

def test_submit_button(app_map):
    app_map.main.submit_button.invoke()
    assert app_map.main.submit_button.is_enabled
```

**Tips:**
- Define all UI elements as fields in your mapping classes.
- Use nested classes for windows, dialogs, or grouped controls.
- Import your mapping in test modules and use as fixtures for easy access.
- This approach works with PyTest, unittest, and other frameworks.

**See `tests/test_utilities/` for more mapping and fixture examples.**

## Full List of Supported Elements

Refer to [automation_elements.py](../flaui/core/automation_elements.py) for all supported element wrappers and patterns.

## Further Reading

- [Basic Usage Guide](usage_basic.md)
- [Contributing](contributing.md)
- [Motivation](motivation.md)
