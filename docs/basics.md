

# Basics

A quick walkthrough: initialize, launch/attach, find, and interact with Windows UI elements.

## 1) Setup

To begin, initialize the library. This steps loads the necessary underlying components.

!!! warning "Required Initialization"
    Always run `setup_pythonnet_bridge()` at the start of your script or in your test fixture setup.

    ```python
    from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
    setup_pythonnet_bridge()
    ```

### UIA2 vs UIA3

When creating the `Automation` object, you choose the backend:
- **UIA3**: Modern, faster, better for WPF/Store Apps. (Recommended default)
- **UIA2**: Older, managed backend. Better for legacy WinForms apps if UIA3 fails.

=== "Python"

    ```python
    from flaui.modules.automation import Automation
    from flaui.lib.enums import UIAutomationTypes

    # Use UIA3 by default
    automation = Automation(UIAutomationTypes.UIA3)
    ```

=== "C#"

    ```csharp
    using FlaUI.UIA3;
    using FlaUI.Core; // for Application

    var automation = new UIA3Automation();
    ```

## 2) Launch or attach

You can either modify an existing running application ("Attach") or start a new one ("Launch").

### Launching a new app

Use `.launch()` when you want to start a fresh instance for your test. This ensures a clean state.

=== "Python"

    ```python
    # Launch notepad
    app = automation.application.launch("notepad.exe")

    # Get the main window (AutomationElement)
    main_window = app.get_main_window(automation)
    ```

=== "C#"

    ```csharp
    var app = Application.Launch("notepad.exe");
    var mainWindow = app.GetMainWindow(automation);
    ```

### Attaching to an existing app

Use `.attach()` or `.attach_or_launch()` if your workflow involves an app that is already open (e.g., debugging locally).

=== "Python"

    ```python
    # Attach to process named "notepad"
    app = automation.application.attach("notepad.exe")
    main_window = app.get_main_window(automation)
    ```

=== "C#"

    ```csharp
    var app = Application.Attach("notepad.exe");
    var mainWindow = app.GetMainWindow(automation);
    ```

## 3) Inspect elements

Before you can find an element, you need to know *how* to identify it. You need an Inspector tool.

- **[FlaUIInspect](https://github.com/FlaUI/FlaUIInspect)**: The official inspector. Shows the tree, properties, and supported patterns.
- **[Accessibility Insights](https://accessibilityinsights.io/)**: Microsoft's modern tool. Great for highlighting elements.

**What to look for (in order of preference):**
1. **AutomationId**: A stable ID set by developers. (e.g., `btnSubmit`). **Always refer this.**
2. **Name**: The visible text (e.g., "Submit"). Good if IDs are missing, but breaks if language changes.
3. **ControlType**: The type of element (e.g., `Button`). Useful to narrow down searches.

## 4) Find elements

Once you have the ID or Name, use the **ConditionFactory** to find it. The `ConditionFactory` (`cf`) builds safe, typed queries.

### Basic Conditions

Access the factory via `automation.cf` or `element.condition_factory`.

=== "Python"

    ```python
    cf = main_window.condition_factory

    # 1. By Automation ID (Recommended)
    # Finds element with AutomationId="submitButton"
    button = main_window.find_first_descendant(cf.by_automation_id("submitButton"))

    # 2. By Name (Visible Text)
    # Finds element with Name="OK"
    ok_btn = main_window.find_first_descendant(cf.by_name("OK"))

    # 3. By Control Type
    # Finds all button elements
    from flaui.core.definitions import ControlType
    all_buttons = main_window.find_all_descendants(cf.by_control_type(ControlType.Button))

    # 4. By Class Name
    # Finds element with specific class name
    textbox = main_window.find_first_descendant(cf.by_class_name("TextBox"))
    ```

=== "C#"

    ```csharp
    var cf = automation.ConditionFactory;

    var button = mainWindow.FindFirstDescendant(cf.ByAutomationId("submitButton"));
    var okBtn = mainWindow.FindFirstDescendant(cf.ByName("OK"));
    var allButtons = mainWindow.FindAllDescendants(cf.ByControlType(ControlType.Button));
    var textbox = mainWindow.FindFirstDescendant(cf.ByClassName("TextBox"));
    ```

*Note: `find_first_descendant` scans the entire tree below the window. For better performance on huge apps, try `find_first_child` if you know it's a direct child.*

## 5) Interact

Once you have the element, **convert it** to its specific type to interact with it.

### Why convert?
`AutomationElement` is generic. To click it, it's just a generic element. But to "Type" into it, it needs to be a `TextBox`. To "Select" it, it needs to be a `ComboBox`.

```python
# Button: Click it
button.as_button().invoke()

# CheckBox: Toggle it
checkbox.as_check_box().toggle()

# TextBox: Type into it
textbox.as_text_box().enter("Hello World")

# ComboBox: Select an item
combo.as_combo_box().select("Option 1")

# Slider: Move it
slider.as_slider().set_value(50)
```

### Programmatic vs Mouse

- **Programmatic (`invoke()`)**: Uses UIA patterns. Fast, works in background/minimized. **Preferred.**
- **Mouse (`click()`)**: Moves the physical mouse cursor. Slower, requires visible screen. Use when patterns fail.

```python
# Preferred
button.as_button().invoke()

# Fallback (Physical Mouse)
button.click(post_wait=True)
```

## 6) Post-wait pattern

UI actions take time. A click might trigger an animation. Instead of writing `sleep(1)` everywhere, use `post_wait`.

- `post_wait=True`: Wait standard 100ms (often enough for UI update).
- `post_wait=0.5`: Wait 0.5 seconds.

```python
# Click and wait 100ms for reaction
button.click(post_wait=True)

# Type and wait 200ms
keyboard.type("Search Term", post_wait=0.2)
```

## 7) Next Steps

You've mastered the basics: Initialize → Launch → Find → Interact.

- **[Advanced Concepts](advanced.md)**: complex searches (XPath), TreeWalker, and performance caching.
- **[Troubleshooting](troubleshooting.md)**: If elements aren't found or tests are flaky.
