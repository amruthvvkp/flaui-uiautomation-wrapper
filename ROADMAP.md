# FlaUI Python Wrapper — Roadmap to v1.0.0

**Project goal:** a production-ready Python wrapper for FlaUI that is as flexible, polished, and
intuitive as Playwright or Selenium — full 1:1 parity with FlaUI C#, backed by Pydantic type safety,
and comprehensive documentation for beginners through advanced users.

The live source of truth is the
**[GitHub milestones](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestones)** board,
now organized as **Phase 0–8**. This file mirrors that board: what's done, what's pending, and the
order we'll tackle the rest.

> **History note:** earlier planning docs — the "Day 1-2 … Day 9-10" `10-DAY-ROADMAP.md`, the
> pre-release `to-do.md`, the MkDocs-era `DOC_PLAN.md` (superseded by the Zensical migration and
> `docs/contributing/`), and the `TEST_PORTING_SUMMARY.md` snapshot — have been retired and folded
> into the Phase 0–8 structure below. Doc/test conventions now live in `CLAUDE.md` and
> [`docs/contributing/`](docs/contributing.md).

---

## Status at a glance

| Phase | Milestone | Status | Open / Closed |
|-------|-----------|--------|---------------|
| — | [Create initial usable release](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/1) | ✅ Done | 0 / 18 |
| 0 | [Stabilize](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/7) | 🟡 In progress | 10 / 1 |
| 1 | [Exceptions & Identifiers](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/8) | ✅ Done | 0 / 6 |
| 2 | [Patterns](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/9) | ✅ Done | 0 / 5 |
| 3 | [Elements & ScrollBars](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/10) | ✅ Done | 0 / 2 |
| 4 | [Events](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/11) | ✅ Done | 0 / 2 |
| 5 | [Capturing / Overlay / Video](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/12) | ✅ Done | 0 / 2 |
| 6 | [Logging / Tools / Enhancers](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/13) | ✅ Done | 1 / 3 |
| 7 | [Docs & Zensical](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/14) | ✅ Done | 0 / 5 |
| 8 | [Polish & v1.0](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/15) | ⏳ Pending | 5 / 0 |
| Post-v1 | [Ecosystem & Playwright-grade polish](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/16) | ⏳ Not started | 9 / 0 |

**Legend:** ✅ done · 🟡 in progress · ⏳ not started

---

## ✅ Completed

### Foundation (closed: *Create initial usable release v1.0.0*)
- Migrated Poetry → **UV** package manager; FlaUI 4 + PythonNet 3 prototype.
- **PythonNet bridge** for C# interop with strict init ordering.
- **Pydantic** validation across all models (type safety + IDE intellisense).
- pytest matrix framework (UIA2/UIA3 × WinForms/WPF), object mapping, pytest-bug tracking.
- Python 3.10+ support, packaging/issue/PR templates.

### Phase 1 — Exceptions & Identifiers *(complete)*
- **#102** Complete exception hierarchy · **#98** Identifier system (EventId/PatternId/PropertyId/
  TextAttributeId) · **#105 / #104** XPath navigation support · **#73** `translate_exceptions`
  Pythonic wrapper over the hierarchy.

### Phase 2 — Patterns *(complete)*
- **#91** All **34 UI Automation patterns** implemented (full parity with FlaUI's `IFrameworkPatterns`).
- **#117** pattern surface · **PR #122** real WinForms/WPF UI integration tests across the matrix.

### Phase 3 — Elements & ScrollBars *(complete)*
- **#99** `ScrollBarBase` / `HorizontalScrollBar` / `VerticalScrollBar` + converters (**PR #123**).

### Phase 4 — Events *(complete)*
- **#94** Event handler system · **#77** `RegisterAutomationEvent` ported with GC keep-alive (**PR #123**).

### Phase 5 — Capturing / Overlay / Video *(complete)*
- **#95** Screen capture & video (`flaui/core/capturing.py` — `Capture`, `CaptureImage`,
  `VideoRecorder`) · **#103** Overlay system (`flaui/core/overlay.py` — `OverlayManager`).

### Phase 6 — Logging / Tools / Enhancers *(complete)*
- **#96** Logging infrastructure (stdlib `logging`, opt-in C#→Python sink via `FLAUI_LOG_CSHARP`) ·
  **#68** mouse busy-spinner / loading-state wait helper.
- **#100** Tools/utilities: `ItemRealizer`, `AccessibilityTextResolver`, `WindowsStoreAppLauncher`,
  `LocalizedStrings`, `SystemInfo` (**PR #123**).
- **#87** Pythonic enhancers: `__repr__`, `Application`/`Automation` context managers,
  `AutomationElementCollection` (`.first`/`.filter`/`.where` + iteration/indexing), `expect()` fluent
  assertions (`flaui/core/expectations.py`), `py.typed` marker + `ty` type-check gate in CI.

### Infrastructure
- **#107** Python `AutomationBase` + UIA2/UIA3 facades · **#118** CI migrated to Azure Pipelines
  (+ AppVeyor UI gate) · **#51** MkDocs/Zensical docs base.

---

## ⏳ Pending — prioritized backlog

Phases 1–7 are now complete (exceptions/identifiers, patterns, elements, events, capturing/overlay/
video, logging/tools/Pythonic enhancers, docs). The remaining v1.0 gate is **Phase 0 → 8**, in that
priority order.

### P1 — Phase 0: Stabilize *(pre-release gate — active)*
- **[#88](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/88)** — `flaui.core` test
  coverage umbrella. Target **95%** (gate raised from the 85% floor; verified on the AppVeyor full
  UI matrix). See [C# Parity Map](parity.md) / `docs/parity.md` for surface coverage.
- Bug fixes: **#74 #75 #76 #78 #79 #80 #82 #83 #89** (see table below). Most are now triaged with
  `platform_limitation` / `bug(run=True)` markers and documented in
  [bug-tracking](bug-tracking.md); several are upstream Windows/.NET issues kept as known xfail/skip.

### ✅ Phase 7: Docs & Zensical *(complete)*
- **[#86](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/86)** comprehensive docs
  (umbrella) · **[#69](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/69)** example
  gallery · sample suites: **[#48](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/48)**
  Behave · **[#49](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/49)** TestPlan ·
  **[#50](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/50)** PyTest.
- Python and C# sit side by side in content tabs across Basics, Advanced, the Element Cookbook, the
  Gallery and the framework pages. Every Python snippet is included from runnable code under
  `examples/` (pytest / unittest / behave / Testplan suites + gallery scripts for the bundled apps,
  Calculator and Notepad); the strict docs build fails if a referenced section disappears. The
  [Upgrade guide](upgrade-guide.md) gained a *Migrating from FlaUI C#* translation table.
  *(Robot Framework deferred to post-v1.)*

### P3 — Phase 8: Polish & release
- **[#85](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/85)** polish & production
  readiness · release automation
  **[#57](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/57)** /
  **[#65](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/65)** /
  **[#66](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/66)** · then
  **[#84](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/84) v1.0.0 release**.
  *(Tag-driven beta automation is wired — see [Release automation](#release-automation) — pending
  token enablement.)*

### Post-v1 — parity gaps & deferred tests (out of scope for v1.0)
- **[#121](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/121)** — CustomNavigation
  pattern (absent from FlaUI.Core; lives only in raw COM interop).
- **Touch input tests** — `TouchTests.cs` is `[Ignore]`d upstream (unreliable on most CI/hardware).
- **Full app integration suites** (Calculator / Notepad / Paint end-to-end) — deferred under #88/#89;
  UI varies by Windows version/language. A `tests/integration/` skeleton (marked
  `@pytest.mark.integration`, skipped by default) is the intended home.

---

## Post-v1 — companion tooling & ecosystem

> These items start **only after v1.0 ships** (the v1 gate above takes priority). Each is intended
> as a **separate, independently versioned companion PyPI package** so the core
> `flaui-uiautomation-wrapper` stays lean — mirroring how `pytest-playwright` ships alongside
> `playwright`. The core wrapper remains the single dependency they all build on.

Tracked in the **[Post-v1 — Ecosystem & Playwright-grade polish](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/16)** milestone.

### Playwright-grade core ergonomics *(in-core, not separate packages)*

`expect()`, `AutomationElementCollection`, context managers and `__repr__` (#87) already shipped.
The remaining gaps against Playwright's developer experience:

| Issue | Feature | Why |
|-------|---------|-----|
| [#139](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/139) | **Auto-waiting** for actions (attached / on-screen / enabled / stable before `click`, `enter`, `invoke`…) | Removes manual `post_wait` / `Retry` / sleeps; the core cause of flaky tests |
| [#140](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/140) | **Locator API** — lazy, re-resolving, chainable (`window.locator(automation_id=…).nth(2).click()`) | Survives UI re-renders / stale elements; output format for the recorder |

### Companion packages

| Issue | Package / effort | What it is | Inspiration |
|-------|------------------|------------|-------------|
| — | **FlaUI agent skills** | Claude Code skills bundle for FlaUI development | — |
| [#142](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/142) | **`flaui-recorder`** | Record-and-generate UI script tool | [twenzel/FlaUIRecorder](https://github.com/twenzel/FlaUIRecorder), Playwright codegen |
| [#143](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/143) | **`flaui-mcp`** | MCP server (control + authoring profiles) — see below | [shanselman/FlaUI-MCP](https://github.com/shanselman/FlaUI-MCP), Playwright MCP |
| [#141](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/141) | **`pytest-flaui`** | pytest plugin: fixtures + backend matrix + capture-on-failure | [`pytest-playwright`](https://github.com/microsoft/playwright-pytest) |

### MCP — first goal ([#143](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/143) umbrella)

One `flaui-mcp` server (own repo) with **two profiles** sharing a session / element-ref / safety layer:

| Issue | Work item |
|-------|-----------|
| [#144](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/144) | **Element-map (name mapping) schema** in core — framework-neutral, versioned YAML/JSON contract shared by MCP authoring, the recorder, codegen and `pytest-flaui` |
| [#145](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/145) | **`control` profile** — launch/attach, pruned snapshots, find, click/type/select, screenshot, `wait_for` for any MCP harness |
| [#146](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/146) | **`authoring` profile** — explore the app, propose/validate element maps, generate pytest/behave/unittest/Robot tests |
| [#147](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/147) | **Isolated efficiency benchmark** — generate the framework example suites via the MCP in a clean workspace; measure tokens, tool calls, pass rate, flakiness, human edits |

**Suggested order:** #144 + #145 (parallel) → #146 → #147; in core, #139 auto-wait → #140 locators
improve generated code as they land; then #141 pytest-flaui → #142 recorder (reuses #144 + #146
selector strategy and codegen templates).

**Repository strategy:** `flaui-mcp`, `flaui-recorder` and `pytest-flaui` each get their own repo
(distinct deps and release cadence). Thin framework adapters (behave, unittest, TestPlan) start in
a shared integrations workspace and split out only when they get real users. Robot Framework support
is pursued by enhancing the existing Robot library with this SDK, coordinated with its maintainers.

### FlaUI agent skills
A bundle of Claude Code skills (`.claude/skills/…`) packaging FlaUI development knowledge so users
building automation get assisted workflows: element/pattern lookup, test scaffolding, and C#→Python
test-porting helpers. Distributable as an installable skills bundle.

### `flaui-recorder` ([#142](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/142))
A Playwright-codegen-style **record-and-generate** tool: watch a user's interactions against a live
Windows app (via UIA events / hit-testing) and emit ready-to-run Python FlaUI scripts. Lowers the
barrier to authoring automation by hand. Builds on this wrapper's event handlers and XPath navigator;
inspired by the C# [twenzel/FlaUIRecorder](https://github.com/twenzel/FlaUIRecorder).

### `flaui-mcp` ([#143](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/143))
An **MCP server** exposing FlaUI Python automation as callable tools so agents/LLMs can drive Windows
desktop apps — the Python counterpart to the C#
[shanselman/FlaUI-MCP](https://github.com/shanselman/FlaUI-MCP).

### `pytest-flaui` ([#141](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/141))
A **pytest plugin** modeled on `pytest-playwright`: ready-made `automation` / session fixtures, the
UIA2×UIA3 matrix helpers this repo already uses, screenshots/video on failure via
[`flaui/core/capturing.py`](flaui/core/capturing.py), and `flaui-recorder` integration for codegen.

### Docs — broaden Python/C# tabbed examples *(enhancement, not net-new infra)*
Side-by-side Python/C# tabs already exist (`pymdownx.tabbed` in `docs/index.md`, `docs/basics.md`,
`docs/advanced.md`). Post-v1 scope is **expanding** C#-parity tabs across the remaining guide and API
pages — valuable because FlaUI's own documentation is sparse, so these become a reference for both
audiences.

---

## Known bugs (Phase 0)

| Issue | Symptom | Tests |
|-------|---------|-------|
| [#74](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74) | Spinner element finding flaky — AutomationID instability | 3 |
| [#75](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/75) | Combobox heavily broken on WinForms (Windows/.NET bugs) | 22 |
| [#76](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/76) | Tree test flaky on AppVeyor CI — only 1 item found | 4 |
| [#78](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/78) | Toggle pattern unsupported on WinForms menu items | 2 |
| [#79](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/79) | WinForms context menu broken on UIA3 / newer .NET | 1 |
| [#80](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/80) | `find_*_with_options` fail on specific UIA/platform combos | 8 |
| [#82](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/82) | `test_get_control_type` fails on UIA2_WinForms (setup) | 4 |
| [#83](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/83) | `test_select_by_index` fails on UIA3_WPF (ListBox) | 4 |
| [#89](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/89) | Notepad UI tests on Windows 11 (Store app) need rework | — |

---

## Release automation

Releases are **tag-driven** so no workflow needs to push to protected `master` (resolves #57):

| Event | Outcome | Where |
|-------|---------|-------|
| Pull request | dev build `1.0.0.dev<buildId>` → **TestPyPI** | Azure `deploy_testpypi` |
| Merge to `master` | next `1.0.0bN` minted → GitHub **pre-release** (notes via release-drafter, #65) + tag `v1.0.0bN` | `.github/workflows/release-beta.yml` |
| Tag `v1.0.0bN` | wheel/sdist → **PyPI** pre-release (links to PyPI + docs on the notes, #66) | Azure `deploy_pypi` |
| Tag `v1.0.0` | stable release + `stable` docs alias | Azure `deploy_pypi` + `deploy_docs` |

All publish paths are **off by default**; enable via Azure `PUBLISH_*` flags + tokens and the GitHub
`ENABLE_BETA_RELEASES` repo variable. Full flow: [Road to v1.0](release-plan.md#how-releases-are-automated).

## C# parity

`docs/parity.md` (generated by `scripts/parity_audit.py`, re-run on DLL bumps) maps the bundled
FlaUI 5.0 surface against the Python wrapper. The user-facing `FlaUI.Core` surface (elements,
patterns, conditions, input, tools, capturing, overlay, identifiers) is the actionable backlog;
UIA2/UIA3 framework-adapter internals are out of scope by design.

---

## Success metrics (v1.0 gate)

| Metric | Target | Current |
|--------|--------|---------|
| Test coverage | 95%+ | gate raised to 95% (verified on AppVeyor full UI matrix) |
| Docstring coverage (`interrogate`) | 95%+ | ~99% ✅ |
| Ruff lint | 0 errors | clean ✅ |
| Pattern parity | 34/34 | ✅ |
| Wrapper overhead vs FlaUI C# | < 5ms avg per call | −8 to +2ms across UIA2/UIA3 × WinForms/WPF ✅ |
| Compared with pywinauto | measured | median/p95 on the same apps; wrapper UIA descendant searches 1.4–5.7× faster than pywinauto `uia`, pywinauto `win32` fastest on WinForms ✅ |
| Wheel size | < 10MB | 0.39MB (386KB, DLLs included) ✅ |

**Absolute latency is reference-only, not a gate.** `scripts/benchmark.py` (GH-85) times each
operation through the wrapper and through the raw C# object it wraps. The wrapper adds nothing
measurable. The absolute numbers depend on Windows UIA and the app under test, so a Python wrapper
cannot gate them. Measured on Windows 11 (26200), Python 3.11, 100 iterations, wrapper mean in ms:

| Operation | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|-----------|---------------|----------|---------------|----------|
| Find descendant by automation id | 113 | 18 | 111 | 18 |
| Find descendant by name | 37 | 26 | 36 | 27 |
| Find all children | 16 | 4 | 16 | 3 |
| Read a property | 0.07 | 0.15 | 0.07 | 0.16 |
| Select radio button / toggle checkbox | 0.1 / 2.1 | 0.4 / 1.0 | 0.1 / 1.8 | 0.4 / 3.6 |
| Mouse click | 130 | 113 | 129 | 113 |

The original "< 100ms find" target is missed only by the WinForms descendant-by-id search, where FlaUI
C# alone takes 112–119ms. The original "< 50ms action" target is missed only by mouse clicks. Those
include FlaUI's built-in wait for input to be processed, and the same call through C# takes just as
long. Clicking one spot repeatedly is slower still (~525ms), because FlaUI waits out the system
double-click time. Re-measure with `uv run python scripts/benchmark.py`, which exits 1 on an overhead miss. User-facing
write-up: [docs/performance.md](docs/performance.md).

**Element name maps add no measurable latency.** `scripts/benchmark_name_map.py` times a lookup of
the Simple Controls `TextBox` four ways: a direct wrapper `find_first_descendant`, the test-suite map
(`tests/test_utilities/elements`), the documented `examples/pytest/app_map.py` recipe, and the
suite map's lookup chain written out without map classes. Results are means from 200 iterations,
in ms, with the Simple Controls tab already selected:

| | UIA2 WinForms | UIA2 WPF | UIA3 WinForms | UIA3 WPF |
|-|---------------|----------|---------------|----------|
| Direct wrapper find | 54 | 9.2 | 52 | 7.8 |
| Suite map vs direct | −12 | −0.4 | −9 | +0.0 |
| Docs map vs direct | −0.9 | +0.7 | −0.0 | +0.4 |
| Building one page class | 0.17 | 0.15 | 0.15 | 0.15 |

The suite map is *faster* on WinForms. It searches only the tab item's direct children, while the
direct call searches every descendant of the window. Building a page class costs about 0.15ms for the
suite's `BaseSettings` classes, which re-read environment variables, and under 0.01ms for the docs
recipe's `BaseModel`. Run-to-run noise is about ±5ms on WinForms. The one real cost is outside this
table: when the tab is not selected, the suite map selects it with `post_wait=True`, a deliberate
100ms+ wait.

**Compared with pywinauto.** `scripts/benchmark_pywinauto.py` (`uv run --group bench`, pywinauto in
the optional `bench` dependency group only) runs the same operations through pywinauto 0.6.9's `uia`
backend on both apps and its `win32` backend on WinForms, in the same process as the wrapper.
Median / p95 in ms over 100 runs:

| Operation | Wrapper UIA3 WinForms | pywinauto `uia` WinForms | pywinauto `win32` WinForms | Wrapper UIA3 WPF | pywinauto `uia` WPF |
|-----------|-----------------------|--------------------------|----------------------------|------------------|---------------------|
| Find descendant by automation id | 114 / 141 | 189 / 248 | n/a | 18 / 21 | 54 / 60 |
| Find descendant by name | 35 / 43 | 198 / 240 | 1.7 / 3.0 | 25 / 28 | 49 / 57 |
| Find all children | 16 / 18 | 23 / 45 | 0.23 / 0.31 | 3.3 / 3.9 | 4.8 / 6.4 |
| Select radio button | 0.09 / 0.12 | 2.6 / 4.9 | 0.06 / 0.11 | 0.36 / 0.47 | 3.4 / 4.5 |
| Toggle checkbox | 2.1 / 3.2 | 2.3 / 3.2 | 0.06 / 0.09 | 4.0 / 4.9 | 3.8 / 4.8 |
| Mouse click | 127 / 142 | 566 / 570 | 566 / 569 | 111 / 127 | 561 / 568 |

pywinauto's `win32` backend beats the wrapper wherever it applies (WinForms only, no AutomationId,
`BM_SETCHECK` instead of UIA patterns). On UIA the gap in searches is pywinauto's strategy (fetch every
descendant, filter in Python, insist on a unique match): the same `FindFirst` through its comtypes
object matches FlaUI. pywinauto's clicks wait out the double-click time since the last input on every
click, plus 90ms. Full tables and caveats: [docs/performance.md](docs/performance.md#compared-with-pywinauto).

---

*Living document — keep the status table and backlog in sync with the
[GitHub milestones](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestones) as work lands.*
