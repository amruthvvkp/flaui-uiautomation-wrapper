# ComboBox

!!! warning "WinForms combo boxes don't work through UI Automation"
    On WinForms, with both UIA2 and UIA3, `items` comes back empty, `select(index)` raises
    `IndexOutOfRangeException`, and `expand()` leaves the box collapsed. The bug is in Windows/.NET,
    not in FlaUI or this wrapper, and upstream FlaUI skips its WinForms combo box tests for the same
    reason ([#75](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/75)). WPF combo boxes work normally.

!!! tip "Usage notes"
    - **Bring the window to the front first.** A WPF drop-down closes as soon as its window loses
      focus, for example when another window overlaps it. Call `set_foreground()` on the window
      before `expand()`.
    - **Wait for the state, not a fixed sleep.** The drop-down animates open. Poll
      `expand_collapse_state` with `Retry.While` until it reports `ExpandCollapseState.Expanded`.
    - **Editable combo boxes** take text through `editable_text`; setting it selects the matching
      item.

::: flaui.core.automation_elements.ComboBox
