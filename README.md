# flaui-uiautomation-wrapper

> Pythonic, type-safe Windows UI automation — the full FlaUI API in Python.

[![PyPI - Version](https://img.shields.io/pypi/v/flaui-uiautomation-wrapper)](https://pypi.org/project/flaui-uiautomation-wrapper/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flaui-uiautomation-wrapper)](https://pypi.org/project/flaui-uiautomation-wrapper/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/flaui-uiautomation-wrapper)](https://pypi.org/project/flaui-uiautomation-wrapper/)
[![License](https://img.shields.io/github/license/amruthvvkp/flaui-uiautomation-wrapper)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/LICENSE)

[![Build Status](https://dev.azure.com/amruthvvkp/amruthvvkp/_apis/build/status%2Fflaui-uiautomation-wrapper-ci?branchName=master)](https://dev.azure.com/amruthvvkp/amruthvvkp/_build/latest?definitionId=1&branchName=master)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Interrogate](badges/interrogate_badge.svg)
[![Docs](https://img.shields.io/badge/docs-zensical-blue)](https://amruthvvkp.github.io/flaui-uiautomation-wrapper)

[FlaUI](https://github.com/FlaUI/FlaUI) is a .NET library for UI automated testing of Windows
desktop applications — Win32, WinForms, WPF, and Store apps — built on top of Microsoft's UI
Automation technology. **flaui-uiautomation-wrapper** brings the complete FlaUI API to Python via
[Python.NET](https://github.com/pythonnet/pythonnet), so you get the full power of FlaUI without
leaving the Python ecosystem.

Unlike existing Python integrations that are tied to a single test runner, this is a plug-and-play
wrapper that works with **any** Python framework — [pytest](https://docs.pytest.org/),
[Behave](https://behave.readthedocs.io/), [TestPlan](https://github.com/morganstanley/testplan),
`unittest`, or your own tooling — with first-class IDE intellisense backed by Pydantic models.

## Key Differentiators

- **Complete feature parity** — a 1:1 mapping of FlaUI's exposed C# API, not a thin subset.
- **Type safety** — every input/output is backed by Pydantic models for validation and IDE
  autocompletion.
- **Any test framework** — pytest, unittest, Behave, TestPlan, or none at all.
- **Pythonic API** — snake_case methods and Python-native types while preserving the C# structure.

## Installation

Windows-only · Python 3.10–3.14. The required C# DLLs are bundled in the wheel — no separate driver
binaries to manage.

```bash
pip install flaui-uiautomation-wrapper
```

```bash
uv add flaui-uiautomation-wrapper
```

## Quick start

```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

# MUST run before importing any C#-backed modules
setup_pythonnet_bridge()

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation

automation = Automation(UIAutomationTypes.UIA3)
main_window = automation.application.launch("notepad.exe").get_main_window(automation)
main_window.find_first_by_x_path("//Button[@Name='OK']").as_button().invoke()
```

## Documentation

Full documentation lives at
**[amruthvvkp.github.io/flaui-uiautomation-wrapper](https://amruthvvkp.github.io/flaui-uiautomation-wrapper)**,
including:

- **Basics & Advanced** guides (Initialize → Launch → Find → Interact, XPath, ConditionFactory,
  caching) with side-by-side Python/C# examples.
- **API Reference** auto-generated for every control and pattern.
- **Examples** for pytest, unittest, Behave, TestPlan, and Robot Framework.
- **Contributing** guides for development, testing, and porting C# tests.

## Roadmap

This project is in active development toward its first major release. Track progress on the
[v1.0.0 milestone](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/1) and the
full [`ROADMAP.md`](ROADMAP.md), which also outlines post-v1 companion tooling (a record-and-generate
recorder, an MCP server, a `pytest-flaui` plugin, and FlaUI agent skills).

Have an idea or feature request? Join the
[GitHub Discussions](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/discussions).

## Inspirations & Credits

- **[FlaUI](https://github.com/FlaUI/FlaUI)** — the C# library this project wraps; its core logic and
  test applications are the foundation of this wrapper.
- **[robotframework-flaui](https://github.com/GDATASoftwareAG/robotframework-flaui)** (GDATA) — the
  prior-art Python integration for FlaUI that influenced this project's direction.
- **[Python.NET](https://github.com/pythonnet/pythonnet)** — the interop bridge that makes calling
  FlaUI from Python possible.
- **[Playwright](https://playwright.dev/python/)** / **[`pytest-playwright`](https://github.com/microsoft/playwright-pytest)**
  and **[FlaUIRecorder](https://github.com/twenzel/FlaUIRecorder)** — inspirations for the planned
  recorder and pytest tooling.

## Contributing

Contributions are welcome! See [docs/contributing.md](docs/contributing.md) for the development
workflow, coding standards, and testing guidelines.

## License

Licensed under the [LGPL-3.0-or-later](LICENSE).
