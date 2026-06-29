# Pytest Example

A complete, runnable pytest suite lives in the repository at
[`examples/pytest/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples/pytest).
It automates the bundled WPF test application (`test_applications/WPFApplication/WpfApplication.exe`),
which ships in the repo, so the suite runs with no external setup.

## Run it

```bash
uv run pytest examples/pytest -v
```

`pytest` is already a project dependency.

## Fixtures (`conftest.py`)

The bridge is initialised **before** any C#-backed import, then the application is launched once per
session and disposed in teardown:

```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()  # must run before importing C#-backed FlaUI types

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest


@pytest.fixture(scope="session")
def automation():
    auto = Automation(UIAutomationTypes.UIA3)
    auto.application.launch(str(find_test_app()))
    auto.application.wait_while_main_handle_is_missing(3000)
    try:
        yield auto
    finally:
        auto.application.kill()
        auto.automation_base.dispose()


@pytest.fixture
def main_window(automation):
    return automation.application.get_main_window(automation)


@pytest.fixture
def condition_factory(automation):
    return automation.cf
```

## A test (`test_simple_controls.py`)

Find → wrap → act, and leave shared state clean:

```python
def test_toggle_checkbox(main_window, condition_factory) -> None:
    checkbox = main_window.find_first_descendant(
        condition=condition_factory.by_name("Test Checkbox")
    ).as_check_box()
    original = checkbox.is_checked
    try:
        checkbox.toggle()
        assert checkbox.is_checked != original
    finally:
        if checkbox.is_checked != original:
            checkbox.toggle()
```

!!! tip "Keep skips/xfails in fixtures, not tests"
    The project's own suite (`tests/conftest.py`) launches all four combinations
    (UIA2/UIA3 × WinForms/WPF) and guards platform limitations in fixtures. See
    [Testing](../contributing/testing.md) for the matrix conventions.
