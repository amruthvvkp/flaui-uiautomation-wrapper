# FlaUI Python Wrapper Documentation Plan

## Overview
Comprehensive MkDocs documentation for FlaUI Python wrapper. Complete, polished, production-ready.

**Status**: ✅ Build successful, all sections implemented
**Build Command**: `uv run mkdocs build --strict`
**Serve Command**: `uv run mkdocs serve`
**Logs**: `%TEMP%\mkdocs-serve-new.log`

---

## Documentation Structure (9 Sections)

### 1. Home (index.md)
- **Content**: Hero section with centered logo, quick-start tabbed code, motivation, key features, bundled versions
- **Layout**: Feature cards with icons, centered design
- **Code Tabs**: Python (default) with bridge setup comment + C# equivalent
- **Includes**: Dynamic library versions table via `{% include "includes/flaui_versions.md" %}`
- **Links**: External links to FlaUI, RobotFlaUI, FlaUIInspect, Microsoft Accessibility Insights
- **No**: Permalink symbols (¶), MkDocs footer text, "Playwright" mentions

### 2. Motivation (motivation.md)
- **Purpose**: Comparison with alternatives (RobotFlaUI, FlaUI C#), advantages, unique features

### 3. Basics (basics.md)
- **9 Sections**: Initialize (with bridge warning box), Launch/Attach, Inspect, Find, Interact, Element Types, Post-wait, Retry, Next Steps
- **Audience**: End users learning the library
- **Code Format**: Tabbed Python/C# examples (Python first)
- **Content**: Simple, focused, no testing infrastructure details
- **External Tools**: Links to [FlaUIInspect](https://github.com/FlaUI/FlaUIInspect) and [Accessibility Insights](https://accessibilityinsights.io/)

### 4. Advanced (advanced.md)
- **Sections**:
  - Element methods by type (quick reference)
  - XPath reference (tabbed)
  - **ConditionFactory** (dedicated section with basic, combined, property-based conditions + best practices)
  - TreeWalker traversal
  - CacheRequest (performance)
  - Retry/polling
  - post_wait on input
  - Exception translation (@handle_csharp_exceptions)
  - Late imports (avoid circular deps)
  - Object mapping pattern (page objects)
  - Deeper inspection tools
  - PythonNet bridge flow (Mermaid diagram, horizontal layout)
  - When to use what (decision table)
- **Code Format**: Tabbed Python/C# where applicable
- **Audience**: Intermediate/advanced users and contributors

### 5. Concepts (concepts.md)
- **Content**: UIA2 vs UIA3, WinForms vs WPF, ControlType hierarchy (Mermaid), patterns, lifecycle/COM, limitations
- **Format**: Tables, hierarchies, decision guides

### 6. Troubleshooting (troubleshooting.md)
- **Content**: Common errors, bridge init, element-not-found debugging, timing, exceptions, Py3.8 compat, matrix skip/xfail conditions, DLL, Win11 behaviors, manual pytest failure tracking

### 7. Agentic Guidelines (agentic-guidelines.md)
- **Audience**: LLM/agentic systems using the library
- **Content**: System prompts, context snippets, do/don't list, documentation expectations, reference to CLAUDE.md/AGENTS.md

### 8. Contributing (contributing.md)
- **Sections**: Getting started, Adding elements, Tests (with matrix fixtures example), Code quality, Packaging, Documentation, Pull requests, Useful references
- **Matrix Fixtures**: Full example showing how tests run 4x (UIA2/UIA3 × WinForms/WPF)

### 9. Examples (examples/)
- **Pytest** (pytest.md): Minimal complete test example with fixtures and element maps
- **Unittest** (unittest.md): Basic setUp/tearDown pattern
- **Robot Framework** (robot-framework.md): Stub with "Coming Soon" admonition
- **Behave** (behave.md): Stub with "Coming Soon" admonition
- **TestPlan** (testplan.md): Stub with "Coming Soon" admonition

### 10. API Reference (api/)
- **Structure**:
  - `api/index.md` - Overview with categorized element lists (Interactive, Containers, Display, Complex), element-specific method counts
  - `api/automation.md`, `api/application.md`, `api/automation_element.md`, `api/condition_factory.md`
  - `api/mouse.md`, `api/keyboard.md`, `api/wait.md`
  - `api/retry.md`, `api/cache_request.md`, `api/drawing.md`, `api/collections.md`, `api/exceptions.md`
  - `api/elements/*.md` (30+ element pages: button, checkbox, combobox, datagridview, etc.)
- **Generation**: Auto-generated via mkdocstrings directives (`::: flaui.core.automation_elements.Button`)
- **Method Counts**: Show element-specific method counts (not inherited), full inheritance shown on API pages

---

## Theme & Styling

### Colors
- **Primary**: Deep Purple (#673AB7)
- **Accent**: Teal (#009688)
- **Modes**: Light (default) + Dark (slate)
- **Toggle**: Sun/Moon icons in header

### Features
- **Navigation**:
  - Horizontal tabs (navigation.tabs, navigation.tabs.sticky)
  - Instant loading (navigation.instant)
  - Tracking (navigation.tracking)
  - Indexes (navigation.indexes)
- **Content**:
  - Code copy button (content.code.copy)
  - Code annotation (content.code.annotate)
  - Tabbed blocks with link sharing (content.tabs.link)
- **Search**: Highlight + suggest
- **TOC**: Follow scrolling
- **Font**: Disabled (use system fonts)
- **Permalinks**: Disabled (no ¶ symbols)

### Custom CSS
- **File**: `docs/stylesheets/extra.css`
- **Features**:
  - Grid cards styling for feature boxes
  - Centered logo
  - Better code blocks
  - Hidden permalink symbols
  - Enhanced navigation tabs
  - Footer improvements

---

## Code Examples Standards

### Python/C# Tabs
- **Format**:
  ```markdown
  === "Python"
      ```python
      code_here()
      ```
  === "C#"
      ```csharp
      CodeHere();
      ```
  ```
- **Default**: Python first (user-facing lib is Python)
- **Bridge Setup**: Always comment with "Initialize Python ↔ .NET bridge" in Home page quick start
- **No "C# imports"**: Bridge setup is Python initialization, don't mention C# in docs

### Code Block Guidelines
- **Comments**: Inline comments explaining non-obvious code
- **Imports**: Show necessary imports for context
- **Python 3.8 Compat**: No `|` unions, no match/case in examples
- **External Projects**: Always include links to referenced tools/libraries

---

## External Project Links

When mentioning external projects, include links:

- **[FlaUI](https://github.com/FlaUI/FlaUI)** - Original C# library
- **[RobotFlaUI](https://github.com/GDATASoftwareAG/robotframework-flaui)** - Robot Framework bindings
- **[FlaUIInspect](https://github.com/FlaUI/FlaUIInspect)** - UI inspection tool
- **[Microsoft Accessibility Insights](https://accessibilityinsights.io/)** - Accessibility testing

---

## Content Guidelines

### Audience Clarity
- **Basics**: End users learning the library (no testing infrastructure)
- **Advanced**: Intermediate users and contributors (performance patterns, interop details)
- **Contributing**: Contributors adding elements/tests (matrix fixtures, C# mapping, code standards)
- **Examples**: Users writing tests with FlaUI (pytest, unittest, other frameworks)
- **Agentic**: LLM/agentic systems using the library (prompts, guardrails)

### Writing Style
- Clear, concise, action-oriented
- ❌ No "Playwright-style" mentions (internal reference only, removed from all pages)
- ✅ Focus on FlaUI capabilities, not framework comparisons
- ✅ Tabbed code showing Python/C# equivalence for understanding
- ✅ Best practices and decision guidance ("When to use what")

### Naming Conventions
- **Python code**: snake_case for methods/properties, PascalCase for classes
- **C# code**: Standard C# conventions (PascalCase for everything)
- **Section headers**: Title case, numbered (1) through (9) for sequential steps

### Admonitions
- **warning**: Bridge setup, critical initialization steps
- **Coming Soon**: Framework stubs (Robot Framework, Behave, TestPlan)
- Other types as needed for notes, tips, etc.

---

## File Organization

```
docs/
├── index.md                          # Home page
├── motivation.md                     # Why this library
├── basics.md                         # 9-step quick start
├── advanced.md                       # Deep dive (XPath, CF, TreeWalker, etc.)
├── concepts.md                       # UIA2/UIA3, WinForms/WPF, patterns
├── troubleshooting.md                # Common issues & fixes
├── agentic-guidelines.md             # LLM/agentic guidance
├── contributing.md                   # Contribution guidelines
├── logo.png                          # Brand logo
├── stylesheets/
│   └── extra.css                     # Custom styling
├── includes/
│   └── flaui_versions.md             # Auto-generated version table
├── examples/
│   ├── pytest.md
│   ├── unittest.md
│   ├── robot-framework.md
│   ├── behave.md
│   └── testplan.md
└── api/
    ├── index.md                      # API overview
    ├── automation.md
    ├── application.md
    ├── automation_element.md
    ├── condition_factory.md
    ├── mouse.md
    ├── keyboard.md
    ├── wait.md
    ├── retry.md
    ├── cache_request.md
    ├── drawing.md
    ├── collections.md
    ├── exceptions.md
    └── elements/
        ├── button.md
        ├── checkbox.md
        ├── combobox.md
        ├── datagridview.md
        ├── datetimepicker.md
        ├── grid.md
        ├── label.md
        ├── listbox.md
        ├── listbox_item.md
        ├── menu.md
        ├── menu_item.md
        ├── progressbar.md
        ├── radiobutton.md
        ├── slider.md
        ├── spinner.md
        ├── tab.md
        ├── tab_item.md
        ├── textbox.md
        ├── thumb.md
        ├── titlebar.md
        ├── togglebutton.md
        ├── tree.md
        ├── tree_item.md
        └── window.md
```

---

## MkDocs Configuration

### Key Settings (mkdocs.yml)
- **Site name**: FlaUI Python Wrapper
- **Theme**: material
- **Logo**: logo.png (in docs root, not docs/docs/logo.png)
- **Palette**: Light + Dark with toggle
- **Font**: false (system fonts)
- **Features**: Navigation tabs, instant, tracking, code copy, search, toc follow
- **Plugins**: search, awesome-pages, mermaid2, mkdocstrings (Python handler, Sphinx style), minify, redirects
- **Markdown extensions**: admonition, toc (no permalink), tabbed, superfences, details, snippets, highlight, inlinehilite, emoji
- **Search boost**: api=2.0, examples=1.5, agentic=1.3, contributing=1.2
- **Version management**: mike provider, latest default, alias enabled
- **Footer**: `generator: false` (no "made with MkDocs" text)
- **Extra CSS**: stylesheets/extra.css

### Navigation (mkdocs.yml)
- 9 main sections + API Reference subsections
- Horizontal tabs enabled
- Awesome Pages plugin for organization

---

## Version Management

### Dynamic Version Table
- **Source**: `flaui/bin/Version.md`
- **Generated**: `docs/includes/flaui_versions.md`
- **Script**: `scripts/extract_versions.py` (wired as mkdocs hook)
- **Usage in docs**: `{% include "includes/flaui_versions.md" %}`
- **Content**: Core/UIA2/UIA3 versions, frameworks, dependencies, licenses

### Build & Deploy
- **Build**: `uv run mkdocs build --strict`
- **Serve**: `uv run mkdocs serve`
- **GitHub Actions**: `.github/workflows/docs.yml` for releases + dev deployment via mike
- **Strategy**: Releases get version tag, master branch deployed as "dev"

---

## Build Requirements

### Dependencies (pyproject.toml)
```toml
[dependency-groups]
docs = [
    "mkdocs>=1.6.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=1.0.2",
    "mkdocstrings-python>=2.0.1",
    "mkdocs-awesome-pages-plugin>=2.10.1",
    "mkdocs-mermaid2-plugin>=1.2.3",
    "pymdown-extensions>=10.20.0",
    "mike>=2.1.3",
    "pyyaml",
    "jinja2",
]
```

### Commands
- **Install**: `uv sync --group docs`
- **Build**: `uv run mkdocs build --strict`
- **Serve**: `uv run mkdocs serve`
- **Version bump**: `uv version <version>` (before commit)

---

## Docstring Standards

### Style
- **Format**: Sphinx-style (`:param name:`, `:return:`, `:raises:`)
- **Coverage**: 95%+ (check with `interrogate`)
- **Python 3.8 Compat**: No modern type union syntax in examples

### Common Mistakes (Fixed)
- ❌ `:param:` (missing name) → ✅ `:param name:` (with name)
- ❌ Parameter name mismatch → ✅ Match actual function signature
- ❌ Missing return type annotation → ✅ Add `:return:` description

---

## Known Decisions & Rationales

1. **Matrix fixtures moved to Contributing**: Not appropriate for Basics (end-user focused)
2. **Table element removed**: Class doesn't exist in flaui.core.automation_elements
3. **Old usage_*.md deleted**: Content merged into Basics/Advanced, files cleaned up
4. **Logo in docs root**: `docs/logo.png` (not `docs/docs/logo.png`)
5. **Jinja2 includes**: `{% include %}` instead of `--8<--` snippets (mkdocs standard)
6. **No permalinks**: Cleaner docs without ¶ symbols
7. **ConditionFactory dedicated section**: Complex enough to warrant full section in Advanced
8. **Mermaid diagram**: Horizontal layout (LR), quoted node labels for special chars
9. **Feature cards**: Grid-based cards for visual interest on home page
10. **Light/Dark mode**: Toggle in header for accessibility

---

## Resuming Documentation Work

### Checklist Before Starting
- [ ] Read this DOC_PLAN.md for standards
- [ ] Review relevant section above for content guidelines
- [ ] Check mkdocs.yml for current config (nav structure, plugins)
- [ ] Verify build: `uv run mkdocs build --strict` (exit code 0)
- [ ] Start serve: `uv run mkdocs serve` (logs to `%TEMP%\mkdocs-serve-new.log`)

### Common Tasks

#### Adding a new page
1. Create `docs/section_name.md` following structure in this plan
2. Use Python/C# tabbed code if showing equivalent code
3. Add to `nav:` in mkdocs.yml
4. Tabbed format: `=== "Python"` + `=== "C#"`
5. Test build: `uv run mkdocs build --strict`

#### Updating existing content
1. Edit `.md` file in `docs/`
2. Ensure docstring standards (Sphinx style, 95% coverage)
3. Remove "Playwright" mentions
4. Add external links where applicable
5. Test build after changes

#### Adding a new element to API
1. Create `docs/api/elements/element_name.md`
2. Add to mkdocs.yml nav under Elements
3. Use mkdocstrings directive: `::: flaui.core.automation_elements.ElementName`
4. Update `docs/api/index.md` with element-specific method count

#### Fixing broken builds
1. Check logs: `Get-Content "$env:TEMP\mkdocs-serve-new.log"`
2. Look for: docstring format issues, missing files, broken includes, invalid YAML
3. Common fixes:
   - Docstring param names must match function signature
   - File paths in includes must use Jinja2: `{% include "path" %}`
   - YAML indentation (2 spaces, not tabs)
   - mkdocstrings classes must actually exist in source code

---

## Next Actions (Future Sessions)

- [ ] Consider adding interactive examples (if needed)
- [ ] Track docstring coverage: `interrogate --generate-badge`
- [ ] Monitor GitHub Actions for doc deployment
- [ ] Update version table when flaui/bin/Version.md changes
- [ ] Expand Concepts section with more patterns
- [ ] Add framework-specific stubs completion status

---

**Last Updated**: January 25, 2026
**Build Status**: ✅ All checks passing
**Next Steps**: Ready for publication via GitHub Actions or manual deployment
