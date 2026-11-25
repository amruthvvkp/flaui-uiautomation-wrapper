# Example Gallery

Complete, runnable automations of real applications. Each one is a plain Python script under
[`examples/scripts/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples/scripts),
with no test framework involved. Each is shown next to the equivalent FlaUI C# program. The
Python tabs are included from the scripts themselves, so what you read here is what runs.

| Application | Kind | Script | Run it |
|-------------|------|--------|--------|
| [Bundled WPF / WinForms app](#bundled-wpf-winforms-test-app) | Custom desktop app | `quickstart.py` | `uv run python examples/scripts/quickstart.py --app wpf` |
| [Calculator](#calculator) | Windows Store (UWP) | `calculator.py` | `uv run python examples/scripts/calculator.py` |
| [Notepad](#notepad) | Win32 (Win 10) / Store (Win 11) | `notepad.py` | `uv run python examples/scripts/notepad.py` |

!!! tip "Want a test suite instead of a script?"
    The [framework examples](index.md) drive the same bundled app with pytest, unittest, behave and
    Testplan. The [Element Cookbook](element-cookbook.md) has one recipe per control.

## Bundled WPF / WinForms test app

The repository ships two test applications under `test_applications/`: a WPF one and a WinForms
one, with the same controls in each. `quickstart.py` drives either app on either automation
stack, so you can try all four combinations:

```bash
uv run python examples/scripts/quickstart.py --app wpf --uia 3
uv run python examples/scripts/quickstart.py --app winforms --uia 2
```

=== "Python"

    ```python
    --8<-- "examples/scripts/quickstart.py:setup"

    --8<-- "examples/scripts/quickstart.py:launch"

    --8<-- "examples/scripts/quickstart.py:find"

    --8<-- "examples/scripts/quickstart.py:interact"
    ```

=== "C#"

    ```csharp
    using FlaUI.Core;
    using FlaUI.Core.Definitions;
    using FlaUI.UIA3;

    using var automation = new UIA3Automation();
    using var app = Application.Launch(executable);
    var window = app.GetMainWindow(automation);
    var cf = automation.ConditionFactory;
    Console.WriteLine($"Launched: {window.Title}");

    var textBox = window.FindFirstDescendant(cf.ByAutomationId("TextBox"));
    var checkBox = window.FindFirstDescendant(cf.ByName("Test Checkbox"));
    var buttons = window.FindAllDescendants(cf.ByControlType(ControlType.Button));
    Console.WriteLine($"Found {buttons.Length} buttons");

    textBox.AsTextBox().Text = "Hello from FlaUI";
    var cb = checkBox.AsCheckBox();
    cb.Toggle();
    Console.WriteLine($"Checkbox is on: {cb.ToggleState == ToggleState.On}");
    cb.Toggle();
    ```

## Calculator

Calculator is a Windows Store (UWP) app. It is launched by its AppUserModelId and driven through
its stable button AutomationIds. Store apps need **UIA3**.

=== "Python"

    ```python
    --8<-- "examples/scripts/calculator.py"
    ```

=== "C#"

    ```csharp
    using FlaUI.Core;
    using FlaUI.Core.Tools;
    using FlaUI.UIA3;

    using var automation = new UIA3Automation();
    using var app = Application.LaunchStoreApp("Microsoft.WindowsCalculator_8wekyb3d8bbwe!App");
    var window = app.GetMainWindow(automation);
    var cf = automation.ConditionFactory;

    void Press(string id) => window.FindFirstDescendant(cf.ByAutomationId(id)).AsButton().Invoke();

    Press("clearButton");
    foreach (var key in new[] { "num1Button", "num2Button", "plusButton", "num3Button", "num0Button", "equalButton" })
        Press(key);

    var display = window.FindFirstDescendant(cf.ByAutomationId("CalculatorResults"));
    Retry.WhileFalse(() => display.Name.EndsWith("42"), TimeSpan.FromSeconds(2));
    Console.WriteLine(display.Name); // "Display is 42"
    ```

## Notepad

On Windows 11, `notepad.exe` is only a launcher stub: it starts the Store version of Notepad and
exits right away. The script therefore finds the window on the desktop by its class name instead
of using the launched process. It also sets the text through the Value pattern, so no keystrokes
are sent and nothing else on the desktop can get mixed into the input.

=== "Python"

    ```python
    --8<-- "examples/scripts/notepad.py"
    ```

=== "C#"

    ```csharp
    using FlaUI.Core;
    using FlaUI.Core.Definitions;
    using FlaUI.Core.Tools;
    using FlaUI.UIA3;

    using var automation = new UIA3Automation();
    var cf = automation.ConditionFactory;
    var desktop = automation.GetDesktop();
    Application.Launch("notepad.exe");

    var window = Retry.WhileNull(
        () => desktop.FindFirstChild(cf.ByClassName("Notepad")),
        TimeSpan.FromSeconds(10), throwOnTimeout: true).Result.AsWindow();
    window.Focus();

    var editor = window.FindFirstDescendant(
        cf.ByControlType(ControlType.Document).Or(cf.ByControlType(ControlType.Edit))).AsTextBox();
    editor.Text = "Hello from FlaUI";
    Console.WriteLine($"Notepad says: {editor.Text}");

    editor.Text = "";
    window.Close();
    ```

!!! note "Python vs C# differences you can see here"
    - In C#, `FindFirstChild` returns `null` when nothing matches. The Python wrapper raises
      `ElementNotFound` instead, so the Python script polls with `Retry.WhileException` where C# uses
      `Retry.WhileNull`.
    - `using var` in C# corresponds to `with Automation(...) as automation:` in Python. Both dispose
      the automation and close the app when the block ends.
