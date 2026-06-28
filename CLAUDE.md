# FlaUI Python Wrapper - Development Guide

This file is the durable reference for developing the FlaUI Python wrapper. It covers the
architecture, conventions, and patterns that rarely change. Step-by-step tutorials and procedural
guides live in `docs/` (see [Where to find the tutorials](#where-to-find-the-tutorials)).

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Architecture](#architecture)
- [Automation stack (UIA2 / UIA3)](#automation-stack-uia2--uia3)
- [PythonNet Bridge](#pythonnet-bridge)
- [C# to Python Mapping Patterns](#c-to-python-mapping-patterns)
- [Pydantic Conventions](#pydantic-conventions)
- [Python Compatibility & Library Preferences](#python-compatibility--library-preferences)
- [Coding Standards](#coding-standards)
- [Key Files Reference](#key-files-reference)
- [Continuous Integration](#continuous-integration)
- [Documentation Standards](#documentation-standards)
- [Where to find the tutorials](#where-to-find-the-tutorials)

---

## Project Overview

This project is a **Python port of the FlaUI C# library** for Windows UI automation. It provides a
**1:1 mapping** of the exposed C# endpoints using PythonNet, enabling full FlaUI capabilities in
Python with complete feature parity.

### Key Differentiators
- **Complete Feature Parity**: Unlike RobotFlaUI (limited to Robot Framework and XPath), this
  wrapper provides plug-and-play Python access to the complete FlaUI API.
- **Type Safety**: All input/output is backed by Pydantic models for IDE intellisense and data
  validation.
- **Any Test Framework**: Works with pytest, unittest, or any Python test framework.
- **Pythonic API**: Snake_case methods with Python-native types while preserving the C# structure.

---

## Repository Structure

```
flaui/
├── bin/               # C# DLLs (packaged in the wheel)
│   ├── FlaUI.Core.dll
│   ├── FlaUI.UIA2.dll
│   ├── FlaUI.UIA3.dll
│   ├── Interop.UIAutomationClient.dll
│   └── System.CodeDom.dll
├── core/              # Core automation wrappers
│   ├── automation_elements.py    # Main element classes (largest module)
│   ├── automation_base.py        # Python facade for C# AutomationBase (UIA2/UIA3)
│   ├── application.py            # Application launch/attach
│   ├── condition_factory.py      # Search-condition builders
│   ├── input.py                  # Mouse / Keyboard / Wait
│   ├── cache_request.py
│   ├── tools.py                  # Retry helpers
│   ├── definitions.py            # Enums and constants
│   └── ...
├── uia2/              # Python facades for FlaUI.UIA2 (delegate to C#)
├── uia3/              # Python facades for FlaUI.UIA3 (delegate to C#)
├── lib/               # Supporting libraries
│   ├── pythonnet_bridge.py       # PythonNet initialization / DLL loading
│   ├── exceptions.py             # C# -> Python exception translation
│   ├── enums.py                  # Enum wrappers + UIAutomationTypes
│   ├── collections.py            # Type-conversion utilities
│   └── system/
│       └── drawing.py            # System.Drawing wrappers (Point, Rectangle, ...)
└── modules/           # High-level automation
    └── automation.py             # Automation class (UIA2/UIA3 setup)

tests/
├── conftest.py                   # Global fixtures and matrix setup
├── ui/                           # UI automation tests
│   └── core/
│       ├── automation_elements/  # Element-specific tests
│       └── patterns/             # Pattern tests
└── unit/                         # Unit tests

tests/test_utilities/             # Test bases and element maps
├── base.py                       # FlaUITestBase
└── elements/
    ├── winforms_application/     # WinForms element map
    └── wpf_application/          # WPF element map

docs/                             # Zensical documentation site (zensical.toml)
scripts/extract_versions.py       # Regenerates docs/_includes/flaui_versions.md
```

The high-level entry point is `flaui.modules.automation.Automation`, which wires up the C#
automation object (`cs_automation`), a `ConditionFactory` (`cf`), a `tree_walker`, and an
`Application` instance based on the chosen `UIAutomationTypes` (UIA2 or UIA3).

---

## Architecture

### Hierarchical Class Structure

The wrapper follows a **4-layer inheritance hierarchy** that mirrors FlaUI C#:

```
1. ElementModel (Pydantic BaseModel)   - validates raw_element exists; holds the C# reference
2. ElementBase  (extends ElementModel) - common properties (name, automation_id, ...) decorated
                                          with @handle_csharp_exceptions
3. Pattern mixins (ABC)                - InvokeAutomationElement, ToggleAutomationElement,
                                          SelectionItemAutomationElement, ...
4. Concrete elements (multiple inheritance) - Button(AutomationElement, InvokeAutomationElement),
                                          CheckBox(AutomationElement, ToggleAutomationElement), ...
```

**Layer 1 — `ElementModel`** validates the wrapped C# object and stores it:

```python
class ElementModel(BaseModel, abc.ABC):
    """Base Pydantic model for all automation elements."""
    raw_element: Any = Field(..., description="Contains the C# automation element in raw form")

    @field_validator("raw_element")
    def validate_element_exists(cls, v: Any, info: ValidationInfo) -> Any:
        """Validate the element exists."""
        if v is None:
            raise ElementNotFound("Element does not exist")
        return v
```

**Layer 2 — `ElementBase`** exposes common properties, each decorated with
`@handle_csharp_exceptions`:

```python
class ElementBase(ElementModel, abc.ABC):
    @property
    @handle_csharp_exceptions
    def name(self) -> str:
        """Return the element name."""
        return self.raw_element.Name
```

**Layer 3 — pattern mixins** add behavior that maps to a UIA pattern:

```python
class ToggleAutomationElement(ElementModel, abc.ABC):
    @property
    @handle_csharp_exceptions
    def toggle_state(self) -> ToggleState:
        """Return the current toggle state."""
        return ToggleState(self.raw_element.ToggleState)

    @handle_csharp_exceptions
    def toggle(self) -> None:
        """Toggle the element."""
        self.raw_element.Toggle()
```

**Layer 4 — concrete elements** combine `AutomationElement` with the relevant mixins:

```python
class Button(AutomationElement, InvokeAutomationElement):
    """Class to interact with a button element."""


class CheckBox(AutomationElement, ToggleAutomationElement):
    @property
    @handle_csharp_exceptions
    def is_checked(self) -> bool:
        """Return whether the element is checked."""
        return self.raw_element.IsChecked
```

### Automation stack (UIA2 / UIA3)

C# FlaUI exposes `FlaUI.Core.AutomationBase` with concrete implementations `FlaUI.UIA2.UIA2Automation` and `FlaUI.UIA3.UIA3Automation`. The Python package mirrors this with Pydantic facades:

- [`flaui/core/automation_base.py`](flaui/core/automation_base.py) — `AutomationBase` (`raw_automation` holds the C# instance); snake_case methods (`get_desktop`, `from_point`, `compare`, `dispose`, …) with `@handle_csharp_exceptions`.
- [`flaui/uia2/automation.py`](flaui/uia2/automation.py) / [`flaui/uia3/automation.py`](flaui/uia3/automation.py) — `UIA2Automation` / `UIA3Automation` construct or wrap the matching C# type.
- [`wrap_cs_automation`](flaui/core/automation_base.py) — maps an existing C# `AutomationBase` (e.g. from `AutomationElement.Automation`) to the correct Python subclass.

[`flaui/modules/automation.py`](flaui/modules/automation.py) sets **`automation_base`** to the Python facade (preferred for typed APIs) and **`cs_automation`** to the **raw C#** object (backward compatible for `isinstance(..., FlaUI.UIA3.UIA3Automation)`, `PatternLibrary`, interop). [`Application`](flaui/core/application.py) accepts C# automation, Python `AutomationBase`, or objects with `cs_automation` via `_coerce_cs_automation`.

[`AutomationElement.automation`](flaui/core/automation_elements.py) returns the Python `AutomationBase` facade, not the bare C# reference.

User-facing docs: [docs/uia2-uia3.md](docs/uia2-uia3.md). Issue tracker: [GH-107](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/107).

---

## PythonNet Bridge

**RULE #1**: Always call `setup_pythonnet_bridge()` **before** importing any C# types. It loads
every DLL in `flaui/bin/` into the runtime and records the FlaUI version.

```python
# flaui/lib/pythonnet_bridge.py (abridged)
def setup_pythonnet_bridge() -> None:
    """Load the FlaUI C# DLLs from flaui/bin/ into the Python.NET runtime."""
    for dll_path in config.settings.BIN_HOME.glob("*.dll"):
        clr.AddReference(dll_path.as_posix())
        clr.AddReference(dll_path.stem)
        assembly = Assembly.LoadFile(dll_path.as_posix())
        if dll_path.name == "FlaUI.Core.dll":
            global FLAUI_CSHARP_VERSION
            FLAUI_CSHARP_VERSION = str(assembly.GetName().Version)
```

Correct import order (e.g. in `tests/conftest.py`):

```python
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

# isort: off  # keep this order
setup_pythonnet_bridge()  # MUST be first

from flaui.lib.enums import UIAutomationTypes  # now safe to import C#-backed modules
```

**Late imports for C# types.** To avoid circular dependencies, import C# types inside the method
that uses them:

```python
def as_button(self) -> Button:
    """Convert the element to a Button."""
    from FlaUI.Core.AutomationElements import Button as CSButton
    return Button(raw_element=CSButton(self.framework_automation_element))
```

Bundled DLLs in `flaui/bin/`: `FlaUI.Core.dll`, `FlaUI.UIA2.dll`, `FlaUI.UIA3.dll`,
`Interop.UIAutomationClient.dll`, `System.CodeDom.dll`. **Do not modify these binaries.**

---

## C# to Python Mapping Patterns

### Naming conventions

| C# | Python | Example |
|----|--------|---------|
| Classes | PascalCase → PascalCase | `Button` → `Button` |
| Methods | PascalCase → snake_case | `Click()` → `click()` |
| Properties | PascalCase → snake_case | `BoundingRectangle` → `bounding_rectangle` |
| Enums | `Type.Member` → `Type.Member` | `ControlType.Button` → `ControlType.Button` |

### Property translation

```python
# C#: public string Name => Properties.Name.Value;
@property
@handle_csharp_exceptions
def name(self) -> str:
    """Return the element name."""
    return self.raw_element.Name
```

### Method translation

```python
# C#: public void Click(bool moveMouseToClickablePoint = false)
@handle_csharp_exceptions
def click(self, move_mouse: bool = False) -> None:
    """Perform a left click on the element.

    :param move_mouse: Move the mouse slowly (True) or instantly (False).
    """
    self.raw_element.Click(move_mouse)
```

### Complex property with a wrapper

C# values such as `System.Drawing.Rectangle` are wrapped in a Python class:

```python
@property
@handle_csharp_exceptions
def bounding_rectangle(self) -> Rectangle:
    """Return the bounding rectangle of this element."""
    return Rectangle(raw_value=self.raw_element.BoundingRectangle)
```

### Method with type conversion

C# arrays become Python lists; conditions pass their `cs_condition`:

```python
@handle_csharp_exceptions
def find_all_children(self, condition: Optional[PropertyCondition] = None) -> List[AutomationElement]:
    """Find all children matching the condition.

    :param condition: Search condition; matches all children when omitted.
    :return: List of matching elements; empty when none are found.
    """
    if condition is None:
        return [AutomationElement(raw_element=_) for _ in self.raw_element.FindAllChildren()]
    return [AutomationElement(raw_element=_)
            for _ in self.raw_element.FindAllChildren(condition.cs_condition)]
```

### Type conversion utilities

`flaui/lib/collections.py` provides helpers for crossing the boundary:

```python
class TypeCast:
    @staticmethod
    def py_list(raw: Any) -> List[Any]:
        """Convert a C# IEnumerable to a Python list."""
        return raw if isinstance(raw, list) else list(map(lambda x: x, raw))

    @staticmethod
    def cs_timespan(value: int) -> TimeSpan:
        """Convert Python milliseconds to a C# TimeSpan."""
        return None if value is None else TimeSpan.FromMilliseconds(value)
```

### Enum translation

C# enums map to Python `Enum` classes with matching member values, then convert at the boundary:

```python
class ToggleState(Enum):
    """Toggle state values."""
    Off = 0
    On = 1
    Indeterminate = 2


@property
@handle_csharp_exceptions
def toggle_state(self) -> ToggleState:
    """Return the current toggle state."""
    return ToggleState(self.raw_element.ToggleState)
```

### `post_wait` for input operations

Input methods (all `Mouse` methods, `AutomationElement.click`, `Tab.select_tab_item`,
`TextBox.enter`) accept an optional `post_wait` to wait for input to be processed:

- `True` → 100ms (`Wait.until_input_is_processed()`)
- `float` → that many seconds (`Wait.for_seconds`)
- `callable` → invoked directly

The shared helper is `Mouse._apply_post_wait` in `flaui/core/input.py`. Because
`automation_elements.py` and `input.py` import each other, use a **late import** of `Mouse` inside
any method that applies a post-wait. See
[Testing → the `post_wait` pattern](docs/contributing/testing.md#the-post_wait-pattern) for usage.

---

## Pydantic Conventions

**Model config** — allow C# types with `arbitrary_types_allowed`:

```python
class PropertyCondition(BaseModel):
    """Base condition model."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    cs_condition: Union[CSPropertyCondition, CSOrCondition, CSAndCondition]
```

**Field validators** — validate inputs before they reach C#:

```python
class ElementModel(BaseModel):
    raw_element: Any = Field(..., description="C# automation element")

    @field_validator("raw_element")
    def validate_element_exists(cls, v: Any, info: ValidationInfo) -> Any:
        """Validate the element exists."""
        if v is None:
            raise ElementNotFound("Element does not exist")
        return v
```

**System.Drawing wrappers** — accept either a raw C# value or Python coordinates, expose
`cs_object` to hand back to C# (`flaui/lib/system/drawing.py`):

```python
class Point(BaseModel):
    """Python wrapper for System.Drawing.Point."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    raw_value: Optional[CSPoint] = None
    x: Optional[int] = None
    y: Optional[int] = None

    @property
    def cs_object(self) -> CSPoint:
        """Return the underlying C# Point."""
        return self.raw_value if self.raw_value is not None else CSPoint(self.x, self.y)
```

Benefits: IDE autocomplete, runtime validation before interop, clear Python error messages, and
static type checking.

---

## Python Compatibility & Library Preferences

### Supported versions: Python 3.10+

This project targets **Python 3.10 through 3.14** (`requires-python = ">=3.10,<3.15"`). On 3.10+
the following modern syntax is **allowed**:

- `|` unions (`int | None`)
- built-in generics (`list[str]`, `dict[str, int]`)
- structural pattern matching (`match` / `case`)

Both styles are fine — do **not** churn existing `typing` imports (`List`, `Dict`, `Optional`,
`Union`) just to switch syntax. Mirror the surrounding file's style when editing.

### Prefer Python libraries over custom C# ports

When porting supplemental code that is **not** core FlaUI functionality, prefer well-established
Python libraries over PythonNet ports, unless the C# implementation provides a concrete benefit.

**Use a Python library when:** an equivalent exists in stdlib or a maintained package, there is no
performance penalty, it reduces interop complexity, or it improves Python ergonomics.

**Use C# via PythonNet when:** it is core FlaUI functionality (automation elements, patterns,
coordinates/rectangles), the C# version performs better for automation, exact parity with FlaUI
behavior is required, or it integrates deeply with other C# FlaUI components.

| C# | Python equivalent | Prefer Python? |
|----|-------------------|----------------|
| `System.DateTime` / `System.TimeSpan` | `datetime` / `timedelta` | ✅ for non-UI date/time |
| `System.IO.Path` | `pathlib.Path` | ✅ |
| `System.Text.RegularExpressions` | `re` | ✅ |
| `System.Threading.Thread.Sleep()` | `time.sleep()` | ✅ |
| `System.Linq` | comprehensions / `itertools` | ✅ |
| `System.Collections.Generic.List/Dictionary` | `list` / `dict` | ✅ |
| `System.Drawing.Point` / `Rectangle` | C# via PythonNet | ❌ UI coordinates |
| `System.Windows.Automation.*` | C# via PythonNet | ❌ core automation |

Note the exception: when a value must be handed back to FlaUI (e.g. setting a `DateTimePicker`),
use the C# type (`System.DateTime`) even though Python's `datetime` exists for everything else.

---

## Coding Standards

1. **Mirror the C# API.** Match FlaUI's class hierarchy for 1:1 parity
   (`class Button(AutomationElement, InvokeAutomationElement)`).
2. **Pydantic for all models.** Use `BaseModel` with field validators for validation and type
   safety.
3. **Decorate interop.** Every method/property that touches C# uses `@handle_csharp_exceptions`.
4. **Convert types at the boundary.** Wrap C# return types (`Rectangle`, enums, collections) in
   their Python equivalents.
5. **Docstrings.** Sphinx/reST style — a one-line imperative summary, then `:param:`, `:return:`,
   `:raises:` for non-trivial APIs. Keep ≥95% coverage (`interrogate`).
6. **Type hints everywhere**, including test fixtures. Both `typing` aliases and 3.10+ built-in
   generics are acceptable; match the file you are editing.
7. **PythonNet first.** Call `setup_pythonnet_bridge()` before any C# import.
8. **Tests:** type-hint fixtures, assert against enums (not strings), and always use the `uv run`
   prefix.

```python
# ✅ enum, not string
assert element.toggle_state == ToggleState.On
# ✅ uv run prefix
# uv run pytest tests/
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| [flaui/core/automation_elements.py](flaui/core/automation_elements.py) | Main element mapping — all automation element classes |
| [flaui/core/automation_base.py](flaui/core/automation_base.py) | Python `AutomationBase` + `wrap_cs_automation` (UIA2/UIA3 facades) |
| [flaui/uia2/automation.py](flaui/uia2/automation.py) | `UIA2Automation` Python wrapper |
| [flaui/uia3/automation.py](flaui/uia3/automation.py) | `UIA3Automation` Python wrapper |
| [flaui/core/application.py](flaui/core/application.py) | Application launch/attach helpers |
| [flaui/core/condition_factory.py](flaui/core/condition_factory.py) | Search-condition builders |
| [flaui/core/input.py](flaui/core/input.py) | Mouse / Keyboard / Wait (incl. `while_cursor_is_busy`), `post_wait` helper |
| [flaui/core/capturing.py](flaui/core/capturing.py) | Screen/element capture + video recording (`Capture`, `CaptureImage`, `VideoRecorder`) |
| [flaui/core/overlay.py](flaui/core/overlay.py) | `OverlayManager` facade (visual-debug overlays) |
| [flaui/core/logging.py](flaui/core/logging.py) | Opt-in C#→Python log bridge (`enable_csharp_logging`, `FLAUI_LOG_CSHARP`) |
| [flaui/lib/pythonnet_bridge.py](flaui/lib/pythonnet_bridge.py) | PythonNet initialization, DLL loading |
| [flaui/lib/exceptions.py](flaui/lib/exceptions.py) | C# → Python exception mapping (`handle_csharp_exceptions`, `translate_exceptions`) |
| [flaui/lib/system/drawing.py](flaui/lib/system/drawing.py) | System.Drawing wrappers (Point, Rectangle, Color) |
| [flaui/lib/enums.py](flaui/lib/enums.py) | Enum wrappers, `UIAutomationTypes` |
| [flaui/lib/collections.py](flaui/lib/collections.py) | Type-conversion utilities |
| [flaui/modules/automation.py](flaui/modules/automation.py) | High-level `Automation` class (UIA2/UIA3 setup) |
| [tests/conftest.py](tests/conftest.py) | Global test fixtures, matrix parametrization |
| [tests/test_utilities/base.py](tests/test_utilities/base.py) | `FlaUITestBase` for test applications |

---

## Continuous Integration

CI/CD runs on a **hybrid Azure Pipelines + AppVeyor** setup. The two systems split responsibilities:

- **Azure Pipelines** ([`azure-pipelines.yml`](azure-pipelines.yml), GitHub check
  `flaui-uiautomation-wrapper-ci`) owns the fast gates and release plumbing: Ruff + Interrogate
  linting, the strict Zensical docs build, a hosted `windows-2022` smoke suite (unit + identifier
  tests), package builds, and gated `deploy_testpypi` / `deploy_pypi` / `deploy_docs` stages.
- **AppVeyor** ([`.appveyor.yml`](.appveyor.yml), checks `continuous-integration/appveyor/pr`
  and `/branch`) is the hosted Windows desktop UI gate on `Visual Studio 2022`. The gate is
  **trimmed**: the slow full UI suite only runs where it gates a merge — **pull requests and pushes
  to `master`** (`APPVEYOR_PULL_REQUEST_NUMBER` set, or `APPVEYOR_REPO_BRANCH == master`). Routine
  feature-branch pushes run the **fast `tests/unit` subset only**, so day-to-day turnaround does not
  pay for the full serial run.
- **GitHub Actions** is kept for CodeQL/labeling only; other workflows are manual-only stubs.

Both runners drive tests with `uv run … pytest` and currently pin Python 3.12 x64 while the hybrid
setup stabilizes (the 3.10–3.14 matrix is commented in both files). Azure cancels stale PR runs via
`pr.autoCancel: true`; AppVeyor relies on the project-level **Rolling builds** setting (not a yaml
key). A conflicting/non-mergeable PR makes AppVeyor report "unable to build non-mergeable pull
request" — rebase or merge the base branch to clear it.

Full procedural detail (scripts, artifacts, caching, deployment variables) lives in
[docs/contributing/development.md](docs/contributing/development.md#cicd-azure-pipelines--appveyor).

---

## Documentation Standards

- Use Sphinx-style docstrings (one-line summary, then `:param:`, `:return:`, `:raises:`).
- Maintain ≥95% docstring coverage (`interrogate`).
- Modern 3.10+ typing is allowed in examples (`|` unions, `match`/`case`, built-in generics);
  existing `typing`-style code does not need rewriting.
- The docs site is built with **Zensical** (configured by `zensical.toml`), with API reference
  generated by **mkdocstrings**.
  - Build: `uv run python scripts/extract_versions.py && uv run zensical build -f zensical.toml`
  - Strict build (CI gate, catches broken nav/links): `uv run zensical build --strict -f zensical.toml`
  - Preview: `uv run zensical serve -f zensical.toml`
- Update docs when adding or changing APIs: Basics for simple flows, Advanced for deep detail, API
  Reference auto-generated via mkdocstrings.
- Prefer Python/C# tabbed examples where parity helps users.
- Regenerate `docs/_includes/flaui_versions.md` with `scripts/extract_versions.py` whenever
  `flaui/bin/Version.md` changes.
- Follow the Agentic Guidelines for LLM/system-prompt instructions; keep `AGENTS.md` aligned with
  this file.

---

## Where to find the tutorials

Procedural and step-by-step content has been relocated to the docs site:

| Topic | Location |
|-------|----------|
| Pytest matrix configuration, writing matrix tests, `post_wait`, assertions | [docs/contributing/testing.md](docs/contributing/testing.md) |
| Porting C# tests step by step, element maps | [docs/contributing/porting-tests.md](docs/contributing/porting-tests.md) |
| UV commands, code quality, pre-commit, exception handling, CI/CD (Azure Pipelines + AppVeyor), docs build | [docs/contributing/development.md](docs/contributing/development.md) |
| pytest-bug usage and current bug markers | [docs/bug-tracking.md](docs/bug-tracking.md) |
| Common issues, fixes, known skips/xfails | [docs/troubleshooting.md](docs/troubleshooting.md) |
| Contributor overview | [docs/contributing.md](docs/contributing.md) |

---

*This document is the single source of truth for FlaUI Python wrapper development. Keep it updated
as patterns evolve, and relocate tutorial-style content to `docs/`.*
