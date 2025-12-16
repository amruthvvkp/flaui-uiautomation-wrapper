# Basic Usage Guide

Welcome to the FlaUI Python port! This guide will help beginners get started with UI automation on Windows using FlaUI.

## What is FlaUI?

FlaUI is a C# library for automating Windows UI applications. This Python port provides a 1:1 mapping of C# endpoints, allowing Python developers to automate WinForms and WPF applications using PythonNet.

## Supported Technologies

- **UIA2**: Microsoft UI Automation (older, for legacy apps)
- **UIA3**: Microsoft UI Automation (newer, for modern apps)
- **WinForms**: Windows Forms applications
- **WPF**: Windows Presentation Foundation applications

## Getting Started

1. **Install dependencies**:
   ```sh
   uv sync --all-groups --all-extras
   ```
2. **Import FlaUI core classes**:
   ```python
   from flaui.core.automation_elements import AutomationElement, Button, TextBox
   ```
3. **Launch and attach to an application**:
   ```python
   # Example: Launch a WinForms app
   from flaui.core.application import Application
   app = Application().launch("path/to/WinFormsApplication.exe")
   main_window = app.get_main_window()
   ```
   **C# Example:**
   ```csharp
   using FlaUI.Core;
   using FlaUI.Core.AutomationElements;
   var app = Application.Launch("path/to/WinFormsApplication.exe");
   var mainWindow = app.GetMainWindow(automation);
   ```
4. **Find and interact with elements**:
   ```python
   # Find a button by automation ID and click it
   button = main_window.find_first_child(condition_factory.by_automation_id("myButton"))
   button.as_button().invoke()
   ```
   **C# Example:**
   ```csharp
   var button = mainWindow.FindFirstChild(cf.ByAutomationId("myButton")).AsButton();
   button.Invoke();
   ```

## Placeholder: UIA2 and UIA3 Port

- The library supports both UIA2 and UIA3 backends. You can select the automation type when initializing your automation context. See advanced guide for details.

## Supported Elements

FlaUI Python port supports a wide range of UI elements:
- Button
- Calendar
- CheckBox
- ComboBox
- DataGridView
- DateTimePicker
- Grid, GridRow, GridCell, GridHeader, GridHeaderItem
- Label
- ListBox, ListBoxItem
- Menu, MenuItem
- ProgressBar
- RadioButton
- Slider
- Spinner
- Tab, TabItem
- TextBox
- Thumb
- TitleBar
- ToggleButton
- Tree, TreeItem
- Window

See the [advanced usage guide](usage_advanced.md) for more details and examples.

---

## Using Supported Elements

Below are examples and tips for working with each supported element type in FlaUI Python port:

### Button
```python
button = main_window.find_first_child(condition_factory.by_automation_id("submitBtn"))
button.as_button().invoke()  # Click the button
```
**C# Example:**
```csharp
var button = mainWindow.FindFirstChild(cf.ByAutomationId("submitBtn")).AsButton();
button.Invoke();
```
**Tip:** Use `.click()` for mouse click simulation, `.invoke()` for programmatic click.

### Calendar
```python
calendar = main_window.find_first_child(condition_factory.by_control_type("Calendar"))
calendar.as_calendar()  # Interact with calendar controls
```
**C# Example:**
```csharp
var calendar = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Calendar)).AsCalendar();
```
**Tip:** Not all calendar controls are supported in WinForms.

### CheckBox
```python
checkbox = main_window.find_first_child(condition_factory.by_automation_id("acceptTerms"))
checkbox.as_check_box().toggle()  # Toggle the checkbox
```
**C# Example:**
```csharp
var checkbox = mainWindow.FindFirstChild(cf.ByAutomationId("acceptTerms")).AsCheckBox();
checkbox.Toggle();
```
**Tip:** Use `.toggle_state` to check or set the state directly.

### ComboBox
```python
combo = main_window.find_first_child(condition_factory.by_automation_id("countryList"))
combo.as_combo_box().select("India")  # Select an item
```
**C# Example:**
```csharp
var combo = mainWindow.FindFirstChild(cf.ByAutomationId("countryList")).AsComboBox();
combo.Select("India");
```
**Tip:** Use `.items` to list all options, `.editable_text` for editable ComboBoxes.

### DataGridView
```python
datagrid = main_window.find_first_child(condition_factory.by_control_type("DataGrid"))
datagrid.as_data_grid_view()  # Interact with grid rows/cells
```
**C# Example:**
```csharp
var datagrid = mainWindow.FindFirstChild(cf.ByControlType(ControlType.DataGrid)).AsDataGridView();
```
**Tip:** Use `.rows`, `.cells`, `.header` for advanced grid operations.

### DateTimePicker
```python
date_picker = main_window.find_first_child(condition_factory.by_control_type("DateTimePicker"))
date_picker.as_date_time_picker().selected_date = "2025-07-25"
```
**C# Example:**
```csharp
var datePicker = mainWindow.FindFirstChild(cf.ByControlType(ControlType.DateTimePicker)).AsDateTimePicker();
datePicker.SelectedDate = new DateTime(2025, 7, 25);
```
**Tip:** Use `.selected_date` to get/set the date.

### Grid, GridRow, GridCell, GridHeader, GridHeaderItem
```python
grid = main_window.find_first_child(condition_factory.by_control_type("Grid"))
grid.as_grid()
row = grid.rows[0]
cell = row.cells[0]
```
**C# Example:**
```csharp
var grid = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Grid)).AsGrid();
var row = grid.Rows[0];
var cell = row.Cells[0];
```
**Tip:** Use `.rows`, `.columns`, `.cells` for navigation.

### Label
```python
label = main_window.find_first_child(condition_factory.by_control_type("Text"))
label.as_label().name  # Get label text
```
**C# Example:**
```csharp
var label = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Text)).AsLabel();
var text = label.Name;
```

### ListBox, ListBoxItem
```python
listbox = main_window.find_first_child(condition_factory.by_control_type("List"))
listbox.as_list_box().items  # List all items
item = listbox.items[0]
item.as_list_box_item().select()  # Select item
```
**C# Example:**
```csharp
var listbox = mainWindow.FindFirstChild(cf.ByControlType(ControlType.List)).AsListBox();
var item = listbox.Items[0].AsListBoxItem();
item.Select();
```

### Menu, MenuItem
```python
menu = main_window.find_first_child(condition_factory.by_control_type("Menu"))
menu.as_menu().items  # List menu items
menu_item = menu.items[0]
menu_item.as_menu_item().invoke()  # Click menu item
```
**C# Example:**
```csharp
var menu = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Menu)).AsMenu();
var menuItem = menu.Items[0].AsMenuItem();
menuItem.Invoke();
```

### ProgressBar
```python
progress = main_window.find_first_child(condition_factory.by_control_type("ProgressBar"))
progress.as_progress_bar().value  # Get progress value
```
**C# Example:**
```csharp
var progress = mainWindow.FindFirstChild(cf.ByControlType(ControlType.ProgressBar)).AsProgressBar();
var value = progress.Value;
```

### RadioButton
```python
radio = main_window.find_first_child(condition_factory.by_control_type("RadioButton"))
radio.as_radio_button().is_checked  # Check if selected
```
**C# Example:**
```csharp
var radio = mainWindow.FindFirstChild(cf.ByControlType(ControlType.RadioButton)).AsRadioButton();
bool isChecked = radio.IsChecked;
```

### Slider
```python
slider = main_window.find_first_child(condition_factory.by_control_type("Slider"))
slider.as_slider().value = 50  # Set slider value
```
**C# Example:**
```csharp
var slider = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Slider)).AsSlider();
slider.Value = 50;
```

### Spinner
```python
spinner = main_window.find_first_child(condition_factory.by_control_type("Spinner"))
spinner.as_spinner().value = 5  # Set spinner value
```
**C# Example:**
```csharp
var spinner = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Spinner)).AsSpinner();
spinner.Value = 5;
```

### Tab, TabItem
```python
tab = main_window.find_first_child(condition_factory.by_control_type("Tab"))
tab.as_tab().items  # List tab items
tab_item = tab.items[0]
tab_item.as_tab_item().select()  # Select tab
```
**C# Example:**
```csharp
var tab = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Tab)).AsTab();
var tabItem = tab.Items[0].AsTabItem();
tabItem.Select();
```

### TextBox
```python
textbox = main_window.find_first_child(condition_factory.by_control_type("Edit"))
textbox.as_text_box().text = "Hello World"
```
**C# Example:**
```csharp
var textbox = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Edit)).AsTextBox();
textbox.Text = "Hello World";
```
**Tip:** Use `.text` to get/set the value.

### Thumb
```python
thumb = main_window.find_first_child(condition_factory.by_control_type("Thumb"))
thumb.as_thumb()  # Interact with thumb controls
```
**C# Example:**
```csharp
var thumb = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Thumb)).AsThumb();
```

### TitleBar
```python
titlebar = main_window.find_first_child(condition_factory.by_control_type("TitleBar"))
titlebar.as_title_bar().name  # Get window title
```
**C# Example:**
```csharp
var titlebar = mainWindow.FindFirstChild(cf.ByControlType(ControlType.TitleBar)).AsTitleBar();
var title = titlebar.Name;
```

### ToggleButton
```python
toggle = main_window.find_first_child(condition_factory.by_control_type("Button"))
toggle.as_toggle_button().toggle()
```
**C# Example:**
```csharp
var toggle = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Button)).AsToggleButton();
toggle.Toggle();
```

### Tree, TreeItem
```python
tree = main_window.find_first_child(condition_factory.by_control_type("Tree"))
tree.as_tree().items  # List tree items
tree_item = tree.items[0]
tree_item.as_tree_item().expand()  # Expand tree item
```
**C# Example:**
```csharp
var tree = mainWindow.FindFirstChild(cf.ByControlType(ControlType.Tree)).AsTree();
var treeItem = tree.Items[0].AsTreeItem();
treeItem.Expand();
```

### Window
```python
window = app.get_main_window()
window.as_window().set_foreground()  # Bring window to front
```
**C# Example:**
```csharp
var window = app.GetMainWindow(automation);
window.SetForeground();
```
**Tip:** Use `.set_foreground()`, `.focus()`, `.capture()` for window operations.

---
