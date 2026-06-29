"""Unit tests closing coverage gaps in :mod:`flaui.core.application`.

The C# ``FlaUI.Core.Application`` is patched with a ``MagicMock`` so these tests exercise the
Python wrapper's property delegation, automation-object coercion, retry logic, and the
launch/attach/close family without driving a real process. Paths that the live UI matrix does not
reach (error branches, store-app launch, attach variants) are the focus here.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from flaui.core.application import Application, _coerce_cs_automation
from flaui.core.automation_base import AutomationBase as PyAutomationBase


def _app_with_mock() -> tuple[Application, MagicMock]:
    """Return an ``Application`` whose backing C# object is a fresh ``MagicMock``."""
    app = Application()
    fake = MagicMock()
    app._application = fake
    return app, fake


# --------------------------------------------------------------------------- #
# _coerce_cs_automation
# --------------------------------------------------------------------------- #
def test_coerce_unwraps_python_automation_base() -> None:
    """A Python ``AutomationBase`` facade yields its underlying ``raw_automation``."""
    sentinel = MagicMock()
    py = PyAutomationBase(raw_automation=sentinel)
    assert _coerce_cs_automation(py) is sentinel


def test_coerce_reads_cs_automation_attribute() -> None:
    """An object exposing ``cs_automation`` is unwrapped through that attribute."""
    holder = MagicMock()
    assert _coerce_cs_automation(holder) is holder.cs_automation


def test_coerce_rejects_unknown_object() -> None:
    """An object with no recognised automation shape raises ``AttributeError``."""

    class _Bare:
        """Object intentionally lacking a ``cs_automation`` attribute."""

    with pytest.raises(AttributeError):
        _coerce_cs_automation(_Bare())


# --------------------------------------------------------------------------- #
# Property delegation
# --------------------------------------------------------------------------- #
def test_property_delegation_reads_backing_object() -> None:
    """Each read-only property returns the matching C# member verbatim."""
    app, fake = _app_with_mock()
    fake.Name = "notepad"
    fake.ProcessId = 4321
    fake.IsStoreApp = True
    fake.HasExited = False
    fake.MainWindowHandle = 99
    fake.ExitCode = 0
    fake.CloseTimeout = 2000

    assert app.name == "notepad"
    assert app.process_id == 4321
    assert app.is_store_app is True
    assert app.has_exited is False
    assert app.main_window_handle == 99
    assert app.exit_code == 0
    assert app.close_timeout == 2000


def test_close_timeout_setter_writes_through() -> None:
    """Assigning ``close_timeout`` writes the value onto the C# object."""
    app, fake = _app_with_mock()
    app.close_timeout = 5000
    assert fake.CloseTimeout == 5000


# --------------------------------------------------------------------------- #
# launch / attach / store-app / lifecycle
# --------------------------------------------------------------------------- #
def test_launch_rebinds_to_launched_process() -> None:
    """``launch`` replaces the backing object with the launched process handle."""
    app, fake = _app_with_mock()
    launched = MagicMock()
    launched.ProcessId = 123  # truthy -> skips the AttachOrLaunch fallback
    fake.Launch.return_value = launched

    app.launch("notepad.exe", "arg")

    fake.Launch.assert_called_once_with("notepad.exe", "arg")
    assert app._application is launched


def test_launch_falls_back_to_attach_or_launch_when_unbound() -> None:
    """When the launched process reports no PID, ``launch`` retries via AttachOrLaunch."""
    app, fake = _app_with_mock()
    launched = MagicMock()
    launched.ProcessId = 0  # falsy -> triggers the fallback
    attached = MagicMock()
    launched.AttachOrLaunch.return_value = attached
    fake.Launch.return_value = launched

    app.launch("notepad.exe")

    launched.AttachOrLaunch.assert_called_once()
    assert app._application is attached


def test_launch_store_app_rebinds() -> None:
    """``launch_store_app`` binds to the store-app handle returned by C#."""
    app, fake = _app_with_mock()
    store = MagicMock()
    fake.LaunchStoreApp.return_value = store
    app.launch_store_app("Some.App_id", "arg")
    fake.LaunchStoreApp.assert_called_once_with("Some.App_id", "arg")
    assert app._application is store


def test_attach_rebinds() -> None:
    """``attach`` binds to the process resolved by C# ``Attach``."""
    app, fake = _app_with_mock()
    attached = MagicMock()
    fake.Attach.return_value = attached
    app.attach(1234)
    fake.Attach.assert_called_once_with(1234)
    assert app._application is attached


def test_attach_or_launch_rebinds() -> None:
    """``attach_or_launch`` wraps the process path in a ProcessStartInfo and rebinds."""
    app, fake = _app_with_mock()
    bound = MagicMock()
    fake.AttachOrLaunch.return_value = bound
    app.attach_or_launch("notepad.exe")
    fake.AttachOrLaunch.assert_called_once()
    assert app._application is bound


def test_kill_dispose_close_delegate() -> None:
    """``kill`` / ``dispose`` / ``close`` forward to the C# object."""
    app, fake = _app_with_mock()
    fake.Close.return_value = True
    app.kill()
    app.dispose()
    assert app.close(kill_if_close_fails=False) is True
    fake.Kill.assert_called_once()
    fake.Dispose.assert_called_once()
    fake.Close.assert_called_once_with(False)


def test_wait_helpers_pass_timespans() -> None:
    """Wait helpers forward to the C# object and return its result."""
    app, fake = _app_with_mock()
    fake.WaitWhileMainHandleIsMissing.return_value = True
    fake.WaitWhileBusy.return_value = False
    assert app.wait_while_main_handle_is_missing(1000) is True
    assert app.wait_while_busy(1000) is False
    # The infinite-timeout (None) branch forwards None straight through.
    app.wait_while_busy()
    fake.WaitWhileBusy.assert_called_with(None)


# --------------------------------------------------------------------------- #
# get_all_top_level_windows / get_main_window
# --------------------------------------------------------------------------- #
def test_get_all_top_level_windows_wraps_results() -> None:
    """Each C# top-level window is wrapped in a Python ``Window``."""
    app, fake = _app_with_mock()
    fake.GetAllTopLevelWindows.return_value = [MagicMock(), MagicMock()]
    windows = app.get_all_top_level_windows(MagicMock())
    assert len(windows) == 2


def test_get_main_window_returns_first_available(monkeypatch: pytest.MonkeyPatch) -> None:
    """``get_main_window`` returns a wrapped Window as soon as one is available."""
    app, fake = _app_with_mock()
    fake.HasExited = False
    fake.ProcessId = 4321
    fake.MainWindowHandle = 7
    fake.GetMainWindow.return_value = MagicMock()

    # Avoid any real polling sleeps.
    monkeypatch.setattr("flaui.core.application.time.sleep", lambda *_: None)

    window = app.get_main_window(MagicMock())
    assert window is not None
    fake.GetMainWindow.assert_called()


def test_get_main_window_raises_when_process_exited(monkeypatch: pytest.MonkeyPatch) -> None:
    """When the process exits before a window appears, the stored error is raised."""
    app, fake = _app_with_mock()
    fake.HasExited = True  # breaks the retry loop immediately
    fake.GetMainWindow.return_value = None  # final attempt also fails
    monkeypatch.setattr("flaui.core.application.time.sleep", lambda *_: None)

    with pytest.raises(RuntimeError):
        app.get_main_window(MagicMock())
