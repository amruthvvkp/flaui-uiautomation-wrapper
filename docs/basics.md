# Basics

A quick walkthrough: initialize, launch or attach, find, and interact with Windows UI elements.
Every step shows the **Python** code next to the original FlaUI **C#**. Pick a language tab once and
the whole page follows.

!!! success "Run this page"
    The Python snippets come from
    [`examples/scripts/quickstart.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/examples/scripts/quickstart.py),
    which drives the bundled test application:

    ```bash
    uv run python examples/scripts/quickstart.py            # WPF app, UIA3
    uv run python examples/scripts/quickstart.py --app winforms --uia 2
    ```

## 1) Setup

Initialize the PythonNet bridge first. It loads the bundled FlaUI assemblies into the .NET runtime.

!!! warning "Required initialization"
    Call `setup_pythonnet_bridge()` **before** importing anything C#-backed: at the top of your
    script, or at the top of `conftest.py` in a test suite. C# has no equivalent step, because the
    assemblies are referenced at build time.

=== "Python"

    ```python
    --8<-- "examples/scripts/quickstart.py:setup"
    ```

=== "C#"

    ```csharp
    using FlaUI.Core;
    using FlaUI.Core.Definitions;
    using FlaUI.UIA3;
    ```

### UIA2 vs UIA3

When you create the `Automation` object, you choose the backend:

- **UIA3**: modern and faster; the right choice for WPF and Store apps. **This is the default to use.**
- **UIA2**: the older managed backend. Try it for legacy WinForms apps if UIA3 struggles.

=== "Python"

    ```python
    automation = Automation(UIAutomationTypes.UIA3)  # or UIAutomationTypes.UIA2
    ```

=== "C#"

    ```csharp
    var automation = new UIA3Automation(); // or new UIA2Automation()
    ```

See [UIA2 vs UIA3](uia2-uia3.md) for the details.

## 2) Launch or attach

### Launching a new app

Launch a fresh instance when you want a clean state. In Python, the application lives on
`automation.application`. `launch()` returns nothing, so ask `automation.application` for the main
window afterwards.

=== "Python"

    ```python
    --8<-- "examples/scripts/quickstart.py:launch"
    ```

=== "C#"

    ```csharp
    using var automation = new UIA3Automation();
    using var app = Application.Launch(executable);
    var window = app.GetMainWindow(automation);
    var cf = automation.ConditionFactory;
    Console.WriteLine($"Launched: {window.Title}");
    ```

### Attaching to an existing app

Attach when the app is already running, for example while debugging locally.
`attach_or_launch()` attaches if a matching process exists and launches one otherwise.
With several copies running, attach by PID instead. See [Multiple instances](multi-instance.md).

=== "Python"

    ```python
    automation.application.attach("notepad.exe")  # process name or PID
    window = automation.application.get_main_window(automation)
    ```

=== "C#"

    ```csharp
    var app = Application.Attach("notepad.exe");
    var window = app.GetMainWindow(automation);
    ```

## 3) Inspect elements

Before you can find an element, you need to know *how* to identify it. Use an inspector:

- **[FlaUInspect](https://github.com/FlaUI/FlaUInspect)**: the official inspector. Shows the tree,
  properties, and supported patterns.
- **[Accessibility Insights](https://accessibilityinsights.io/)**: Microsoft's modern tool. Good
  for highlighting elements.

**What to look for, in order of preference:**

1. **AutomationId**: a stable ID set by the developers (e.g. `TextBox`). **Use it whenever it exists.**
2. **Name**: the visible text (e.g. "Test Checkbox"). Useful when IDs are missing, but it changes
   when the UI language does.
3. **ControlType**: the kind of element (e.g. `Button`). Useful to narrow a search.

## 4) Find elements

The **ConditionFactory** (`automation.cf`) builds typed search conditions. Pass them to the
`find_*` methods of any element.

=== "Python"

    ```python
    --8<-- "examples/scripts/quickstart.py:find"
    ```

=== "C#"

    ```csharp
    var textBox = window.FindFirstDescendant(cf.ByAutomationId("TextBox"));
    var checkBox = window.FindFirstDescendant(cf.ByName("Test Checkbox"));
    var buttons = window.FindAllDescendants(cf.ByControlType(ControlType.Button));
    Console.WriteLine($"Found {buttons.Length} buttons");
    ```

!!! note "No match: `null` in C#, an exception in Python"
    In C#, `FindFirst*` returns `null` when nothing matches. In Python it raises `ElementNotFound`
    (from `flaui.lib.exceptions`), so a typo fails at the line that caused it instead of turning
    into a confusing `None` error further down.

`find_first_descendant` searches the whole subtree. On very large trees, `find_first_child` is
faster when you know the element is a direct child.

## 5) Interact

**Convert** the generic `AutomationElement` to its specific type with an `as_*` helper. The
specific type is what gives you `text`, `toggle()`, `select()` and so on.

=== "Python"

    ```python
    --8<-- "examples/scripts/quickstart.py:interact"
    ```

=== "C#"

    ```csharp
    textBox.AsTextBox().Text = "Hello from FlaUI";
    var cb = checkBox.AsCheckBox();
    cb.Toggle();
    Console.WriteLine($"Checkbox is on: {cb.ToggleState == ToggleState.On}");
    cb.Toggle(); // put it back
    ```

The [Element Cookbook](examples/element-cookbook.md) has a runnable recipe for every common control.

### Programmatic vs mouse

- **Programmatic (`invoke()`, `toggle()`, `text = ...`)** uses UIA patterns. It is fast and works
  while the window is in the background. **Prefer it.**
- **Mouse (`click()`)** moves the real cursor. It is slower and needs the element on screen. Use it
  when no pattern fits.

=== "Python"

    ```python
    button.invoke()               # preferred
    button.click(post_wait=True)  # fallback: real mouse click, then wait for the UI to settle
    ```

=== "C#"

    ```csharp
    button.Invoke();
    button.Click();
    Wait.UntilInputIsProcessed();
    ```

## 6) The `post_wait` shortcut

UI actions take time to land. Instead of sprinkling `sleep()` calls, input methods (`Mouse`
methods, `click`, `TextBox.enter`, `Tab.select_tab_item`) accept `post_wait`:

- `post_wait=True`: wait until input is processed (~100 ms).
- `post_wait=0.5`: wait half a second.
- `post_wait=callable`: call your own wait function.

=== "Python"

    ```python
    button.click(post_wait=True)
    text_box.enter("Search term", post_wait=0.2)
    ```

=== "C#"

    ```csharp
    button.Click();
    Wait.UntilInputIsProcessed();
    textBox.Enter("Search term");
    Thread.Sleep(200);
    ```

`post_wait` is a Python addition. C# FlaUI uses an explicit `Wait` call after the action.

## 7) Next steps

You've covered the basics: initialize → launch → find → interact.

- **[Example Gallery](examples/gallery.md)**: complete scripts for Calculator, Notepad, and the
  bundled apps.
- **[Advanced](advanced.md)**: XPath, combined conditions, tree walking, caching, and retries.
- **[Troubleshooting](troubleshooting.md)**: what to check when elements aren't found or tests are
  flaky.
