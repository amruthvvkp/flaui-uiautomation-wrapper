# Roadmap

A living view of where **FlaUI for Python** is, what is shipped, what is in flight, and what is
parked for after v1.0. It mirrors the
[GitHub milestones](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestones) and
[issues](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues) — those remain the source
of truth; this page is the human-friendly summary.

!!! tip "How to read this"
    - ✅ Done &nbsp; 🚧 In progress &nbsp; 🗓️ Planned &nbsp; 💡 Wishlist (post‑v1)
    - Each item links to its tracking issue or milestone where one exists.

## Status at a glance

| Milestone | Theme | Status |
|-----------|-------|--------|
| [Initial release](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/1) | FlaUI 4 + PythonNet 3 prototype, packaging, PyPI plumbing | ✅ Complete |
| [Phase 1 — Exceptions & Identifiers](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/8) | Pythonic exceptions, identifier system | ✅ Complete |
| [Phase 2 — Patterns](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/9) | 35+ UIA control patterns | ✅ Complete |
| [Phase 3 — Elements & ScrollBars](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/10) | Element wrappers, scrollbars | ✅ Complete |
| [Phase 4 — Events](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/11) | Event handler system, automation events | ✅ Complete |
| [Phase 5 — Capturing/Overlay/Video](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/12) | Screenshots, overlays, video recording | ✅ Complete |
| [Phase 6 — Logging/Tools/Enhancers](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/13) | Logging bridge, tools, Pythonic enhancers | ✅ Complete |
| [Phase 0 — Stabilize](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/7) | Green CI, stable matrix, 100% core coverage | 🚧 In progress |
| [Phase 7 — Docs & Zensical](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/14) | v1 docs, per-framework guides, API reference | 🗓️ Planned |
| [Phase 8 — Polish & v1.0](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/15) | Release plumbing, beta soak, v1.0.0 | 🗓️ Planned |

## ✅ Completed

### Foundation & packaging
- [x] PythonNet bridge and bundled FlaUI DLLs
- [x] Upgrade to FlaUI 4/5 + PythonNet 3
- [x] Pydantic-backed `AutomationElement` models
- [x] `uv`-based packaging and PyPI publishing plumbing
- [x] Python 3.10–3.14 support
- [x] [Python `AutomationBase` + UIA2/UIA3 facades (#107)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/107)

### Core API surface (1:1 with FlaUI)
- [x] [Complete exception hierarchy + `translate_exceptions` (#102, #73)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/102)
- [x] [Identifier system (#98)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/98)
- [x] [35+ UI Automation patterns (#91)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/91)
- [x] [ScrollBar elements (#99)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/99)
- [x] [XPath navigation (#105)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/105)
- [x] [Event handler system + `RegisterAutomationEvent` (#94, #77)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/94)
- [x] [Screen capturing & video recording (#95)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/95)
- [x] [Overlay management (#103)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/103)
- [x] [Logging infrastructure (C#→Python bridge) (#96)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/96)
- [x] [Tools & utilities incl. `Retry` and cursor-busy waiting (#100, #68)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/100)

### CI & docs platform
- [x] [Migrate Windows UI CI from AppVeyor to a hybrid Azure Pipelines + AppVeyor setup (#118)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/118)
- [x] Zensical documentation site with auto-generated API reference (mkdocstrings)

### Phase 6 — Enhanced Python integration ([#87](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/87))
- [x] `__repr__` on elements
- [x] Context-manager support for `Application` / `Automation` (`with` auto-dispose)
- [x] Iterator/collection protocol on element results (`AutomationElementCollection` with `.first`, `.filter`, `.where`, indexing/iteration)
- [x] Fluent waiting + Playwright-style assertions (`expect(el).to_be_visible()`, `flaui/core/expectations.py`)
- [x] `py.typed` marker + `ty` (Astral) type-check gate in CI

## 🚧 In progress

### Phase 0 — Stabilize ([milestone](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/7))
- [ ] [Achieve ~90–95% `flaui.core` coverage + enforce a coverage gate (#88)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/88)
- [ ] [Spinner AutomationID flakiness (#74)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74) — harden locator
- [ ] [Tree-item flakiness on CI (#76)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/76) — wait for items to materialize
- [ ] [`test_get_control_type` setup flakiness (#82)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/82) — harden fixture
- [ ] [`find_all/first_with_options` matrix failures (#80)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/80) — investigate `TreeTraversalOptions`
- [ ] [`ListBox.select_by_index` on UIA3/WPF (#83)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/83) — fix selection
- [ ] [Notepad tests on Windows 11 Store app (#89)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/89) — environment guard
- [ ] Document upstream Windows/.NET limitations — [ComboBox/WinForms (#75)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/75), [Toggle on WinForms menus (#78)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/78), [UIA3 WinForms context menus (#79)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/79)

## 🗓️ Planned

### Phase 7 — Docs & Zensical ([milestone](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/14))
- [ ] [Comprehensive production docs (#86)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/86)
- [ ] [Worked testing examples (#69)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/69)
- [ ] [pytest sample suites (#50)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/50)
- [ ] [TestPlan sample suites (#49)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/49)
- [ ] [Behave sample suites (#48)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/48)

### Phase 8 — Polish & v1.0 ([milestone](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/milestone/15))
- [ ] [v1.0.0 official release (#84)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/84)
- [ ] [Final polish & production readiness (#85)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/85)
- [ ] [release-drafter on PR merge (#65)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/65)
- [ ] [Publish workflow: PR-on-release → master (#57)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/57)
- [ ] [Link PyPI version in release notes (#66)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/66)

## 💡 Wishlist (post‑v1)
- [ ] [`CustomNavigation` pattern (#121)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/121)
- [ ] UI recorder / codegen (inspired by FlaUIRecorder & Playwright codegen)
- [ ] Reference MCP server / agent-tool example exposing element find/click/type as tools (see [Use with AI agents](agentic-guidelines.md#use-with-ai-agents-and-mcp))
- [ ] Async / `pytest-asyncio` ergonomics evaluation
- [ ] Enhanced HTML/Allure reporting helpers

---

*Maintainers: keep this page aligned with milestones as phases close. It is linked from the site
nav and is intended as the at-a-glance overview of overall scale.*
