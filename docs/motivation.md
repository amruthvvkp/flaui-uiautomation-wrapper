# Motivation

## Why was this library created?

While RobotFlaUI provided some UI automation capabilities for Python, it was limited to Robot Framework and XPath-based element finding. There was no solution that offered full access to the FlaUI C# API for Python developers.

This library was created to:

- Enable Python developers to use the complete FlaUI API for Windows UI automation
- Provide robust, validated, and type-safe Python wrappers for all automation elements and patterns
- Achieve feature parity with the original C# library
- Support plug-and-play usage by packaging all required C# binaries
- Make it easy to port and run C# UI and unit tests in Python

## How it compares to other Python tools

Several libraries can automate Windows UIs from Python. They differ in the technology they sit on,
how typed and Pythonic the API feels, and how much of the underlying UI Automation surface they
expose.

| Tool | Underlying tech | Backends | Typed API / IDE support | Test-framework lock-in | Notes |
|------|-----------------|----------|-------------------------|------------------------|-------|
| **FlaUI for Python** (this project) | [FlaUI](https://github.com/FlaUI/FlaUI) C# via [Python.NET](https://github.com/pythonnet/pythonnet) | UIA2 + UIA3 | ✅ Pydantic models, full hints | None — pytest, unittest, Robot, Behave, anything | 1:1 mapping of the FlaUI C# API; bundles all DLLs |
| [pywinauto](https://github.com/pywinauto/pywinauto) | Pure Python (ctypes/comtypes) | Win32 + UIA | ⚠️ Partial; dynamic attribute access | None | Mature and popular; dynamic API is flexible but harder to introspect |
| [uiautomation](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows) | `comtypes` over UIA COM | UIA only | ⚠️ Limited | None | Lightweight, single-author; thin wrapper over raw UIA |
| [robotframework-flaui](https://github.com/GDATASoftwareAG/robotframework-flaui) (RobotFlaUI) | FlaUI C# via Python.NET | UIA2 + UIA3 | ❌ Keyword-based | Robot Framework only | Same engine, but usage limited to Robot keywords and XPath |
| [WinAppDriver](https://github.com/microsoft/WinAppDriver) + [Appium-Python-Client](https://github.com/appium/python-client) | WebDriver/Appium server | UIA | ⚠️ Selenium-style | None | Server-based; WinAppDriver is no longer actively maintained by Microsoft |
| [PyAutoGUI](https://github.com/asweigart/pyautogui) / [AutoIt](https://www.autoitscript.com/) | Coordinates + image matching | N/A | ⚠️ | None | Not UIA-aware; brittle for structural automation |

### Where FlaUI for Python fits

- **You want the full FlaUI surface, not a subset.** Unlike RobotFlaUI (Robot Framework + XPath
  only), this wrapper exposes the complete FlaUI C# API in idiomatic Python.
- **You value type safety.** Every element, pattern, and coordinate type is backed by Pydantic, so
  you get autocompletion and validation before calls ever cross the interop boundary.
- **You are not tied to one test runner.** Use it with pytest, unittest, Robot Framework, Behave,
  or your own harness — see the [Examples](examples/pytest.md).
- **You are migrating from C#.** The 1:1 mapping (and side-by-side C# snippets throughout these
  docs) makes porting existing FlaUI test suites straightforward.

When another tool may be the better fit: choose **pywinauto** if you need pure-Python with no .NET
runtime and want Win32 (non-UIA) support; choose **uiautomation** for a minimal dependency
footprint; choose **WinAppDriver/Appium** if you are standardizing on the WebDriver protocol across
platforms.

## Advantages over alternatives

- 1:1 mapping of C# endpoints, not just limited to XPath or Robot Framework
- Built on Pydantic for validation and type hints
- PythonNet for seamless C# interop
- Designed for extensibility and future support of other test frameworks

## Who should use this library?

- Python developers needing advanced Windows UI automation
- Teams migrating C# FlaUI tests to Python
- Anyone seeking a modern, validated, and extensible automation solution for Windows applications
