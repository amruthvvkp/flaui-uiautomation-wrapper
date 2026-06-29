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
Feature: WPF simple controls
  Scenario: Enter text into the text box
    Given the WPF test application is running
    When I enter "hello from behave" into the text box
    Then the text box contains "hello from behave"

  Scenario: Toggle the test checkbox
    Given the WPF test application is running
    When I toggle the test checkbox
    Then the test checkbox state is inverted
```

## Setup (`features/environment.py`)

`before_all` initialises the bridge, launches the app once, and stores the window and condition
factory on the behave `context`:

```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()  # before any C#-backed FlaUI import / step module

from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation


def before_all(context):
    context.automation = Automation(UIAutomationTypes.UIA3)
    context.automation.application.launch(str(find_test_app()))
    context.automation.application.wait_while_main_handle_is_missing(3000)
    context.window = context.automation.application.get_main_window(context.automation)
    context.cf = context.automation.cf


def after_all(context):
    context.automation.application.kill()
    context.automation.automation_base.dispose()
```

## Steps (`features/steps/simple_controls_steps.py`)

```python
from behave import given, then, when


@when('I enter "{value}" into the text box')
def step_enter_text(context, value):
    text_box = context.window.find_first_descendant(
        condition=context.cf.by_automation_id("TextBox")
    ).as_text_box()
    text_box.text = value


@then('the text box contains "{value}"')
def step_text_box_contains(context, value):
    text_box = context.window.find_first_descendant(
        condition=context.cf.by_automation_id("TextBox")
    ).as_text_box()
    assert text_box.text == value
```

!!! note "Bridge before steps"
    behave imports step modules at startup, so `setup_pythonnet_bridge()` runs at the top of
    `environment.py` (loaded first) to guarantee the bridge is ready before any C#-backed type is
    touched.
