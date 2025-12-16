# FlaUI Python Wrapper - Comprehensive Development Guide

**Last Updated**: December 15, 2025

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [PythonNet Bridge](#pythonnet-bridge)
- [C# to Python Mapping Patterns](#c-to-python-mapping-patterns)
- [Pydantic Validation](#pydantic-validation)
- [Pytest Matrix Configuration](#pytest-matrix-configuration)
- [Pytest-Bug Integration](#pytest-bug-integration)
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

### Post-Wait Pattern for Input Operations

Many UI automation operations require waiting for input to be processed after execution. To avoid repetitive `Wait.until_input_is_processed()` calls, the wrapper provides an optional `post_wait` parameter pattern.

#### Pattern Implementation

**Helper Method** (in `flaui/core/input.py`):
```python
from typing import Union, Callable, Optional

class Mouse:
    @staticmethod
    def _apply_post_wait(post_wait: Optional[Union[bool, float, Callable[[], None]]]) -> None:
        """Apply post-operation wait based on parameter type.

        :param post_wait: True=100ms wait, float=custom seconds, callable=custom function
        """
        if post_wait is True:
            Wait.until_input_is_processed()  # 100ms default
        elif isinstance(post_wait, (int, float)):
            Wait.for_seconds(post_wait)
        elif callable(post_wait):
            post_wait()
```

#### Methods Supporting post_wait

**Mouse Class** (all 15 methods):
- `move_by()`, `move_to()`, `click()`, `double_click()`, `down()`, `up()`
- `scroll()`, `horizontal_scroll()`, `drag_horizontally()`, `drag_vertically()`, `drag()`
- `left_click()`, `left_double_click()`, `right_click()`, `right_double_click()`

**AutomationElement Methods**:
- `click(move_mouse, post_wait)` - Performs left click
- `Tab.select_tab_item(index, value, post_wait)` - Selects tab item
- `TextBox.enter(value, post_wait)` - Types text

#### Usage Examples

**Before (Repetitive Wait Calls):**
```python
from flaui.core.input import Mouse, Wait

# Multiple wait calls needed
Mouse.move_by(800, 0)
Wait.until_input_is_processed()

Mouse.click(button.get_clickable_point())
Wait.until_input_is_processed()

tab.select_tab_item(1)
Wait.until_input_is_processed()
```

**After (Cleaner with post_wait):**
```python
from flaui.core.input import Mouse

# Built-in wait with default 100ms
Mouse.move_by(800, 0, post_wait=True)

# Custom wait duration
Mouse.click(button.get_clickable_point(), post_wait=0.5)  # 500ms

# Direct on element methods
tab.select_tab_item(1, post_wait=True)
textbox.enter("Hello World", post_wait=True)
button.click(post_wait=True)
```

**Advanced (Custom Wait Function):**
```python
def custom_wait():
    """Custom wait with retry logic."""
    Wait.for_seconds(0.2)
    Wait.until_input_is_processed()

Mouse.drag(start_pos, end_pos, post_wait=custom_wait)
```

#### Implementation in New Methods

When adding new methods that may require post-operation waits:

```python
from typing import Union, Callable, Optional

@handle_csharp_exceptions
def new_input_method(self, param: str, post_wait: Optional[Union[bool, float, Callable[[], None]]] = None) -> None:
    """New input operation.

    :param param: Operation parameter
    :param post_wait: Optional wait after operation. True=100ms, float=custom seconds, callable=custom function
    """
    from flaui.core.input import Mouse  # Late import to avoid circular dependency

    # Perform the operation
    self.raw_element.DoSomething(param)

    # Apply post-wait if requested
    Mouse._apply_post_wait(post_wait)
```

#### Circular Import Prevention

Since `automation_elements.py` and `input.py` import each other, use **late imports** inside methods:

```python
# In automation_elements.py
def click(self, move_mouse: bool = False, post_wait: Optional[Union[bool, float, Callable[[], None]]] = None) -> None:
    """Performs a left click on the element."""
    from flaui.core.input import Mouse  # ← Import inside method

    self.raw_element.Click(move_mouse)
    Mouse._apply_post_wait(post_wait)
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

## Python Compatibility & Library Preferences

### Python 3.8+ Compatibility Requirement

**CRITICAL**: This project **MUST** maintain compatibility with Python 3.8+.

```toml
# From pyproject.toml
requires-python = ">=3.8"
```

#### Version-Specific Considerations

**Python 3.8 Limitations:**
- No `|` union syntax (use `Union[X, Y]` instead)
- No `list[X]` syntax (use `List[X]` from typing)
- No `dict[X, Y]` syntax (use `Dict[X, Y]` from typing)
- No structural pattern matching (match/case)
- No `Self` type hint (use string forward reference or TypeVar)

**✅ Python 3.8+ Compatible:**
```python
from typing import List, Dict, Union, Optional

def process_elements(items: List[str]) -> Dict[str, int]:
    """Process a list of elements."""
    result: Dict[str, int] = {}
    value: Union[int, None] = None
    return result
```

**❌ Python 3.9+ Only (DO NOT USE):**
```python
def process_elements(items: list[str]) -> dict[str, int]:  # ← Python 3.9+
    result: dict[str, int] = {}
    value: int | None = None  # ← Python 3.10+
    return result
```

#### Testing Python 3.8 Compatibility

```bash
# Use tox or nox to test multiple Python versions
uv run --python 3.8 pytest tests/

# CI/CD should test against 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
```

### Prefer Python Libraries Over Custom C# Ports

When porting supplemental C# code that is **not** core FlaUI functionality, prefer well-established Python libraries over custom PythonNet ports **unless the C# implementation provides specific benefits**.

#### Decision Framework

**Use Python Library When:**
- ✅ Equivalent functionality exists in Python stdlib or well-maintained package
- ✅ No performance penalty compared to C# version
- ✅ Reduces PythonNet complexity and potential interop issues
- ✅ Better Python developer ergonomics
- ✅ Fewer dependencies on C# runtime

**Use C# PythonNet When:**
- ✅ Core FlaUI functionality (automation elements, patterns, etc.)
- ✅ C# version offers better performance for automation tasks
- ✅ Python equivalent would require complex reimplementation
- ✅ Need exact parity with FlaUI C# behavior
- ✅ Deep integration with other C# FlaUI components

#### Common C# → Python Library Mappings

| C# Class/Namespace | Python Equivalent | When to Use Python |
|-------------------|------------------|-------------------|
| `System.DateTime` | `datetime.datetime` | ✅ For date/time operations unrelated to UI automation |
| `System.TimeSpan` | `datetime.timedelta` | ✅ For duration calculations |
| `System.IO.Path` | `pathlib.Path` | ✅ For file path manipulation |
| `System.Text.RegularExpressions` | `re` module | ✅ For regex operations |
| `System.Threading.Thread.Sleep()` | `time.sleep()` | ✅ For delays/waits |
| `System.Linq` | `itertools`, comprehensions | ✅ For collection operations |
| `System.Collections.Generic.List<T>` | `list` | ✅ For general collections |
| `System.Collections.Generic.Dictionary<K,V>` | `dict` | ✅ For mappings |
| `System.Drawing.Point` | **C# via PythonNet** | ❌ UI automation coordinate system |
| `System.Drawing.Rectangle` | **C# via PythonNet** | ❌ UI automation bounding boxes |
| `System.Windows.Automation.*` | **C# via PythonNet** | ❌ Core automation functionality |

#### Example: DateTime Conversion

**❌ Unnecessary C# PythonNet:**
```python
from System import DateTime as CSDateTime

def log_timestamp() -> str:
    """Get current timestamp for logging."""
    # Unnecessarily uses C# when Python stdlib is sufficient
    now = CSDateTime.Now
    return now.ToString("yyyy-MM-dd HH:mm:ss")
```

**✅ Prefer Python stdlib:**
```python
from datetime import datetime

def log_timestamp() -> str:
    """Get current timestamp for logging."""
    # Use Python's datetime - simpler and no interop overhead
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

**✅ C# Required for Automation:**
```python
from System import DateTime as CSDateTime
from arrow import Arrow

def set_date_picker(element: DateTimePicker, date: datetime) -> None:
    """Set DateTimePicker value - MUST use C# DateTime for FlaUI interop."""
    # C# required here - FlaUI expects System.DateTime
    cs_date = CSDateTime.Parse(date.strftime("%Y-%m-%d"))
    element.raw_element.SelectedDate = cs_date
```

#### Example: File Path Operations

**❌ Unnecessary C# PythonNet:**
```python
from System.IO import Path as CSPath

def get_log_directory(base_path: str) -> str:
    """Construct log directory path."""
    return CSPath.Combine(base_path, "logs")
```

**✅ Prefer Python pathlib:**
```python
from pathlib import Path

def get_log_directory(base_path: str) -> Path:
    """Construct log directory path."""
    return Path(base_path) / "logs"
```

#### Example: Collection Operations

**❌ Unnecessary LINQ via C#:**
```python
from System.Linq import Enumerable

def filter_visible_elements(elements: List[AutomationElement]) -> List[AutomationElement]:
    """Filter to visible elements."""
    cs_list = List[Object]([e.raw_element for e in elements])
    filtered = Enumerable.Where(cs_list, lambda e: e.IsOffscreen == False)
    return [AutomationElement(raw_element=e) for e in filtered]
```

**✅ Prefer Python comprehensions:**
```python
def filter_visible_elements(elements: List[AutomationElement]) -> List[AutomationElement]:
    """Filter to visible elements."""
    return [e for e in elements if not e.is_offscreen]
```

### Best Practices Summary

1. **Always target Python 3.8+** - use `typing` module for type hints
2. **Prefer Python stdlib** for general-purpose operations (datetime, pathlib, re, itertools)
3. **Use C# PythonNet** for core FlaUI automation functionality
4. **Document reasoning** when choosing C# over Python equivalent
5. **Test with Python 3.8** to ensure compatibility
6. **Minimize interop overhead** by batching C# calls when necessary

### Related Documentation

- [Python 3.8 Release Notes](https://docs.python.org/3/whatsnew/3.8.html)
- [typing Module](https://docs.python.org/3/library/typing.html) - Type hints for 3.8+
- [PEP 585](https://peps.python.org/pep-0585/) - Why `list[X]` requires Python 3.9+

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

## Pytest-Bug Integration

### Overview

This project uses [pytest-bug](https://github.com/tolstislon/pytest-bug) plugin to mark and track tests with known bugs. The plugin provides:

- **Bug Markers**: Tag tests with bug identifiers and descriptions
- **Skip/XFail Control**: Choose whether to skip or run (xfail) bug-marked tests
- **Query Capability**: Filter and run tests by bug pattern
- **Summary Statistics**: See "Bugs skipped: X, Bugs passed: Y, Bugs failed: Z" in output
- **GitHub Integration**: Link tests to GitHub issues for traceability

### Installation

pytest-bug is already included in project dependencies:

```toml
[dependency-groups]
unit-test = [
    "pytest>=9.0.0",
    "pytest-bug>=1.4.0",
    # ...
]
```

Install with: `uv sync --all-groups --all-extras`

### Basic Usage

#### Marker Signature

```python
@pytest.mark.bug(identifier, description, run=False)
```

**Parameters:**
- `identifier` (str): Bug ID or issue number (e.g., "GH-74", "C18")
- `description` (str): Brief description of the bug
- `run` (bool):
  - `False` (default): Skip the test (shown as "BUG-SKIP")
  - `True`: Run the test, mark as xfail if it fails (shown as "BUG-FAIL" or "BUG-PASS")

#### Class-Level Skip Example

```python
@pytest.mark.bug("GH-74", "Spinner control AutomationID instability")
class TestSpinner:
    """All tests in this class will be skipped and marked as bugs"""

    def test_set_value(self, spinner: Spinner) -> None:
        spinner.value = 10
        assert spinner.value == 10
```

#### Method-Level XFail Example

```python
@pytest.mark.bug("GH-77", "RegisterAutomationEvent not yet ported", run=True)
def test_invoke_with_event(self, button: Button) -> None:
    """Test will be marked as BUG-FAIL if run parameter is True"""
    # This test would fail, so it's xfailed
    button.invoke()
    assert event_was_raised()
```

### Marker Relationship

**CRITICAL**: pytest-bug markers are **additive metadata**, not replacements for xfail/skip.

#### ✅ Correct Pattern (Both Markers)

```python
# For class-level skip
@pytest.mark.bug("GH-74", "AutomationID instability")
@pytest.mark.xfail(reason="Spinner broken")  # ← Still needed for behavior
class TestSpinner:
    pass

# For method-level skip
@pytest.mark.bug("GH-77", "Not yet ported", run=True)
@pytest.mark.skip(reason="TODO: Port this feature")  # ← Still needed
def test_feature():
    pass

# For conditional skip in body
def test_conditional(test_application_type: str):
    if test_application_type == "WinForms":
        pytest.bug("GH-75", "Broken on WinForms")  # ← Metadata
        pytest.skip("WinForms not supported")  # ← Actual behavior
```

#### ❌ Incorrect (Missing Behavior Control)

```python
# Bug marker alone doesn't control execution
@pytest.mark.bug("GH-74", "Broken")  # ← Only metadata
class TestSpinner:  # ← Tests will RUN normally
    pass
```

### Output Symbols

When tests run, pytest-bug uses special symbols:

| Symbol | Meaning | Description |
|--------|---------|-------------|
| `b` | BUG-SKIP | Test skipped due to known bug |
| `f` | BUG-FAIL | Test ran but failed (expected) |
| `p` | BUG-PASS | Test ran and passed (bug may be fixed) |

**Example output:**
```bash
$ uv run pytest tests/ui/core/automation_elements/test_spinner.py -v

test_spinner.py::TestSpinner::test_set_value[UIA2_WinForms] BUG-SKIP  [ 25%]
test_spinner.py::TestSpinner::test_set_value[UIA2_WPF] BUG-SKIP       [ 50%]
test_spinner.py::TestSpinner::test_set_value[UIA3_WinForms] BUG-SKIP  [ 75%]
test_spinner.py::TestSpinner::test_set_value[UIA3_WPF] BUG-SKIP       [100%]

--------------------------- Bugs skipped: 4 ---------------------------
Results (0.12s): 4 skipped
```

### CLI Options

#### Query and Filter

```bash
# Run only bug-marked tests (using pytest -m)
uv run pytest -m bug -v

# Run tests matching bug pattern (using pytest-bug)
uv run pytest --bug-pattern="GH-7[4-9]"

# Run ALL bug-marked tests (even if normally skipped)
uv run pytest --bug-all-run

# Skip ALL bug-marked tests
uv run pytest --bug-all-skip
```

#### Customize Output

```bash
# Disable bug statistics summary
uv run pytest --bug-no-stats

# Change output symbols
uv run pytest --bug-skip-letter=s --bug-fail-letter=x --bug-pass-letter=o

# Change verbose output words
uv run pytest --bug-skip-word=SKIPPED --bug-fail-word=XFAIL --bug-pass-word=PASSED -v
```

### Configuration Options

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "bug: Known bug tracked in GitHub issues"
]

# Optional: Customize pytest-bug defaults
bug_summary_stats = true  # Show "Bugs skipped: X" summary
bug_skip_letter = "b"     # Symbol for skipped bugs
bug_fail_letter = "f"     # Symbol for failed bugs
bug_pass_letter = "p"     # Symbol for passed bugs
bug_skip_word = "BUG-SKIP"  # Verbose output for skipped
bug_fail_word = "BUG-FAIL"  # Verbose output for failed
bug_pass_word = "BUG-PASS"  # Verbose output for passed
```

### GitHub Issue Integration

Link tests to GitHub issues for full traceability:

```python
@pytest.mark.bug(
    "GH-74",
    "Spinner control element finding is flaky - AutomationID sometimes returns uuid. "
    "See: https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74"
)
@pytest.mark.xfail(reason="Spinner broken due to upstream FlaUI bug")
class TestSpinner:
    """
    Known Issues:
    - GH-74: AutomationID instability in bulk test runs
    - Upstream: https://github.com/FlaUI/FlaUI/issues/XXX
    """
```

**Benefits:**
- Each bug ID maps to a GitHub issue
- Issue contains detailed investigation, root cause, workarounds
- Test docstring references upstream FlaUI issues when applicable
- Use `pytest -m bug --co` to see all bug-marked tests without running

### Current Bug Markers in Project

| Issue | Description | Tests | Status |
|-------|-------------|-------|--------|
| [GH-74](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74) | Spinner AutomationID instability | 3 | Flaky |
| [GH-75](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/75) | Combobox broken on WinForms | 22 | Known issue |
| [GH-76](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/76) | Tree test flaky on CI | 4 | CI-specific |
| [GH-77](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/77) | RegisterAutomationEvent not ported | 4 | TODO |
| [GH-78](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/78) | Toggle pattern unsupported WinForms | 2 | UIA limitation |
| [GH-79](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/79) | Context menu UIA3+WinForms broken | 1 | .NET bug |

**Total**: 36 tests marked with bugs (7.2% of test suite)

### Best Practices

1. **Always use both markers**: Bug marker for tracking + xfail/skip for behavior
2. **Use descriptive IDs**: "GH-74" better than "bug1"
3. **Link to issues**: Include GitHub issue URLs in docstrings
4. **Use `run=True` sparingly**: Only when you want to detect if bug is fixed
5. **Query before adding**: Check existing bugs with `pytest --bug-pattern="GH-" --co`
6. **Update when fixed**: Remove bug markers when upstream issues resolved
7. **Document in test class**: Add Known Issues section to docstring

### Troubleshooting

#### Bug marker not working

**Problem**: Test runs normally despite bug marker

**Solution**: Add `@pytest.mark.xfail` or `pytest.skip()`:
```python
@pytest.mark.bug("GH-74", "Broken")  # ← Only metadata
@pytest.mark.xfail(reason="Known bug")  # ← Actual behavior control
```

#### "Bugs passed" count high

**Problem**: Many tests show "BUG-PASS" (may indicate bugs are fixed)

**Solution**: Review tests with `run=True`, verify if bugs are actually fixed:
```bash
uv run pytest --bug-all-run -v | Select-String "BUG-PASS"
```

#### Can't query specific bugs

**Problem**: Need to see all Spinner-related bug tests

**Solution**: Use bug-pattern or pytest markers:
```bash
# Using pytest-bug pattern
uv run pytest --bug-pattern="GH-74" --co

# Using pytest marker query
uv run pytest -m bug --co -q | Select-String "spinner"
```

### Related Documentation

- [docs/bug-tracking.md](docs/bug-tracking.md) - Full bug tracking guide
- [pytest-bug GitHub](https://github.com/tolstislon/pytest-bug) - Official documentation
- [pytest markers](https://docs.pytest.org/en/stable/how-to/mark.html) - pytest marker basics

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

The project uses AppVeyor for continuous integration testing on Windows with Visual Studio 2022.

#### Matrix Testing

```yaml
# From .appveyor.yml
environment:
  UV_FROZEN: "1"  # Use exact versions from uv.lock
  matrix:
    - job_name: Python 3.12 x64
      PYTHON: "C:\\Python312"
      PYTHON_VERSION: 3.12
      PYTHON_ARCH: 64
```

#### Test Script with Timeout and Allure

```yaml
test_script:
  - ps: |
      $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
      Write-Host "Running tests with pytest..."
      uv run --group unit-test --no-dev --package flaui-uiautomation-wrapper --extra coverage coverage run -m pytest --timeout=15 --timeout-method=thread --junit-xml=test-results.xml --alluredir=allure-results
      if ($LASTEXITCODE -ne 0) { Write-Host "Tests failed."; exit 1 }
      Write-Host "Tests completed."
```

**Key Parameters:**
- `--timeout=15` - Maximum test execution time (15 seconds per test)
- `--timeout-method=thread` - Use thread-based timeout (safe for Windows)
- `--junit-xml=test-results.xml` - JUnit XML report for CI integration
- `--alluredir=allure-results` - Generate Allure JSON reports for detailed test analytics

#### Artifacts Collection

```yaml
artifacts:
  - path: test-results.xml
    name: test-results

  - path: coverage.xml
    name: coverage

  - path: htmlcov
    name: coverage-html
    type: directory

  - path: allure-results
    name: allure-results
    type: directory
```

**Available Artifacts:**
1. **test-results.xml** - JUnit XML format for CI test result parsing
2. **coverage.xml** - XML coverage report for code coverage tracking
3. **htmlcov/** - HTML coverage report with line-by-line coverage details
4. **allure-results/** - Allure JSON reports containing:
   - Test execution history
   - Test parameters (UIA2/UIA3, WinForms/WPF)
   - Step-by-step execution details
   - Screenshots and attachments (if configured)
   - Timing information
   - Categorization by test type

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

**Rule**: Sphinx/reST docstrings with a one-line summary for all public symbols.

- First line: single-sentence summary in imperative mood (Sphinx one-liner)
- Follow with Sphinx fields for non-trivial APIs: `:param:`, `:return:`, `:raises:`
- Keep summaries concise; add details after the blank line when needed

Minimal one‑liner examples:

```python
@property
def name(self) -> str:
    """Return the element name."""

def click(self) -> None:
    """Perform a left click on the element."""
```

With Sphinx fields:

```python
def find_all_children(self, condition: Optional[PropertyCondition] = None) -> List[AutomationElement]:
    """Find all children matching the condition.

    :param condition: Search condition to filter results; matches all when omitted.
    :return: List of matching elements; empty list when none are found.
    :raises ElementNotAvailableException: If the element is no longer available.
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
