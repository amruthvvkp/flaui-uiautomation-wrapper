# Porting C# tests

This wrapper mirrors FlaUI's C# test suite. Use this step-by-step process to port a test from
[`FlaUI.Core.UITests`](https://github.com/FlaUI/FlaUI/tree/master/src/FlaUI.Core.UITests) to Python.

For matrix fixtures and assertion helpers used below, see [Testing](testing.md).

## Step 1 — Locate the C# test

Find the corresponding test in the FlaUI repository, e.g.:

```
FlaUI/src/FlaUI.Core.UITests/Elements/ComboBoxTests.cs
```

## Step 2 — Create the Python test file

```
tests/ui/core/automation_elements/test_combobox.py
```

## Step 3 — Map the test class

Add a `Test` prefix so pytest collects it:

```python
# C#: class ComboBoxTests { }
class TestComboBoxElements:
    """Tests for the Combobox class."""
```

## Step 4 — Create element fixtures

```python
@pytest.fixture(name="editable_combo_box")
def get_editable_combobox_control(
    self,
    test_application: WinFormsApplicationElements | WPFApplicationElements,
) -> Generator[ComboBox, Any, None]:
    """Return the editable combobox element.

    :param test_application: Test application element map.
    :yield: Editable combobox element.
    """
    yield test_application.simple_controls_tab.editable_combo_box
```

## Step 5 — Port the test methods

```csharp
// C#
[TestMethod]
public void SelectedItemTest() {
    var comboBox = app.GetMainWindow()
        .FindFirstDescendant(cf => cf.ByAutomationId("EditableCombo"))
        .AsComboBox();
    comboBox.Items[1].Select();
    Assert.AreEqual("Item 2", comboBox.SelectedItem.Text);
}
```

```python
# Python
def test_selected_item(self, editable_combo_box: ComboBox) -> None:
    """Test the selected item property (C#: SelectedItemTest)."""
    editable_combo_box.items[1].select()
    assert editable_combo_box.selected_item == HasAttributes(text="Item 2")
```

## Step 6 — Use expressive assertions

```python
from dirty_equals import HasAttributes, IsFalseLike

assert checkbox.is_checked is True
assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Expanded)
assert combobox == HasAttributes(is_offscreen=IsFalseLike)
```

## Step 7 — Handle matrix-specific logic

Use `@pytest.mark.xfail` with a `condition` lambda when a test only fails for some matrix combinations:

```python
@pytest.mark.xfail(
    condition=lambda request: (
        request.getfixturevalue("ui_automation_type") == UIAutomationTypes.UIA2
        and request.getfixturevalue("test_application_type") == "WPF"
    ),
    reason="Known issue with UIA2 + WPF combination",
)
def test_specific_case(self, element: ComboBox) -> None:
    """Test that fails on UIA2 + WPF only."""
    ...
```

## Test application element maps

Tests address controls through page-object style element maps under
`tests/test_utilities/elements/`. Each map exposes properties that resolve controls lazily via the
condition factory.

```python
# tests/test_utilities/elements/winforms_application/base.py
class WinFormsApplicationElements(BaseSettings):
    """Element locators for the WinForms application."""

    main_window: Window

    @property
    def _cf(self) -> ConditionFactory:
        """Return the condition factory for the main window."""
        return self.main_window.condition_factory

    @property
    def simple_controls_tab(self) -> SimpleControlsElements:
        """Return the simple-controls tab element map."""
        return SimpleControlsElements(main_window=self.main_window, tab=self.tab)
```

```python
# tests/test_utilities/elements/winforms_application/simple_controls.py
class SimpleControlsElements(BaseSettings):
    """Element locators for the simple-controls tab."""

    main_window: Window
    tab: Tab

    @property
    def editable_combo_box(self) -> ComboBox:
        """Return the editable combo box element."""
        return self.main_window.find_first_descendant(
            condition=self._cf.by_automation_id("EditableCombo")
        ).as_combo_box()

    @property
    def read_only_checkbox(self) -> CheckBox:
        """Return the read-only checkbox element."""
        return self.main_window.find_first_descendant(
            condition=self._cf.by_automation_id("ReadOnlyCheckBox")
        ).as_check_box()
```

When you introduce a new control, add its locator to the matching element map so tests can reach it
in both the WinForms and WPF applications.
