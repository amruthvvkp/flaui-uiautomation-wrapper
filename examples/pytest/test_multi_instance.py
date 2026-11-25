"""Runnable recipes for the *Multiple instances* guide: several copies of one app, side by side.

Run it from the project root::

    uv run pytest examples/pytest/test_multi_instance.py -v

These tests launch their own copies of the bundled WPF app (they don't use the session app from
``conftest.py``) and close them again. The guide includes each recipe's Python tab from this file via
the ``# --8<-- [start:name]`` / ``# --8<-- [end:name]`` section markers.
"""

from typing import Generator

from flaui.core.application import Application
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation
import pytest

from conftest import find_test_app

EXE = str(find_test_app())


@pytest.fixture
def automation() -> Generator[Automation, None, None]:
    """A fresh automation object with no application attached (overrides the conftest one)."""
    auto = Automation(UIAutomationTypes.UIA3)
    try:
        yield auto
    finally:
        auto.automation_base.dispose()


def test_two_instances(automation: Automation) -> None:
    """Launch two copies, drive each through its own Application, and keep them apart."""
    # --8<-- [start:two_instances]
    from flaui.core.application import Application

    # One Application object per process. automation.application is just the first one;
    # calling launch() on it twice would lose track of the first process.
    with Application() as first, Application() as second:
        first.launch(EXE)
        second.launch(EXE)

        first_window = first.get_main_window(automation)
        second_window = second.get_main_window(automation)
        print(first.process_id, second.process_id)  # two different PIDs

        cf = automation.cf
        first_box = first_window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
        second_box = second_window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
        first_box.text = "instance one"
        second_box.text = "instance two"
        # --8<-- [end:two_instances]
        texts = (first_box.text, second_box.text)
        pids = (first.process_id, second.process_id)
    # Leaving the `with` block closes both processes.
    assert pids[0] != pids[1]
    assert texts == ("instance one", "instance two")  # each copy kept its own text


def test_window_from_handle(automation: Automation) -> None:
    """Go straight from an instance to its window by native handle (no desktop search)."""
    with Application() as first, Application() as second:
        first.launch(EXE)
        second.launch(EXE)
        first.get_main_window(automation)
        second.get_main_window(automation)
        app = second
        # --8<-- [start:from_handle]
        # Each process knows its own main window handle, so no searching is needed.
        window = automation.automation_base.from_handle(app.main_window_handle).as_window()
        # --8<-- [end:from_handle]
        assert window.raw_element.Properties.ProcessId.Value == second.process_id


# Desktop-wide searches ask every top-level window on the machine, so one unresponsive window
# elsewhere on the desktop can make them slow. Give them more than the default 30 s.
@pytest.mark.timeout(180)
def test_find_window_by_process_id(automation: Automation) -> None:
    """Pick one instance's window off the desktop by process id."""
    with Application() as first, Application() as second:
        first.launch(EXE)
        second.launch(EXE)
        first.get_main_window(automation)
        second.get_main_window(automation)
        app = second
        # --8<-- [start:by_process_id]
        desktop = automation.automation_base.get_desktop()
        cf = automation.cf

        # Every copy has the same title, so search by process id: it is unique per instance.
        condition = cf.by_process_id(app.process_id).And(cf.by_name("FlaUI WPF Test App"))
        window = desktop.find_first_child(condition).as_window()
        # --8<-- [end:by_process_id]
        assert window.raw_element.Properties.ProcessId.Value == second.process_id


def test_attach_by_pid(automation: Automation) -> None:
    """Attach to one specific running instance by PID rather than by name."""
    with Application() as launcher, Application() as other:
        launcher.launch(EXE)
        other.launch(EXE)
        launcher.get_main_window(automation)
        other.get_main_window(automation)
        target_pid = other.process_id
        # --8<-- [start:attach_by_pid]
        import psutil

        # attach("WpfApplication.exe") picks *a* matching process: with several running, you
        # can't choose which. List the candidates yourself and attach by PID instead.
        candidates = sorted(
            (p for p in psutil.process_iter(["pid", "name", "create_time"]) if p.info["name"] == "WpfApplication.exe"),
            key=lambda p: p.info["create_time"],
        )
        newest_pid = candidates[-1].info["pid"]  # e.g. the most recently started copy

        app = Application()
        app.attach(newest_pid)
        window = app.get_main_window(automation)
        # --8<-- [end:attach_by_pid]
        assert newest_pid == target_pid
        assert app.process_id == target_pid
        assert window.title == "FlaUI WPF Test App"


@pytest.mark.timeout(180)  # also a desktop-wide search (see test_find_window_by_process_id)
def test_all_windows_of_one_instance(automation: Automation) -> None:
    """List every top-level window that belongs to a single instance."""
    with Application() as app:
        app.launch(EXE)
        app.get_main_window(automation)
        # --8<-- [start:top_level_windows]
        windows = app.get_all_top_level_windows(automation)  # only this process's windows
        titles = [w.title for w in windows]
        # --8<-- [end:top_level_windows]
        assert "FlaUI WPF Test App" in titles
