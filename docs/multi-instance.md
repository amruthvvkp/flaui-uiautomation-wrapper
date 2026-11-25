# Multiple instances

This page covers driving several copies of the same application at once, attaching to one specific
copy that's already running, and telling apart windows that look identical.

!!! success "Every Python snippet on this page runs"
    The snippets come from
    [`examples/pytest/test_multi_instance.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/examples/pytest/test_multi_instance.py),
    which launches two copies of the bundled WPF app:

    ```bash
    uv run pytest examples/pytest/test_multi_instance.py -v
    ```

## The rule: one `Application` per process

An `Application` object is a handle to **one** process. A single `Automation` can drive any number
of them, because it is the connection to UI Automation, not to an app.

`automation.application` is simply one `Application` that comes built in. If you call `launch()` on
it a second time, it switches to the new process and you lose your handle to the first one. For a
second copy, create a second `Application()`.

=== "Python"

    ```python
    --8<-- "examples/pytest/test_multi_instance.py:two_instances"
    ```

=== "C#"

    ```csharp
    using var automation = new UIA3Automation();
    using var first = Application.Launch(exe);
    using var second = Application.Launch(exe);

    var firstWindow = first.GetMainWindow(automation);
    var secondWindow = second.GetMainWindow(automation);
    Console.WriteLine($"{first.ProcessId} {second.ProcessId}");

    var cf = automation.ConditionFactory;
    firstWindow.FindFirstDescendant(cf.ByAutomationId("TextBox")).AsTextBox().Text = "instance one";
    secondWindow.FindFirstDescendant(cf.ByAutomationId("TextBox")).AsTextBox().Text = "instance two";
    ```

In C#, `Application.Launch` returns a new `Application` each time. In Python you create the
`Application()` yourself and then call `launch()` on it.

## Finding one copy's window

Every copy has the same title, class name and AutomationIds, so a normal search can't tell them
apart. Use something that is unique to the process.

### From the window handle (fastest)

Every `Application` knows its main window's native handle, so you can go straight to the window
without searching:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_multi_instance.py:from_handle"
    ```

=== "C#"

    ```csharp
    var window = automation.FromHandle(app.MainWindowHandle).AsWindow();
    ```

`app.get_main_window(automation)` returns the same window and also waits for it to appear (see
[Timeouts](configuration.md#timeouts)).

### By process id

To search instead, for example for a dialog that belongs to one copy, combine `by_process_id` with
the rest of your condition:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_multi_instance.py:by_process_id"
    ```

=== "C#"

    ```csharp
    var desktop = automation.GetDesktop();
    var condition = cf.ByProcessId(app.ProcessId).And(cf.ByName("FlaUI WPF Test App"));
    var window = desktop.FindFirstChild(condition).AsWindow();
    ```

### Every window of one copy

`get_all_top_level_windows` returns only the top-level windows that belong to that process:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_multi_instance.py:top_level_windows"
    ```

=== "C#"

    ```csharp
    var windows = app.GetAllTopLevelWindows(automation);
    var titles = windows.Select(w => w.Title).ToList();
    ```

!!! warning "Searching the whole desktop can be slow"
    `by_process_id` searches from the desktop and `get_all_top_level_windows` both ask **every**
    top-level window on the machine. One window that is slow to answer, in any app at all, slows the
    whole search down. On a busy machine this can take tens of seconds (the example tests allow
    180 s). Use `from_handle` / `get_main_window` when you can, and start searches from that window
    rather than from the desktop.

## Attaching to a specific running copy

`attach("WpfApplication.exe")` attaches to whichever matching process it finds first. When several
are running you can't choose which one, so pick the process yourself (by start time, command line,
window title, and so on) and attach **by PID**:

=== "Python"

    ```python
    --8<-- "examples/pytest/test_multi_instance.py:attach_by_pid"
    ```

=== "C#"

    ```csharp
    var newest = Process.GetProcessesByName("WpfApplication")
        .OrderBy(p => p.StartTime)
        .Last();

    var app = Application.Attach(newest.Id);
    var window = app.GetMainWindow(automation);
    ```

[`psutil`](https://psutil.readthedocs.io/) is already a dependency of FlaUI for Python, so the
Python recipe needs no extra install. Besides `create_time`, `psutil` can also filter on
`cmdline()`, `exe()` or `cwd()`, which helps when the copies were started with different arguments.

## Apps that reuse one process

Some apps never start a second process. Calculator and the Windows 11 Notepad, for example, open new
windows or tabs inside the process that's already running. For them:

- Launching "again" gives you a new **window**, not a new process. Use
  `get_all_top_level_windows(automation)` on the one `Application`, or `window.modal_windows` for
  dialogs.
- Tell the windows apart by title, or by a control inside them, rather than by process id.
- See the [Notepad gallery script](examples/gallery.md#notepad) for finding a Store app's window
  when the process you launched exits straight away.

## Cleaning up

- Put every `Application` in a `with` block (or close it in a `finally`). Leaving the block closes
  that process gracefully and kills it if closing fails.
- An `Application` you attached to is also closed when its block ends. Don't use `with` on a copy
  you need to leave running.
- If a test run is interrupted (a timeout, Ctrl+C), copies can be left running. Clean them up before
  the next run, for example with `taskkill /IM WpfApplication.exe /F`.

## Running tests in parallel

- **One process per worker.** With [pytest-xdist](https://pytest-xdist.readthedocs.io/)
  (`pytest -n 4`), each worker is its own Python process. Give each worker its own copy of the app,
  with a session fixture that launches it and a separate `Automation`. Never share element objects
  between workers.
- **Keep UI work on one thread.** FlaUI and UI Automation are not designed for driving the same
  element from several threads at once. If you need concurrency inside one process, give each thread
  its own app copy and its own elements.
- **The mouse and keyboard are shared.** Every worker on a machine uses the same physical cursor and
  keyboard focus, so tests that click or type in parallel will interfere with each other. Prefer
  pattern-based actions in parallel runs (`invoke()`, `toggle()`, `text = ...`), or run the
  input-heavy tests one at a time.
