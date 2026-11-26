# ListBox

!!! tip "Usage notes"
    - **Selection persists.** A list box keeps its selection across tests while the app stays open.
      If your tests share one app instance, clear any leftover selection with
      `remove_from_selection(...)` before asserting on `selected_items` ([#83](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/83)).
    - **WinForms single-select lists can't be emptied.** Once an item is selected, removing it raises
      "Selection container requires one selection". Select the item you need instead of clearing
      first.
    - **Large WPF lists are virtualised.** Items that are off screen don't exist in the automation tree
      yet. Call `scroll_into_view()` on an item, or `ItemRealizer.realize_items(list_box)` to
      realise them all, before searching.
    - **`select` takes an index or the item text.** `select(0)` and `select("Item 1")` call FlaUI's
      matching overloads directly.

::: flaui.core.automation_elements.ListBox
