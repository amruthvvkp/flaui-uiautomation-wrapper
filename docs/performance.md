# Performance

FlaUI for Python is a thin layer over FlaUI C#, and the numbers below show that. Every call costs
the same, within measurement noise, as making it from C#. The time you see goes to Windows UI
Automation and to the app under test, so faster tests come from *what* you ask UIA to do, not from
the wrapper.

!!! info "How these numbers were measured"
    Windows 11 (build 26200), Python 3.11, the bundled WinForms and WPF test apps, with the Simple
    Controls tab open. Each operation ran 100–200 times after 3 warm-up runs; the tables show the
    mean in milliseconds, except the [pywinauto comparison](#compared-with-pywinauto), which shows
    the median and p95. Your machine and your app will give different absolute numbers, but the
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

## Compared with pywinauto

[pywinauto](https://github.com/pywinauto/pywinauto) 0.6.9 ran the same operations on the same apps,
in the same process and session as the wrapper: its `uia` backend on both apps, and its `win32`
backend on WinForms (WPF controls have no window handles, so `win32` cannot see them). pywinauto
code is written the way its documentation shows, for example
`window.child_window(auto_id="SimpleCheckBox").wrapper_object()`. Both libraries use their default
timings.

### Summary

Median in milliseconds over 100 runs. The fastest cell in each row is in bold. The last column is
pywinauto `uia` time divided by wrapper UIA3 time, so 5.6× means the wrapper took a fifth of the
time and 0.95× means pywinauto was slightly faster. n/a means the backend cannot do that operation
on that app.

| Operation | App | Wrapper UIA2 | Wrapper UIA3 | pywinauto `uia` | pywinauto `win32` | Wrapper UIA3 vs pywinauto `uia` |
|-----------|-----|--------------|--------------|-----------------|-------------------|---------------------------------|
| Find descendant by AutomationId | WinForms | 132 | **114** | 189 | n/a | 1.7× |
| Find descendant by AutomationId | WPF | 19 | **18** | 54 | n/a | 3.0× |
| Find descendant by Name | WinForms | 43 | 35 | 198 | **1.7** | 5.6× |
| Find descendant by Name | WPF | 29 | **25** | 49 | n/a | 2.0× |
| Find all children | WinForms | 19 | 16 | 23 | **0.23** | 1.5× |
| Find all children | WPF | 4.1 | **3.3** | 4.8 | n/a | 1.5× |
| Read a property | WinForms | 0.07 | 0.07 | 0.10 | **0.04** | 1.5× |
| Read a property | WPF | **0.14** | 0.14 | 0.49 | n/a | 3.4× |
| Select a radio button | WinForms | 0.10 | 0.09 | 2.6 | **0.06** | 29× |
| Select a radio button | WPF | **0.34** | 0.36 | 3.4 | n/a | 9.3× |
| Toggle a checkbox | WinForms | 1.8 | 2.1 | 2.3 | **0.06** | 1.1× |
| Toggle a checkbox | WPF | **0.95** | 4.0 | 3.8 | n/a | 0.95× |
| Mouse click | WinForms | 127 | **127** | 566 | 566 | 4.5× |
| Mouse click | WPF | **111** | 111 | 561 | n/a | 5.0× |

Where two cells look equal, the bold one had the lower unrounded median. The mouse-click gap comes
from pywinauto's built-in wait before each click, explained below.

### Full results

Each cell is the **median / p95** in milliseconds over 100 runs. The "UIA FindFirst" column makes
the same `FindFirst` call FlaUI makes, through pywinauto's own comtypes UI Automation object, so it
shows what COM itself costs.

**WinForms**

| Operation | FlaUI UIA2 | FlaUI UIA3 | pywinauto `uia` | UIA FindFirst | pywinauto `win32` |
|-----------|------------|------------|-----------------|---------------|-------------------|
| Find descendant by AutomationId | 132 / 163 | 114 / 141 | 189 / 248 | 135 / 150 | n/a |
| Find descendant by Name | 43 / 57 | 35 / 43 | 198 / 240 | 44 / 60 | 1.7 / 3.0 |
| Find all children | 19 / 23 | 16 / 18 | 23 / 45 | | 0.23 / 0.31 |
| Read a property | 0.07 / 0.08 | 0.07 / 0.08 | 0.10 / 0.14 | | 0.04 / 0.06 |
| Select a radio button | 0.10 / 0.22 | 0.09 / 0.12 | 2.6 / 4.9 | | 0.06 / 0.11 |
| Toggle a checkbox | 1.8 / 2.5 | 2.1 / 3.2 | 2.3 / 3.2 | | 0.06 / 0.09 |
| Mouse click | 127 / 142 | 127 / 142 | 566 / 570 | | 566 / 569 |

**WPF**

| Operation | FlaUI UIA2 | FlaUI UIA3 | pywinauto `uia` | UIA FindFirst |
|-----------|------------|------------|-----------------|---------------|
| Find descendant by AutomationId | 19 / 22 | 18 / 21 | 54 / 60 | 19 / 23 |
| Find descendant by Name | 29 / 42 | 25 / 28 | 49 / 57 | 26 / 29 |
| Find all children | 4.1 / 5.1 | 3.3 / 3.9 | 4.8 / 6.4 | |
| Read a property | 0.14 / 0.17 | 0.14 / 0.23 | 0.49 / 0.62 | |
| Select a radio button | 0.34 / 0.50 | 0.36 / 0.47 | 3.4 / 4.5 | |
| Toggle a checkbox | 0.95 / 1.2 | 4.0 / 4.9 | 3.8 / 4.8 | |
| Mouse click | 111 / 117 | 111 / 127 | 561 / 568 | |

What the numbers say:

- **pywinauto's `win32` backend is the fastest option where it works.** On WinForms it found the
  button by name in under 2 ms and set a checkbox in under 0.1 ms, because it sends window messages
  straight to the control instead of going through UI Automation. It only sees controls that have
  their own window handle, so it cannot reach WPF content, has no AutomationId, and its checkbox and
  radio actions send `BM_SETCHECK` rather than calling a UIA pattern.
- **On UIA, pywinauto's searches are slower, and its search strategy is the reason, not COM.**
  `child_window(...).wrapper_object()` fetches every descendant of the window in one call and then
  filters them in Python, because it checks that exactly one element matches. FlaUI asks UIA for the
  first match and stops there. The same `FindFirst` call made through pywinauto's comtypes object
  takes about as long as FlaUI's. The gap is largest for the name search on WinForms (198 ms against
  35–43 ms).
- **Pattern calls cost a few milliseconds more in pywinauto.** Selecting a radio button took
  2.6–3.4 ms against well under 1 ms. A toggle is close: on WPF, pywinauto (3.8 ms) beat FlaUI UIA3
  (4.0 ms) and lost to FlaUI UIA2 (0.95 ms).
- **pywinauto's mouse clicks wait for longer on purpose.** Before every click, `click_input()` waits
  until the system double-click time (500 ms by default) has passed since the last input, and then
  sleeps 90 ms (`Timings.after_clickinput_wait`). FlaUI waits only when you click the same spot twice
  in a row. Clicks in a tight loop show pywinauto's full wait. In a real test, with other steps
  between the clicks, it waits for less of that time.

The operations do the same job, but not always in the same way:

- On WPF, the button's text child is also named `BigButton`. FlaUI returns the first match. pywinauto
  rejects a search that matches more than one element, so its name search also passes
  `control_type="Button"`.
- pywinauto's window specification looks up the window again on each call, which is how its
  documentation uses it. FlaUI searches from a window object it already holds.
- Both libraries run the default settings. pywinauto's `Timings` can be shortened, and FlaUI's
  `post_wait` and `Retry` settings can be changed. Neither was tuned here.

## Workloads for AI agents

A test finds a few elements and acts on them. An AI computer-use agent, such as one driving the
desktop through an MCP server, does different work on every step: it dumps the accessibility tree
so the model can see the screen, takes screenshots, and sometimes starts a new process for each
command. `scripts/benchmark_agent.py` times that work on the same four combinations. Each cell is
the **median / p95** in milliseconds: 10 runs for snapshots, captures and lists, 10 fresh processes
for cold start, and 500 cycles for reliability. pywinauto 0.6.9 and Pillow ran in the same process
and session.

### Accessibility-tree snapshot

Each method walks every control-view element under the main window (Simple Controls tab: 55
elements on WinForms, 69 on WPF). It reads name, AutomationId, control type, bounding rectangle and
enabled state, and builds a Python tuple for each element. All the methods return the same
elements:

- **wrapper**: `find_all_descendants()`, then `properties.<name>.value_or_default` for each
  property. That is one UIA round trip per property, and the call works on UIA2 elements that have
  no AutomationId.
- **cached**: the same calls with a `CacheRequest` (`TreeScope.Element`) active for the five
  properties, so `FindAll` returns them along with each element.
- **cached subtree**: fetches the window once under a `TreeScope.Subtree` request, then walks
  `cached_children`. One UIA call returns the whole tree.
- **raw C#**: the same calls made directly on the FlaUI objects.
- **pywinauto `uia`**: `descendants()`, then reads from `element_info`.
- **comtypes**: pywinauto's own `IUIAutomation` called directly, in two forms: `FindAll` with
  `Current*` reads, and `FindAllBuildCache` with `Cached*` reads. Windows-MCP and pathlight-mcp
  talk to UIA this way.

| Method | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|--------|---------------|----------|---------------|----------|
| Wrapper | 237 / 275 | 125 / 154 | 207 / 214 | 108 / 122 |
| Wrapper, cached | 237 / 285 | 87 / 109 | 190 / 201 | 83 / 86 |
| Wrapper, cached subtree | 320 / 441 | **71** / 86 | 192 / 209 | **62** / 65 |
| Raw C# | 306 / 343 | 129 / 153 | 198 / 207 | 102 / 105 |
| Raw C#, cached subtree | 286 / 320 | **64** / 70 | 215 / 410 | **59** / 60 |
| pywinauto `uia` `descendants()` | 318 / 499 | 139 / 147 | 211 / 242 | 137 / 153 |
| comtypes `FindAll` + `Current*` | 269 / 326 | 101 / 112 | 189 / 200 | 101 / 106 |
| comtypes `FindAllBuildCache` | 285 / 385 | 84 / 88 | 189 / 226 | 83 / 87 |

The UIA2 WinForms column had more run-to-run noise than the others: its p95 values are well above
its medians.

What the numbers say:

- **On WPF, caching halves the cost.** A cached-subtree snapshot took 62–71 ms, or about 0.9 ms per
  element, against 108–125 ms for plain property reads. That beats pywinauto's `descendants()` (137–139
  ms) and comtypes `FindAllBuildCache` (83–84 ms), the approach the Python MCP servers use.
- **On WinForms, nothing helps.** Every method, cached or not, through any library, took about
  190–320 ms, or 3.4–5.8 ms per element. Each element costs that much on the app's side, because
  WinForms answers UIA slowly. Caching saves round trips, not the app's own work.
- **The wrapper adds nothing measurable.** The wrapper and raw C# rows are within noise of each
  other.
- **This is fine for one step, and slow for a big screen.** At about 1 ms per element on WPF and
  4 ms per element on WinForms, a window with 1,000 elements takes about 1 second on WPF and 4
  seconds on WinForms. An agent should snapshot a pane or dialog rather than the whole window.

What would make snapshots faster (not changed in this benchmark):

- A helper that runs the cached-subtree walk and returns plain Python data. Today, `cached_children`
  returns raw C# objects that you wrap yourself.
- A `TreeScope.Subtree` cache with a narrow `tree_filter`, such as only enabled controls or only
  on-screen ones, so fewer elements cross the process boundary.

### Cold start

Each run is a new Python process that attaches to an app that is already running and finds the
`SimpleCheckBox` once. The parent process measures the total, which includes interpreter start-up
and exit. A bare `python -c` took 79–105 ms on the same machine.

| Phase | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|-------|---------------|----------|---------------|----------|
| `import flaui.lib.pythonnet_bridge` | 1193 / 1825 | 1026 / 1080 | 1013 / 1130 | 1030 / 1536 |
| `setup_pythonnet_bridge()` + C#-backed imports | 313 / 377 | 277 / 310 | 272 / 319 | 284 / 437 |
| Create `Automation` | 60 / 117 | 54 / 67 | 22 / 24 | 22 / 45 |
| Attach + `get_main_window` | 99 / 174 | 75 / 85 | 49 / 58 | 48 / 123 |
| First find | 189 / 268 | 34 / 41 | 45 / 51 | 112 / 138 |
| **Whole process** | **2589** / 3627 | **2059** / 2262 | **2003** / 2151 | **2078** / 2716 |
| pywinauto `uia`, whole process | | | 844 / 872 | 892 / 1149 |

**Cold start is the wrapper's weak spot.** It takes about 2 seconds before the first find, against
under 1 second for pywinauto. Most of that time is spent importing: starting the .NET runtime
(`clr`, about 0.4 s) and loading `pydantic_settings` (about 0.3 s, see `python -X importtime`). Once
the process is running, attaching and finding take tens of milliseconds. An agent should therefore
keep one process alive, as an MCP server does, rather than start a new interpreter for each command.
Loading the settings and the bridge lazily would shorten the import, but that is library work this
benchmark does not do.

### Screenshots

`Capture.element()` on the main window (843×672 on WinForms, 944×774 on WPF) and on one small
control. "PNG bytes" saves the bitmap to a `MemoryStream` and copies it into Python `bytes`, which
is what an agent sends to a model. There is no helper for this in the wrapper yet. "PIL" grabs the
same rectangle with Pillow's `ImageGrab` and saves PNG to `BytesIO`, which is how pyautogui-based
agents do it.

| Operation | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|-----------|---------------|----------|---------------|----------|
| Window: capture | 16.6 / 17.2 | 16.6 / 17.2 | 16.5 / 17.8 | 16.6 / 18.5 |
| Window: capture + PNG bytes | 16.6 / 16.9 | 33.0 / 38.6 | 16.7 / 17.8 | 33.3 / 36.5 |
| Window: PIL `ImageGrab` + PNG | 66.6 / 69.1 | 66.1 / 70.0 | 66.5 / 76.1 | 66.1 / 73.7 |
| Element: capture + PNG bytes | 16.7 / 19.3 | 16.3 / 18.3 | 16.6 / 17.7 | 16.9 / 17.6 |
| Element: PIL `ImageGrab` + PNG | 61.6 / 78.9 | 49.7 / 57.3 | 54.1 / 75.3 | 49.7 / 52.2 |

The PNGs were 1–4 KiB for the control and 22–74 KiB for the window.

- **A screenshot costs one display frame.** Almost every capture took 16.6 ms, which is one refresh
  at 60 Hz, whatever its size. With PNG encoding, the larger WPF window took two frames (33 ms),
  probably because encoding pushed the work past the first one.
- **FlaUI's capture is 2–4× faster than Pillow's** for the same rectangle and a PNG of about the
  same size: 17–33 ms against 50–67 ms.

### Large lists and grids

`find_all_descendants()` on each list and grid in the test apps:

| Control | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|---------|---------------|----------|---------------|----------|
| `LargeListView` | 10.5 / 11.0 (36 el) | 17.3 / 17.6 (19 el) | 9.7 / 10.2 (36 el) | 12.2 / 13.2 (19 el) |
| `dataGridView` | 10.3 / 13.5 (21 el) | 40.2 / 41.1 (41 el) | 7.9 / 8.6 (21 el) | 26.9 / 29.2 (41 el) |
| `LargeListBox` | n/a | 7.9 / 12.5 (8 el) | n/a | 5.8 / 11.8 (8 el) |

Raw C# made the same calls within noise of these numbers. The test apps don't have a list large
enough to show how this scales: WPF virtualises its lists, so UIA only sees the rows that have been
drawn, and the WinForms More Controls tab is not exposed to UIA. These numbers come to 0.3–1.0 ms
per element. To measure a list with thousands of rows, run the script against your own app.

### Reliability

Each cycle finds `SimpleCheckBox` from the window, reads its toggle state, toggles it, and checks
that the state changed:

| | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|-|---------------|----------|---------------|----------|
| Succeeded | 500 / 500 | 500 / 500 | 500 / 500 | 500 / 500 |
| Cycle time | 125 / 155 | 20 / 23 | 118 / 144 | 23 / 34 |

No cycle failed on any combination. A cycle on WinForms takes as long as the WinForms descendant
search in the tables above.

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

The repository has four scripts that produced these tables. All of them launch the bundled test
apps and click controls, so run them on an interactive desktop, not on a headless CI agent:

```bash
uv run python scripts/benchmark.py -n 100                  # wrapper vs C#, all four combinations
uv run python scripts/benchmark.py -n 200 --json out.json  # also write raw statistics
uv run python scripts/benchmark_name_map.py -n 200         # name maps vs direct finds
uv run --group bench python scripts/benchmark_pywinauto.py -n 100  # wrapper vs pywinauto
uv run --group bench python scripts/benchmark_agent.py --json agent.json  # agent workloads
```

`benchmark_agent.py` runs without the `bench` group too. It then skips the pywinauto and comtypes
rows, and skips the Pillow rows if Pillow is not installed. `--sections` runs only some workloads,
for example `--sections snapshot capture`. The script exits 1 if any reliability cycle fails.

`benchmark.py` exits 1 if the wrapper adds 5 ms or more to any operation, so you can use it to
check a change for performance regressions. `benchmark_name_map.py` and `benchmark_pywinauto.py`
only report numbers. pywinauto is not a dependency of FlaUI for Python. The `bench` dependency
group installs it for the comparison only.
