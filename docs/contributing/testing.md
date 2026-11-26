# Testing (pytest matrix)

This project's UI tests run across a **4-combination matrix**:

- **UI Automation**: UIA2 vs UIA3
- **Test Application**: WinForms vs WPF

Most test logic is identical across combinations, with only a few exceptions (e.g. WinForms ComboBox is broken). The matrix is handled by **fixtures**, not by `@pytest.mark.parametrize`, so test bodies stay clean.

## Fixture-based parametrization

The fixtures below live in [`tests/conftest.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/tests/conftest.py).

### Step 1 — Session-level application launcher

Launches all four applications once per session.

```python
@pytest.fixture(scope="session")
def launch_all_test_applications() -> Generator[dict[UIAutomationTypes, dict[str, FlaUITestBase]], Any, None]:
    """Launch all test applications ONCE per session (UIA2/UIA3 x WinForms/WPF)."""
    result = {UIAutomationTypes.UIA2: {}, UIAutomationTypes.UIA3: {}}

    for app_type in ["WinForms", "WPF"]:
        for ui_automation_type in [UIAutomationTypes.UIA2, UIAutomationTypes.UIA3]:
            test_base = FlaUITestBase(ui_automation_type, app_type)
            try:
                test_base.launch_test_app()
                time.sleep(1)  # Give the UI time to initialize
                assert test_base.automation.application, "Application did not start correctly!"
            except Exception as e:
                logger.error(f"Error launching test app: {e}")
                pytest.exit("Test application failed to launch!")
            else:
                result[ui_automation_type][app_type] = test_base

    yield result

    for ui_automation_type in [UIAutomationTypes.UIA2, UIAutomationTypes.UIA3]:
        for app_type in ["WinForms", "WPF"]:
            result[ui_automation_type][app_type].close_test_app()
            gc.collect()
```

### Step 2 — Parametrized environment fixture

Each test using this fixture runs four times.

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
    launch_all_test_applications: dict[UIAutomationTypes, dict[str, FlaUITestBase]],
) -> Generator[FlaUITestBase, Any, None]:
    """Parametrize tests across all 4 matrix combinations."""
    ui_automation_type, test_application_type = request.param
    yield launch_all_test_applications[ui_automation_type][test_application_type]
```

### Step 3 — Element map fixture

Returns the WinForms or WPF element map for the current parametrization.

```python
@pytest.fixture(scope="class", name="test_application")
def get_ui_test_application(
    setup_ui_testing_environment: FlaUITestBase,
) -> Generator[WinFormsApplicationElements | WPFApplicationElements, Any, None]:
    """Return the WinForms or WPF element map for the active parametrization."""
    application = setup_ui_testing_environment.automation.application
    automation = setup_ui_testing_environment.automation.cs_automation
    test_application_type = setup_ui_testing_environment.app_type

    elements = (
        get_winforms_application_elements(application.get_main_window(automation))
        if test_application_type == "WinForms"
        else get_wpf_application_elements(application.get_main_window(automation))
    )

    try:
        elements.main_window.find_first_descendant(
            condition=elements._cf.by_name("Simple Controls")
        ).as_tab_item().click()
    except ElementNotFound as e:
        logger.error(f"Error: {e}")

    yield elements
```

### Step 4 — Helper context fixtures

```python
@pytest.fixture()
def ui_automation_type(setup_ui_testing_environment: FlaUITestBase) -> Generator[UIAutomationTypes, None, None]:
    """Return the UIAutomation type (UIA2 or UIA3) for the active parametrization."""
    yield setup_ui_testing_environment.ui_automation_type


@pytest.fixture()
def test_application_type(setup_ui_testing_environment: FlaUITestBase) -> Generator[str, None, None]:
    """Return the test application type (WinForms or WPF) for the active parametrization."""
    yield setup_ui_testing_environment.app_type
```

## Writing matrix tests

### Basic test (runs on all 4 combinations)

```python
class TestCheckBoxElements:
    """Tests for the CheckBox class."""

    @pytest.fixture(name="read_only_checkbox")
    def get_read_only_checkbox_control(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> Generator[CheckBox, Any, None]:
        """Return the read-only checkbox element."""
        yield test_application.simple_controls_tab.read_only_checkbox

    def test_properties(self, read_only_checkbox: CheckBox) -> None:
        """Test the properties of the checkbox (runs 4x automatically)."""
        assert read_only_checkbox.toggle_state == ToggleState.Off
        assert not read_only_checkbox.is_checked
```

### Conditional skip with `xfail`

Use `@pytest.mark.xfail` with a `condition` lambda for dynamic skipping:

```python
@pytest.mark.xfail(
    condition=lambda request: request.getfixturevalue("test_application_type") == "WinForms",
    reason="Combobox got heavily broken with UIA2/UIA3 WinForms due to bugs in Windows/.Net",
)
class TestComboBoxElements:
    """Tests for the Combobox class."""

    @pytest.fixture(name="editable_combo_box")
    def get_editable_combobox_control(
        self,
        test_application: WinFormsApplicationElements | WPFApplicationElements,
    ) -> Generator[ComboBox, Any, None]:
        """Return the editable combobox element."""
        yield test_application.simple_controls_tab.editable_combo_box

    def test_selected_item(self, editable_combo_box: ComboBox) -> None:
        """Test the selected item property."""
        editable_combo_box.items[1].select()
        assert editable_combo_box.selected_item == HasAttributes(text="Item 2")
```

### Alternative: fixture-level skip

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
        skip_winforms: None,  # skip applied here
    ) -> Generator[ComboBox, Any, None]:
        yield test_application.simple_controls_tab.editable_combo_box
```

## Running tests

```bash
# Run a test file with all parametrizations
uv run pytest tests/ui/core/automation_elements/test_combobox.py -v

# Run only the UIA3 + WPF combination
uv run pytest tests/ui/ -k "UIA3_WPF"

# Run only WinForms tests
uv run pytest tests/ui/ -k "WinForms"

# Run with coverage
uv run --group unit-test --extra coverage coverage run -m pytest
```

Example output:

```
test_combobox.py::TestComboBoxElements::test_selected_item[UIA2_WinForms] XFAIL
test_combobox.py::TestComboBoxElements::test_selected_item[UIA2_WPF] PASSED
test_combobox.py::TestComboBoxElements::test_selected_item[UIA3_WinForms] XFAIL
test_combobox.py::TestComboBoxElements::test_selected_item[UIA3_WPF] PASSED
```

## Assertions

Use [PyHamcrest](https://github.com/hamcrest/PyHamcrest) and [dirty-equals](https://dirty-equals.helpmanual.io/) for expressive assertions:

```python
from dirty_equals import HasAttributes, IsFalseLike

# Basic equality
assert checkbox.is_checked is True

# Property matching
assert combobox == HasAttributes(expand_collapse_state=ExpandCollapseState.Expanded)

# Negation
assert combobox == HasAttributes(is_offscreen=IsFalseLike)
```

## The `post_wait` pattern

Many UI operations require a wait for input to be processed afterward. Rather than sprinkling `Wait.until_input_is_processed()` everywhere, input methods accept an optional `post_wait` parameter.

`post_wait` accepts:

- `True` — wait the default 100ms (`Wait.until_input_is_processed()`)
- a `float` — wait that many seconds (`Wait.for_seconds(value)`)
- a `callable` — invoke a custom wait function

```python
from flaui.core.input import Mouse

Mouse.move_by(800, 0, post_wait=True)                  # default 100ms
Mouse.click(button.get_clickable_point(), post_wait=0.5)  # 500ms
tab.select_tab_item(1, post_wait=True)
textbox.enter("Hello World", post_wait=True)
button.click(post_wait=True)
```

All `Mouse` methods, plus `AutomationElement.click`, `Tab.select_tab_item`, and `TextBox.enter`, support `post_wait`. The shared helper lives in `flaui/core/input.py` as `Mouse._apply_post_wait`. Because `automation_elements.py` and `input.py` import each other, use a **late import** of `Mouse` inside any new method that applies a post-wait.

## Integration journeys (`tests/integration`)

`tests/unit` checks the wrapper without a UI, and `tests/ui` checks each wrapped method against
the live test apps. `tests/integration` checks **multi-step user journeys** end to end: launch an
app, drive several controls in a row, change pages, and read the results back.

| | `tests/ui` | `tests/integration` |
|---|---|---|
| Scope | One wrapper method or property per test | A multi-step user journey per test |
| Application | One shared instance per matrix combo, for the whole session | A **fresh process per test**, killed afterwards |
| State | Tests must restore what they change | Any state may change; the next test starts clean |
| Matrix | `setup_ui_testing_environment` (session scope) | `journey_app` (function scope), same 4 ids |
| Marker | none | `integration` |

### Running the suite

```bash
# The whole suite on all 4 combinations (UIA2/UIA3 x WinForms/WPF)
uv run --group unit-test pytest tests/integration

# Integration journeys only, wherever they live
uv run --group unit-test pytest -m integration

# One combination
uv run --group unit-test pytest tests/integration -k UIA3_WPF

# Everything except the journeys
uv run --group unit-test pytest -m "not integration"
```

The journeys send real mouse and keyboard input, so they need an interactive, unlocked desktop.
Do not run two UI or integration runs on the same desktop at once: they steal focus from each other
and hang.

Run `-k UIA3_WinForms` together with a UIA2 combination (for example
`-k "UIA3_WinForms or UIA2_WPF"`). In a process that has only used UIA3, the WinForms tab pages
appear as siblings of their `TabItem`s instead of children, so the element maps raise
`ElementNotFound`. Once UIA2 has been used in the same process, its client-side proxies change that
tree shape. `tests/ui` has the same dependency. Full runs are unaffected because the UIA2 ids run
first.

Python's `faulthandler` is switched off while each journey runs (autouse fixture in
`tests/integration/conftest.py`) and switched back on afterwards. Journeys kill app processes, so
the UIA client keeps raising first-chance `RPC_S_SERVER_UNAVAILABLE` exceptions that .NET handles;
with `faulthandler` on, one of them intermittently became `Fatal Python error: Aborted` and killed
the whole pytest run.

### Journeys covered

| Module | Journey | Combos |
|---|---|---|
| `test_app_lifecycle_journeys.py` | Launch, attach a second `Application` by process id, drive the UI through it, close gracefully | all 4 |
| | Close the app with the title bar's Close button | all 4 |
| `test_simple_controls_journeys.py` | Fill the form (text box, check boxes, radio buttons, slider), switch tabs, come back and read every value | all 4 |
| | Visit every tab, check each page loads, and confirm re-found elements match the old references | all 4 |
| | Pick combo box items by index and text, then type a custom value | WPF (GH-75) |
| | Keyboard only: type, Tab, Space to toggle, Ctrl+Tab / Ctrl+Shift+Tab between tabs | all 4 |
| `test_menu_journeys.py` | Click through `Edit > Copy` and close it with Escape | all 4 |
| | Untick and re-tick the checkable `Edit > Show Label` item and watch the label hide and return | WPF (GH-78) |
| | Right-click for the context menu, open its submenu, dismiss every level | not UIA3 + WinForms (GH-79) |
| `test_complex_controls_journeys.py` | Expand two tree levels, select a leaf, collapse | all 4 (`bug` GH-76, `run=True`) |
| | Read the list grid, select a row by index and another by cell text | all 4 |
| `test_waits_and_diagnostics_journeys.py` | `expect()` / `Retry` across a check box, a text box and a tab-page change | all 4 |
| | `expect()` waits for a button caption to change after Invoke | WPF (WinForms app has no such button) |
| | Save an element screenshot when a step fails (`capture_on_failure`) | all 4 |

Neither test app opens a modal dialog, and `File > Exit` has no handler in either, so those
journeys are not covered.

### Writing a journey

- Request `journey_app` (a `JourneyApp`): it has the element map (`elements`), `automation`,
  `application`, `menu`, `refresh()` to rebuild the map after the window changes, `bring_to_front()`
  before any real mouse or keyboard input, and `dismiss_popups()` to close open menus.
- Mark the module with `pytestmark = pytest.mark.integration`.
- Use the shared skip fixtures (`skip_on_winforms`, `skip_on_uia3_winforms`, ...) with
  `@pytest.mark.platform_limitation`, or `@pytest.mark.bug(...)`, with the issue in a comment, as in
  `tests/ui`. `test_application_type` and `ui_automation_type` are overridden for `journey_app`, so
  these fixtures work without starting the session-wide `tests/ui` apps.
- Wait for UI changes with `expect()` or `Retry`, not `time.sleep`.

## Known bug markers

Tracked-failure tests are tagged with `pytest-bug` markers linked to GitHub issues. See [Bug tracking](../bug-tracking.md) for the full guide and the current list of marked issues.
