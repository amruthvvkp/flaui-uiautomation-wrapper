# Element Cookbook

Control-by-control snippets, organised by category. Each shows the original FlaUI **C#** call (from
the FlaUI UITests) and its **Python** equivalent. For full, runnable suites that string these
together, see the [Examples overview](index.md).

All snippets assume a `window` (an automation element / `Window`) and a condition factory `cf` — see
any [example suite](pytest.md) for how to obtain them.

## Interactive controls

### Button
```csharp
var button = window.FindFirstByXPath("//Button[@Name='OK']").AsButton();
button.Invoke();
```
```python
button = window.find_first_by_x_path("//Button[@Name='OK']").as_button()
button.invoke()
```

### CheckBox
```csharp
var cb = window.FindFirstDescendant(cf => cf.ByAutomationId("accept"))?.AsCheckBox();
cb.Toggle();
```
```python
cb = window.find_first_descendant(cf.by_automation_id("accept")).as_check_box()
cb.toggle()
```

### RadioButton
```csharp
var radio = window.FindFirstDescendant(cf => cf.ByAutomationId("RadioButton1"))?.AsRadioButton();
radio.IsChecked = true;
```
```python
radio = window.find_first_descendant(cf.by_automation_id("RadioButton1")).as_radio_button()
radio.is_checked = True
```

### ComboBox
```csharp
var combo = window.FindFirstDescendant(cf => cf.ByAutomationId("Countries"))?.AsComboBox();
combo.Select("India");
```
```python
combo = window.find_first_descendant(cf.by_automation_id("Countries")).as_combo_box()
combo.select("India")
```

### TextBox
```csharp
var textBox = window.FindFirstDescendant(cf => cf.ByAutomationId("TextBox"))?.AsTextBox();
textBox.Text = "hello";
```
```python
text_box = window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
text_box.text = "hello"
```

### Slider
```csharp
var slider = window.FindFirstDescendant(cf => cf.ByAutomationId("Slider"))?.AsSlider();
slider.Value = 7;
```
```python
slider = window.find_first_descendant(cf.by_automation_id("Slider")).as_slider()
slider.value = 7
```

## Containers

### ListBox
```csharp
var listBox = window.FindFirstDescendant(cf => cf.ByAutomationId("ListBox"))?.AsListBox();
listBox.Select(0);
```
```python
list_box = window.find_first_descendant(cf.by_automation_id("ListBox")).as_list_box()
list_box.select(0)
```

### Tree
```csharp
var tree = window.FindFirstDescendant(cf => cf.ByControlType(ControlType.Tree))?.AsTree();
var node = tree.Items[0];
node.Expand();
```
```python
tree = window.find_first_descendant(cf.by_control_type(ControlType.Tree)).as_tree()
node = tree.items[0]
node.expand()
```

### Grid / DataGrid
```csharp
var grid = window.FindFirstDescendant(cf => cf.ByControlType(ControlType.DataGrid))?.AsGrid();
var cell = grid.Rows[0].Cells[1];
```
```python
grid = window.find_first_descendant(cf.by_control_type(ControlType.DataGrid)).as_grid()
cell = grid.rows[0].cells[1]
```

### Tab
```csharp
var tab = window.FindFirstDescendant(cf => cf.ByControlType(ControlType.Tab))?.AsTab();
tab.SelectTabItem("Complex Controls");
```
```python
tab = window.find_first_descendant(cf.by_control_type(ControlType.Tab)).as_tab()
tab.select_tab_item(value="Complex Controls")  # or select_tab_item(index=1)
```

## Display

### Label
```csharp
var label = window.FindFirstDescendant(cf => cf.ByAutomationId("Label"))?.AsLabel();
var text = label.Text;
```
```python
label = window.find_first_descendant(cf.by_automation_id("Label")).as_label()
text = label.text
```

### ProgressBar
```csharp
var bar = window.FindFirstDescendant(cf => cf.ByAutomationId("ProgressBar"))?.AsProgressBar();
var value = bar.Value;
```
```python
bar = window.find_first_descendant(cf.by_automation_id("ProgressBar")).as_progress_bar()
value = bar.value
```

## Windows & dialogs

### Modal dialogs
```csharp
var dialog = window.ModalWindows.First();
dialog.Close();
```
```python
dialog = window.modal_windows[0]
dialog.close()
```

### Title bar
```csharp
var titleBar = window.TitleBar;
titleBar.MinimizeButton.Invoke();
```
```python
title_bar = window.title_bar
title_bar.minimize_button.invoke()
```
