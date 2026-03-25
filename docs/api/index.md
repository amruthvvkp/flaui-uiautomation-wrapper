# API Reference

Auto-generated with mkdocstrings from the FlaUI Python wrapper. Element-specific method counts below refer to methods defined on the element (not inherited base methods); each page shows all available methods and properties.

## Core
- [Automation](automation.md) — entrypoint (UIA2/UIA3 selection, condition factory access)
- [Application](application.md) — launch/attach, main window
- [Automation Element](automation_element.md) — base element operations and `as_*` conversions
- [Condition Factory](condition_factory.md) — build search conditions

## Input
- [Mouse](mouse.md) — 15 mouse operations with `post_wait`
- [Keyboard](keyboard.md) — typing, modifiers, context manager
- [Wait](wait.md) — wait helpers

## Tools
- [Retry](retry.md) — polling helpers
- [Cache Request](cache_request.md) — caching scope
- [Drawing](drawing.md) — Point/Rectangle/Color wrappers
- [Collections](collections.md) — type conversion utilities
- [Exceptions](exceptions.md) — translated exception types

## Elements (by category, element-specific methods)

**Interactive**

- [Button](elements/button.md) — 4 methods (click, double_click, right_click, invoke)
- [CheckBox](elements/checkbox.md) — 2 methods (toggle, toggle_state)
- [RadioButton](elements/radiobutton.md) — 2 methods (select, is_selected)
- [ToggleButton](elements/togglebutton.md) — 2 methods (toggle, toggle_state)
- [ComboBox](elements/combobox.md) — 4 methods (select, expand, collapse, items)
- [ComboBoxItem](elements/combobox_item.md) — 2 methods (select, is_selected)
- [TextBox](elements/textbox.md) — 5 methods (enter, append_text, clear, select_all, text)
- [Slider](elements/slider.md) — 3 methods (set_value, value, range)
- [Spinner](elements/spinner.md) — 3 methods (increment, decrement, value)
- [TabItem](elements/tab_item.md) — 2 methods (select, is_selected)

**Containers**

- [Window](elements/window.md) — 6 methods (close, patterns, dialogs, visibility, resize)
- [Menu](elements/menu.md) — 3 methods (items, select, invoke)
- [Tab](elements/tab.md) — 2 methods (select_tab_item, selected_tab)
- [ListBox](elements/listbox.md) — 3 methods (items, select, selected_item)
- [Tree](elements/tree.md) — 4 methods (nodes, expand_all, collapse_all, select_path)
- [Grid](elements/grid.md) — 4 methods (rows, columns, cells, get_item)
- [DataGridView](elements/datagridview.md) — 5 methods (rows, cells, headers, select_cell, scroll_into_view)
- [Calendar](elements/calendar.md) — 3 methods (selected_date, set_date, patterns)

**Display**

- [Label](elements/label.md) — 1 method (text)
- [ProgressBar](elements/progressbar.md) — 2 methods (value, is_indeterminate)

**Complex**

- [DateTimePicker](elements/datetimepicker.md) — 4 methods (value, set_value, parts, open)
- [MenuItem](elements/menu_item.md) — 3 methods (invoke, expand, collapse)
- [TreeItem](elements/tree_item.md) — 4 methods (expand, collapse, children, select)
- [ListBoxItem](elements/listbox_item.md) — 2 methods (select, is_selected)
- [Thumb](elements/thumb.md) — 2 methods (drag, position)
- [TitleBar](elements/titlebar.md) — 2 methods (close, buttons)

!!! warning "UIA2/UIA3 modules are in active porting"
    UIA2 and UIA3 interop are still being ported from C#. Minor API changes are possible before final release.
