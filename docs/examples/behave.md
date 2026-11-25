# Behave (BDD) Example

A complete, runnable behave suite lives in the repository at
[`examples/behave/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples/behave).
It automates the bundled WPF test application with Gherkin scenarios.

## Install + run

`behave` is not a project dependency — install it first:

```bash
uv pip install behave
uv run behave examples/behave/features
```

## The feature (`features/simple_controls.feature`)

```gherkin
--8<-- "examples/behave/features/simple_controls.feature"
```

## Setup (`features/environment.py`)

`before_all` initialises the bridge, launches the app once, and stores the window and condition
factory on the behave `context`:

```python
--8<-- "examples/behave/features/environment.py"
```

## Steps (`features/steps/simple_controls_steps.py`)

```python
--8<-- "examples/behave/features/steps/simple_controls_steps.py"
```

!!! note "Bridge before steps"
    behave imports step modules at startup, so `setup_pythonnet_bridge()` runs at the top of
    `environment.py` (loaded first) to guarantee the bridge is ready before any C#-backed type is
    touched.
