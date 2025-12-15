# FlaUI Python Wrapper - Comprehensive Development Guide

**Last Updated**: December 15, 2025

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [PythonNet Bridge](#pythonnet-bridge)
- [C# to Python Mapping Patterns](#c-to-python-mapping-patterns)
- [Pydantic Validation](#pydantic-validation)
- [Pytest Matrix Configuration](#pytest-matrix-configuration)
- [Test Porting Methodology](#test-porting-methodology)
- [Development Workflow](#development-workflow)
- [CI/CD Configuration](#cicd-configuration)
- [Coding Standards](#coding-standards)
- [Key Files Reference](#key-files-reference)

---

## Project Overview

This project is a **Python port of the FlaUI C# library** for Windows UI automation. It provides **1:1 mapping** of all exposed C# endpoints using PythonNet, enabling full FlaUI capabilities in Python with complete feature parity.

### Key Differentiators
- **Complete Feature Parity**: Unlike RobotFlaUI (limited to Robot Framework and XPath), this wrapper provides plug-and-play Python access to the complete FlaUI API
- **Type Safety**: All input/output backed by Pydantic models for IDE intellisense and data validation
- **Any Test Framework**: Works with pytest, unittest, or any Python test framework
- **Pythonic API**: Snake_case methods with Python-native types while maintaining C# structure

### Repository Structure
```
flaui/
├── bin/               # C# DLLs (FlaUI.Core, UIA2, UIA3) - packaged in wheel
├── core/              # Core automation element wrappers
│   ├── automation_elements.py    # Main element classes (3309 lines)
│   ├── condition_factory.py
│   ├── definitions.py            # Enums and constants
│   └── ...
├── lib/               # Supporting libraries
│   ├── pythonnet_bridge.py       # PythonNet initialization
│   ├── exceptions.py             # Exception translation
│   ├── enums.py
│   ├── collections.py            # Type conversion utilities
│   └── system/
│       └── drawing.py            # System.Drawing wrappers
└── modules/           # High-level automation
    └── automation.py             # Automation class (UIA2/UIA3)

tests/
├── conftest.py                   # Global fixtures and matrix setup
├── ui/                           # UI automation tests
│   ├── core/
│   │   ├── automation_elements/  # Element-specific tests
│   │   └── patterns/             # Pattern tests
└── unit/                         # Unit tests
    └── lib/

test_applications/                # WinForms and WPF test apps
test_utilities/                   # Test element mappings
├── base.py                       # FlaUITestBase
└── elements/
    ├── winforms_application/     # WinForms element map
    └── wpf_application/          # WPF element map
```

---

## Architecture

### Hierarchical Class Structure

The Python wrapper follows a **4-layer inheritance hierarchy** that mirrors FlaUI C#:

```
1. ElementModel (Pydantic BaseModel)
   ↓ - Validates raw_element exists
   ↓ - Holds C# object reference

2. ElementBase (extends ElementModel)
   ↓ - Common properties (name, automation_id, bounding_rectangle, etc.)
   ↓ - All properties decorated with @handle_csharp_exceptions

3. Pattern Mixins (ABC)
   ↓ - InvokeAutomationElement (invoke() method)
   ↓ - ToggleAutomationElement (toggle(), toggle_state)
   ↓ - SelectionItemAutomationElement (select(), is_selected)

4. Concrete Elements (multiple inheritance)
   - Button(AutomationElement, InvokeAutomationElement)
   - CheckBox(AutomationElement, ToggleAutomationElement)
   - ComboBox(AutomationElement) with custom methods
```

#### Layer 1: ElementModel (Base Validation)

```python
# From flaui/core/automation_elements.py
from pydantic import BaseModel, Field, ValidationInfo, field_validator

class ElementModel(BaseModel, abc.ABC):
    """Base Pydantic model for all automation elements"""
    raw_element: Any = Field(
        ...,
        title="Automation Element",
        description="Contains the C# automation element in raw form"
    )

    @field_validator("raw_element")
    def validate_element_exists(cls, v: Any, info: ValidationInfo) -> Any:
        """Validate the element exists"""
        if v is None:
            raise ElementNotFound("Element does not exist")
        return v
```

#### Layer 2: ElementBase (Common Properties)

```python
class ElementBase(ElementModel, abc.ABC):
    """Automation Element base abstract class"""

    @property
    @handle_csharp_exceptions
    def automation_id(self) -> str:
        """The automation id of the element"""
        return self.raw_element.AutomationId

    @property
    @handle_csharp_exceptions
    def name(self) -> str:
        """The name of the element"""
        return self.raw_element.Name

    @property
    @handle_csharp_exceptions
    def bounding_rectangle(self) -> Rectangle:
        """The bounding rectangle of this element"""
        return Rectangle(raw_value=self.raw_element.BoundingRectangle)
```

#### Layer 3: Pattern Mixins

```python
class InvokeAutomationElement(ElementModel, abc.ABC):
    """An element that supports the InvokePattern"""

    @handle_csharp_exceptions
    def invoke(self) -> None:
        """Invokes the element."""
        self.raw_element.Invoke()


class ToggleAutomationElement(ElementModel, abc.ABC):
    """Class for an element that supports the TogglePattern"""

    @property
    @handle_csharp_exceptions
    def toggle_state(self) -> ToggleState:
        """Gets the current toggle state."""
        return ToggleState(self.raw_element.ToggleState)

    @handle_csharp_exceptions
    def toggle(self) -> None:
        """Toggles the element."""
        self.raw_element.Toggle()
```

#### Layer 4: Concrete Elements

```python
class Button(AutomationElement, InvokeAutomationElement):
    """Class to interact with a button element"""
    pass  # Inherits invoke() and all AutomationElement methods


class CheckBox(AutomationElement, ToggleAutomationElement):
    """Class to interact with a checkbox element"""

    @property
    @handle_csharp_exceptions
    def is_checked(self) -> bool:
        """Flag if the element is checked"""
        return self.raw_element.IsChecked

    @property
    @handle_csharp_exceptions
    def text(self) -> str:
        """Gets the text of the element"""
        return self.raw_element.Text
```

---

## PythonNet Bridge

### Critical Initialization Pattern

**RULE #1**: Always call `setup_pythonnet_bridge()` **BEFORE** importing any C# types.

#### Bridge Setup Function

```python
# From flaui/lib/pythonnet_bridge.py
import clr
from loguru import logger
from System.Reflection import Assembly

def setup_pythonnet_bridge() -> None:
    """
    Sets up Python.NET bridge for FlaUI and automation dependencies.
    Loads all C# DLLs from flaui/bin/ into Python runtime.

    :raises err: On failure to load C# dependencies
    """
    BIN_HOME = config.settings.BIN_HOME  # Path to flaui/bin/
    global FLAUI_CSHARP_VERSION

    try:
        for dll_path in BIN_HOME.glob("*.dll"):
            clr.AddReference(dll_path.as_posix())
            clr.AddReference(dll_path.stem)
            assembly = Assembly.LoadFile(dll_path.as_posix())
            version = assembly.GetName().Version
            logger.info(f"Added {dll_path.name} v{version} DLL to Python.NET bridge")

            if dll_path.name == "FlaUI.Core.dll":
                FLAUI_CSHARP_VERSION = str(version)
    except Exception as err:
        logger.exception(f"{err}")
        raise err

    logger.info("Python.NET bridge setup complete")
```

#### Correct Usage in Tests

```python
# From tests/conftest.py - CORRECT ORDER
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
import pytest

# isort: off  # Prevent auto-sorting from breaking the order

setup_pythonnet_bridge()  # ← MUST BE FIRST

# Now safe to import C# types
from loguru import logger
from flaui.lib.enums import UIAutomationTypes
from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
```

#### Late Imports in Methods

For circular dependency prevention, use **late imports inside methods**:

```python
def as_button(self) -> Button:
    """Converts the element to a Button."""
    # Import C# type only when needed
    from FlaUI.Core.AutomationElements import Button as CSButton
    return Button(raw_element=CSButton(self.framework_automation_element))

def as_combo_box(self) -> ComboBox:
    """Converts the element to a ComboBox."""
    from FlaUI.Core.AutomationElements import ComboBox as CSComboBox
    return ComboBox(raw_element=CSComboBox(self.framework_automation_element))
```

#### Included C# Binaries

Located in `flaui/bin/`:
- **FlaUI.Core.dll** - Core automation library
- **FlaUI.UIA2.dll** - UI Automation 2 provider
- **FlaUI.UIA3.dll** - UI Automation 3 provider
- **Interop.UIAutomationClient.dll** - COM interop
- **System.CodeDom.dll** - Code DOM support

---

## C# to Python Mapping Patterns

### Naming Conventions

| C# | Python | Example |
|----|--------|---------|
| Classes | PascalCase → PascalCase | `Button` → `Button` |
| Methods | PascalCase → snake_case | `Click()` → `click()` |
| Properties | PascalCase → snake_case | `BoundingRectangle` → `bounding_rectangle` |
| Enums | PascalCase.Member → PascalCase.Member | `ControlType.Button` → `ControlType.Button` |

### Property Translation Pattern

**C# Property:**
```csharp
public string Name => Properties.Name.Value;
```

**Python Equivalent:**
```python
@property
@handle_csharp_exceptions
def name(self) -> str:
    """The name of the element"""
    return self.raw_element.Name
```

### Method Translation Pattern

**C# Method:**
```csharp
public void Click(bool moveMouseToClickablePoint = false) {
    PerformClick(moveMouseToClickablePoint);
}
```

**Python Equivalent:**
```python
@handle_csharp_exceptions
def click(self, move_mouse: bool = False) -> None:
    """Performs a left click on the element.

    :param move_mouse: Flag to indicate if mouse should move slowly (True) or instantly (False)
    """
    self.raw_element.Click(move_mouse)
```

### Type Conversion Pattern

#### C# Collections to Python

```python
# From flaui/lib/collections.py
class TypeCast:
    """Type conversion utilities for C#/Python interop"""

    @staticmethod
    def py_list(raw: Any) -> List[Any]:
        """Converts C# IEnumerable → Python list"""
        return raw if isinstance(raw, list) else list(map(lambda x: x, raw))

    @staticmethod
    def py_dict(raw: Any) -> Dict[Any, Any]:
        """Converts C# Dictionary → Python dict"""
        return raw if isinstance(raw, dict) else {_.Key: _.Value for _ in raw.GetEnumerator()}
```

#### Python to C# Types

```python
@staticmethod
def cs_timespan(value: int) -> TimeSpan:
    """Converts Python milliseconds → C# TimeSpan"""
    if value is None:
        return None
    return TimeSpan.FromMilliseconds(value)

@staticmethod
def cs_datetime(date: date) -> CSDateTime:
    """Converts Python date → C# DateTime"""
    return CSDateTime.Parse(arrow.get(date).strftime("%Y-%m-%d"))
```

### Complex Property with Wrapper

**C# Property:**
```csharp
public Rectangle BoundingRectangle => Properties.BoundingRectangle.Value;
```

**Python with Wrapper:**
```python
@property
@handle_csharp_exceptions
def bounding_rectangle(self) -> Rectangle:
    """The bounding rectangle of this element"""
    # Wrap C# Rectangle in Python Rectangle class
    return Rectangle(raw_value=self.raw_element.BoundingRectangle)
```

### Method with Type Conversion

**C# Method:**
```csharp
public AutomationElement[] FindAllChildren(ConditionBase condition = null) {
    return condition == null
        ? FrameworkElement.FindAllChildren()
        : FrameworkElement.FindAllChildren(condition);
}
```

**Python Equivalent:**
```python
@handle_csharp_exceptions
def find_all_children(self, condition: Optional[PropertyCondition] = None) -> List[AutomationElement]:
    """Finds all children with the condition.

    :param condition: The search condition.
    :return: The found elements or an empty list if no elements were found.
    """
    if condition is None:
        # Convert C# array to Python list
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllChildren()]
    else:
        return [AutomationElement(raw_element=_)
                for _ in self.raw_element.FindAllChildren(condition.cs_condition)]
```

### Enum Translation

**C# Enum:**
```csharp
public enum ToggleState {
    Off = 0,
    On = 1,
    Indeterminate = 2
}
```

**Python Enum:**
```python
from enum import Enum

class ToggleState(Enum):
    """Toggle state values"""
    Off = 0
    On = 1
    Indeterminate = 2
```

**Usage in Property:**
```python
@property
@handle_csharp_exceptions
def toggle_state(self) -> ToggleState:
    """Gets the current toggle state."""
    # Convert C# enum to Python enum
    return ToggleState(self.raw_element.ToggleState)
```

---

## Pydantic Validation

### Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class PropertyCondition(BaseModel):
    """Base condition model"""
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Allow C# types
    cs_condition: Union[CSPropertyCondition, CSOrCondition, CSAndCondition]
```

### Field Validators

```python
from pydantic import field_validator, ValidationInfo

class ElementModel(BaseModel):
    raw_element: Any = Field(..., description="C# automation element")

    @field_validator("raw_element")
    def validate_element_exists(cls, v: Any, info: ValidationInfo) -> Any:
        """Validate the element exists"""
        if v is None:
            raise ElementNotFound("Element does not exist")
        return v
```

### System.Drawing Wrapper Pattern

```python
# From flaui/lib/system/drawing.py
from pydantic import BaseModel, field_validator
from System.Drawing import Point as CSPoint

class Point(BaseModel):
    """Python wrapper for System.Drawing.Point"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_value: Optional[CSPoint] = None
    x: Optional[int] = None
    y: Optional[int] = None

    @field_validator("raw_value")
    def validate_raw_or_coordinates(cls, v, info):
        """Accepts either raw C# Point OR x/y values"""
        data = info.data
        if v is None and (data.get("x") is None or data.get("y") is None):
            raise ValueError("Either raw_value or both x and y must be provided")
        return v

    @property
    def cs_object(self) -> CSPoint:
        """Returns C# Point object"""
        if self.raw_value is not None:
            return self.raw_value
        return CSPoint(self.x, self.y)
```

### Benefits of Pydantic Approach

1. **IDE Autocomplete**: Full intellisense for all properties and methods
2. **Runtime Validation**: Catches type mismatches before C# interop
3. **Clear Error Messages**: Python exceptions instead of cryptic C# errors
4. **Type Safety**: Type hints for static analysis tools

---

## Pytest Matrix Configuration

### The Challenge

Tests must run across a **4-combination matrix**:
- **UI Automation**: UIA2 vs UIA3
- **Test Application**: WinForms vs WPF

Most test logic is identical across combinations, with only a few exceptions (e.g., WinForms ComboBox is broken).

### Solution: Fixture-Based Parametrization

This approach keeps tests clean and handles matrix logic in fixtures, not test bodies.

#### Step 1: Session-Level Application Launcher

```python
# From tests/conftest.py
@pytest.fixture(scope="session")
def launch_all_test_applications() -> Generator[dict[UIAutomationTypes, dict[str, FlaUITestBase]], Any, None]:
    """
    Fixture to launch all test applications ONCE per session.
    Creates all 4 combinations: UIA2/UIA3 × WinForms/WPF.
    """
    result = {UIAutomationTypes.UIA2: {}, UIAutomationTypes.UIA3: {}}

    # Launch all 4 combinations
    for app_type in ["WinForms", "WPF"]:
        for ui_automation_type in [UIAutomationTypes.UIA2, UIAutomationTypes.UIA3]:
            test_base = FlaUITestBase(ui_automation_type, app_type)
            try:
                logger.debug(f"Launching test application: {app_type} with {ui_automation_type}")
                test_base.launch_test_app()
                time.sleep(1)  # Give time for UI to initialize
                assert test_base.automation.application, "Application did not start correctly!"
            except Exception as e:
                logger.error(f"Error launching test app: {e}")
                pytest.exit("Test application failed to launch!")
            else:
                result[ui_automation_type][app_type] = test_base

    yield result

    # Cleanup all applications
    for ui_automation_type in [UIAutomationTypes.UIA2, UIAutomationTypes.UIA3]:
        for app_type in ["WinForms", "WPF"]:
            test_base = result[ui_automation_type][app_type]
            test_base.close_test_app()
            gc.collect()
```

#### Step 2: Parametrized Test Environment Fixture

```python
@pytest.fixture(
    scope="session",
    params=[
        pytest.param((UIAutomationTypes.UIA2, "WinForms"), id="UIA2_WinForms"),
        pytest.param((UIAutomationTypes.UIA2, "WPF"), id="UIA2_WPF"),
        pytest.param((UIAutomationTypes.UIA3, "WinForms"), id="UIA3_WinForms"),
        pytest.param((UIAutomationTypes.UIA3, "WPF"), id="UIA3_WPF"),
    ],
)
def setup_ui_testing_environment(
    request: pytest.FixtureRequest,
    launch_all_test_applications: dict[UIAutomationTypes, dict[str, FlaUITestBase]]
) -> Generator[FlaUITestBase, Any, None]:
    """
    Fixture that parametrizes tests across all 4 matrix combinations.
    Each test class using this fixture will run 4 times automatically.
    """
    ui_automation_type, test_application_type = request.param
    yield launch_all_test_applications[ui_automation_type][test_application_type]
```

#### Step 3: Test Application Element Map Fixture

```python
@pytest.fixture(scope="class", name="test_application")
def get_ui_test_application(
    setup_ui_testing_environment: FlaUITestBase,
) -> Generator[WinFormsApplicationElements | WPFApplicationElements, Any, None]:
    """
    Fixture to get the test application element map.
    Returns WinForms or WPF element map based on current parametrization.
    """
    application = setup_ui_testing_environment.automation.application
    automation = setup_ui_testing_environment.automation.cs_automation
    test_application_type = setup_ui_testing_environment.app_type

    # Select appropriate element map
    elements = (
        get_winforms_application_elements(application.get_main_window(automation))
        if test_application_type == "WinForms"
        else get_wpf_application_elements(application.get_main_window(automation))
    )

    # Navigate to Simple Controls tab
    try:
        elements.main_window.find_first_descendant(
            condition=elements._cf.by_name("Simple Controls")
        ).as_tab_item().click()
    except ElementNotFound as e:
        logger.error(f"Error: {e}")

    yield elements
```

#### Step 4: Helper Fixtures for Test Context

```python
@pytest.fixture()
def ui_automation_type(setup_ui_testing_environment: FlaUITestBase) -> Generator[UIAutomationTypes, None, None]:
    """Fixture to get the UIAutomation type (UIA2 or UIA3)."""
    yield setup_ui_testing_environment.ui_automation_type


@pytest.fixture()
def test_application_type(setup_ui_testing_environment: FlaUITestBase) -> Generator[str, None, None]:
    """Fixture to get the test application type (WinForms or WPF)."""
    yield setup_ui_testing_environment.app_type
```

### Writing Tests with Matrix Support

#### Basic Test (Runs on All 4 Combinations)

```python
# From tests/ui/core/automation_elements/test_checkbox.py
class TestCheckBoxElements:
    """Tests for the CheckBox class."""

    @pytest.fixture(name="read_only_checkbox")
    def get_read_only_checkbox_control(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[CheckBox, Any, None]:
        """Returns the read-only checkbox element."""
        yield test_application.simple_controls_tab.read_only_checkbox

    def test_properties(self, read_only_checkbox: CheckBox) -> None:
        """Tests the properties of the checkbox."""
        # This test runs 4 times automatically (UIA2/UIA3 × WinForms/WPF)
        assert read_only_checkbox.toggle_state == ToggleState.Off
        assert not read_only_checkbox.is_checked
```

#### Test with Conditional Skip

Use `@pytest.mark.xfail` with lambda for dynamic skipping:

```python
@pytest.mark.xfail(
    condition=lambda request: request.getfixturevalue("test_application_type") == "WinForms",
    reason="Combobox got heavily broken with UIA2/UIA3 Winforms due to bugs in Windows/.Net"
)
class TestComboBoxElements:
    """Tests for the Combobox class."""

    @pytest.fixture(name="editable_combo_box")
    def get_editable_combobox_control(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> Generator[ComboBox, Any, None]:
        """Returns the editable combobox element."""
        yield test_application.simple_controls_tab.editable_combo_box

    def test_selected_item(self, editable_combo_box: ComboBox) -> None:
        """Tests the selected item property."""
        # Runs on WPF (both UIA2/UIA3), marked xfail on WinForms
        editable_combo_box.items[1].select()
        assert editable_combo_box.selected_item == HasAttributes(text="Item 2")
```

#### Alternative: Fixture-Level Skip

```python
class TestComboBoxElements:
    @pytest.fixture
    def skip_winforms(self, test_application_type: str) -> None:
        """Skip WinForms tests."""
        if test_application_type == "WinForms":
            pytest.skip("Combobox broken with WinForms")

    @pytest.fixture(name="editable_combo_box")
    def get_editable_combobox_control(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
        skip_winforms: None  # ← Skip applied here
    ) -> Generator[ComboBox, Any, None]:
        yield test_application.simple_controls_tab.editable_combo_box
```

### Running Tests

```bash
# Run all tests with all parametrizations
uv run pytest tests/ui/core/automation_elements/test_combobox.py -v

# Run only UIA3 + WPF combination
uv run pytest tests/ui/ -k "UIA3_WPF"

# Run only WinForms tests
uv run pytest tests/ui/ -k "WinForms"

# Run with coverage
uv run --group unit-test --extra coverage coverage run -m pytest
```

### Test Output Example

```
test_combobox.py::TestComboBoxElements::test_selected_item[UIA2_WinForms] XFAIL
test_combobox.py::TestComboBoxElements::test_selected_item[UIA2_WPF] PASSED
test_combobox.py::TestComboBoxElements::test_selected_item[UIA3_WinForms] XFAIL
test_combobox.py::TestComboBoxElements::test_selected_item[UIA3_WPF] PASSED
```

---

## Test Porting Methodology

### Step-by-Step C# Test Port Process

#### 1. Locate C# Test

Find the corresponding test in FlaUI repository:
```
FlaUI/src/FlaUI.Core.UITests/Elements/ComboBoxTests.cs
```

#### 2. Create Python Test File

```
tests/ui/core/automation_elements/test_combobox.py
```

#### 3. Map Test Class

```python
# C# class name
class ComboBoxTests { }

# Python equivalent (add "Test" prefix for pytest)
class TestComboBoxElements:
    """Tests for the Combobox class."""
```

#### 4. Create Element Fixtures

```python
@pytest.fixture(name="editable_combo_box")
def get_editable_combobox_control(
    self,
    test_application: WinFormsApplicationElements | WPFApplicationElements
) -> Generator[ComboBox, Any, None]:
    """Returns the editable combobox element.

    :param test_application: Test application elements.
    :yield: Editable combobox element.
    """
    yield test_application.simple_controls_tab.editable_combo_box
```

#### 5. Port Test Methods

**C# Test:**
```csharp
[TestMethod]
public void SelectedItemTest() {
    var app = Application.Launch("WpfApplication.exe");
    var comboBox = app.GetMainWindow().FindFirstDescendant(cf => cf.ByAutomationId("EditableCombo")).AsComboBox();
    comboBox.Items[1].Select();
    Assert.AreEqual("Item 2", comboBox.SelectedItem.Text);
}
```

**Python Test:**
```python
def test_selected_item(self, editable_combo_box: ComboBox) -> None:
    """Tests the selected item property (C#: SelectedItemTest)."""
    editable_combo_box.items[1].select()
    assert editable_combo_box.selected_item == HasAttributes(text="Item 2")
```

#### 6. Use PyHamcrest for Assertions

```python
from pyhamcrest import assert_that, equal_to, has_property
from dirty_equals import HasAttributes, IsFalseLike

# Basic equality
assert checkbox.is_checked == True

# Property matching
assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Expanded)

# Negation
assert combobox == HasAttributes(is_offscreen=IsFalseLike)
```

#### 7. Handle Matrix-Specific Logic

```python
@pytest.mark.xfail(
    condition=lambda request: (
        request.getfixturevalue("ui_automation_type") == UIAutomationTypes.UIA2
        and request.getfixturevalue("test_application_type") == "WPF"
    ),
    reason="Known issue with UIA2 + WPF combination"
)
def test_specific_case(self, element: ComboBox) -> None:
    """Test that fails on UIA2 + WPF only."""
    # Test logic
```

### Test Application Element Mapping

#### WinForms Element Map

```python
# From tests/test_utilities/elements/winforms_application/base.py
class WinFormsApplicationElements(BaseSettings):
    """Element locators for the WinForms application."""

    main_window: Window

    @property
    def _cf(self) -> ConditionFactory:
        """Returns the condition factory element."""
        return self.main_window.condition_factory

    @property
    def simple_controls_tab(self) -> SimpleControlsElements:
        """Returns the simple controls tab element and all child controls."""
        return SimpleControlsElements(main_window=self.main_window, tab=self.tab)
```

#### Simple Controls Sub-Map

```python
# From tests/test_utilities/elements/winforms_application/simple_controls.py
class SimpleControlsElements(BaseSettings):
    """Element locators for simple controls tab."""

    main_window: Window
    tab: Tab

    @property
    def editable_combo_box(self) -> ComboBox:
        """Returns the editable combo box element."""
        return self.main_window.find_first_descendant(
            condition=self._cf.by_automation_id("EditableCombo")
        ).as_combo_box()

    @property
    def read_only_checkbox(self) -> CheckBox:
        """Returns the read-only checkbox element."""
        return self.main_window.find_first_descendant(
            condition=self._cf.by_automation_id("ReadOnlyCheckBox")
        ).as_check_box()
```

---

## Development Workflow

### UV Package Manager Commands

```bash
# Install all dependencies (including dev and test groups)
uv sync --all-groups --all-extras

# Build wheel
uv build

# Bump version
uv version 0.2.0

# Update all dependencies
uv sync --all-groups --all-extras -U

# Run tests
uv run --group unit-test pytest tests/ui/ -v

# Run with coverage
uv run --group unit-test --extra coverage coverage run -m pytest
uv run --no-project --with coverage coverage html
```

### Code Quality Tools

```bash
# Ruff linting (check only)
ruff check .

# Ruff auto-fix
ruff check --fix .

# Format code
ruff format .

# Interrogate docstring coverage (95% required)
interrogate flaui/ --fail-under=95
```

### Pre-commit Hooks

Defined in `.pre-commit-config.yaml`:
- Trailing whitespace removal
- EOF fixes
- Ruff linting and formatting
- Interrogate docstring checks
- Python AST validation

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Exception Handling

All C# interop must use the `@handle_csharp_exceptions` decorator:

```python
# From flaui/lib/exceptions.py
def handle_csharp_exceptions(func):
    """Wraps function to handle C# FlaUI exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except CSharpPropertyNotSupportedException as e:
            raise PropertyNotSupportedException(f"...'{func.__name__}'...")
        except CSharpElementNotAvailableException as e:
            raise ElementNotAvailableException(f"...'{func.__name__}'...")
        except System.Exception as e:
            raise SystemException(f"...'{func.__name__}'...")
    return wrapper
```

**Usage:**
```python
@property
@handle_csharp_exceptions  # ← Always use this decorator
def name(self) -> str:
    """The name of the element"""
    return self.raw_element.Name
```

### Custom Exceptions

```python
# Python equivalents of C# FlaUI exceptions
class ElementNotFound(Exception):
    """Element does not exist in the UI tree"""

class PropertyNotSupportedException(Exception):
    """Property not supported by this element"""

class ElementNotEnabledException(Exception):
    """Element is disabled and cannot be interacted with"""

class NoClickablePointException(Exception):
    """No clickable point found for this element"""
```

---

## CI/CD Configuration

### AppVeyor Configuration

#### Matrix Testing

```yaml
# From .appveyor.yml
environment:
  matrix:
    - job_name: Python 3.12 x64
      PYTHON: "C:\\Python312"
      PYTHON_VERSION: 3.12
      PYTHON_ARCH: 64
```

#### Build Script

```yaml
test_script:
  - ps: |
      $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
      Write-Host "Running tests with pytest..."
      uv run --group unit-test --no-dev --package flaui-uiautomation-wrapper --extra coverage coverage run -m pytest --junit-xml=test-results.xml
      if ($LASTEXITCODE -ne 0) { Write-Host "Tests failed."; exit 1 }
      Write-Host "Tests completed."
```

#### Coverage Reporting

```yaml
after_test:
  - ps: |
      Write-Host "Generating test coverage report..."
      uv run --no-project --with coverage coverage combine
      uv run --no-project --with coverage coverage xml
      uv run --no-project --with coverage coverage html
      Write-Host "Coverage report generated."
```

### Python Compatibility Matrix

Tested on:
- **Python 3.8** (x86, x64)
- **Python 3.9** (x86, x64)
- **Python 3.10** (x86, x64)
- **Python 3.11** (x86, x64)
- **Python 3.12** (x86, x64)
- **Python 3.13** (x64)

Currently CI runs on **Python 3.12 x64** only (other versions commented out for speed).

---

## Coding Standards

### 1. Mirror C# API

**Rule**: All classes/methods must match FlaUI C# structure for 1:1 feature parity.

```python
# C# class hierarchy
class Button : InvokeAutomationElement { }

# Python must match
class Button(AutomationElement, InvokeAutomationElement):
    pass
```

### 2. Pydantic for All Models

**Rule**: Use `BaseModel` for validation and type safety.

```python
class ElementModel(BaseModel, abc.ABC):
    raw_element: Any = Field(..., description="C# automation element")

    @field_validator("raw_element")
    def validate_element_exists(cls, v: Any, info: ValidationInfo) -> Any:
        if v is None:
            raise ElementNotFound("Element does not exist")
        return v
```

### 3. Exception Decoration

**Rule**: All C# interop must use `@handle_csharp_exceptions`.

```python
@property
@handle_csharp_exceptions  # ← Required
def name(self) -> str:
    return self.raw_element.Name
```

### 4. Type Conversion

**Rule**: Translate C# types to Python equivalents or wrappers.

```python
# C# returns System.Drawing.Rectangle
@property
@handle_csharp_exceptions
def bounding_rectangle(self) -> Rectangle:  # Python Rectangle wrapper
    return Rectangle(raw_value=self.raw_element.BoundingRectangle)
```

### 5. Docstrings

**Rule**: Google-style docstrings for all public methods.

```python
def find_all_children(self, condition: Optional[PropertyCondition] = None) -> List[AutomationElement]:
    """Finds all children with the condition.

    :param condition: The search condition.
    :return: The found elements or an empty list if no elements were found.
    """
```

### 6. Type Hints

**Rule**: Full type annotations (Python 3.8+ compatible).

```python
from typing import List, Optional, Union  # Not list, optional (3.10+)

def select(self, value: Union[int, str]) -> ComboBoxItem:
    """Select by index or text."""
    return ComboBoxItem(raw_element=self.raw_element.Select(value))
```

### 7. PythonNet First

**Rule**: Always call `setup_pythonnet_bridge()` before C# imports.

```python
# ✅ CORRECT
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
setup_pythonnet_bridge()
from FlaUI.Core import AutomationBase

# ❌ WRONG
from FlaUI.Core import AutomationBase  # Will fail - DLLs not loaded
```

### 8. Test-Specific Rules

#### Type Hints in Tests

```python
# ✅ CORRECT
def test_checkbox(self, checkbox: CheckBox) -> None:
    assert checkbox.is_checked

# ❌ WRONG (missing type hint)
def test_checkbox(self, checkbox):
    assert checkbox.is_checked
```

#### Enum Usage

```python
# ✅ CORRECT
assert element.toggle_state == ToggleState.On

# ❌ WRONG (using strings)
assert element.toggle_state == "On"
```

#### UV Command Prefix

```bash
# ✅ CORRECT
uv run pytest tests/

# ❌ WRONG
pytest tests/  # May use wrong Python environment
```

---

## Key Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| [flaui/core/automation_elements.py](flaui/core/automation_elements.py) | **Main element mapping** - All automation element classes | 3309 |
| [flaui/lib/pythonnet_bridge.py](flaui/lib/pythonnet_bridge.py) | PythonNet initialization, DLL loading | 50 |
| [flaui/lib/exceptions.py](flaui/lib/exceptions.py) | C# exception → Python exception mapping | 186 |
| [flaui/lib/system/drawing.py](flaui/lib/system/drawing.py) | System.Drawing wrappers (Point, Rectangle, Color) | 300 |
| [flaui/lib/enums.py](flaui/lib/enums.py) | Enum wrappers (ControlType, ToggleState, TreeScope) | 400 |
| [flaui/lib/collections.py](flaui/lib/collections.py) | Type conversion utilities (C# ↔ Python) | 50 |
| [flaui/core/condition_factory.py](flaui/core/condition_factory.py) | Search condition builders | 200 |
| [flaui/modules/automation.py](flaui/modules/automation.py) | High-level Automation class (UIA2/UIA3 setup) | 100 |
| [tests/conftest.py](tests/conftest.py) | Global test fixtures, matrix parametrization | 146 |
| [tests/test_utilities/base.py](tests/test_utilities/base.py) | FlaUITestBase class for test applications | 100 |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Project overview and coding standards | 100 |

---

## Quick Reference

### Common Tasks

#### Add New Element Class

1. Find C# class in `FlaUI/src/FlaUI.Core/AutomationElements/`
2. Create Python class extending appropriate mixins:
   ```python
   class NewElement(AutomationElement, InvokeAutomationElement):
       """Class to interact with a new element"""
   ```
3. Add properties and methods with `@handle_csharp_exceptions`
4. Add `as_new_element()` method to `AutomationElement`
5. Write tests in `tests/ui/core/automation_elements/test_new_element.py`

#### Add Test for Existing Element

1. Locate C# test in `FlaUI/src/FlaUI.Core.UITests/`
2. Create test class: `class TestElementName:`
3. Create element fixture(s)
4. Port test methods with descriptive docstrings
5. Add matrix skip logic if needed
6. Run: `uv run pytest tests/ui/core/automation_elements/test_element.py -v`

#### Debug PythonNet Issues

1. Ensure `setup_pythonnet_bridge()` called first
2. Check DLL versions: `flaui/bin/Version.md`
3. Use late imports for circular dependencies
4. Check exception translation in `flaui/lib/exceptions.py`

#### Add New Property to Element

```python
@property
@handle_csharp_exceptions
def new_property(self) -> str:
    """Description of the new property.

    :return: Property value
    """
    return self.raw_element.NewProperty
```

---

## Best Practices

### ✅ DO

- **Always** call `setup_pythonnet_bridge()` first
- Use `@handle_csharp_exceptions` on all C# interop
- Follow PascalCase → snake_case naming conversion
- Add comprehensive docstrings (95% coverage required)
- Use fixture parametrization for matrix testing
- Type hint everything (including test fixtures)
- Convert C# types to Python wrappers when appropriate
- Test on multiple Python versions locally

### ❌ DON'T

- Import C# types before bridge setup
- Use strings instead of enums
- Skip exception decorators
- Use C# naming conventions (PascalCase methods)
- Add test logic in test bodies for matrix handling
- Forget to add new tests for new features
- Use `pytest.parametrize` for matrix (use fixtures instead)
- Modify C# binaries in `flaui/bin/`

---

## Troubleshooting

### "Module not found" for C# types

**Problem**: `ImportError: No module named 'FlaUI'`

**Solution**: Ensure `setup_pythonnet_bridge()` called before imports:
```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
setup_pythonnet_bridge()  # ← Must be first
from FlaUI.Core import AutomationBase
```

### Tests not running on all combinations

**Problem**: Test only runs once instead of 4 times

**Solution**: Ensure test class uses `test_application` fixture:
```python
def test_method(self, test_application: WinFormsApplicationElements | WPFApplicationElements):
    # This will run 4 times
```

### Element not found errors

**Problem**: `ElementNotFound` exception

**Solution**:
1. Check automation ID in test application
2. Verify element map in `test_utilities/elements/`
3. Add wait/sleep if timing issue
4. Use `find_first_descendant` instead of `find_first_child` for nested elements

### CI/CD failures on Windows

**Problem**: Tests pass locally but fail in AppVeyor

**Solution**:
1. Check Python version compatibility
2. Verify UV is installed: `uv --version`
3. Check test application paths in `test_utilities/config.py`
4. Review AppVeyor logs for specific errors

---

## Contributing Checklist

Before submitting changes:

- [ ] Read entire codebase if required
- [ ] Follow C# to Python mapping conventions
- [ ] Add `@handle_csharp_exceptions` to all C# interop
- [ ] Write comprehensive docstrings (95% coverage)
- [ ] Add type hints to all functions/methods
- [ ] Create tests for new features (pytest matrix)
- [ ] Run `ruff check --fix .`
- [ ] Run `interrogate flaui/`
- [ ] Run full test suite: `uv run pytest tests/`
- [ ] Update `CLAUDE.md` if patterns change
- [ ] Commit with descriptive message

---

## Version Information

- **Python Wrapper Version**: Managed via `uv version <version>`
- **FlaUI C# Version**: Stored in `FLAUI_CSHARP_VERSION` after bridge setup
- **PythonNet Version**: 3.0.5+
- **Supported Python**: 3.8 - 3.13

---

## Additional Resources

- **FlaUI C# Repository**: `c:\Users\Amruth.Vithala\projects\FlaUI`
- **Original C# Tests**: `FlaUI/src/FlaUI.Core.UITests/`
- **Original C# Source**: `FlaUI/src/FlaUI.Core/`
- **Issue Tracker**: GitHub Issues (when repository is public)

---

*This document is the single source of truth for FlaUI Python wrapper development. Keep it updated as patterns evolve.*
