# Test design tips

Patterns that keep a UI automation suite readable, fast and dependable as it grows. Each section
explains *why* the pattern matters and shows how this project's own test suite uses it.

!!! success "Every Python snippet on this page runs"
    The snippets come from the runnable suites under
    [`examples/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples):
    `examples/pytest/app_map.py`, `app_settings.py`, `test_name_mapping.py` and `conftest.py`, plus
    the unittest and behave suites.

    ```bash
    uv run pytest examples/pytest/test_name_mapping.py -v
    ```

## Build a name map for your elements

A **name map**, also called page objects, gives every element your tests touch a readable name
and keeps its locator in exactly **one** place. Tests then read like the UI
(`app.simple.accept_terms.toggle()`) instead of like a query.

**Why it matters:**

- **Locators change.** When a developer renames an AutomationId, you fix one line in the map, not
  every test that uses it.
- **Navigation lives in one place.** "This control is on the second tab" is written once, in the
  map, instead of each test switching tabs before it finds anything.
- **Your IDE helps.** Properties return typed elements (`TextBox`, `CheckBox`, ...), so you get
  autocompletion for `.text`, `.toggle()`, and so on.
- **The same tests run against different builds.** If two apps have the same screens, give each
  its own map with the same property names and run one set of tests against both.

### A map built on pydantic

=== "Python"

    ```python
    --8<-- "examples/pytest/app_map.py:map"
    ```

=== "C#"

    ```csharp
    public class SimpleControlsPage(Window window)
    {
        private ConditionFactory Cf => window.ConditionFactory;

        public TextBox NameBox =>
            window.FindFirstDescendant(Cf.ByAutomationId("TextBox")).AsTextBox();
        public CheckBox AcceptTerms =>
            window.FindFirstDescendant(Cf.ByName("Test Checkbox")).AsCheckBox();
        public Button InvokeButton =>
            window.FindFirstDescendant(Cf.ByAutomationId("InvokableButton")).AsButton();
    }
    ```

Hand the map to tests through a fixture, and have tests use only the map:

```python
--8<-- "examples/pytest/test_name_mapping.py:fixture"
```

```python
--8<-- "examples/pytest/test_name_mapping.py:use_map"
```

### Find elements when they're used, not when the map is built

Each property runs its lookup **every time** you read it. Don't store found elements on the map, or
in a session fixture:

```python
--8<-- "examples/pytest/test_name_mapping.py:lazy"
```

A stored element points at one specific UI Automation node. That node goes stale when the app
rebuilds that part of its UI: after switching tabs, closing a dialog, re-rendering a list, or
restarting the app. Reading a stale element raises a COM error or `ElementNotFound`. A fresh lookup
costs a few milliseconds ([measured](performance.md#element-name-maps-cost-nothing-extra)), which is a good trade for never hitting a stale reference. The objects
that are safe to keep are the ones that live as long as the app does: the `Automation`, the
`Application`, and the main `Window`.

### Tips for the map itself

- **Name properties after what they mean** (`accept_terms`), not after their ID (`checkbox_17`).
- **Use the most stable locator.** AutomationId first, then Name (which changes with the UI
  language), then ControlType. If you can, ask the developers to add AutomationIds; that is the
  biggest single improvement to test stability.
- **Return the specific type.** `.as_text_box()`, `.as_check_box()`, and so on, so callers don't
  have to.
- **One class per screen or dialog.** Create a dialog's map when the dialog opens, for example from
  `window.modal_windows[0]`, rather than finding the dialog in advance.
- **Keep assertions out of the map.** The map finds and returns elements; tests decide what is
  correct.

### How this project does it

The project's own suite keeps one map per test app in
[`tests/test_utilities/elements/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/tests/test_utilities/elements):
`wpf_application/` and `winforms_application/`. Each has a class per tab (`simple_controls.py`,
`complex_controls.py`, `menu.py`, ...) and a root map that `get_wpf_application_elements(main_window)`
builds.

Both maps expose the **same property names**. The class-scoped `test_application` fixture in
`tests/conftest.py` returns the right map for each combination of WPF / WinForms and UIA2 / UIA3, so
a single test runs on all four. Tab pages select themselves inside their `parent_element` property,
which is the navigation-in-the-map rule in practice.

!!! note "`BaseModel` for maps, `BaseSettings` for configuration"
    The project's maps currently subclass pydantic-settings' `BaseSettings`. That works, but
    `BaseSettings` also reads environment variables for every field, so a variable named
    `PROCESS_NAME` would quietly override the map's `process_name` field. The example above uses
    a plain `BaseModel` with `arbitrary_types_allowed=True`, which validates the fields without
    reading the environment. Keep `BaseSettings` for real configuration, covered next.

## Keep configuration in pydantic-settings

Put everything a run might change in one settings class: app paths, which automation stack to use,
timeouts, and where to write artifacts. Values come from environment variables or a `.env` file,
are converted to the right types, and are validated **once, at start-up**.

```python
--8<-- "examples/pytest/app_settings.py:settings"
```

**Why it matters:**

- **One suite, every environment.** CI sets `EXAMPLE_AUTOMATION_TYPE=UIA2` on a job, a developer
  sets `EXAMPLE_LAUNCH_TIMEOUT_MS` in their `.env`, and neither touches code:

    ```python
    --8<-- "examples/pytest/test_name_mapping.py:settings_env"
    ```

- **Mistakes surface early and clearly.** A wrong path or an out-of-range timeout fails before any
  test opens a window, and the error names each bad field:

    ```python
    --8<-- "examples/pytest/test_name_mapping.py:settings_invalid"
    ```

**Tips:**

- **Always set an `env_prefix`.** Without one, a field called `path` would read your `PATH`
  variable. FlaUI's own settings use `FLAUI_` for the same reason (see
  [Configuration](configuration.md#environment-variables)).
- **Use pydantic's types to validate for you:** `FilePath` / `DirectoryPath` (must exist), enums
  (`UIAutomationTypes`), `Field(ge=...)` for ranges, and `SecretStr` for passwords, so they don't
  show up in logs or tracebacks.
- **Create the settings object once** and import it everywhere, as with `settings = ExampleSettings()`.
  In tests, build a fresh `ExampleSettings()` with `monkeypatch.setenv(...)` to try other values.
- **Don't commit `.env`.** Commit a `.env.example` that lists the variables instead.

### How this project does it

- [`tests/test_utilities/config.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/tests/test_utilities/config.py)
  defines `TestSettings`, where both test-app paths are `FilePath`s, so a missing build fails at
  import time.
- [`flaui/lib/config.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/flaui/lib/config.py)
  holds the library's own settings with the `FLAUI_` prefix.
- Every element and pattern wrapper in the library is a pydantic model. That's why constructing one
  around a missing element raises `ElementNotFound` straight away, instead of failing later with a
  confusing `None` error.

## Where to start the application

Most test frameworks let you run setup code at several levels: once per run, per file, per class,
or per test. Where you launch the app is the biggest single factor in how fast your suite is and
how far one failure spreads.

### What matters

1. **Set up the bridge before anything else.** `setup_pythonnet_bridge()` must run before the
   first FlaUI import that touches C#. Put it at the very top of the file your framework loads
   first: `conftest.py` for pytest, `environment.py` for behave, or the top of the test module for
   unittest. If it runs too late, the C# namespaces fail to import.
2. **Launching costs seconds; reusing the app costs isolation.** Starting an app and waiting for its
   window typically takes 1–3 s, so launching per test multiplies your run time. Sharing one app
   across tests is fast, but a test that leaves a dialog open, a checkbox ticked, or the wrong tab
   selected can break the tests after it.
3. **Cleanup must run even when setup or a test fails.** Use `yield` + `finally` (pytest),
   `addClassCleanup` (unittest), or `after_all` (behave), and kill the app if closing it fails.
   Otherwise a crashed run leaves copies running, and the next run may attach to the wrong one.
4. **Elements must not outlive the app they came from.** Keep the `Automation` and `Application`
   at the scope where you launch, and look elements up inside each test (see the
   [name map](#find-elements-when-theyre-used-not-when-the-map-is-built)).

### What matters less than you might think

- **Creating the `Automation` object** is cheap. What costs time is launching the app.
- **Creating map and page objects per test** is cheap, because they hold no elements. Build them
  in function-scoped fixtures.
- **Reusing one `ConditionFactory`** makes no measurable difference; take it from
  `automation.cf`.

### Choosing a scope

| Scope | Speed | Isolation | Use it when |
|-------|-------|-----------|-------------|
| Once per run (pytest `session`, behave `before_all`, unittest `setUpModule`) | Fastest | Lowest: tests share state | Most suites, together with a reset step between tests |
| Per file or class (pytest `module` / `class`, unittest `setUpClass`, behave `before_feature`) | Medium | Groups of tests are isolated from each other | Feature areas that change a lot of state |
| Per test (pytest `function`, unittest `setUp`, behave `before_scenario`) | Slowest | Full | Tests that close windows, crash the app, or test start-up itself |

A good default: **launch once per run, and reset to a known screen before each test.** This
project's suite launches all four app/automation combinations once per session. Its class-scoped
`test_application` fixture then clicks back to the **Simple Controls** tab, retrying up to five
times, before handing over the map.

### Per framework

=== "pytest"

    `conftest.py` sets up the bridge first, then launches the app once per session. `finally` makes
    sure the app is killed even if a test fails or the run is interrupted:

    ```python
    --8<-- "examples/pytest/conftest.py:bridge"

    --8<-- "examples/pytest/conftest.py:session_fixture"
    ```

    Build per-test objects (maps, the main window) in function-scoped fixtures on top of the session
    one, as `main_window` and `app` do.

=== "unittest"

    `setUpClass` / `tearDownClass` share one app across a class:

    ```python
    --8<-- "examples/unittest/test_simple_controls.py:class_setup"
    ```

    `tearDownClass` does **not** run if `setUpClass` raises after launching the app. For guaranteed
    cleanup, register it straight after launching with
    `cls.addClassCleanup(cls.automation.application.kill)`. Use `setUpModule` /
    `addModuleCleanup` to share one app across a whole module.

=== "behave"

    `environment.py` is loaded before the step modules, so set up the bridge at the top of that
    file. `before_all` launches once per run and stores everything on `context`:

    ```python
    --8<-- "examples/behave/features/environment.py:before_all"
    ```

    Use `before_feature` / `before_scenario` for narrower scopes, and reset UI state in
    `after_scenario`.

=== "Testplan"

    Launch in the suite's `setup(self, env)` and clean up in `teardown(self, env)`. See the
    [Testplan example](examples/testplan.md). For isolation between groups of tests, put each group
    in its own `MultiTest`, with its own app.

### Capture evidence on failure

A screenshot of the moment a test failed often explains the failure on its own. Take it in a
framework hook, so every test gets it without any changes to the tests:

=== "pytest"

    ```python
    --8<-- "examples/pytest/conftest.py:screenshot_on_failure"
    ```

=== "behave"

    ```python
    --8<-- "examples/behave/features/environment.py:after_step"
    ```

Upload the `artifacts/` folder from CI (it's git-ignored). With
[C# logging](configuration.md#c-logging) turned on, `caplog` and the pytest report add a text
timeline next to the image.

## More tips

- **Prefer patterns to real input.** `invoke()`, `toggle()` and `text = ...` work through UI
  Automation patterns: they are fast, they work while the window is in the background, and
  nothing else on the desktop can interfere. Use the mouse and keyboard only when the app needs
  real input events.
- **Never `sleep()` to wait for the UI.** Use `post_wait=` on input, `Retry.WhileFalse(...)` for
  a condition, or `expect(element).to_...()` for an assertion that waits. Each of these returns
  as soon as the UI is ready, and each fails with a clear message when it isn't.
- **Assert on enums, not strings.** `assert checkbox.toggle_state == ToggleState.On` keeps working
  when the UI language changes, and typos show up as errors.
- **Mark platform limitations instead of deleting tests.** The project uses `skip_if_matrix`,
  `platform_limitation` and `pytest-bug` markers so a known problem stays visible. See
  [Bug tracking](bug-tracking.md).
- **Kill leftovers before the run.** A crashed or interrupted run can leave copies of the app
  running, and the next run may then attach to the wrong one. `tests/test_utilities/base.py` has a
  `force_close_test_application_process()` helper that ends stray test-app processes with
  `psutil`. Call something like it at the start of your session fixture.
- **Running several copies or workers?** See [Multiple instances](multi-instance.md).
