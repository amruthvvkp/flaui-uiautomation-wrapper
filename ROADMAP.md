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
| 0 | [Stabilize](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/7) | ⏳ Pending | 10 / 1 |
| 1 | [Exceptions & Identifiers](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/8) | 🟡 Almost done | 1 / 5 |
| 2 | [Patterns](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/9) | ✅ Done | 0 / 5 |
| 3 | [Elements & ScrollBars](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/10) | ✅ Done | 0 / 2 |
| 4 | [Events](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/11) | ✅ Done | 0 / 2 |
| 5 | [Capturing / Overlay / Video](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/12) | ⏳ Pending | 2 / 0 |
| 6 | [Logging / Tools / Enhancers](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/13) | 🟡 In progress | 3 / 1 |
| 7 | [Docs & Zensical](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/14) | ⏳ Pending | 5 / 0 |
| 8 | [Polish & v1.0](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/15) | ⏳ Pending | 5 / 0 |

**Legend:** ✅ done · 🟡 in progress · ⏳ not started

---

## ✅ Completed

### Foundation (closed: *Create initial usable release v1.0.0*)
- Migrated Poetry → **UV** package manager; FlaUI 4 + PythonNet 3 prototype.
- **PythonNet bridge** for C# interop with strict init ordering.
- **Pydantic** validation across all models (type safety + IDE intellisense).
- pytest matrix framework (UIA2/UIA3 × WinForms/WPF), object mapping, pytest-bug tracking.
- Python 3.10+ support, packaging/issue/PR templates.

### Phase 1 — Exceptions & Identifiers *(5 of 6 closed)*
- **#102** Complete exception hierarchy · **#98** Identifier system (EventId/PatternId/PropertyId/
  TextAttributeId) · **#105 / #104** XPath navigation support.

### Phase 2 — Patterns *(complete)*
- **#91** All **34 UI Automation patterns** implemented (full parity with FlaUI's `IFrameworkPatterns`).
- **#117** pattern surface · **PR #122** real WinForms/WPF UI integration tests across the matrix.

### Phase 3 — Elements & ScrollBars *(complete)*
- **#99** `ScrollBarBase` / `HorizontalScrollBar` / `VerticalScrollBar` + converters (**PR #123**).

### Phase 4 — Events *(complete)*
- **#94** Event handler system · **#77** `RegisterAutomationEvent` ported with GC keep-alive (**PR #123**).

### Phase 6 — Tools *(partial)*
- **#100** Tools/utilities: `ItemRealizer`, `AccessibilityTextResolver`, `WindowsStoreAppLauncher`,
  `LocalizedStrings`, `SystemInfo` (**PR #123**).

### Infrastructure
- **#107** Python `AutomationBase` + UIA2/UIA3 facades · **#118** CI migrated to Azure Pipelines
  (+ AppVeyor UI gate) · **#51** MkDocs/Zensical docs base.

---

## ⏳ Pending — prioritized backlog

Priority order: **P1 → P6**. Per direction, the next focus is **Phase 1 → 5 → 6**, and all feature
areas (capturing, overlay, video, logging) are **in scope for v1.0**.

### P1 — Finish Phase 1
- **[#73](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/73)** — `translate_exceptions`
  Pythonic exception-translation wrapper over the hierarchy built in #102. *Small; closes the milestone.*

### P2 — Phase 5: Capturing / Overlay / Video *(new modules)*
- **[#95](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/95)** — Screen capturing &
  video: `flaui/core/capturing/` wrapping `Capture` / `CaptureImage` / `VideoRecorder` (wire the
  existing `VideoRecordingMode` enum; video needs ffmpeg).
- **[#103](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/103)** — Overlay system:
  `flaui/core/overlay/` wrapping `IOverlayManager` / `WinFormsOverlayManager` for visual debugging.

### P3 — Phase 6: Logging / Enhancers
- **[#96](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/96)** — Logging infrastructure:
  - **Drop Loguru**, standardize on stdlib `logging`.
  - **C#→Python sink:** a Python `ILogger` implementation assigned to FlaUI's `Logger.Default` so C#
    log output flows into Python `logging` — unified telemetry in one destination.
  - **Opt-in** via a `Settings` flag / env var (`FLAUI_LOG_CSHARP`); off by default.
- **[#68](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/68)** — Mouse busy-spinner /
  loading-state waiting helper (align with `Wait` / `post_wait`).
- **[#87](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/87)** — Enhanced Python
  integration (umbrella): context managers, iterators, `__repr__`/`__str__`, fluent waits. *Triage;
  not all required for v1.0.*

### P4 — Phase 0: Stabilize *(pre-release gate)*
- **[#88](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/88)** — `flaui.core` test
  coverage umbrella.
- Bug fixes: **#74 #75 #76 #78 #79 #80 #82 #83 #89** (see table below). Several are upstream
  Windows/.NET issues — fix where feasible, otherwise document as known xfail/skip.

### P5 — Phase 7: Docs & Zensical
- **[#86](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/86)** comprehensive docs
  (umbrella) · **[#69](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/69)** example
  gallery · sample suites: **[#48](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/48)**
  Behave · **[#49](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/49)** TestPlan ·
  **[#50](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/50)** PyTest.

### P6 — Phase 8: Polish & release
- **[#85](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/85)** polish & production
  readiness · release automation
  **[#57](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/57)** /
  **[#65](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/65)** /
  **[#66](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/66)** · then
  **[#84](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/84) v1.0.0 release**.

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

| Package / effort | What it is | Inspiration |
|------------------|------------|-------------|
| **FlaUI agent skills** | Claude Code skills bundle for FlaUI development | — |
| **`flaui-recorder`** | Record-and-generate UI script tool | [twenzel/FlaUIRecorder](https://github.com/twenzel/FlaUIRecorder), Playwright codegen |
| **`flaui-mcp`** | MCP server exposing FlaUI automation as tools | [shanselman/FlaUI-MCP](https://github.com/shanselman/FlaUI-MCP) |
| **`pytest-flaui`** | pytest plugin: fixtures + recorder + capture-on-failure | [`pytest-playwright`](https://github.com/microsoft/playwright-pytest) |

### FlaUI agent skills
A bundle of Claude Code skills (`.claude/skills/…`) packaging FlaUI development knowledge so users
building automation get assisted workflows: element/pattern lookup, test scaffolding, and C#→Python
test-porting helpers. Distributable as an installable skills bundle.

### `flaui-recorder`
A Playwright-codegen-style **record-and-generate** tool: watch a user's interactions against a live
Windows app (via UIA events / hit-testing) and emit ready-to-run Python FlaUI scripts. Lowers the
barrier to authoring automation by hand. Builds on this wrapper's event handlers and XPath navigator;
inspired by the C# [twenzel/FlaUIRecorder](https://github.com/twenzel/FlaUIRecorder).

### `flaui-mcp`
An **MCP server** exposing FlaUI Python automation as callable tools so agents/LLMs can drive Windows
desktop apps — the Python counterpart to the C#
[shanselman/FlaUI-MCP](https://github.com/shanselman/FlaUI-MCP).

### `pytest-flaui`
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

## Success metrics (v1.0 gate)

| Metric | Target | Current |
|--------|--------|---------|
| Test coverage | 95%+ | ~85% |
| Docstring coverage (`interrogate`) | 95%+ | ~99% ✅ |
| Ruff lint | 0 errors | clean ✅ |
| Pattern parity | 34/34 | ✅ |
| Element finding | < 100ms avg | — |
| Action execution | < 50ms avg | — |
| Wheel size | < 10MB | — |

---

*Living document — keep the status table and backlog in sync with the
[GitHub milestones](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestones) as work lands.*
