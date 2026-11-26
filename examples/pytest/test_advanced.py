"""Runnable recipes for the *Advanced* guide: XPath, combined conditions, tree walking, caching,
retries, fluent assertions and ``post_wait``.

Run it from the project root::

    uv run pytest examples/pytest/test_advanced.py -v

The docs page *Guide → Advanced* includes the Python tab of each recipe straight from this file via
the ``# --8<-- [start:name]`` / ``# --8<-- [end:name]`` section markers.
"""

from flaui.core.automation_elements import AutomationElement, Window
from flaui.core.condition_factory import ConditionFactory
from flaui.core.definitions import ControlType
from flaui.modules.automation import Automation


def test_xpath(main_window: Window) -> None:
    """Find elements with XPath."""
    window = main_window
    # --8<-- [start:xpath]
    button = window.find_first_by_x_path("//Button[@AutomationId='InvokableButton']").as_button()
    tabs = window.find_all_by_x_path("//Tab/TabItem")  # every tab page
    checkbox = window.find_first_by_x_path("//CheckBox[@Name='Test Checkbox']").as_check_box()
    # --8<-- [end:xpath]
    assert button.automation_id == "InvokableButton"
    assert [t.name for t in tabs][:2] == ["Simple Controls", "Complex Controls"]
    assert checkbox.name == "Test Checkbox"


def test_combined_conditions(main_window: Window, condition_factory: ConditionFactory) -> None:
    """Combine conditions with ``&`` / ``|`` / ``~`` (or ``and_`` / ``or_`` / ``not_``)."""
    window, cf = main_window, condition_factory
    # --8<-- [start:conditions]
    # AND: a Button whose AutomationId is "InvokableButton"
    invoke = cf.by_control_type(ControlType.Button) & cf.by_automation_id("InvokableButton")

    # OR: either radio button
    radios = cf.by_automation_id("RadioButton1") | cf.by_automation_id("RadioButton2")

    # NOT: every check box except the three-state one
    two_state = cf.by_control_type(ControlType.CheckBox) & ~cf.by_automation_id("ThreeStateCheckBox")

    # The same with methods: and_() / or_() / not_()
    same_invoke = cf.by_control_type(ControlType.Button).and_(cf.by_automation_id("InvokableButton"))

    button = window.find_first_descendant(invoke)
    radio_buttons = window.find_all_descendants(radios)
    check_boxes = window.find_all_descendants(two_state)
    # --8<-- [end:conditions]
    assert str(same_invoke) == str(invoke)
    assert button.automation_id == "InvokableButton"
    assert len(radio_buttons) == 2
    assert all(cb.automation_id != "ThreeStateCheckBox" for cb in check_boxes)


def test_true_condition(main_window: Window, condition_factory: ConditionFactory) -> None:
    """Build a condition up from ``true_condition()``."""
    window, cf = main_window, condition_factory
    # --8<-- [start:true_condition]
    # false_condition() matches nothing, so it is the neutral start for a chain of "|"
    wanted = ["InvokableButton", "RadioButton1", "ThreeStateCheckBox"]
    any_of = ConditionFactory.false_condition()
    for automation_id in wanted:
        any_of = any_of | cf.by_automation_id(automation_id)

    # true_condition() matches everything, so it is the neutral start for a chain of "&"
    button_condition = ConditionFactory.true_condition() & cf.by_control_type(ControlType.Button)

    found = window.find_all_descendants(any_of)
    buttons = window.find_all_descendants(button_condition)
    # --8<-- [end:true_condition]
    assert {e.automation_id for e in found} == set(wanted)
    assert buttons and all(b.control_type == ControlType.Button for b in buttons)


def test_collection_helpers(main_window: Window, condition_factory: ConditionFactory) -> None:
    """Filter ``find_all_*`` results with the collection helpers."""
    window, cf = main_window, condition_factory
    # --8<-- [start:collections]
    buttons = window.find_all_descendants(cf.by_control_type(ControlType.Button))
    first = buttons.first  # None when empty
    enabled = buttons.filter(lambda b: b.is_enabled)
    invokable = buttons.where(automation_id="InvokableButton")
    # --8<-- [end:collections]
    assert first is not None
    assert len(enabled) <= len(buttons)
    assert len(invokable) == 1


def test_tree_walker(automation: Automation, main_window: Window) -> None:
    """Walk the direct children of the window with the raw-view tree walker."""
    window = main_window
    # --8<-- [start:tree_walker]
    walker = automation.tree_walker  # FlaUI ITreeWalker over the raw view
    names = []
    child = walker.GetFirstChild(window.raw_element)
    while child is not None:
        names.append(AutomationElement(raw_element=child).control_type)
        child = walker.GetNextSibling(child)
    # Most of the time the Pythonic equivalent is simpler:
    children = window.find_all_children()
    # --8<-- [end:tree_walker]
    assert len(names) == len(children)


def test_cache_request(automation: Automation, main_window: Window, condition_factory: ConditionFactory) -> None:
    """Fetch the names of all buttons in one cached round trip."""
    window, cf = main_window, condition_factory
    # --8<-- [start:cache_request]
    from flaui.core.cache_request import CacheRequest
    from flaui.core.definitions import TreeScope

    cache_request = CacheRequest()
    cache_request.tree_scope = TreeScope.Element
    cache_request.add_property(automation.cs_automation.PropertyLibrary.Element.Name)

    with cache_request.activate():
        # Elements found while the request is active come back with Name pre-fetched,
        # so reading it does not cost another cross-process call per element.
        buttons = window.find_all_descendants(cf.by_control_type(ControlType.Button))
        names = [b.name for b in buttons]
    # --8<-- [end:cache_request]
    assert "Invoke me!" in names or "Invoked!" in names


def test_retry(main_window: Window, condition_factory: ConditionFactory) -> None:
    """Poll until an element appears (or a condition holds)."""
    window, cf = main_window, condition_factory
    # --8<-- [start:retry]
    from flaui.core.tools import Retry

    # Keep trying while the lookup raises ElementNotFound; give up after 5 s.
    button = Retry.WhileException(
        lambda: window.find_first_descendant(cf.by_automation_id("InvokableButton")),
        timeout=5000,
        interval=100,
        throw_on_timeout=True,
    ).as_button()

    # Or wait for a predicate to become true.
    ready = Retry.WhileFalse(lambda: button.is_enabled, timeout=2000)
    # --8<-- [end:retry]
    assert ready


def test_expect(main_window: Window, condition_factory: ConditionFactory) -> None:
    """Auto-waiting, Playwright-style assertions."""
    window, cf = main_window, condition_factory
    # --8<-- [start:expect]
    from flaui.core.expectations import expect

    text_box = window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
    text_box.text = "42"

    expect(text_box).to_be_visible()
    expect(text_box).to_be_enabled(timeout=2000)
    expect(text_box).to_have_text("42")  # to_have_value() reads `.value` (sliders, spinners, ...)
    expect(text_box).not_.to_be_offscreen()
    # --8<-- [end:expect]


def test_post_wait(main_window: Window, condition_factory: ConditionFactory) -> None:
    """Real mouse input followed by a wait for the UI to settle."""
    window, cf = main_window, condition_factory
    # --8<-- [start:post_wait]
    from flaui.core.input import Mouse

    text_box = window.find_first_descendant(cf.by_automation_id("TextBox"))
    Mouse.click(text_box.get_clickable_point(), post_wait=True)  # ~100 ms
    text_box.as_text_box().enter("typed", post_wait=0.25)  # 250 ms
    # --8<-- [end:post_wait]
    assert text_box.as_text_box().text.endswith("typed")
