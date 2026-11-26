# Window

!!! tip "Usage notes"
    - **Bring the window to the front before mouse input.** Clicks land on whatever is on top at
      that point. When several app windows overlap (for example a test matrix), call
      `set_foreground()` first.
    - **A stray popup can become the main window.** If a context menu or drop-down is left open,
      `get_main_window()` may return it instead of your form. See [Menu](menu.md).

::: flaui.core.automation_elements.Window
