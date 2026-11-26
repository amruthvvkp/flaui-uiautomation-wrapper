# Mouse

!!! tip "Usage notes"
    - **Prefer patterns to clicks.** `invoke()`, `toggle()` and `select()` skip the mouse
      entirely, and are tens to hundreds of times faster than a click. See [Performance](../performance.md).
    - **Clicking the same spot twice in a row is slow on purpose.** FlaUI waits out the system
      double-click time (about 500 ms) so two single clicks aren't read as a double click. Clicks on
      different spots don't wait.
    - **Use `post_wait`** on mouse methods when the app needs a moment to react, instead of a
      separate sleep.

::: flaui.core.input.Mouse
