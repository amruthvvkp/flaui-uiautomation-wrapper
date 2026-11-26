# Performance

FlaUI for Python is a thin layer over FlaUI C#, and the numbers below show that. Every call costs
the same, within measurement noise, as making it from C#. The time you see goes to Windows UI
Automation and to the app under test, so faster tests come from *what* you ask UIA to do, not from
the wrapper.

!!! info "How these numbers were measured"
    Windows 11 (build 26200), Python 3.11, the bundled WinForms and WPF test apps, with the Simple
    Controls tab open. Each operation ran 100–200 times after 3 warm-up runs; the tables show the
    mean in milliseconds. Your machine and your app will give different absolute numbers, but the
    comparisons hold. To reproduce them, see [Measure it yourself](#measure-it-yourself).

## The wrapper adds no measurable overhead

Each operation was timed twice: through the Python wrapper, and by calling the C# object it wraps
directly. The difference is the cost of PythonNet, the Pydantic models and exception translation:

| Operation | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|-----------|---------------|----------|---------------|----------|
| Find descendant by AutomationId | +1.6 | +1.3 | −7.8 | +1.0 |
| Find descendant by Name | +0.2 | −0.8 | +0.7 | +0.4 |
| Find all children | +0.8 | +0.2 | +0.2 | +0.1 |
| Read a property | +0.00 | +0.00 | +0.00 | +0.01 |
| Toggle a checkbox | +0.4 | +0.0 | +0.1 | −0.4 |
| Mouse click | +0.6 | −1.5 | −0.5 | −0.6 |

Negative values are noise: one side happened to be faster in that run. The project treats an
overhead under **5 ms per call** as its v1.0 performance gate.

## What operations cost

Average time through the wrapper. These numbers come from UIA and the app, so use them to compare
approaches, not as guarantees:

| Operation | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|-----------|---------------|----------|---------------|----------|
| Find descendant by AutomationId | 113 | 18 | 111 | 18 |
| Find descendant by Name | 37 | 26 | 36 | 27 |
| Find all children | 16 | 4 | 16 | 3 |
| Read a property | 0.07 | 0.15 | 0.07 | 0.16 |
| Select a radio button | 0.1 | 0.4 | 0.1 | 0.4 |
| Toggle a checkbox | 2.1 | 1.0 | 1.8 | 3.6 |
| Mouse click | 130 | 113 | 129 | 113 |

Three things stand out:

- **WinForms searches are slower than WPF ones.** A search from the window walks every element in
  it, and WinForms is slower to answer each step. Here, finding by AutomationId took over 100 ms
  on WinForms against under 20 ms on WPF.
- **Patterns are much faster than the mouse.** `toggle()`, `invoke()` and setting `is_checked`
  talk to the control directly and finish in a few milliseconds. `click()` moves the real cursor and
  then waits for Windows to process the input, so it takes over 100 ms.
- **Clicking the same spot twice in a row is slower still**, at about 525 ms. FlaUI waits out the
  system double-click time so that two separate clicks are not read as a double-click.

## Element name maps cost nothing extra

A [name map](test-design.md#build-a-name-map-for-your-elements) runs its lookup every time you read
a property. To see what that costs, the Simple Controls `TextBox` was found four ways:

- with a direct `window.find_first_descendant(...)`;
- through the documented map in `examples/pytest/app_map.py`;
- through this project's own test-suite map in `tests/test_utilities/elements`;
- with the test-suite map's lookups written out by hand, without the map classes.

The table shows each map's average time minus the direct find:

| | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|-|---------------|----------|---------------|----------|
| Direct find (ms) | 54 | 9.2 | 52 | 7.8 |
| Documented map vs direct | −0.9 | +0.7 | −0.0 | +0.4 |
| Test-suite map vs direct | −12 | −0.4 | −9 | +0.0 |
| Creating one map page class | 0.17 | 0.15 | 0.15 | 0.15 |

- **The map classes are nearly free.** A `BaseModel` page class takes under 0.01 ms to create. The
  test-suite map's classes take about 0.15 ms, because they are built on `BaseSettings` and re-read
  environment variables. That is one more reason to use
  [`BaseModel` for maps](test-design.md#how-this-project-does-it).
- **A narrow search can make a map faster than a direct find.** The test-suite map first finds the
  tab, then searches only that tab's direct children. On WinForms this beat a whole-window search
  by 9–12 ms.
- **The cost to watch is waiting, not the lookup.** If a map switches to a tab and then waits for
  the UI to settle (`post_wait=True`), that wait adds 100 ms or more on every access to a tab that
  isn't already open.

## Tips for faster tests

- **Narrow the search.** Find a container once per action, such as a tab, a pane or a dialog, and
  search inside it. Use `find_first_child` when the element is a direct child, rather than
  `find_first_descendant` from the window.
- **Prefer patterns to mouse input** when the test is not about the mouse itself: `invoke()`,
  `toggle()`, `select()`, `is_checked = True`, or setting `text`.
- **Use AutomationId when it exists.** It is the most stable locator, and the most stable locator
  saves more time on retries and reruns than any speed difference between locators.
- **Wait on conditions, not fixed sleeps.** `Retry` and `expect(...)` return as soon as the
  condition holds. A `post_wait` or `time.sleep` always takes its full time.
- **Try both automation types on WinForms.** UIA2 and UIA3 were within noise of each other here,
  but legacy apps vary. See [UIA2 vs UIA3](uia2-uia3.md).

## Measure it yourself

The repository has two scripts that produced these tables. Both launch the bundled test apps and
click controls, so run them on an interactive desktop, not on a headless CI agent:

```bash
uv run python scripts/benchmark.py -n 100                  # wrapper vs C#, all four combinations
uv run python scripts/benchmark.py -n 200 --json out.json  # also write raw statistics
uv run python scripts/benchmark_name_map.py -n 200         # name maps vs direct finds
```

`benchmark.py` exits 1 if the wrapper adds 5 ms or more to any operation, so you can use it to
check a change for performance regressions. `benchmark_name_map.py` only reports numbers.
