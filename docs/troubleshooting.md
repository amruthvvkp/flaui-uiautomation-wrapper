# Troubleshooting

Common issues, fixes, and known test skips/xfails.

## Installation problems

FlaUI for Python needs **64-bit CPython 3.11–3.15 on Windows** with the **.NET Framework 4.8**
runtime. The wheel bundles the FlaUI C# DLLs, so there is nothing else to download at runtime.

### Quick check

Run this in the environment you installed into. Each line is one of the requirements:

```powershell
python -c "import platform, struct; print(platform.python_version(), struct.calcsize('P') * 8, 'bit')"
python -m pip show flaui-uiautomation-wrapper pythonnet
python -c "import flaui.lib.pythonnet_bridge as b; b.setup_pythonnet_bridge(); print('FlaUI', b.FLAUI_CSHARP_VERSION)"
```

A working install prints a Python version from 3.11 to 3.15, `64 bit`, a `flaui-uiautomation-wrapper`
version of 1.0 or later, `pythonnet` 3.2.1, and `FlaUI 5.0.0.0`. If one line is wrong, find it below.

CI runs the same checks, and more, on every build with
[`scripts/wheel_smoke.py`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/scripts/wheel_smoke.py).
It installs the built wheel into clean virtual environments (uv-managed CPython with `uv pip`, plus
the build image's python.org or tool-cache CPython with `pip`). Then it drives the test
applications on UIA2 and UIA3 from site-packages.

### Unsupported Python version

- **Python 3.10 or older does not fail. It installs an old release.** On those versions,
  `pip install flaui-uiautomation-wrapper` quietly picks the legacy `0.1.x` or `0.0.x` releases,
  which still allow old Pythons. With `--pre` on 3.10 it picks `1.0.0b1`, an early beta. Their
  APIs differ from these docs, so imports from the guides fail. `pip show` reveals it
  (`Version: 0.1.1`). Install Python 3.11 or later and create a fresh virtual environment.
- **Pin the major version** in your requirements (`flaui-uiautomation-wrapper>=1.0`) so an old
  interpreter fails loudly instead. pip then reports
  `Ignored the following versions that require a different python version: ... Requires-Python >=3.11,<3.16`
  and `No matching distribution found`.
- **Python 3.16 and newer** are not supported yet. `pythonnet` 3.2.1 itself requires `<3.16`.
- **uv projects** must declare a compatible range, for example `requires-python = ">=3.11"`.
  Otherwise `uv add` fails to resolve, because the project's lowest Python is below what FlaUI
  supports.
- Free-threaded builds (`3.13t`, `3.14t`) and PyPy are untested.

### .NET Framework 4.8 missing

The bundled FlaUI 5 assemblies target **.NET Framework 4.8**, and PythonNet loads them in the .NET
Framework runtime. Windows 10 (version 1903 and later), Windows 11, and Windows Server 2022 and
later include it. Windows Server 2016 and 2019, and some trimmed images, ship an older 4.x.

- **Symptom:** `import clr` or `setup_pythonnet_bridge()` fails with
  `RuntimeError: Failed to create a .NET runtime (netfx)`, or with a `FileLoadException` naming
  `FlaUI.Core`.
- **Check** (prints `True` when 4.8 or later is installed):

    ```powershell
    (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full').Release -ge 528040
    ```

- **Fix:** install the .NET Framework 4.8 (or 4.8.1) runtime from Microsoft, then reboot.

### PythonNet runtime missing or wrong

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'clr'` | `pythonnet` is not installed in *this* interpreter: installed with `--no-deps`, or into another venv. | `python -m pip install pythonnet==3.2.1` with the same `python` you run. |
| `AttributeError: module 'clr' has no attribute 'AddReference'` | The unrelated PyPI package **`clr`** is installed and shadows PythonNet's `clr` module. | `python -m pip uninstall clr`, then `python -m pip install --force-reinstall pythonnet==3.2.1`. |
| `RuntimeError: Failed to create a .NET runtime (coreclr) using the parameters {}.` | `PYTHONNET_RUNTIME` is set to `coreclr` (or `mono`), or code called `pythonnet.load("coreclr")` before FlaUI. The bundled DLLs need .NET Framework. | Unset `PYTHONNET_RUNTIME` (or set it to `netfx`). Do not load another runtime first. |

### 32-bit vs 64-bit Python

CI tests **64-bit** CPython only. The dependencies publish 32-bit wheels, so a 32-bit Python
installs without errors. It is untested, though, and a 32-bit process is limited in what it can
inspect about 64-bit processes, which are most desktop apps today.

- **Check:** the first quick-check line prints `32 bit`.
- **Fix:** install the 64-bit build. With the python.org installer, choose
  *Windows installer (64-bit)*. With uv, run `uv python install cpython-3.12-windows-x86_64-none`.
  With the `py` launcher, list the installs with `py --list` and pick the one without `-32`.

### Blocked or quarantined DLLs

**Blocked (Mark of the Web).** Windows tags files that came from the internet or another
untrusted zone. This happens when a `site-packages` folder or wheel contents are copied out of a
downloaded ZIP, an email attachment, or a network share. .NET Framework then refuses to load the
DLLs:

```text
System.IO.FileLoadException: Could not load file or assembly 'file:///...\flaui\bin\FlaUI.Core.dll'
or one of its dependencies. Operation is not supported. (Exception from HRESULT: 0x80131515)
---> System.NotSupportedException: An attempt was made to load an assembly from a network location ...
```

Unblock the bundled folder, or reinstall with `pip` (pip-installed files are not tagged):

```powershell
$bin = python -c "import flaui, pathlib; print(pathlib.Path(flaui.__file__).parent / 'bin')"
Get-ChildItem $bin | Unblock-File
```

The same error appears when the virtual environment lives on a UNC path or a mapped network drive.
Create it on a local disk instead.

**Quarantined.** Antivirus or EDR tools sometimes quarantine unsigned DLLs such as
`Interop.UIAutomationClient.dll`. The bridge then fails with `FileNotFoundException`, or a DLL is
missing from the folder. List the folder: it must contain `FlaUI.Core.dll`, `FlaUI.UIA2.dll`,
`FlaUI.UIA3.dll`, `Interop.UIAutomationClient.dll` and `System.CodeDom.dll`.

```powershell
Get-ChildItem $bin
```

Restore the files with
`python -m pip install --force-reinstall --no-deps flaui-uiautomation-wrapper`, and ask your
security team to allow-list the folder so it does not happen again.

**Overridden.** If `FLAUI_BIN_HOME` is set, the DLLs load from that folder instead, and the bridge
logs a warning saying so. Unset it unless you are testing another FlaUI build (see
[Environment variables](configuration.md#environment-variables)).

### Corporate proxies and offline installs

- **Proxy:** pass `--proxy http://proxy.example.com:8080` to pip, or set `HTTPS_PROXY`. pip and uv
  both honor it.
- **TLS inspection** (`CERTIFICATE_VERIFY_FAILED`): point pip at your company root certificate with
  `--cert C:\path\to\corp-root.pem` (or `PIP_CERT`). Recent pip releases already check the Windows
  certificate store. For uv, pass `--native-tls` (or set `UV_NATIVE_TLS=1`) to use the Windows
  certificate store.
- **Internal mirror** (Artifactory, Nexus, devpi): use `--index-url` / `PIP_INDEX_URL` for pip,
  and `--default-index` / `UV_DEFAULT_INDEX` for uv.
- **Offline machine:** on a connected machine, download wheels for the *target* machine's Python
  version, copy the folder across, and install with no index:

    ```powershell
    # connected machine: match the offline machine's Python (here 3.12, 64-bit)
    python -m pip download flaui-uiautomation-wrapper --dest wheels --only-binary=:all: --platform win_amd64 --python-version 3.12
    # offline machine
    python -m pip install --no-index --find-links wheels flaui-uiautomation-wrapper
    ```

    Add `--pre` to both commands to get a beta release. Every dependency ships `win_amd64` wheels
    for Python 3.11–3.15, so no compiler is needed. If pip starts *building* a package
    (`Building wheel for cffi ...`), the downloaded wheels do not match the target's Python version
    or bitness.

### Still stuck?

Open an [issue](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues) and include the
quick-check output, your Windows version (`winver`), and how you installed Python (python.org,
uv, the Microsoft Store, conda, ...).

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
- Targets Python 3.11–3.15 (`requires-python = ">=3.11,<3.16"`); modern syntax (`|` unions, `match`, built-in generics) is supported.
- If you hit syntax errors, confirm you are running Python ≥ 3.11. See
  [Unsupported Python version](#unsupported-python-version).

## DLL loading
- Confirm `flaui/bin` is packaged and reachable; rerun `setup_pythonnet_bridge()`.
- For blocked, quarantined or missing DLLs, see
  [Blocked or quarantined DLLs](#blocked-or-quarantined-dlls).

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

## Seeing what FlaUI is doing
- Turn on FlaUI's C# messages with `FLAUI_LOG_CSHARP=1` (or `enable_csharp_logging()`), and show
  them live in pytest with `-o log_cli=true --log-cli-level=DEBUG`. See
  [Configuration & logging](configuration.md#logging).
- If `get_main_window` gives up too early on a slow machine, raise the wait with
  `Automation(timeout=...)` or `FLAUI_MAIN_WINDOW_TIMEOUT` (milliseconds). See
  [Timeouts](configuration.md#timeouts).

## Flakiness tips
- Add short post_waits on mouse moves/drags.
- Use Retry with smaller intervals (50–100ms) and bounded timeouts.
- Keep UIA2 available for legacy WinForms when UIA3 is unstable.
