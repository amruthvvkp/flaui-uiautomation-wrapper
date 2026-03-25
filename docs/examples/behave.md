# Behave (Coming Soon)

!!! warning "Coming Soon (Issue #48)"
    Pseudocode scaffold for BDD workflows.

```gherkin
Feature: Save document
  Scenario: User saves a document
    Given Notepad is running
    When I click the Save button
    Then a Save dialog appears
```

```python
# steps/save_steps.py
from behave import given, when, then
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
from flaui.modules.automation import Automation
from flaui.lib.enums import UIAutomationTypes

setup_pythonnet_bridge()
automation = Automation(UIAutomationTypes.UIA3)

@given("Notepad is running")
def step_launch_notepad(context):
    context.app = automation.application.launch("notepad.exe")
    context.window = context.app.get_main_window(automation)

@when("I click the Save button")
def step_click_save(context):
    button = context.window.find_first_by_x_path("//Button[@Name='Save']").as_button()
    button.invoke()

@then("a Save dialog appears")
def step_save_dialog(context):
    dialog = context.window.find_first_descendant(context.window.condition_factory.by_name("Save"))
    assert dialog is not None
```
