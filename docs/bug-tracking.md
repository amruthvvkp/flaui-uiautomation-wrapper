# Bug Tracking with pytest-bug

This project now uses `pytest-bug` to track known issues and limitations linked to GitHub issues.

## GitHub Issues Created

Categories: **Upstream** = Windows/.NET/UIA limitation (documented, not a wrapper bug);
**Flaky** = environment/timing instability hardened and/or CI-scoped; **Wrapper** = under
investigation as a genuine wrapper bug; **Env** = environment guard.

| Issue | Title | Tests Affected | Platform | Category |
|-------|-------|----------------|----------|----------|
| [#74](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74) | Spinner control AutomationID instability | test_spinner.py (3 tests) | UIA3 + WinForms | Flaky |
| [#75](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/75) | Combobox broken on WinForms | test_combobox.py, test_listbox.py, test_pop_up.py (22 tests) | UIA2/UIA3 + WinForms | Upstream |
| [#76](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/76) | Tree test flaky on AppVeyor CI | test_tree.py::test_selection (4 tests) | All (CI only) | Flaky |
| ~~[#77](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/77)~~ | RegisterAutomationEvent not ported | test_invoke_pattern.py::test_invoke_with_event | All | ✅ Resolved (ported) |
| [#78](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/78) | Toggle pattern unsupported on WinForms menus | test_menu.py::test_checked_menu_item (2 tests) | UIA2/UIA3 + WinForms | Upstream |
| [#79](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/79) | Context menu broken with UIA3 + WinForms | test_window.py::test_context_menu (1 test) | UIA3 + WinForms | Upstream |
| [#80](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/80) | find_all/first_with_options fail on some UIA/platform combos | test_automation_element.py (8 parametrizations) | UIA2 (all), UIA3+WinForms | Upstream (UIA2) + test fix — see outcomes below |

> **Note on #80 vs #81.** [#81](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/81)
> is a **closed duplicate** of #80. The in-code markers now reference `GH-80` (the canonical open
> issue); any lingering `GH-81` references should be treated as `GH-80`.
| [#82](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/82) | test_get_control_type Tab not found during setup | test_value_converter.py::test_get_control_type | UIA2 + WinForms | Flaky |
| [#83](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/83) | ListBox select_by_index fails | test_listbox.py::test_select_by_index | UIA3 + WPF | Wrapper (investigating) |
| [#89](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/89) | Notepad tests on Windows 11 (Store app) | Notepad-based tests (test_getter/search/xpath/keyboard) | Windows 11 | Env (guarded via `skip_notepad_on_win11`) |

> **Triage policy (Phase 0).** Upstream issues are documented and skipped with `platform_limitation`
> / `skip` markers — they are not wrapper defects and will not be "fixed" here. Flaky issues are
> hardened (retry/wait) and CI-scoped where needed. Wrapper issues (#80, #83) remain `xfail` with a
> `bug` marker until a fix is verified against the full UIA2/UIA3 × WinForms/WPF matrix. The #88
> coverage gate is enforced on the full suite (AppVeyor PR/master) — see
> [Road to v1.0](release-plan.md).

### Marker taxonomy (which marker to use)

`pytest-bug`'s `@pytest.mark.bug` is **whole-test**: with the default `run=False` it skips the test
on *every* matrix combo, and with `run=True` it treats the *whole* test as xfail. It cannot express
"skip on WinForms but pass on WPF". Choose the marker by failure shape:

| Failure shape | Marker | Behaviour | Query |
|---------------|--------|-----------|-------|
| Whole test broken/flaky on **all** affected combos, under active triage | `@pytest.mark.bug(id=…, url=…, reason=…, run=True)` | runs, treated as xfail (BUG-PASS / BUG-FAIL); detects a future fix | `-m bug`, `--bug-pattern=GH-XX` |
| Upstream limitation on **specific** matrix combos only (passes on the rest) | `@pytest.mark.platform_limitation` + a conditional skip fixture (`skip_on_winforms`, `skip_on_uia3_winforms`, …) | healthy combos run for real; only the broken combo is skipped | `-m platform_limitation` |
| Notepad / Store-app environment guard | `@pytest.mark.skip_notepad_on_win11(reason=…)` | skipped only on Windows 11 (build ≥ 22000) | `-m skip_notepad_on_win11` |

Current assignments after the Phase 0 marker-hygiene pass:

- **#76** (tree, flaky on CI across all combos): `bug(run=True)` — replaced the previous inline
  `try/except AssertionError → pytest.xfail`.
- **#78** (menu Toggle, WinForms only) and **#79** (context menu, UIA3+WinForms only):
  `platform_limitation` + conditional skip fixture — replaced the previous in-body `pytest.skip`.
- **#75** (combobox, WinForms): `platform_limitation` + `bug` + class-level `xfail`. Restoring real
  WPF combobox coverage (skip on WinForms only) is deferred to the coverage PR so it can be
  validated against the full matrix.
- **#89** (`test_application.py`): aligned to `skip_notepad_on_win11` (was a `windows11` +
  conditional `xfail`), which also avoids the Win11 Store-notepad launch hanging until timeout.

### Bug-fix pass outcomes (Phase 0)

Investigation results from running each item against the local UIA2/UIA3 × WinForms/WPF matrix:

- **#74** (spinner) — **locator hardened**. The WinForms app exposes two `ControlType.Spinner`
  controls; the target is now located by `ControlType.Spinner` + `Name == "Spinner"` (independent
  of the unstable AutomationID) with a retry and an explicit Simple-Controls tab selection
  (`tests/test_utilities/elements/winforms_application/simple_controls.py`). Passes reliably in
  isolation. A residual flakiness remains only in large bulk runs (the WinForms app is backgrounded
  while other matrix combos run first), so the class keeps a non-blocking `bug(run=True)` monitor.
- **#80** (find_*_with_options) — **fixed / reclassified, not a wrapper bug**. FlaUI's own UIA2
  layer raises `NotSupportedByFrameworkException` (these methods don't exist in UIA2), so UIA2 is
  skipped via `skip_on_uia2` + `platform_limitation`. The `find_all` test also used
  `by_class_name("TabControl")` (WPF-only); switched to `by_control_type(ControlType.Tab)` so it
  passes on UIA3 + WinForms too. Now passes on UIA3 (both frameworks) and skips on UIA2.
- **#82** (test_get_control_type) and **#83** (ListBox select_by_index) — **not reproducible**.
  Both pass on all four matrix combos locally (the conftest tab-navigation retry already mitigates
  the #82 setup flakiness). Kept as `bug(run=True)` monitors; close once CI confirms green.

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

### `run` parameter

The marker accepts a `run` flag that controls whether the marked test is skipped or executed:

- `run=False` (default): skip the test, shown as **BUG-SKIP**.
- `run=True`: run the test; it is treated as xfail, shown as **BUG-PASS** if it passes or **BUG-FAIL** if it fails. Use this sparingly, only when you want to detect that a bug has been fixed upstream.

### Output symbols

| Symbol | Word | Meaning |
|--------|------|---------|
| `b` | BUG-SKIP | Test skipped due to a known bug |
| `f` | BUG-FAIL | Bug-marked test ran and failed (expected) |
| `p` | BUG-PASS | Bug-marked test ran and passed (bug may be fixed) |

A summary line such as `Bugs skipped: 4` is printed at the end of the run.

### Available pytest-bug Options

- `--bug-all-skip`: Skip all bug-marked tests
- `--bug-all-run`: Run all bug-marked tests (respects their xfail/skip)
- `--bug-pattern=REGEX`: Run matching bug tests only
- `--bug-no-stats`: Disable summary statistics
- `--bug-skip-letter` / `--bug-fail-letter` / `--bug-pass-letter`: customize output symbols
- `--bug-skip-word` / `--bug-fail-word` / `--bug-pass-word`: customize verbose output words

### Customizing defaults in `pyproject.toml`

```toml
[tool.pytest.ini_options]
markers = ["bug: Known bug tracked in GitHub issues"]

# Optional pytest-bug overrides
bug_summary_stats = true
bug_skip_letter = "b"
bug_fail_letter = "f"
bug_pass_letter = "p"
bug_skip_word = "BUG-SKIP"
bug_fail_word = "BUG-FAIL"
bug_pass_word = "BUG-PASS"
```

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
