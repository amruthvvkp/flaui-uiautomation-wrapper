"""Runnable recipes for the *Test design tips* guide: element name maps and pydantic settings.

Run it from the project root::

    uv run pytest examples/pytest/test_name_mapping.py -v

Uses ``app_map.py`` (the element name map) and ``app_settings.py`` (pydantic-settings config).
"""

from flaui.core.automation_elements import Window
from flaui.core.definitions import ToggleState
from flaui.core.tools import Retry
from flaui.lib.enums import UIAutomationTypes
from pydantic import ValidationError
import pytest

from app_map import TestAppMap
from app_settings import ExampleSettings, settings


# --8<-- [start:fixture]
@pytest.fixture
def app(main_window: Window) -> TestAppMap:
    """The element map for the running app: tests talk to `app`, never to raw locators."""
    return TestAppMap(window=main_window)


# --8<-- [end:fixture]


def test_use_the_map(app: TestAppMap) -> None:
    """Tests read like the UI, and every locator lives in app_map.py."""
    # --8<-- [start:use_map]
    app.simple.name_box.text = "Ada Lovelace"
    app.simple.accept_terms.toggle()
    app.simple.invoke_button.invoke()

    headers = [c.name for c in app.complex.key_value_grid.header.columns]  # switches tab itself
    # --8<-- [end:use_map]
    try:
        assert headers == ["Key", "Value"]
        assert app.simple.name_box.text == "Ada Lovelace"  # back on Simple Controls, found afresh
        assert Retry.WhileFalse(lambda: app.simple.invoke_button.name == "Invoked!", timeout=2000)
    finally:
        if app.simple.accept_terms.toggle_state == ToggleState.On:
            app.simple.accept_terms.toggle()


def test_lookups_are_lazy(app: TestAppMap) -> None:
    """Each property access finds the element again, so the map never holds stale references."""
    # --8<-- [start:lazy]
    first = app.simple.name_box
    _ = app.complex.tree  # switching tabs can rebuild the Simple Controls subtree...
    second = app.simple.name_box  # ...but the property simply finds the box again
    # --8<-- [end:lazy]
    assert first.automation_id == second.automation_id == "TextBox"


def test_settings_defaults() -> None:
    """Defaults work out of the box; paths are validated at start-up."""
    assert settings.app_path.exists()
    assert settings.automation_type in (UIAutomationTypes.UIA2, UIAutomationTypes.UIA3)


def test_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variables override defaults and are converted to the right types."""
    # --8<-- [start:settings_env]
    monkeypatch.setenv("EXAMPLE_AUTOMATION_TYPE", "UIA2")  # in CI: an env var on the job
    monkeypatch.setenv("EXAMPLE_LAUNCH_TIMEOUT_MS", "20000")

    configured = ExampleSettings()
    assert configured.automation_type is UIAutomationTypes.UIA2  # str -> enum
    assert configured.launch_timeout_ms == 20000  # str -> int
    # --8<-- [end:settings_env]


def test_settings_reject_bad_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Misconfiguration fails once, with a clear message, before any test touches the UI."""
    # --8<-- [start:settings_invalid]
    monkeypatch.setenv("EXAMPLE_APP_PATH", r"C:\does\not\exist.exe")
    monkeypatch.setenv("EXAMPLE_LAUNCH_TIMEOUT_MS", "50")  # below the ge=1000 floor

    with pytest.raises(ValidationError) as error:
        ExampleSettings()
    print(error.value)  # names both fields: app_path (path does not exist), launch_timeout_ms (>= 1000)
    # --8<-- [end:settings_invalid]
    assert {e["loc"][0] for e in error.value.errors()} == {"app_path", "launch_timeout_ms"}
