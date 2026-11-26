# Utilities

FlaUI ships a set of helpers alongside the element API: waiting and retrying, keyboard and mouse
input, the `System.Drawing` value types, screenshots, highlight overlays, and a few small tools.
FlaUI for Python ports all of them. This page shows each one next to its C# original.

!!! success "Every Python snippet on this page runs"
    The snippets come from
    [`examples/pytest/test_utilities.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/examples/pytest/test_utilities.py)
    and [`examples/pytest/test_advanced.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/examples/pytest/test_advanced.py),
    which run against the bundled WPF app:

    ```bash
    uv run pytest examples/pytest/test_utilities.py -v
    ```

| Helper | Python | C# | Use it to... |
|--------|--------|----|--------------|
| [Retry](#retry) | `flaui.core.tools.Retry` | `FlaUI.Core.Tools.Retry` | poll until a condition holds |
| [Wait](#wait) | `flaui.core.input.Wait` | `FlaUI.Core.Input.Wait` | let input settle, wait for a window to respond |
| [Keyboard](#keyboard) | `flaui.core.input.Keyboard` | `FlaUI.Core.Input.Keyboard` | type text, send shortcuts |
| [Mouse](#mouse) | `flaui.core.input.Mouse` | `FlaUI.Core.Input.Mouse` | move, click, scroll, drag the real cursor |
| [Drawing types](#drawing-types) | `flaui.lib.system.drawing` | `System.Drawing` | points, sizes, rectangles, colours |
| [Capturing](#screenshots-and-video) | `flaui.core.capturing` | `FlaUI.Core.Capturing` | screenshots and screen recordings |
| [Highlighting](#highlighting-elements) | `draw_highlight`, `OverlayManager` | `DrawHighlight`, `IOverlayManager` | see which element a locator found |
| [Debug](#debugging-elements) | `flaui.core.debug` | `FlaUI.Core.Debug` | dump an element, get an XPath to it |
| [Tools](#other-tools) | `flaui.core.tools` | `FlaUI.Core.Tools` | virtualized lists, MSAA text, system info |
| [TypeCast](#converting-values-typecast) | `flaui.lib.collections.TypeCast` | n/a | convert values at the Python/.NET boundary |

!!! warning "Check the units"
    `Retry` timeouts and intervals are **milliseconds** (int). `Wait` timeouts are **seconds** (float).
    C# uses `TimeSpan` for both. The [units table](configuration.md#units-at-a-glance) lists every API.

## Retry

`Retry` calls a function over and over until its condition holds or the timeout runs out. Pick the
method by what you're waiting for:

| You're waiting for... | Method | Returns |
|-----------------------|--------|---------|
| an element lookup to stop raising `ElementNotFound` | `WhileException` | the element |
| something to become true (`is_enabled`, a name change, ...) | `WhileFalse` | `True` / `False` |
| something to become false | `WhileTrue` | `True` / `False` |
| a truthy value, which you then use | `While` | the value |
| a value that isn't `None` | `WhileNull` | the value, or `None` on timeout |
| a value to go away (become `None`) | `WhileNotNull` | `None`, or the last value on timeout |
| a non-empty list | `WhileEmpty` | the list |

=== "Python"

    ```python
    --8<-- "examples/pytest/test_advanced.py:retry"
    ```

=== "C#"

    ```csharp
    var button = Retry.WhileNull(
        () => window.FindFirstDescendant(cf.ByAutomationId("InvokableButton")),
        timeout: TimeSpan.FromSeconds(5),
        interval: TimeSpan.FromMilliseconds(100),
        throwOnTimeout: true).Result.AsButton();

    var ready = Retry.WhileFalse(() => button.IsEnabled, TimeSpan.FromSeconds(2)).Result;
    ```

How it differs from C#:

- **Lookups raise instead of returning `null`.** In C#, `FindFirst*` returns `null`, so you poll
  with `WhileNull`. In Python it raises `ElementNotFound`, so poll with **`WhileException`**. The
  other methods only retry on `ValueError` / `AssertionError` (and only with
  `ignore_exception=True`); any other exception stops them straight away.
- **No `RetryResult`.** Python returns the value or `bool` directly, rather than `.Result`.
- **No separate check function.** C#'s `Retry.While(method, checkMethod)` tests a second callable;
  Python's `While` tests the method's own return value for truthiness.
- **`throw_on_timeout`** behaves differently depending on the method: `WhileFalse` / `WhileTrue` /
  `WhileNull` / `WhileNotNull` return quietly on timeout unless it is set, while `While`,
  `WhileNot` and `WhileEmpty` always raise unless you give them `last_value_on_timeout` or
  `default_on_timeout`. Each method's [API reference](api/retry.md) spells this out.

For assertions that wait, [`expect(...)`](advanced.md#fluent-assertions-expect) reads better than
wrapping `Retry` in an `assert`.

## Wait

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:wait"
    ```

=== "C#"

    ```csharp
    Wait.UntilInputIsProcessed();
    Wait.UntilResponsive(window, TimeSpan.FromSeconds(5));
    // No C# equivalent of while_cursor_is_busy: it is a Python addition.
    ```

- `until_input_is_processed()` pauses briefly (100 ms by default) so queued input can land. The
  `post_wait=True` argument on input methods does the same thing.
- `until_responsive(element)` waits until the element's window accepts input again, for example
  after a long-running click. `until_responsive_hwnd(handle)` does the same from a window handle.
- `while_cursor_is_busy()` waits while the mouse cursor shows the busy or "working in background"
  shape. It's useful after an action that triggers a load with no UI you can poll.

## Keyboard

`Keyboard.type` sends real key presses to whichever control has focus. Hold modifier keys with
`Keyboard.pressing`, which returns a context manager that releases the keys when the block ends,
even if it raises:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:keyboard"
    ```

=== "C#"

    ```csharp
    textBox.Focus();
    using (Keyboard.Pressing(VirtualKeyShort.CONTROL))
    {
        Keyboard.Type(VirtualKeyShort.KEY_A);
    }
    Keyboard.Type("replaced");
    Keyboard.Type(VirtualKeyShort.TAB);
    Wait.UntilInputIsProcessed();
    ```

Other methods: `type_simultaneously([...])` presses several keys together, `press` / `release`
give manual control, and `type_scan_code` / `type_virtual_key_code` send raw codes. Key names are on
`flaui.core.windows_api.VirtualKeyShort`.

!!! tip "Prefer patterns over keystrokes"
    Real keystrokes go to whatever has focus, and anything else happening on the desktop can get
    mixed in. Setting `text_box.text = ...` uses the Value pattern and sends no keys at all. Use the
    keyboard when the app needs real key events: shortcuts, key-driven navigation, or input
    validation that only runs on typing.

## Mouse

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:mouse"
    ```

=== "C#"

    ```csharp
    var point = textBox.GetClickablePoint();
    Mouse.MoveTo(point);
    Console.WriteLine(Mouse.Position);
    Mouse.Click(point);
    Wait.UntilInputIsProcessed();
    Mouse.Scroll(-2);
    ```

Also available: `right_click`, `double_click`, `drag(start, end)`, `drag_horizontally` /
`drag_vertically`, and `horizontal_scroll`. Every method accepts `post_wait`. Movement speed is set
by `Mouse.move_pixels_per_millisecond` (see [Configuration](configuration.md#mouse-speed)).
`element.click()` combines finding the clickable point and clicking it.

## Drawing types

Screen geometry and colours use the `System.Drawing` types, wrapped as pydantic models.
`bounding_rectangle` returns a `Rectangle`, `get_clickable_point()` returns a `Point`, and so on.
Build your own from Python values with `raw_value=`:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:drawing"
    ```

=== "C#"

    ```csharp
    var bounds = window.BoundingRectangle;
    var middle = bounds.Center();

    var p = new Point(10, 20);
    var moved = p + new Size(5, 5);
    var box = new Rectangle(0, 0, 100, 50);
    var inside = box.Contains(new Point(10, 10));

    var blue = Color.FromName("Blue");
    ```

Each wrapper exposes `.raw_value` (or `.cs_object` for colours) when you need to hand the real
.NET value to FlaUI yourself.

## Screenshots and video

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:capture"
    ```

=== "C#"

    ```csharp
    using (var image = Capture.Element(window))
    {
        image.ToFile(@"C:\temp\window.png");
    }
    using (var screen = Capture.MainScreen(new CaptureSettings { OutputScale = 0.5 }))
    {
        screen.ToFile(@"C:\temp\screen.png");
    }
    window.CaptureToFile(@"C:\temp\shortcut.png");
    ```

`Capture` can also grab a single screen (`screen(index)`), any rectangle (`rectangle(bounds)`), or
every screen an element spans (`screens_with_element`). To record video, use `VideoRecorder`. It
needs ffmpeg, which `VideoRecorder.download_ffmpeg(folder)` can fetch for you. See the
[Capturing reference](api/capturing.md).

!!! tip "Screenshot every failure automatically"
    Taking the screenshot from a test-framework hook means every failure gets one without any
    changes to the tests themselves. See [Test design tips](test-design.md#capture-evidence-on-failure).

## Highlighting elements

When you're not sure which element a locator found, draw a frame around it:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:highlight"
    ```

=== "C#"

    ```csharp
    button.DrawHighlight(false, Color.Blue, TimeSpan.FromMilliseconds(500));

    automation.OverlayManager.Show(window.BoundingRectangle, Color.Red, 500);
    ```

`show()` returns straight away; `show_blocking()` waits until the frame has disappeared. Durations
are in milliseconds.

## Debugging elements

`flaui.core.debug` wraps `FlaUI.Core.Debug`. `details()` dumps an element's properties and
supported patterns (and those of its children) as text, which is useful in a failure message or a
log. `get_xpath_to_element()` turns an element you already found into an XPath locator. Both are
also methods on every element.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:debug"
    ```

=== "C#"

    ```csharp
    Console.WriteLine(Debug.Details(button));

    var desktop = automation.GetDesktop();
    var xpath = Debug.GetXPathToElement(button, desktop);
    var sameButton = window.FindFirstByXPath(xpath);
    ```

How the root changes the path:

| Call | Example result | Search it from |
|------|----------------|----------------|
| `get_xpath_to_element(element)` | `/Window[1]/Tab/TabItem[1]/Button[2]` | the desktop |
| `get_xpath_to_element(element, desktop)` | `/Tab/TabItem[1]/Button[2]` | the top-level window |
| `get_xpath_to_element(element, window)` | `/TabItem[1]/Button[2]` | the window's `Tab` child |

!!! note "A root leaves out the step for its direct child"
    Like FlaUI C#, passing `root_element` drops the step for the root's direct child. Pass the
    desktop to get a path you can hand to `window.find_first_by_x_path()`. Without a root, FlaUI
    indexes the window among every top-level window, which is slower on a busy desktop and depends
    on what else is open, so prefer the desktop-rooted form for locators.

!!! warning "`details()` can return an empty string"
    FlaUI returns `""` when it cannot read one of the properties it dumps. This happens now and then
    on WinForms, where the MSAA proxy rejects a cached `HelpText` or `AutomationId`. FlaUI's error
    text is logged as a warning on the `flaui.core.debug` logger.

## Other tools

### Virtualized lists (`ItemRealizer`)

Large WPF lists and grids only create UI Automation elements for the rows on screen. Realize them
before searching through all of them:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:item_realizer"
    ```

=== "C#"

    ```csharp
    var largeList = window.FindFirstDescendant(cf.ByAutomationId("LargeListView"));
    ItemRealizer.RealizeItems(largeList);
    ```

### System information (`SystemInfo`)

CPU and memory figures, useful to log next to a slow or flaky test. The Python version uses
[psutil](https://psutil.readthedocs.io/) instead of Windows performance counters.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:system_info"
    ```

=== "C#"

    ```csharp
    Console.WriteLine($"CPU {SystemInfo.CpuUsage}%  RAM {SystemInfo.PhysicalMemoryUsedPercent}% used");
    ```

### MSAA role and state text (`AccessibilityTextResolver`)

=== "Python"

    ```python
    --8<-- "examples/pytest/test_utilities.py:accessibility_text"
    ```

=== "C#"

    ```csharp
    var legacy = window.Patterns.LegacyIAccessible.Pattern;
    var role = AccessibilityTextResolver.GetRoleText(legacy.Role.Value);
    var state = AccessibilityTextResolver.GetStateText(legacy.State.Value);
    ```

### Also in `flaui.core.tools`

- **`WindowsStoreAppLauncher.launch(aumid)`** starts a Store app and returns its process id.
  `automation.application.launch_store_app(aumid)` wraps it, as the
  [Calculator gallery script](examples/gallery.md#calculator) shows.
- **`LocalizedStrings`** gives the scroll-bar names FlaUI uses for the current Windows language.

## Converting values (`TypeCast`)

Most of the API converts values for you. When you call FlaUI directly through `.raw_element`, these
helpers convert at the boundary:

```python
--8<-- "examples/pytest/test_utilities.py:type_cast"
```

`TypeCast` also has `py_dict` (a C# dictionary to a Python `dict`) and `cs_datetime` (a Python
`date` to `System.DateTime`, e.g. to set a `DateTimePicker`).
