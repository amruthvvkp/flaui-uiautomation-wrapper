---
name: flaui-write-tests
description: Write pytest UI tests with FlaUI for Python. Covers the conftest bridge and session fixture, element name maps (page objects) on pydantic, asserting against enums, auto-waiting expect() assertions, and the project's UIA2/UIA3 x WinForms/WPF matrix fixtures. Use when adding or porting Windows desktop UI tests, or when contributing tests to flaui-uiautomation-wrapper.
---

# FlaUI for Python: write tests

FlaUI works with any test framework (pytest, unittest, behave, Robot Framework, Testplan). These
notes use pytest. Complete runnable suites live in `examples/` in the repository.

## conftest.py: bridge first, then one app per session

The bridge must be initialised at the very top of `conftest.py`, before other imports. Fence it so
import sorters leave it alone:

```python
# isort: off  -- the bridge must be initialised before any C#-backed import is used.
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

from flaui.core.automation_elements import Window
from flaui.core.condition_factory import ConditionFactory
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

# isort: on
```

Launching an app is slow, so launch it once per session and always clean up:

```python
@pytest.fixture(scope="session")
def automation() -> Generator[Automation, None, None]:
    """Launch the WPF test application for the whole session and dispose it afterwards.

    :yield: A ready ``Automation`` instance with the application launched.
    """
    auto = Automation(UIAutomationTypes.UIA3)
    auto.application.launch(str(find_test_app()))
    auto.application.wait_while_main_handle_is_missing(3000)
    try:
        yield auto
    finally:
        auto.application.kill()
        auto.automation_base.dispose()
```

Because the app is shared, a test that changes state (toggles, selections, text) must restore it
(`try`/`finally`) or reset it in a fixture.

## Name maps: one locator, one place

Give each element a readable property on a pydantic model, and find the element **when the property
is read**, not when the map is built, so stale references cannot leak between tests:

```python
class PageMap(BaseModel):
    """Base for every page: holds the window and finds elements *when they are used*."""

    # FlaUI elements are pydantic models wrapping C# objects; allow them as fields.
    model_config = ConfigDict(arbitrary_types_allowed=True)

    window: Window
```

The full map is `examples/pytest/app_map.py`.

## Tests and assertions

- Assert against **enums**, not strings: `ToggleState.On`, `ControlType.Button`, `ExpandCollapseState`.
- Wait for asynchronous UI changes instead of asserting once:

```python
button.invoke()  # raises if the Invoke pattern is unavailable
# The test app renames the button once the invoke is processed.
assert Retry.WhileFalse(lambda: button.name == "Invoked!", timeout=2000)
```

`flaui.core.expectations.expect` gives Playwright-style assertions that retry until a timeout:

```python
from flaui.core.expectations import expect

text_box = window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
text_box.text = "42"

expect(text_box).to_be_visible()
expect(text_box).to_be_enabled(timeout=2000)
expect(text_box).to_have_text("42")  # to_have_value() reads `.value` (sliders, spinners, ...)
expect(text_box).not_.to_be_offscreen()
```

Capture a screenshot on failure with a `pytest_runtest_makereport` hook and
`flaui.core.capturing.Capture.main_screen()`. A ready-made hook is in `examples/pytest/conftest.py`
(section `screenshot_on_failure`).

## Contributing to flaui-uiautomation-wrapper itself

The project's own suite (`tests/`) runs every UI test on a 2 x 2 matrix: UIA2/UIA3 x the bundled
WinForms/WPF test apps.

- Use the fixtures in `tests/conftest.py`. `test_application` (class scoped) is the element map for
  the current combination. `ui_automation_type` and `test_application_type` (`"WinForms"` or
  `"WPF"`) name it. `condition_factory` is its factory.
- Element maps live in `tests/test_utilities/elements/{winforms,wpf}_application/`. Both expose the
  same property names (`test_application.simple_controls_tab.read_only_checkbox`), so one test body
  covers both apps.
- Put skips in fixtures (`skip_on_winforms`, `skip_on_wpf`, `skip_on_uia2`, `skip_on_uia3`), not
  in test bodies. Mark tracked failures with `pytest.mark.xfail` or the `bug` marker.
- Type-hint every fixture and always run with the `uv run` prefix:

```bash
uv run pytest tests/ui/ -k "UIA3_WPF"   # one matrix combination
```

The step-by-step guide is `docs/contributing/testing.md`. To port FlaUI C# tests, see
`docs/contributing/porting-tests.md`.
