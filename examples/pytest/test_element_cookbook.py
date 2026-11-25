"""Runnable Element Cookbook: one test per control, driving the bundled WPF test application.

Run it from the project root::

    uv run pytest examples/pytest/test_element_cookbook.py -v

The docs page *Examples → Element Cookbook* includes the Python tab of each recipe straight from
this file. The ``# --8<-- [start:name]`` / ``# --8<-- [end:name]`` comments mark those sections, so
the published snippets are always code that actually runs. Keep each section self-contained: it
should read naturally given only a ``window`` (the main ``Window``) and ``cf`` (the
``ConditionFactory``).
"""

from typing import Generator

from flaui.core.automation_elements import Tab, Window
from flaui.core.condition_factory import ConditionFactory
from flaui.core.definitions import ControlType, ToggleState
from flaui.core.tools import Retry
import pytest

SIMPLE_CONTROLS = 0
COMPLEX_CONTROLS = 1


@pytest.fixture
def window(main_window: Window) -> Window:
    """Alias the main window to the ``window`` name the cookbook snippets use.

    :param main_window: The application's main window.
    :return: The same ``Window``.
    """
    return main_window


@pytest.fixture
def cf(condition_factory: ConditionFactory) -> ConditionFactory:
    """Alias the condition factory to the ``cf`` name the cookbook snippets use.

    :param condition_factory: The shared condition factory.
    :return: The same ``ConditionFactory``.
    """
    return condition_factory


@pytest.fixture
def tab(window: Window, cf: ConditionFactory) -> Tab:
    """Return the application's main tab control.

    :param window: The application's main window.
    :param cf: The shared condition factory.
    :return: The ``Tab`` hosting the Simple / Complex / More Controls pages.
    """
    return window.find_first_descendant(cf.by_control_type(ControlType.Tab)).as_tab()


@pytest.fixture
def simple_controls(tab: Tab) -> Generator[None, None, None]:
    """Make sure the Simple Controls page is showing.

    :param tab: The main tab control.
    :yield: Nothing; the page stays selected for the test.
    """
    tab.select_tab_item(SIMPLE_CONTROLS, post_wait=True)
    yield


@pytest.fixture
def complex_controls(tab: Tab) -> Generator[None, None, None]:
    """Show the Complex Controls page, then switch back so other tests find Simple Controls.

    :param tab: The main tab control.
    :yield: Nothing; the page stays selected for the test.
    """
    tab.select_tab_item(COMPLEX_CONTROLS, post_wait=True)
    yield
    tab.select_tab_item(SIMPLE_CONTROLS, post_wait=True)


# ---------------------------------------------------------------------------------------------
# Interactive controls
# ---------------------------------------------------------------------------------------------


@pytest.mark.usefixtures("simple_controls")
def test_button(window: Window, cf: ConditionFactory) -> None:
    """Find a button by automation id and invoke it."""
    # --8<-- [start:button]
    button = window.find_first_descendant(cf.by_automation_id("InvokableButton")).as_button()
    button.invoke()  # Invoke pattern: no mouse movement, works when the window is in the background
    # --8<-- [end:button]
    # The test app renames the button once the invoke is processed.
    assert Retry.WhileFalse(lambda: button.name == "Invoked!", timeout=2000)


@pytest.mark.usefixtures("simple_controls")
def test_checkbox(window: Window, cf: ConditionFactory) -> None:
    """Toggle a checkbox and read back its state."""
    # --8<-- [start:checkbox]
    checkbox = window.find_first_descendant(cf.by_name("Test Checkbox")).as_check_box()
    checkbox.toggle()
    state = checkbox.toggle_state  # ToggleState.On / Off / Indeterminate
    # --8<-- [end:checkbox]
    try:
        assert state in (ToggleState.On, ToggleState.Off)
    finally:
        checkbox.toggle()  # restore the shared application state


@pytest.mark.usefixtures("simple_controls")
def test_radio_button(window: Window, cf: ConditionFactory) -> None:
    """Select a radio button by assigning ``is_checked``."""
    # --8<-- [start:radio_button]
    radio = window.find_first_descendant(cf.by_automation_id("RadioButton1")).as_radio_button()
    radio.is_checked = True
    # --8<-- [end:radio_button]
    assert radio.is_checked


@pytest.mark.usefixtures("simple_controls")
def test_combo_box(window: Window, cf: ConditionFactory) -> None:
    """Select a combo box item by its text (an index works too)."""
    # --8<-- [start:combo_box]
    combo = window.find_first_descendant(cf.by_automation_id("NonEditableCombo")).as_combo_box()
    combo.select("Item 2")  # or combo.select(1)
    selected = combo.selected_item.text
    # --8<-- [end:combo_box]
    assert selected == "Item 2"


@pytest.mark.usefixtures("simple_controls")
def test_text_box(window: Window, cf: ConditionFactory) -> None:
    """Set and read the text of a text box."""
    # --8<-- [start:text_box]
    text_box = window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
    text_box.text = "hello"  # Value pattern: sets the text directly
    text_box.enter(" world")  # Keyboard: types into the focused box
    # --8<-- [end:text_box]
    assert text_box.text.endswith("world")


@pytest.mark.usefixtures("simple_controls")
def test_slider(window: Window, cf: ConditionFactory) -> None:
    """Move a slider and read its range."""
    # --8<-- [start:slider]
    slider = window.find_first_descendant(cf.by_automation_id("Slider")).as_slider()
    slider.value = 6
    print(slider.minimum, slider.value, slider.maximum)
    # --8<-- [end:slider]
    assert slider.value == 6


# ---------------------------------------------------------------------------------------------
# Containers
# ---------------------------------------------------------------------------------------------


@pytest.mark.usefixtures("simple_controls")
def test_list_box(window: Window, cf: ConditionFactory) -> None:
    """Select a list box item by its text."""
    # --8<-- [start:list_box]
    list_box = window.find_first_descendant(cf.by_automation_id("ListBox")).as_list_box()
    item = list_box.select("ListBox Item #2")  # or list_box.select(1)
    names = [i.text for i in list_box.items]
    # --8<-- [end:list_box]
    assert item.text == "ListBox Item #2"
    assert "ListBox Item #2" in names


@pytest.mark.usefixtures("complex_controls")
def test_tree(window: Window, cf: ConditionFactory) -> None:
    """Expand tree nodes and select a leaf."""
    # --8<-- [start:tree]
    tree = window.find_first_descendant(cf.by_automation_id("treeView1")).as_tree()
    tree.items[0].expand()
    tree.items[0].items[1].expand()
    tree.items[0].items[1].items[0].select()
    selected = tree.selected_tree_item.text
    # --8<-- [end:tree]
    assert selected == "Lvl3 a"


@pytest.mark.usefixtures("complex_controls")
def test_grid(window: Window, cf: ConditionFactory) -> None:
    """Read grid headers and cells, then select a row."""
    # --8<-- [start:grid]
    grid = window.find_first_descendant(cf.by_automation_id("listView1")).as_grid()
    headers = [column.name for column in grid.header.columns]  # ["Key", "Value"]
    first_row = [cell.value for cell in grid.rows[0].cells]  # ["1", "10"]
    grid.select(1)
    # --8<-- [end:grid]
    assert headers == ["Key", "Value"]
    assert first_row == ["1", "10"]
    assert grid.selected_item.cells[0].value == "2"


def test_tab(tab: Tab) -> None:
    """Switch tabs by index and read the selected tab."""
    # --8<-- [start:tab]
    tab.select_tab_item(1, post_wait=True)  # "Complex Controls"
    selected = tab.selected_tab_item.name
    # --8<-- [end:tab]
    try:
        assert selected == "Complex Controls"
    finally:
        tab.select_tab_item(SIMPLE_CONTROLS, post_wait=True)


# ---------------------------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------------------------


@pytest.mark.usefixtures("simple_controls")
def test_label(window: Window, cf: ConditionFactory) -> None:
    """Read the text of a label."""
    # --8<-- [start:label]
    label = window.find_first_descendant(cf.by_text("Test Label")).as_label()
    text = label.text
    # --8<-- [end:label]
    assert text == "Test Label"


@pytest.mark.usefixtures("simple_controls")
def test_progress_bar(window: Window, cf: ConditionFactory) -> None:
    """Read a progress bar's value and range."""
    # --8<-- [start:progress_bar]
    bar = window.find_first_descendant(cf.by_automation_id("ProgressBar")).as_progress_bar()
    progress = (bar.value - bar.minimum) / (bar.maximum - bar.minimum)
    # --8<-- [end:progress_bar]
    assert 0.0 <= progress <= 1.0


# ---------------------------------------------------------------------------------------------
# Windows
# ---------------------------------------------------------------------------------------------


def test_window_and_title_bar(window: Window) -> None:
    """Read window state, its modal dialogs, and its title bar."""
    # --8<-- [start:window]
    print(window.title)  # "FlaUI WPF Test App"
    dialogs = window.modal_windows  # [] while no modal dialog is open
    title_bar = window.title_bar  # .minimize_button / .maximize_button / .restore_button / .close_button
    # --8<-- [end:window]
    assert window.title == "FlaUI WPF Test App"
    assert dialogs == []
    assert title_bar.is_available
