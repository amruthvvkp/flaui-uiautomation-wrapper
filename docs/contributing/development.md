# Development workflow

This page collects the day-to-day commands and conventions for working on the wrapper. For
testing specifics see [Testing](testing.md) and [Porting C# tests](porting-tests.md).

## UV package manager

```bash
# Install all dependencies (dev + test groups + extras)
uv sync --all-groups --all-extras

# Update all dependencies to latest allowed
uv sync --all-groups --all-extras -U

# Build the wheel
uv build

# Bump the version
uv version 0.2.0

# Run tests
uv run --group unit-test pytest tests/ui/ -v

# Run with coverage
uv run --group unit-test --extra coverage coverage run -m pytest
uv run --no-project --with coverage coverage html
```

Always prefix commands with `uv run` so the correct environment is used.

The package builds with uv's own build backend (`uv_build`, configured under
`[tool.uv.build-backend]` in `pyproject.toml`). It packages everything under `flaui/`, including
`py.typed` and the C# DLLs in `flaui/bin/`. After changing the build settings, confirm that
`uv build` still puts all five DLLs in the wheel.

## Code quality

```bash
ruff check .             # lint (check only)
ruff check --fix .       # lint and auto-fix
ruff format .            # format
interrogate flaui/ --fail-under=95   # docstring coverage (95% required)
```

### Static analysis

Run these before opening a PR; the Azure `linting_checks` job enforces all of them.

```bash
uv run --group dev ty check flaui                    # type check
uv run --group dev pylint flaui --fail-under=9.5     # lint score must stay >= 9.5
uv run --group dev bandit -c pyproject.toml -r flaui # security lint
uv run --group dev vulture                           # dead code (paths and options come from pyproject.toml)
```

All three tools are configured in `pyproject.toml`:

- **Pylint** (`[tool.pylint.*]`). PythonNet loads the C# namespaces (`FlaUI.*`, `System.*`, `clr`)
  only at runtime, so they are listed in `ignored-modules`. That is the pylint counterpart of
  `[tool.ty.rules]`. Do not add per-line `# pylint: disable=import-error` / `no-member` for C#
  imports. A small set of checks is disabled on purpose, and the comments next to `disable` explain
  each one: late imports and the cycles they break, C#-parity class and module sizes, broad catches
  around .NET exceptions, and the line-length and import-order checks that Ruff and isort own. C#
  names kept for parity (`ControlType.Button`, `Retry.While`, `PropertyCondition.And`) are allowed
  through `class-const-naming-style` and `good-names-rgxs`.
- **Bandit** (`[tool.bandit]`). Do not silence a finding without saying why. Prefer fixing it. For
  a silent `except: pass`, log at `debug` with `exc_info=True`. If a finding really is safe, use
  `# nosec BXXX  # <reason>`.
- **Vulture** (`[tool.vulture]`). `flaui` is a library, so most of its public API is never called
  inside the package. Members decorated with `@property`, `@handle_csharp_exceptions`,
  `@staticmethod` / `@classmethod` or a Pydantic validator are skipped. The remaining public names
  are listed in `vulture_whitelist.py`, grouped by module. When vulture flags new code, delete it if
  it is dead. If it is public API, add it to the whitelist. Run
  `uv run --group dev vulture flaui --make-whitelist` for a draft.

## Pre-commit hooks

Defined in `.pre-commit-config.yaml`:

- Trailing whitespace removal
- End-of-file fixes
- Ruff linting and formatting
- Interrogate docstring checks
- Pylint, Bandit and Vulture (local hooks that run through `uv run`)
- Python AST validation

```bash
pre-commit install        # install hooks
pre-commit run --all-files  # run manually
```

## Performance benchmark

`scripts/benchmark.py` times element finding and actions against the bundled WinForms and WPF test
apps on all four UIA2/UIA3 combinations. It runs each operation through the wrapper and through the
raw C# object, so the table shows how much the wrapper adds on top of FlaUI:

```bash
uv run python scripts/benchmark.py              # 50 iterations per operation
uv run python scripts/benchmark.py -n 200 --json results.json
```

`scripts/benchmark_name_map.py` (same flags, minus `--json`) does the same for element name maps. It
compares a direct find with the test-suite map and the documented `examples/pytest/app_map.py`
recipe, and splits the difference into extra UIA lookups and map-class cost. It only reports, so it
always exits 0.

`scripts/benchmark_pywinauto.py` runs the same finds and actions through pywinauto's `uia` backend
(and its `win32` backend on WinForms) next to the wrapper on UIA2 and UIA3, in one process, and
prints the median and p95 for each. pywinauto is not a dependency of the package; it lives in the
optional `bench` dependency group:

```bash
uv run --group bench python scripts/benchmark_pywinauto.py -n 100
uv run --group bench python scripts/benchmark_pywinauto.py -n 100 --json pywinauto.json
uv run --group bench python scripts/benchmark_pywinauto.py --skip-flaui   # pywinauto only
```

The operations match in intent, not always in mechanism (pywinauto's search strategy, its own
post-click sleep, `BM_SETCHECK` on `win32`). The script prints where they differ under the table.
It only reports, so it always exits 0.

`scripts/benchmark_agent.py` times what an AI computer-use agent does on each step, rather than
single finds: a full accessibility-tree snapshot (wrapper properties, a `CacheRequest`, raw C#, and,
with the `bench` group, pywinauto and raw comtypes), cold start in fresh processes, window and
element screenshots encoded to PNG bytes, `find_all_descendants` on the largest lists and grids, and
repeated find-plus-toggle cycles. It prints median and p95, and exits 1 if any reliability cycle
fails:

```bash
uv run python scripts/benchmark_agent.py                            # flaui only
uv run --group bench python scripts/benchmark_agent.py --json agent.json
uv run python scripts/benchmark_agent.py --sections snapshot capture -n 20
uv run python scripts/benchmark_agent.py --sections cold --cold-runs 20
```

`-n` sets the timed runs for snapshot, capture and scaling (default 10), `--cold-runs` the fresh
processes per combination (default 10), and `--cycles` the find-plus-toggle cycles (default 500).

All four scripts need an interactive desktop, because they launch the apps and click controls, so they
are not run in CI. The v1 gate is wrapper overhead under 5 ms mean per operation, and
`benchmark.py` exits 1 when any operation misses it. Absolute timings are printed for reference only: they come from Windows UIA and
the app under test. Current numbers are on the [Performance](../performance.md) page.

## Exception handling

All C# interop must use the `@handle_csharp_exceptions` decorator (from `flaui/lib/exceptions.py`),
which translates C# FlaUI exceptions into Python equivalents:

```python
def handle_csharp_exceptions(func):
    """Wrap a function to translate C# FlaUI exceptions into Python exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except CSharpPropertyNotSupportedException:
            raise PropertyNotSupportedException(f"...'{func.__name__}'...")
        except CSharpElementNotAvailableException:
            raise ElementNotAvailableException(f"...'{func.__name__}'...")
        except System.Exception:
            raise SystemException(f"...'{func.__name__}'...")
    return wrapper
```

```python
@property
@handle_csharp_exceptions  # always decorate interop
def name(self) -> str:
    """Return the element name."""
    return self.raw_element.Name
```

Python equivalents of the C# FlaUI exceptions (in `flaui/lib/exceptions.py`) include
`ElementNotFound`, `PropertyNotSupportedException`, `ElementNotEnabledException`, and
`NoClickablePointException`.

## CI/CD (Azure Pipelines + AppVeyor)

The project uses a hybrid CI setup:

- Azure Pipelines (`azure-pipelines.yml`) owns linting, documentation, packaging, deployment
  plumbing, and a hosted Windows smoke suite.
- AppVeyor (`.appveyor.yml`) is the hosted Windows desktop UI gate. The gate is **trimmed**: the
  slow full FlaUI UI suite only runs where it gates a merge — pull requests and pushes to `master`
  (`APPVEYOR_PULL_REQUEST_NUMBER` set, or `APPVEYOR_REPO_BRANCH == master`). Routine feature-branch
  pushes run the fast `tests/unit` subset only. Paint-specific XPath cases that can abort native
  UIA/COM on hosted CI are skipped there and remain runnable locally.
- GitHub Actions workflows are retained as manual-only stubs while CI/CD ownership moves to Azure
  and AppVeyor.

Azure runs these PR validation jobs in parallel:

- Ruff and Interrogate checks
- Strict documentation build
- Windows hosted smoke tests, a matrix over Python versions and Windows images (see below)
- Clean wheel install smoke (`wheel_install_smoke`, see below)

AppVeyor runs on `Visual Studio 2026`, one job per supported Python. The full Windows desktop UI
suite runs on the `FULL_UI` jobs (Python 3.11, 3.12 and 3.15) for pull requests and `master`.
Every other job, and routine feature-branch pushes, run the fast `tests/unit` subset. The gate is
selected in `test_script` from `FULL_UI`, `APPVEYOR_PULL_REQUEST_NUMBER` and
`APPVEYOR_REPO_BRANCH`. AppVeyor runs jobs one after another, so the full-UI jobs go first and
`matrix.fast_finish` stops at the first failure.

### Stale build cancellation

Azure Pipelines cancels stale pull-request validation runs through `pr.autoCancel: true` and batches
stale branch pushes through `trigger.batch: true`.

AppVeyor stale PR cancellation is handled by the project-level **Rolling builds** setting, not by
`appveyor.yml`. Keep rolling builds enabled for pull requests and leave
`rollingBuildsDoNotCancelRunningBuilds` disabled so queued and running stale PR builds are cancelled
when a newer commit is pushed.

### Azure hosted smoke script

```yaml
- pwsh: |
    uv run --group unit-test --no-dev --package flaui-uiautomation-wrapper --extra coverage \
      coverage run -m pytest tests/unit/lib tests/unit/core/test_identifiers.py \
      --timeout=45 --timeout-method=thread \
      --junit-xml=test-results.xml --alluredir allure-results
```

### AppVeyor test script (trimmed gate)

```yaml
- ps: |
    # Full UI suite only on the FULL_UI jobs, where it gates a merge; fast unit subset otherwise.
    $gatesMerge = ($env:APPVEYOR_REPO_BRANCH -eq 'master') -or [bool]$env:APPVEYOR_PULL_REQUEST_NUMBER
    $runFull = $gatesMerge -and ($env:FULL_UI -eq 'true')
    if ($runFull) {
      uv run --group unit-test --no-dev --package flaui-uiautomation-wrapper --extra coverage \
        coverage run -m pytest --timeout=45 --timeout-method=thread \
        --junit-xml=test-results.xml --alluredir allure-results
    } else {
      uv run --group unit-test --no-dev --package flaui-uiautomation-wrapper --extra coverage \
        coverage run -m pytest tests/unit --timeout=45 --timeout-method=thread \
        --junit-xml=test-results.xml --alluredir allure-results
    }
```

Key parameters:

- `--timeout=45` — maximum execution time per test (seconds)
- `--timeout-method=thread` — thread-based timeout (safe on Windows)
- `--junit-xml=test-results.xml` — JUnit XML for CI parsing
- `--alluredir=allure-results` — Allure JSON reports for analytics

Azure publishes `test-results.xml` through `PublishTestResults@2`, so pytest smoke test cases are
visible in the Azure Tests tab. AppVeyor uploads the full-suite JUnit XML with fixture matrix IDs
such as `UIA2_WPF` and `UIA3_WinForms`. The raw `test-report.jsonl` file is uploaded as an artifact
for detailed pytest diagnostics.

### Artifacts

- `test-results.xml` — JUnit XML test results
- `test-report.jsonl` — pytest report log
- `coverage.xml` — XML coverage report
- `htmlcov/` — HTML coverage report
- `allure-results/` — Allure JSON reports (parameters, steps, timing, categorization)

### Coverage reporting

```yaml
- pwsh: |
    uv run --with coverage coverage xml
    uv run --with coverage coverage html
```

### Python compatibility matrix

Every supported Python (3.11–3.15, 64-bit CPython) runs in CI. To keep turnaround reasonable, only
the oldest, newest and 3.12 pay for the slow full UI suite:

| Python | AppVeyor (Visual Studio 2026) | Azure hosted smoke |
|--------|-------------------------------|--------------------|
| 3.11 | full UI suite on PRs/`master`, unit subset otherwise | `windows-2022`, `windows-2025` |
| 3.12 | full UI suite on PRs/`master`, unit subset otherwise, plus wheel smoke | `windows-2022` |
| 3.13 | unit subset | `windows-2022` |
| 3.14 | unit subset | `windows-2022` |
| 3.15 | full UI suite on PRs/`master`, unit subset otherwise | `windows-2022`, `windows-2025` |

The Azure smoke legs install a uv-managed CPython (`uv python install`), so a new Python release
does not wait for the hosted image's tool cache.

### Windows versions covered

| Where | Image | Windows version | What runs |
|-------|-------|-----------------|-----------|
| AppVeyor | `Visual Studio 2026` | Windows Server (exact build logged in each job's `init` step) | Full desktop UI suite, wheel smoke with UI checks |
| Azure | `windows-2022` | Windows Server 2022 | Hosted smoke on every Python, clean wheel install smoke |
| Azure | `windows-2025` | Windows Server 2025 | Hosted smoke on 3.11 and 3.15 |
| Contributors | local machines | Windows 10 / 11 | Full suite locally (`uv run pytest`) |

Each Azure smoke leg logs the exact OS caption and build number in its *Install and show Python*
step. Windows 11-specific behavior (the Store Notepad and the new Paint) is handled by the markers
listed in [Troubleshooting](../troubleshooting.md#known-pytest-skipsxfails-manual-list).

### Clean wheel install smoke

`scripts/wheel_smoke.py` checks the wheel as users get it. CI builds the wheel, installs it with
no dev dependencies into fresh virtual environments *outside* the checkout, and runs the script
with `python -I` from that directory, so `flaui` can only resolve from site-packages. The script
asserts that:

- `flaui` is imported from site-packages, not a source tree;
- the five bundled DLLs and `py.typed` are installed;
- `setup_pythonnet_bridge()` loads FlaUI 5.x.

With `--apps-dir test_applications` it also launches the WPF and WinForms test apps on UIA2 and
UIA3, toggles a checkbox and sets text in the TextBox.

| Job | Installation types | UI checks |
|-----|--------------------|-----------|
| Azure `wheel_install_smoke` (`windows-2022`) | tool-cache CPython 3.12 + `pip`; uv-managed CPython 3.11 and 3.15 + `uv pip` | no (no interactive desktop) |
| AppVeyor 3.12 job (`WHEEL_SMOKE`) | uv-managed CPython 3.12 + `uv pip`; the image's newest python.org `C:\Python3XY-x64` + `pip` | yes |

Run it locally against a fresh venv:

```powershell
$repo = (Get-Location).Path
uv build --wheel
uv venv $env:TEMP\flaui-smoke --python 3.12
uv pip install --python $env:TEMP\flaui-smoke\Scripts\python.exe (Get-ChildItem dist\*.whl).FullName
Push-Location $env:TEMP
& $env:TEMP\flaui-smoke\Scripts\python.exe -I "$repo\scripts\wheel_smoke.py" --apps-dir "$repo\test_applications"
Pop-Location
```

Azure caches both the UV runtime/download cache and the project virtualenv with `Cache@2`, keyed by
OS (the image name for the venv), Python version, `uv.lock`, and `pyproject.toml`. AppVeyor caches the UV download cache and
`.venv` with the same lockfile inputs. The bundled FlaUI DLLs and test application executables are
already tracked in the repository, so there is no separate FlaUI build cache in the initial jobs.

### Future deployment options

Azure also builds package distributions and contains gated deployment stages:

- `deploy_testpypi` runs only when `PUBLISH_TEST_PYPI=true` on a non-PR run and requires
  `TEST_PYPI_API_TOKEN`.
- `deploy_pypi` runs only on `v*` tags when `PUBLISH_PYPI=true` and requires `PYPI_API_TOKEN`.
- `deploy_docs` runs only when `PUBLISH_DOCS=true` on a non-PR run and requires
  `GITHUB_PAGES_TOKEN`.

Use Azure Environments named `test-pypi`, `pypi`, and `github-pages` for approvals before enabling
these deployment variables.

## Documentation

The docs site is built with [Zensical](https://zensical.org), configured by `zensical.toml`. API
reference pages are generated by [mkdocstrings](https://mkdocstrings.github.io/).

```bash
# Regenerate the FlaUI versions include, then build
uv run python scripts/extract_versions.py
uv run zensical build -f zensical.toml          # build
uv run zensical build --strict -f zensical.toml # strict build (CI gate)
uv run zensical serve -f zensical.toml          # local preview
```

Regenerate `docs/_includes/flaui_versions.md` with `scripts/extract_versions.py` whenever
`flaui/bin/Version.md` changes.

## Troubleshooting

For common runtime issues (PythonNet bridge errors, element-not-found, timing/sync, DLL loading,
Windows/OS specifics, and the current list of test skips/xfails) see
[Troubleshooting](../troubleshooting.md).
