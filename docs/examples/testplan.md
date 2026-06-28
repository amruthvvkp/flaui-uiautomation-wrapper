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
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()  # before any C#-backed FlaUI import

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
from testplan import test_plan
from testplan.testing.multitest import MultiTest, testcase, testsuite


@testsuite
class SimpleControlsSuite:
    def setup(self, env, result):
        self.automation = Automation(UIAutomationTypes.UIA3)
        self.automation.application.launch(str(find_test_app()))
        self.automation.application.wait_while_main_handle_is_missing(3000)
        self.window = self.automation.application.get_main_window(self.automation)
        self.cf = self.automation.cf

    def teardown(self, env, result):
        self.automation.application.kill()
        self.automation.automation_base.dispose()

    @testcase
    def enter_text(self, env, result):
        text_box = self.window.find_first_descendant(
            condition=self.cf.by_automation_id("TextBox")
        ).as_text_box()
        text_box.text = "hello from testplan"
        result.equal(text_box.text, "hello from testplan", description="text entered")


@test_plan(name="FlaUI for Python TestPlan example")
def main(plan):
    plan.add(MultiTest(name="WPF Simple Controls", suites=[SimpleControlsSuite()]))


if __name__ == "__main__":
    import sys

    sys.exit(not main())
```

!!! tip "Testplan assertions"
    Interactions use the same Find → wrap → act pattern as the other suites, but results are
    recorded through the `result` collector (`result.equal`, `result.not_equal`, …) rather than bare
    `assert`, which feeds Testplan's structured report.
