# Examples

This section pairs **runnable example suites** (in the repository under
[`examples/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples)) with
the docs that walk through them. Every suite automates the same controls on the bundled WPF test
application, so you can compare frameworks side by side.

## Which test framework, when?

| Framework | Reach for it when… | Runnable suite | Walkthrough |
|-----------|--------------------|----------------|-------------|
| **pytest** | You want the default. Fixtures, parametrization, and the richest plugin ecosystem. | `examples/pytest/` | [Pytest](pytest.md) |
| **unittest** | You want zero extra dependencies — it's in the standard library. | — | [Unittest](unittest.md) |
| **behave** | Non-engineers read or own the specs (BDD / Gherkin). | `examples/behave/` | [Behave](behave.md) |
| **Testplan** | You run large, structured campaigns and want rich built-in reporting. | `examples/testplan/` | [Testplan](testplan.md) |
| **Robot Framework** | Your organisation already standardises on Robot keywords. | — | [Robot Framework](robot-framework.md) |

`pytest` ships with the project; `behave` and `testplan` are installed on demand
(`uv pip install behave` / `uv pip install testplan`).

## The shape every suite shares

1. **Initialise the bridge first.** Call `setup_pythonnet_bridge()` before importing or using any
   C#-backed FlaUI type.
2. **Launch once, dispose at the end.** Create an `Automation`, launch the app, and kill/dispose it
   in teardown.
3. **Find → wrap → act.** Locate an element with the `ConditionFactory`, convert it with an `as_*`
   helper, then call typed methods/properties.
4. **Leave shared state clean.** When the app is shared across cases, restore anything you change.

Looking for control-by-control snippets instead of full suites? See the
[Element Cookbook](element-cookbook.md).
