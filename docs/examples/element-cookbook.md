# Element Cookbook

C# snippets are hardcoded from FlaUI UITests; Python equivalents follow each.

## Button
```csharp
var button = window.FindFirstByXPath("//Button[@Name='OK']").AsButton();
button.Invoke();
```
```python
button = window.find_first_by_x_path("//Button[@Name='OK']").as_button()
button.invoke()
```

## CheckBox
```csharp
var cb = window.FindFirstDescendant(cf => cf.ByAutomationId("accept"))?.AsCheckBox();
cb.Toggle();
```
```python
cb = window.find_first_descendant(cf.by_automation_id("accept")).as_check_box()
cb.toggle()
```

## ComboBox
```csharp
var combo = window.FindFirstDescendant(cf => cf.ByAutomationId("Countries"))?.AsComboBox();
combo.Select("India");
```
```python
combo = window.find_first_descendant(cf.by_automation_id("Countries")).as_combo_box()
combo.select("India")
```

## Tree
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

## Grid
```csharp
var grid = window.FindFirstDescendant(cf => cf.ByControlType(ControlType.DataGrid))?.AsGrid();
var cell = grid.Rows[0].Cells[1];
```
```python
grid = window.find_first_descendant(cf.by_control_type(ControlType.DataGrid)).as_grid()
cell = grid.rows[0].cells[1]
```

## Window dialogs
```csharp
var dialog = window.ModalWindows.First();
dialog.Close();
```
```python
dialog = window.modal_windows[0]
dialog.close()
```
