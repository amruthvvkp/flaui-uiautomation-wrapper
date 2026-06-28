# FlaUI for Python

> The premier Windows UI Automation library for Python.

![FlaUI Logo](logo.png)

## Get Started

=== "Python"

    ```python
    # Standard initialization
    from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
    setup_pythonnet_bridge()

    from flaui.modules.automation import Automation
    from flaui.lib.enums import UIAutomationTypes

    automation = Automation(UIAutomationTypes.UIA3)
    main_window = automation.application.launch("notepad.exe").get_main_window(automation)
    main_window.find_first_by_x_path("//Button[@Name='OK']").as_button().invoke()
    ```

=== "C#"

    ```csharp
    using FlaUI.UIA3;
    using FlaUI.Core;

    var automation = new UIA3Automation();
    var app = Application.Launch("notepad.exe");
    var mainWindow = app.GetMainWindow(automation);
    mainWindow.FindFirstByXPath("//Button[@Name='OK']").AsButton().Invoke();
    ```

## Why FlaUI?

FlaUI provides a modern, clean, and typed API for automating Windows applications.

- **Native UI Automation**: Built on Microsoft's UI Automation (UIA) technology, allowing you to inspect and interact with any Windows application (WinForms, WPF, Store Apps, etc.).
- **Modern & Typed**: Fully typed with **Pydantic** models, offering excellent IDE support, autocompletion, and compile-time-like checks.
- **Batteries Included**: Zero-configuration setup. All necessary dependencies are bundled, so you don't need to manage external driver binaries.
- **Rich Interaction Model**: Beyond simple clicks, FlaUI fully supports complex UIA patterns (Toggle, Select, Expand, Scroll, etc.) for robust application control.

## Key Features

- **Dual-Backend Support**: Seamlessly switch between UIA3 (COM-based, recommended for modern apps) and UIA2 (Managed, for legacy apps).
- **Advanced Element Search**: flexible strategies including Accessibility ID, Name, XPath, or arbitrary condition logic.
- **Resilient Automation**: Built-in mechanisms for `Retry`, dynamic timeouts, and input waiting ensure your tests aren't flaky.
- **Drawing & Debugging**: Helpers to highlight elements on screen during test execution.

## Bundled Library Versions

--8<-- "docs/_includes/flaui_versions.md"

## Inspirations & Credits

- **[FlaUI](https://github.com/FlaUI/FlaUI)**: The core logic and test applications are derived from the upstream C# project.
- **[robotframework-flaui](https://github.com/GDATASoftwareAG/robotframework-flaui)** (GDATA): The prior-art Python integration for FlaUI that influenced this project's direction.
- **[Python.NET](https://github.com/pythonnet/pythonnet)**: The interop bridge that makes calling FlaUI from Python possible.
- **[Playwright](https://playwright.dev/python/) / [`pytest-playwright`](https://github.com/microsoft/playwright-pytest)** and **[FlaUIRecorder](https://github.com/twenzel/FlaUIRecorder)**: Inspirations for the planned recorder and pytest tooling.
- **Community**: Special thanks to the contributors of FlaUI and the Python.NET team.

## Next Steps

- **[Basics](basics.md)**: Learn the core workflow: Initialize → Launch → Find → Interact.
- **[Advanced Concepts](advanced.md)**: Master XPath, ConditionFactory, and Caching.
- **[API Reference](api/index.md)**: Explore the full method documentation for every control.
- **[Troubleshooting](troubleshooting.md)**: Resolve common setup and finding issues.
