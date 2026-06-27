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

## CI/CD (Azure Pipelines)

The project runs continuous integration on Azure Pipelines. Configuration lives in
`azure-pipelines.yml`. The previous AppVeyor configuration is retained as a commented backup below a
no-op AppVeyor job, and GitHub Actions workflows are retained as manual-only stubs while the Azure
migration is validated.

Azure currently runs three PR validation jobs in parallel:

- Ruff and Interrogate checks
- Strict documentation build
- Windows FlaUI UI tests on Microsoft-hosted `windows-2025`

### Test script

```yaml
- pwsh: |
    uv run --group unit-test --no-dev --package flaui-uiautomation-wrapper --extra coverage \
      coverage run -m pytest --timeout=45 --timeout-method=thread \
      --junit-xml=test-results.xml --alluredir allure-results
```

Key parameters:

- `--timeout=45` — maximum execution time per test (seconds)
- `--timeout-method=thread` — thread-based timeout (safe on Windows)
- `--junit-xml=test-results.xml` — JUnit XML for CI parsing
- `--alluredir=allure-results` — Allure JSON reports for analytics

Azure publishes `test-results.xml` through `PublishTestResults@2`, so pytest test cases and
fixture matrix IDs such as `UIA2_WPF` and `UIA3_WinForms` are visible in the Azure Tests tab.
The raw `test-report.jsonl` file is also uploaded as an artifact for detailed pytest diagnostics.

### Artifacts

- `test-results.xml` — JUnit XML test results
- `test-report.jsonl` — pytest report log
- `coverage.xml` — XML coverage report
- `htmlcov/` — HTML coverage report
- `allure-results/` — Allure JSON reports (parameters, steps, timing, categorization)

### Coverage reporting

```yaml
- pwsh: |
    uv run --with coverage coverage combine
    uv run --with coverage coverage xml
    uv run --with coverage coverage html
```

### Python compatibility matrix

The Azure proof of concept starts with a single hosted Windows job on Python 3.12 x64 and the
`windows-2025` image to avoid slowing development while we validate FlaUI UI automation on
Microsoft-hosted agents. The supported Python 3.10 through 3.14 x64 matrix is kept commented in
`azure-pipelines.yml` and can be enabled after the hosted-agent behavior is stable.

The pipeline caches both the UV runtime/download cache and the project virtualenv with `Cache@2`,
keyed by OS, Python version, `uv.lock`, and `pyproject.toml`. The bundled FlaUI DLLs and test
application executables are already tracked in the repository, so there is no separate FlaUI build
cache in the initial Azure job.

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
