# Bug Tracking with pytest-bug

This project now uses `pytest-bug` to track known issues and limitations linked to GitHub issues.

## GitHub Issues Created

| Issue | Title | Tests Affected | Platform |
|-------|-------|----------------|----------|
| [#74](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74) | Spinner control AutomationID instability | test_spinner.py (3 tests) | UIA3 + WinForms |
| [#75](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/75) | Combobox broken on WinForms | test_combobox.py, test_listbox.py, test_pop_up.py (22 tests) | UIA2/UIA3 + WinForms |
| [#76](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/76) | Tree test flaky on AppVeyor CI | test_tree.py::test_selection (4 tests) | All (CI only) |
| [#77](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/77) | RegisterAutomationEvent not ported | test_invoke_pattern.py::test_invoke_with_event (4 tests) | All |
| [#78](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/78) | Toggle pattern unsupported on WinForms menus | test_menu.py::test_checked_menu_item (2 tests) | UIA2/UIA3 + WinForms |
| [#79](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/79) | Context menu broken with UIA3 + WinForms | test_window.py::test_context_menu (1 test) | UIA3 + WinForms |

## Usage Examples

### Query tests by bug ID
```bash
# List all tests affected by bugs
uv run pytest --co -m bug -q

# List tests for specific issue
uv run pytest --co -m "bug and GH-74" -q

# Run tests excluding known bugs
uv run pytest -m "not bug" -v
```

### Check bug annotations in code
```python
@pytest.mark.bug(
    id="GH-74",
    url="https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74",
    reason="Spinner control element finding is flaky"
)
@pytest.mark.xfail(reason="...")
def test_flaky_feature():
    pass
```

### Generate bug report
```bash
# Show all tests with bug markers
uv run pytest --collect-only -m bug --tb=no

# Count tests per issue
uv run pytest --co -m bug -q | Select-String "test_" | Measure-Object
```

## Marker Usage Pattern

**Important**: Bug markers are **additive metadata**, not replacements for xfail/skip markers.

### Correct Usage

Always use bug markers **alongside** xfail/skip:

```python
# For class-level xfail
@pytest.mark.bug(
    id="GH-74",
    url="https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74",
    reason="Spinner control AutomationID instability"
)
class TestSpinner:
    pass

```

### What Bug Markers Provide

- GitHub issue tracking and links
- Query capability: `pytest -m bug`
- Summary statistics: "Bugs skipped: X"
- Traceability from test → issue → upstream bug report

### What Bug Markers Don't Do

- Don't automatically make tests xfail/skip
- Don't change test execution behavior
- Are metadata only

### Available pytest-bug Options

- `--bug-all-skip`: Skip all bug-marked tests
- `--bug-all-run`: Run all bug-marked tests (respects their xfail/skip)
- `--bug-pattern=REGEX`: Run matching bug tests only
- `--bug-no-stats`: Disable summary statistics

## Benefits

1. **Traceability**: Each failing/flaky test is linked to a GitHub issue
2. **Queryable**: Use `-m bug` to filter tests by known issues
3. **Documentation**: Issue URLs provide context and discussion
4. **Prioritization**: See which bugs affect the most tests
5. **CI Integration**: Can fail builds only for non-bug failures

## Test Status Summary (from AppVeyor)

- **Total Tests**: 502
- **Passed**: 423 (84.3%)
- **Skipped**: 54 (10.8%) - Most due to known bugs
- **Xfailed**: 12 (2.4%) - Flaky tests
- **Tests with Bug Markers**: 40 (7.9%)

## Next Steps

1. Monitor GitHub issues for upstream fixes (Windows/.NET, FlaUI)
2. Retest when issues are resolved and remove markers
3. Add bug markers to any new flaky/broken tests discovered
4. Use `pytest-bug` metadata in CI reporting

## Related Configuration

- **pyproject.toml**: Added `pytest-bug>=1.4.0` to `[dependency-groups] unit-test`
- **Markers**: Added `bug` marker to pytest configuration
- **CI**: AppVeyor already captures xfail/skip reasons in test-results.xml
