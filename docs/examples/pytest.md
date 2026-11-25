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
--8<-- "examples/pytest/conftest.py"
```

## The tests (`test_simple_controls.py`)

Find → wrap → act, and leave shared state clean:

```python
--8<-- "examples/pytest/test_simple_controls.py"
```

## More in this folder

The same fixtures also drive the recipes the docs include:

| File | Docs page |
|------|-----------|
| `test_element_cookbook.py` | [Element Cookbook](element-cookbook.md): one test per control |
| `test_advanced.py` | [Advanced](../advanced.md): XPath, conditions, caching, retry, `expect`, `post_wait` |
| `test_configuration.py` | [Configuration & logging](../configuration.md): C# logging, timeouts, mouse speed |
| `test_multi_instance.py` | [Multiple instances](../multi-instance.md): several copies of one app |

!!! tip "Keep skips/xfails in fixtures, not tests"
    The project's own suite (`tests/conftest.py`) launches all four combinations
    (UIA2/UIA3 × WinForms/WPF) and guards platform limitations in fixtures. See
    [Testing](../contributing/testing.md) for the matrix conventions.
