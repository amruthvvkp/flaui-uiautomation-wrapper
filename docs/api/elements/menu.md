# Menu

!!! tip "Usage notes"
    - **Close context menus when you're done.** A context menu left open is a visible top-level
      window of the app. Windows can then report it as the app's main window, and
      `get_main_window()` returns the popup instead of your form. Press Escape until no menu is
      left before the next step ([#82](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/82)).
    - **Checkable menu items on WinForms** don't support the Toggle pattern, so
      `toggle()`/`is_checked` fail there ([#78](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/78)). They work on WPF.
    - **UIA3 + WinForms context menus** are unreliable. Use UIA2 for them ([#79](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/79)).

::: flaui.core.automation_elements.Menu
