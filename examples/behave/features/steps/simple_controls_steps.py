"""Behave step implementations for the WPF simple-controls feature.

The application is launched once in ``environment.py`` and exposed on the behave ``context`` as
``context.window`` (the main window) and ``context.cf`` (the condition factory).
"""

from behave import given, then, when


@given("the WPF test application is running")
def step_app_running(context) -> None:
    """Assert the shared main window is available.

    :param context: The behave scenario context.
    """
    assert context.window is not None


@then('the window title is "{title}"')
def step_window_title(context, title: str) -> None:
    """Assert the window title matches.

    :param context: The behave scenario context.
    :param title: The expected window title.
    """
    assert context.window.title == title


@when('I enter "{value}" into the text box')
def step_enter_text(context, value: str) -> None:
    """Type ``value`` into the Simple Controls text box.

    :param context: The behave scenario context.
    :param value: The text to enter.
    """
    text_box = context.window.find_first_descendant(condition=context.cf.by_automation_id("TextBox")).as_text_box()
    text_box.text = value


@then('the text box contains "{value}"')
def step_text_box_contains(context, value: str) -> None:
    """Assert the text box currently holds ``value``.

    :param context: The behave scenario context.
    :param value: The expected text.
    """
    text_box = context.window.find_first_descendant(condition=context.cf.by_automation_id("TextBox")).as_text_box()
    assert text_box.text == value


@when("I toggle the test checkbox")
def step_toggle_checkbox(context) -> None:
    """Toggle the test checkbox, remembering its original state.

    :param context: The behave scenario context.
    """
    checkbox = context.window.find_first_descendant(condition=context.cf.by_name("Test Checkbox")).as_check_box()
    context.checkbox_original = checkbox.is_checked
    checkbox.toggle()


@then("the test checkbox state is inverted")
def step_checkbox_inverted(context) -> None:
    """Assert the checkbox state flipped, then restore the original state.

    :param context: The behave scenario context.
    """
    checkbox = context.window.find_first_descendant(condition=context.cf.by_name("Test Checkbox")).as_check_box()
    assert checkbox.is_checked != context.checkbox_original
    # Leave the shared application as we found it.
    checkbox.toggle()
