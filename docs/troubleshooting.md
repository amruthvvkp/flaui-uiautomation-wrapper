# Troubleshooting

Common issues, fixes, and known test skips/xfails.

## PythonNet bridge not initialized
- **Symptom:** `System.IO.FileNotFoundException` or `TypeInitializationException`
- **Fix:** Call `setup_pythonnet_bridge()` before any C# imports.

## Element not found
- Verify `automation_id` spelling (use Accessibility Insights or FlaUIInspect).
- Use `Retry.While` for slow-loading UI.
- Prefer `condition_factory.by_automation_id` over XPath when possible.

## Timing and sync
- Use `post_wait=True|seconds|callable` on mouse/keyboard actions.
- `Retry.While/WhileNot` for async UI.
- `Wait.until_input_is_processed()` after sequences when needed.

## C# exception translation
- Ensure interop methods use `@handle_csharp_exceptions`; otherwise raw C# exceptions may leak.

## Python compatibility
- Targets Python 3.10–3.14 (`requires-python = ">=3.10,<3.15"`); modern syntax (`|` unions, `match`, built-in generics) is supported.
- If you hit syntax errors, confirm you are running Python ≥ 3.10.

## DLL loading
- Confirm `flaui/bin` is packaged and reachable; rerun `setup_pythonnet_bridge()`.

## Windows/OS specifics
- Windows 11 Notepad is a Store app; Notepad-based tests are skipped there.
- MS Paint UI varies by Windows version; some Paint XPath tests are xfailed locally and skipped on
  hosted CI because native UIA/COM failures can abort the Python process before pytest records an
  xfail.

## Known pytest skips/xfails (manual list)
- `skip_notepad_on_win11`: Notepad tests (XPath, getter/search) skipped on Windows 11 Store app.
- `skip_if_matrix` UIA2_WinForms: XPath IsPassword property unavailable in UIA2+WinForms.
- `xfail` / hosted-CI skip Paint XPath tests: Windows 11 Paint structure changed and hosted CI can
  abort in native UIA/COM before pytest records an xfail (issue #89).
- `skipif` Paint mouse drag: Paint UI varies significantly.
- `bug` GH-91 Mouse movement/drag flakiness under runners (mouse position reads may lag).
- `bug` GH-75/others: ListBox instability on WinForms (see ListBox tests) — keep an eye on CI.

## Flakiness tips
- Add short post_waits on mouse moves/drags.
- Use Retry with smaller intervals (50–100ms) and bounded timeouts.
- Keep UIA2 available for legacy WinForms when UIA3 is unstable.
