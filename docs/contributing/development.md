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

## Code quality

```bash
ruff check .             # lint (check only)
ruff check --fix .       # lint and auto-fix
ruff format .            # format
interrogate flaui/ --fail-under=95   # docstring coverage (95% required)
```

## Pre-commit hooks

Defined in `.pre-commit-config.yaml`:

- Trailing whitespace removal
- End-of-file fixes
- Ruff linting and formatting
- Interrogate docstring checks
- Python AST validation

```bash
pre-commit install        # install hooks
pre-commit run --all-files  # run manually
```

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

Azure currently runs three PR validation jobs in parallel:

- Ruff and Interrogate checks
- Strict documentation build
- Windows hosted smoke tests on Microsoft-hosted `windows-2022`

AppVeyor runs on `Visual Studio 2022`. It runs the full Windows desktop UI suite on pull requests
and on `master`, and the fast `tests/unit` subset on routine feature-branch pushes (the gate is
selected in `test_script` from `APPVEYOR_PULL_REQUEST_NUMBER` / `APPVEYOR_REPO_BRANCH`).

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
    # Full UI suite only where it gates a merge; fast unit subset otherwise.
    $runFull = ($env:APPVEYOR_REPO_BRANCH -eq 'master') -or [bool]$env:APPVEYOR_PULL_REQUEST_NUMBER
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

Both CI systems start with Python 3.12 x64 only to avoid slowing development while the migration is
validated. The supported Python 3.10 through 3.14 x64 matrix is kept commented in both
`azure-pipelines.yml` and `.appveyor.yml` and can be enabled after the hybrid setup is stable.

Azure caches both the UV runtime/download cache and the project virtualenv with `Cache@2`, keyed by
OS, Python version, `uv.lock`, and `pyproject.toml`. AppVeyor caches the UV download cache and
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
