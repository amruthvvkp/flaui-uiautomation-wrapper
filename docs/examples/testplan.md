# Testplan Example

A complete, runnable [Testplan](https://testplan.readthedocs.io/) suite lives in the repository at
[`examples/testplan/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples/testplan).
It automates the bundled WPF test application with a `MultiTest` / `@testsuite` / `@testcase`
structure.

## Install + run

`testplan` is not a project dependency — install it first:

```bash
uv pip install testplan
uv run python examples/testplan/test_plan.py
```

## The suite (`test_plan.py`)

The bridge is initialised before any C#-backed import; the application is launched in `setup` and
disposed in `teardown`:

```python
--8<-- "examples/testplan/test_plan.py"
```

!!! tip "Testplan assertions"
    Interactions use the same Find → wrap → act pattern as the other suites, but results are
    recorded through the `result` collector (`result.equal`, `result.not_equal`, …) rather than bare
    `assert`, which feeds Testplan's structured report.
