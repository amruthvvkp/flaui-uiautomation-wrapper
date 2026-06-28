"""Example pytest suite driving the bundled WPF test application with FlaUI for Python.

Run it from the project root::

    uv run pytest examples/pytest

Each test finds a control on the **Simple Controls** tab by automation id (or name), wraps it with
the matching typed element, and asserts a real interaction. The session-scoped ``automation``
fixture (see ``conftest.py``) launches the application once and disposes it at the end.
"""

from flaui.core.automation_elements import Window
from flaui.core.condition_factory import ConditionFactory


def test_window_title(main_window: Window) -> None:
    """The launched application exposes its title."""
    assert main_window.title == "FlaUI WPF Test App"


def test_enter_text(main_window: Window, condition_factory: ConditionFactory) -> None:
    """Typing into the text box round-trips through the ``text`` property."""
    text_box = main_window.find_first_descendant(
        condition=condition_factory.by_automation_id("TextBox")
    ).as_text_box()
    text_box.text = "hello from pytest"
    assert text_box.text == "hello from pytest"


def test_invoke_button(main_window: Window, condition_factory: ConditionFactory) -> None:
    """The invokable button can be located and invoked through the Invoke pattern."""
    button = main_window.find_first_descendant(
        condition=condition_factory.by_automation_id("InvokableButton")
    ).as_button()
    assert button.name == "Invoke me!"
    button.invoke()  # raises if the Invoke pattern is unavailable


def test_toggle_checkbox(main_window: Window, condition_factory: ConditionFactory) -> None:
    """Toggling the checkbox flips its state; the test restores the original state."""
    checkbox = main_window.find_first_descendant(condition=condition_factory.by_name("Test Checkbox")).as_check_box()
    original = checkbox.is_checked
    try:
        checkbox.toggle()
        assert checkbox.is_checked != original
    finally:
        # The application is shared across the session, so leave the checkbox as we found it.
        if checkbox.is_checked != original:
            checkbox.toggle()


def test_read_slider(main_window: Window, condition_factory: ConditionFactory) -> None:
    """The slider exposes its current value within its reported range."""
    slider = main_window.find_first_descendant(condition=condition_factory.by_automation_id("Slider")).as_slider()
    assert slider.minimum <= slider.value <= slider.maximum
