# Automation Element

!!! tip "Usage notes"
    - **`find_first_with_options` / `find_all_with_options` need UIA3.** UIA2 doesn't implement
      them, and FlaUI raises `NotSupportedByFrameworkException` ([#80](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/80)).
    - **Search close to the target.** `find_first_child` on a nearby container is much cheaper than
      `find_first_descendant` from the window. See [Performance](../performance.md).

::: flaui.core.automation_elements.AutomationElement
