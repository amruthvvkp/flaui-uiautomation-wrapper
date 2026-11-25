# Element Cookbook

Control-by-control recipes against the bundled WPF test application. Each recipe shows the
**Python** call next to the original FlaUI **C#** call. Pick a tab once and every recipe on the
page switches with it.

!!! success "Every Python snippet on this page runs"
    The Python tabs are included straight from
    [`examples/pytest/test_element_cookbook.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/examples/pytest/test_element_cookbook.py),
    one test per recipe, and the docs build fails if a referenced section disappears. Run them all:

    ```bash
    uv run pytest examples/pytest/test_element_cookbook.py -v
    ```

All recipes assume a `window` (the main `Window`) and a condition factory `cf`. The
[pytest example](pytest.md) shows how to get both. In C#, `cf` is the lambda parameter of
`FindFirstDescendant(cf => …)`.

## Interactive controls

### Button

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:button"
    ```

=== "C#"

    ```csharp
    var button = window.FindFirstDescendant(cf => cf.ByAutomationId("InvokableButton")).AsButton();
    button.Invoke(); // Invoke pattern: no mouse movement
    ```

### CheckBox

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:checkbox"
    ```

=== "C#"

    ```csharp
    var checkBox = window.FindFirstDescendant(cf => cf.ByName("Test Checkbox")).AsCheckBox();
    checkBox.Toggle();
    var state = checkBox.ToggleState; // ToggleState.On / Off / Indeterminate
    ```

### RadioButton

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:radio_button"
    ```

=== "C#"

    ```csharp
    var radio = window.FindFirstDescendant(cf => cf.ByAutomationId("RadioButton1")).AsRadioButton();
    radio.IsChecked = true;
    ```

### ComboBox

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:combo_box"
    ```

=== "C#"

    ```csharp
    var combo = window.FindFirstDescendant(cf => cf.ByAutomationId("NonEditableCombo")).AsComboBox();
    combo.Select("Item 2"); // or combo.Select(1)
    var selected = combo.SelectedItem.Text;
    ```

### TextBox

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:text_box"
    ```

=== "C#"

    ```csharp
    var textBox = window.FindFirstDescendant(cf => cf.ByAutomationId("TextBox")).AsTextBox();
    textBox.Text = "hello";  // Value pattern
    textBox.Enter(" world"); // Keyboard
    ```

### Slider

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:slider"
    ```

=== "C#"

    ```csharp
    var slider = window.FindFirstDescendant(cf => cf.ByAutomationId("Slider")).AsSlider();
    slider.Value = 6;
    Console.WriteLine($"{slider.Minimum} {slider.Value} {slider.Maximum}");
    ```

## Containers

### ListBox

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:list_box"
    ```

=== "C#"

    ```csharp
    var listBox = window.FindFirstDescendant(cf => cf.ByAutomationId("ListBox")).AsListBox();
    var item = listBox.Select("ListBox Item #2"); // or listBox.Select(1)
    var names = listBox.Items.Select(i => i.Text).ToList();
    ```

### Tree

The tree lives on the **Complex Controls** tab. The runnable test switches to that tab first.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:tree"
    ```

=== "C#"

    ```csharp
    var tree = window.FindFirstDescendant(cf => cf.ByAutomationId("treeView1")).AsTree();
    tree.Items[0].Expand();
    tree.Items[0].Items[1].Expand();
    tree.Items[0].Items[1].Items[0].Select();
    var selected = tree.SelectedTreeItem.Text;
    ```

### Grid

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:grid"
    ```

=== "C#"

    ```csharp
    var grid = window.FindFirstDescendant(cf => cf.ByAutomationId("listView1")).AsGrid();
    var headers = grid.Header.Columns.Select(c => c.Name).ToList(); // ["Key", "Value"]
    var firstRow = grid.Rows[0].Cells.Select(c => c.Value).ToList(); // ["1", "10"]
    grid.Select(1);
    ```

### Tab

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:tab"
    ```

=== "C#"

    ```csharp
    tab.SelectTabItem(1); // "Complex Controls"
    var selected = tab.SelectedTabItem.Name;
    ```

## Display

### Label

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:label"
    ```

=== "C#"

    ```csharp
    var label = window.FindFirstDescendant(cf => cf.ByText("Test Label")).AsLabel();
    var text = label.Text;
    ```

### ProgressBar

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:progress_bar"
    ```

=== "C#"

    ```csharp
    var bar = window.FindFirstDescendant(cf => cf.ByAutomationId("ProgressBar")).AsProgressBar();
    var progress = (bar.Value - bar.Minimum) / (bar.Maximum - bar.Minimum);
    ```

## Windows & dialogs

=== "Python"

    ```python
    --8<-- "examples/pytest/test_element_cookbook.py:window"
    ```

=== "C#"

    ```csharp
    Console.WriteLine(window.Title);   // "FlaUI WPF Test App"
    var dialogs = window.ModalWindows; // empty while no modal dialog is open
    var titleBar = window.TitleBar;    // .MinimizeButton / .MaximizeButton / .RestoreButton / .CloseButton
    ```

!!! note "Title bar buttons"
    FlaUI finds the title bar buttons by their AutomationIds. Standard Win32 and Store windows
    expose them; the WPF test app's title bar does not. The [Calculator gallery](gallery.md#calculator)
    script is an example where they work.
