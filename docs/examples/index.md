# Examples

Everything in this section is backed by **runnable code** in the repository under
[`examples/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples). The
Python snippets are included from those files when the docs are built, and the build fails if a
referenced file or section goes missing, so the docs can't drift from code that runs. Wherever it
helps, the **C#** equivalent sits in a tab next to the Python.

## Start here

<div class="grid cards" markdown>

- **[Gallery](gallery.md)**: complete scripts for Calculator, Notepad, and the bundled WPF /
  WinForms apps.
- **[Element Cookbook](element-cookbook.md)**: one runnable recipe per control (button, combo
  box, tree, grid, ...).

</div>

## Which test framework, when?

Every suite automates the same controls on the bundled WPF test application, so you can compare
frameworks side by side.

| Framework | Reach for it when… | Runnable suite | Walkthrough |
|-----------|--------------------|----------------|-------------|
| **pytest** | You want the default: fixtures, parametrization, and the richest plugin ecosystem. | `examples/pytest/` | [Pytest](pytest.md) |
| **unittest** | You want zero extra dependencies; it's in the standard library. | `examples/unittest/` | [Unittest](unittest.md) |
| **behave** | Non-engineers read or own the specs (BDD / Gherkin). | `examples/behave/` | [Behave](behave.md) |
| **Testplan** | You run large, structured campaigns and want rich built-in reporting. | `examples/testplan/` | [Testplan](testplan.md) |
| **Robot Framework** | Your organisation already standardises on Robot keywords. | Planned after v1 | [Robot Framework](robot-framework.md) |

`pytest` ships with the project and `unittest` with Python. Install `behave` and `testplan` when
you need them (`uv pip install behave` / `uv pip install testplan`).

## Run everything

```bash
uv run pytest examples/pytest -v                              # pytest, cookbook, advanced recipes
uv run python -m unittest discover -s examples/unittest -v    # unittest
uv run behave examples/behave/features                        # behave
uv run python examples/testplan/test_plan.py                  # Testplan
uv run python examples/scripts/quickstart.py --app winforms   # gallery scripts
```

## The shape every suite shares

1. **Initialise the bridge first.** Call `setup_pythonnet_bridge()` before importing or using any
   C#-backed FlaUI type.
2. **Launch once, dispose at the end.** Create an `Automation`, launch the app, and kill or dispose
   it in teardown (or use `with Automation(...)`).
3. **Find → wrap → act.** Locate an element with the `ConditionFactory`, convert it with an `as_*`
   helper, then call typed methods and properties.
4. **Leave shared state clean.** When the app is shared across tests, undo anything you change.
