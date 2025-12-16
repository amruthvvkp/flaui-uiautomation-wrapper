# FlaUI Python Wrapper - Roadmap to v1.0.0

**Project Goal**: Create a production-ready Python wrapper for FlaUI that is as flexible, polished, and intuitive as Playwright or Selenium, with comprehensive documentation for beginners to advanced users.

**Reference Issue**: [#46 - Basic Unit Tests](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/46)

---

## Project History & Context

### Completed Milestones ✅
- [x] Migrated from Poetry to UV package manager
- [x] Established pytest-based test framework with matrix parametrization
- [x] Implemented fixture setup for UIA2/UIA3 × WinForms/WPF combinations
- [x] Created comprehensive object mapping system
- [x] Ported core FlaUI.Core automation elements (Button, CheckBox, ComboBox, etc.)
- [x] Implemented PythonNet bridge for C# interop
- [x] Added Pydantic validation for type safety and IDE intellisense
- [x] Set up pytest-bug integration for issue tracking
- [x] Established CI/CD pipeline with AppVeyor

### Challenges Overcome
- Complex fixture setup for multi-platform testing
- Matrix combination handling (UIA2/UIA3 × WinForms/WPF)
- C# to Python type conversion
- Maintaining 1:1 API parity with FlaUI C#
- PythonNet initialization ordering
- Flaky test management and bug tracking

---

## Phase 1: Complete flaui.core Testing 🎯
**Target**: 100% test coverage for flaui.core module

### 1.1 Core Automation Elements Testing
**Priority**: HIGH | **Estimated Effort**: 2-3 weeks

- [ ] **Audit existing test coverage**
  - [ ] Run coverage report: `uv run coverage html`
  - [ ] Identify untested classes in `flaui/core/automation_elements.py`
  - [ ] Document missing test cases per element

- [ ] **Add missing element tests**
  - [ ] `VerticalScrollBar` and `HorizontalScrollBar` tests
  - [ ] `ToolTip` element tests
  - [ ] `StatusBar` element tests
  - [ ] `SplitButton` tests
  - [ ] `HyperlinkControl` tests
  - [ ] `Document` and `Pane` tests
  - [ ] `Image` element tests
  - [ ] `SemanticZoom` tests (if applicable)

- [ ] **Pattern Coverage**
  - [ ] `DockPattern` tests
  - [ ] `DragPattern` tests
  - [ ] `DropTargetPattern` tests
  - [ ] `ItemContainerPattern` tests
  - [ ] `LegacyIAccessiblePattern` tests
  - [ ] `MultipleViewPattern` tests
  - [ ] `ObjectModelPattern` tests
  - [ ] `RangeValuePattern` tests (expand coverage)
  - [ ] `ScrollItemPattern` tests
  - [ ] `ScrollPattern` tests (expand coverage)
  - [ ] `SelectionPattern` tests (expand coverage)
  - [ ] `SelectionItemPattern` tests (expand coverage)
  - [ ] `SpreadsheetPattern` tests
  - [ ] `SpreadsheetItemPattern` tests
  - [ ] `StylesPattern` tests
  - [ ] `SynchronizedInputPattern` tests
  - [ ] `TablePattern` tests (expand coverage)
  - [ ] `TableItemPattern` tests
  - [ ] `TextPattern` tests (expand coverage)
  - [ ] `TextPattern2` tests
  - [ ] `TransformPattern` tests
  - [ ] `TransformPattern2` tests
  - [ ] `ValuePattern` tests (expand coverage)
  - [ ] `VirtualizedItemPattern` tests
  - [ ] `WindowPattern` tests (expand coverage)

### 1.2 Core Infrastructure Testing
**Priority**: MEDIUM | **Estimated Effort**: 1-2 weeks

- [ ] **Condition Factory**
  - [ ] Test all condition types (And, Or, Not, Property)
  - [ ] Test complex condition combinations
  - [ ] Test XPath condition building

- [ ] **TreeWalker**
  - [ ] Test tree traversal methods
  - [ ] Test TreeScope options
  - [ ] Test TreeTraversalOptions

- [ ] **CacheRequest**
  - [ ] Test property caching
  - [ ] Test pattern caching
  - [ ] Test cache activation/deactivation

- [ ] **Event Handling**
  - [ ] Port `RegisterAutomationEvent` (currently TODO - GH-77)
  - [ ] Test automation event registration
  - [ ] Test structure changed events
  - [ ] Test property changed events
  - [ ] Test focus changed events

### 1.3 System.Drawing Wrappers
**Priority**: MEDIUM | **Estimated Effort**: 1 week

- [ ] **Expand coverage for**
  - [ ] `Point` class edge cases
  - [ ] `Rectangle` class operations (union, intersection, contains)
  - [ ] `Color` class conversions (RGB, hex, named colors)
  - [ ] `Size` class operations

---

## Phase 2: flaui.uia2 Module Implementation 🔧
**Target**: Complete UIA2 provider support with tests

### 2.1 UIA2 Core Implementation
**Priority**: HIGH | **Estimated Effort**: 3-4 weeks

- [ ] **Port C# UIA2 Classes**
  - [ ] Review `FlaUI/src/FlaUI.UIA2/UIA2Automation.cs`
  - [ ] Port `UIA2Automation` class to `flaui/modules/uia2/`
  - [ ] Port `UIA2PropertyLibrary`
  - [ ] Port `UIA2EventLibrary`
  - [ ] Port `UIA2PatternLibrary`
  - [ ] Port `UIA2TextAttributeLibrary`
  - [ ] Port `UIA2TreeWalkerFactory`

- [ ] **UIA2-Specific Elements**
  - [ ] Port any UIA2-specific element wrappers
  - [ ] Implement UIA2 COM interop wrappers
  - [ ] Add UIA2 condition factory specializations

- [ ] **Type Converters**
  - [ ] Port UIA2 `AutomationElementConverter`
  - [ ] Port UIA2 `ValueConverter`
  - [ ] Test all type conversions

### 2.2 UIA2 Testing
**Priority**: HIGH | **Estimated Effort**: 2-3 weeks

- [ ] **Unit Tests**
  - [ ] Test UIA2 automation initialization
  - [ ] Test UIA2 property library
  - [ ] Test UIA2 event library
  - [ ] Test UIA2 pattern library
  - [ ] Test UIA2 tree walker

- [ ] **Integration Tests**
  - [ ] Verify UIA2 works with existing test applications
  - [ ] Test UIA2-specific behavior differences from UIA3
  - [ ] Test UIA2 performance characteristics

---

## Phase 3: flaui.uia3 Module Implementation 🚀
**Target**: Complete UIA3 provider support with tests

### 3.1 UIA3 Core Implementation
**Priority**: HIGH | **Estimated Effort**: 3-4 weeks

- [ ] **Port C# UIA3 Classes**
  - [ ] Review `FlaUI/src/FlaUI.UIA3/UIA3Automation.cs`
  - [ ] Port `UIA3Automation` class to `flaui/modules/uia3/`
  - [ ] Port `UIA3PropertyLibrary`
  - [ ] Port `UIA3EventLibrary`
  - [ ] Port `UIA3PatternLibrary`
  - [ ] Port `UIA3TextAttributeLibrary`
  - [ ] Port `UIA3TreeWalkerFactory`

- [ ] **UIA3-Specific Elements**
  - [ ] Port any UIA3-specific element wrappers
  - [ ] Implement UIA3 COM interop wrappers
  - [ ] Add UIA3 condition factory specializations
  - [ ] Port UIA3-specific patterns (Annotation, etc.)

- [ ] **Type Converters**
  - [ ] Port UIA3 `AutomationElementConverter`
  - [ ] Port UIA3 `ValueConverter`
  - [ ] Test all type conversions

### 3.2 UIA3 Testing
**Priority**: HIGH | **Estimated Effort**: 2-3 weeks

- [ ] **Unit Tests**
  - [ ] Test UIA3 automation initialization
  - [ ] Test UIA3 property library
  - [ ] Test UIA3 event library
  - [ ] Test UIA3 pattern library
  - [ ] Test UIA3 tree walker

- [ ] **Integration Tests**
  - [ ] Verify UIA3 works with existing test applications
  - [ ] Test UIA3-specific behavior differences from UIA2
  - [ ] Test UIA3 performance characteristics
  - [ ] Test newer Windows 10/11 specific features

---

## Phase 4: Enhanced Python Integration 🐍
**Target**: Make the library Pythonic and intuitive

### 4.1 Python Native Alternatives
**Priority**: MEDIUM | **Estimated Effort**: 2-3 weeks

- [ ] **Evaluate Python Libraries**
  - [ ] Compare `typing` vs Pydantic for type hints
  - [ ] Evaluate `pathlib` for file path handling
  - [ ] Consider `dataclasses` for simple data structures
  - [ ] Evaluate `attrs` as Pydantic alternative
  - [ ] Review `pytest-asyncio` for async test support

- [ ] **Implement Pythonic Wrappers**
  - [ ] Add context manager support (`with automation.launch_app() as app:`)
  - [ ] Add iterator protocols for element collections
  - [ ] Add `__repr__` and `__str__` for debugging
  - [ ] Add property decorators for cleaner syntax
  - [ ] Implement Python-native retry mechanisms

### 4.2 Developer Experience Improvements
**Priority**: MEDIUM | **Estimated Effort**: 2 weeks

- [ ] **Type Hints**
  - [ ] Audit all type hints for completeness
  - [ ] Add type stubs (`.pyi` files) where needed
  - [ ] Test with `mypy` static type checker
  - [ ] Test with `pyright` (VS Code default)

- [ ] **Error Messages**
  - [ ] Improve exception messages with actionable guidance
  - [ ] Add element locator suggestions on ElementNotFound
  - [ ] Add timeout context to error messages
  - [ ] Create exception hierarchy documentation

- [ ] **Logging**
  - [ ] Add debug logging for element searches
  - [ ] Add performance logging for slow operations
  - [ ] Create logging configuration guide
  - [ ] Add log filtering for C# interop noise

### 4.3 Playwright/Selenium Parity Features
**Priority**: HIGH | **Estimated Effort**: 3-4 weeks

- [ ] **Locator Strategies**
  - [ ] Enhance CSS selector support (if feasible)
  - [ ] Add fluent waiting API (`.wait_for_element()`)
  - [ ] Add assertion helpers (`.expect(element).to_be_visible()`)
  - [ ] Add screenshot capabilities per element

- [ ] **Session Management**
  - [ ] Add application lifecycle helpers
  - [ ] Add automatic cleanup on errors
  - [ ] Add session recording/replay (for debugging)
  - [ ] Add parallel test execution support

- [ ] **Reporting**
  - [ ] Add Allure report integration (already has pytest-allure)
  - [ ] Add HTML report generation
  - [ ] Add execution trace/timeline
  - [ ] Add screenshot attachments to reports

---

## Phase 5: Comprehensive Documentation 📚
**Target**: Production-ready documentation with mkdocs

### 5.1 Documentation Infrastructure
**Priority**: HIGH | **Estimated Effort**: 1 week

- [ ] **Setup mkdocs**
  - [ ] Install mkdocs and mkdocs-material theme
  - [ ] Configure `mkdocs.yml`
  - [ ] Set up auto-deployment (GitHub Pages or ReadTheDocs)
  - [ ] Add search functionality
  - [ ] Configure code highlighting

- [ ] **Documentation Structure**
  ```
  docs/
  ├── index.md                    # Landing page
  ├── getting-started/
  │   ├── installation.md
  │   ├── quickstart.md
  │   └── first-automation.md
  ├── user-guide/
  │   ├── automation-basics.md
  │   ├── element-finding.md
  │   ├── interactions.md
  │   ├── patterns.md
  │   └── advanced-techniques.md
  ├── api-reference/
  │   ├── automation.md
  │   ├── elements.md
  │   ├── patterns.md
  │   └── conditions.md
  ├── examples/
  │   ├── calculator-automation.md
  │   ├── notepad-automation.md
  │   ├── web-browser-automation.md
  │   └── custom-app-automation.md
  ├── testing/
  │   ├── pytest-integration.md
  │   ├── fixtures.md
  │   └── best-practices.md
  ├── troubleshooting/
  │   ├── common-issues.md
  │   ├── debugging.md
  │   └── faq.md
  └── contributing.md
  ```

### 5.2 Beginner Documentation
**Priority**: HIGH | **Estimated Effort**: 2-3 weeks

- [ ] **Getting Started**
  - [ ] Installation guide (Windows versions, Python versions)
  - [ ] Dependencies explanation (PythonNet, FlaUI DLLs)
  - [ ] Quick start tutorial (5-minute automation)
  - [ ] First automation script walkthrough
  - [ ] Common pitfalls for beginners

- [ ] **Core Concepts**
  - [ ] UI Automation overview (UIA2 vs UIA3)
  - [ ] Automation tree structure
  - [ ] Element identification strategies
  - [ ] Control types and patterns
  - [ ] Basic interactions (click, type, select)

- [ ] **Example Gallery**
  - [ ] Automating Calculator
  - [ ] Automating Notepad
  - [ ] Automating Windows Settings
  - [ ] Automating custom WinForms app
  - [ ] Automating custom WPF app

### 5.3 Intermediate Documentation
**Priority**: MEDIUM | **Estimated Effort**: 2-3 weeks

- [ ] **Element Finding**
  - [ ] Condition factory deep dive
  - [ ] XPath vs property conditions
  - [ ] Caching strategies
  - [ ] Performance optimization
  - [ ] Handling dynamic UIs

- [ ] **Patterns Guide**
  - [ ] Pattern availability by control type
  - [ ] When to use which pattern
  - [ ] Pattern-specific examples for each type
  - [ ] Pattern fallbacks and alternatives

- [ ] **Testing Integration**
  - [ ] Pytest setup and configuration
  - [ ] Fixture design patterns
  - [ ] Matrix testing explained
  - [ ] Handling flaky tests
  - [ ] CI/CD integration (AppVeyor, GitHub Actions)

### 5.4 Advanced Documentation
**Priority**: MEDIUM | **Estimated Effort**: 2-3 weeks

- [ ] **Architecture**
  - [ ] PythonNet bridge internals
  - [ ] C# to Python mapping patterns
  - [ ] Pydantic validation architecture
  - [ ] Exception handling strategy
  - [ ] Type conversion system

- [ ] **Performance**
  - [ ] Benchmarking automation scripts
  - [ ] Optimizing element searches
  - [ ] Caching best practices
  - [ ] Parallel execution strategies
  - [ ] Memory management

- [ ] **Extending the Library**
  - [ ] Creating custom elements
  - [ ] Adding new patterns
  - [ ] Contributing to the project
  - [ ] Testing new features
  - [ ] Maintaining C# parity

### 5.5 API Reference
**Priority**: HIGH | **Estimated Effort**: 2 weeks

- [ ] **Auto-generated API docs**
  - [ ] Setup mkdocstrings
  - [ ] Generate module documentation
  - [ ] Add code examples to docstrings
  - [ ] Cross-reference related APIs
  - [ ] Add type hint visualization

- [ ] **Manual API Pages**
  - [ ] High-level Automation class
  - [ ] AutomationElement base class
  - [ ] All element types (Button, TextBox, etc.)
  - [ ] All patterns (InvokePattern, ValuePattern, etc.)
  - [ ] Condition factory
  - [ ] Type converters

### 5.6 Comparison Documentation
**Priority**: LOW | **Estimated Effort**: 1 week

- [ ] **FlaUI Python vs FlaUI C#**
  - [ ] API differences
  - [ ] Performance comparison
  - [ ] Migration guide from C#

- [ ] **vs Other Python Libraries**
  - [ ] vs pywinauto (feature comparison)
  - [ ] vs Robot Framework FlaUI (why use this instead)
  - [ ] vs Selenium (when to use each)
  - [ ] vs Playwright (desktop vs web)

---

## Phase 6: Polish & Production Readiness ✨
**Target**: v1.0.0 release quality

### 6.1 Code Quality
**Priority**: HIGH | **Estimated Effort**: 2 weeks

- [ ] **Code Review**
  - [ ] Review all modules for consistency
  - [ ] Ensure naming conventions are uniform
  - [ ] Verify all public APIs have docstrings
  - [ ] Check for unused imports and code
  - [ ] Verify type hints are complete

- [ ] **Testing**
  - [ ] Achieve 95%+ test coverage
  - [ ] Fix all xfailed tests (GH-74 to GH-83)
  - [ ] Add integration test suite
  - [ ] Add performance benchmarks
  - [ ] Test on multiple Python versions (3.8-3.13)
  - [ ] Test on multiple Windows versions

- [ ] **Static Analysis**
  - [ ] Run mypy with strict mode
  - [ ] Run pylint and achieve 9.5+ score
  - [ ] Run bandit for security issues
  - [ ] Run vulture for dead code

### 6.2 Performance
**Priority**: MEDIUM | **Estimated Effort**: 1-2 weeks

- [ ] **Benchmarking**
  - [ ] Create benchmark suite
  - [ ] Compare with FlaUI C# performance
  - [ ] Compare with pywinauto
  - [ ] Identify bottlenecks

- [ ] **Optimization**
  - [ ] Optimize element finding
  - [ ] Optimize property access
  - [ ] Reduce PythonNet overhead
  - [ ] Implement caching strategies

### 6.3 Packaging & Distribution
**Priority**: HIGH | **Estimated Effort**: 1 week

- [ ] **Package Metadata**
  - [ ] Update `pyproject.toml` with complete metadata
  - [ ] Add keywords for PyPI discoverability
  - [ ] Add classifiers (Python versions, OS, topics)
  - [ ] Verify license information

- [ ] **Distribution**
  - [ ] Test wheel installation on clean systems
  - [ ] Verify C# DLLs are included correctly
  - [ ] Test on different Python installations
  - [ ] Create installation troubleshooting guide

- [ ] **Release Process**
  - [ ] Document release checklist
  - [ ] Automate version bumping
  - [ ] Create GitHub release workflow
  - [ ] Set up PyPI publishing automation

### 6.4 Community & Support
**Priority**: MEDIUM | **Estimated Effort**: 1 week

- [ ] **GitHub Repository**
  - [ ] Update README with badges and quick start
  - [ ] Create issue templates
  - [ ] Create PR template
  - [ ] Add CONTRIBUTING.md guidelines
  - [ ] Add CODE_OF_CONDUCT.md

- [ ] **Communication**
  - [ ] Create announcement blog post
  - [ ] Post to Reddit (r/Python, r/learnpython)
  - [ ] Share on Twitter/LinkedIn
  - [ ] Consider creating Discord/Slack community

---

## Phase 7: v1.0.0 Release 🎉
**Target**: Official production release

### 7.1 Pre-Release Checklist
**Priority**: CRITICAL | **Estimated Effort**: 1 week

- [ ] **Code Freeze**
  - [ ] All tests passing (0 failures)
  - [ ] All documentation complete
  - [ ] All known bugs fixed or documented
  - [ ] Performance benchmarks acceptable

- [ ] **Quality Gates**
  - [ ] 95%+ test coverage achieved
  - [ ] 95%+ docstring coverage achieved
  - [ ] All static analysis checks passing
  - [ ] No security vulnerabilities

- [ ] **Release Artifacts**
  - [ ] Build final wheel
  - [ ] Generate API documentation
  - [ ] Create release notes
  - [ ] Tag version in git

### 7.2 Release Activities
**Priority**: CRITICAL | **Estimated Effort**: 2-3 days

- [ ] **Publishing**
  - [ ] Publish to PyPI
  - [ ] Publish documentation to ReadTheDocs/GitHub Pages
  - [ ] Create GitHub release with notes
  - [ ] Update CHANGELOG.md

- [ ] **Announcement**
  - [ ] Write release announcement
  - [ ] Share on social media
  - [ ] Submit to Python Weekly
  - [ ] Post on relevant forums

### 7.3 Post-Release
**Priority**: HIGH | **Estimated Effort**: Ongoing

- [ ] **Monitoring**
  - [ ] Monitor PyPI download stats
  - [ ] Monitor GitHub issues/discussions
  - [ ] Collect user feedback
  - [ ] Track bug reports

- [ ] **Support**
  - [ ] Respond to issues promptly
  - [ ] Update documentation based on feedback
  - [ ] Create FAQ based on common questions
  - [ ] Plan v1.1.0 features

---

## Known Issues to Resolve

### High Priority Bugs
- [ ] **GH-74**: Spinner control AutomationID instability (3 tests)
- [ ] **GH-75**: Combobox broken on WinForms (22 tests)
- [ ] **GH-76**: Tree test flaky on CI (4 tests)
- [ ] **GH-77**: RegisterAutomationEvent not ported (4 tests)
- [ ] **GH-78**: Toggle pattern unsupported on WinForms menus (2 tests)
- [ ] **GH-79**: Context menu broken on UIA3+WinForms (1 test)
- [ ] **GH-81**: find_*_with_options failures (8 tests)
- [ ] **GH-82**: test_get_control_type flaky (4 tests)
- [ ] **GH-83**: test_select_by_index fails on UIA3+WPF (4 tests)

### Technical Debt
- [ ] Refactor test fixture architecture for better reusability
- [ ] Standardize error messages across all exceptions
- [ ] Create helper utilities for common automation patterns
- [ ] Add async/await support for long-running operations
- [ ] Implement connection pooling for multiple app automation

---

## Success Metrics

### Code Quality Metrics
- **Test Coverage**: 95%+ (Currently: ~85%)
- **Docstring Coverage**: 95%+ (Currently: 95% ✅)
- **Mypy Compliance**: 100% (strict mode)
- **Ruff Linting**: 0 errors, 0 warnings

### Performance Metrics
- **Element Finding**: < 100ms average
- **Action Execution**: < 50ms average (click, type, etc.)
- **Test Suite**: < 2 minutes for full suite
- **Package Size**: < 10MB wheel

### Documentation Metrics
- **Pages**: 50+ documentation pages
- **Examples**: 20+ complete examples
- **API Coverage**: 100% public APIs documented
- **Tutorial Completion Rate**: Track user engagement

### Adoption Metrics
- **PyPI Downloads**: 1000+/month by end of Q1 2026
- **GitHub Stars**: 100+ stars
- **Issues Resolved**: Maintain < 1 week response time
- **Community**: 50+ active users/contributors

---

## Timeline Estimate

### Aggressive Timeline (3-4 months)
```
Month 1: Phase 1 (flaui.core testing completion)
Month 2: Phase 2 (flaui.uia2) + Phase 3 (flaui.uia3)
Month 3: Phase 4 (Python integration) + Phase 5 (Documentation)
Month 4: Phase 6 (Polish) + Phase 7 (Release)
```

### Realistic Timeline (5-6 months)
```
Month 1-2: Phase 1 (flaui.core testing completion)
Month 2-3: Phase 2 (flaui.uia2)
Month 3-4: Phase 3 (flaui.uia3)
Month 4-5: Phase 4 (Python integration) + Phase 5 (Documentation)
Month 5-6: Phase 6 (Polish) + Phase 7 (Release)
```

### Conservative Timeline (7-8 months)
```
Month 1-2: Phase 1 (flaui.core testing completion)
Month 3-4: Phase 2 (flaui.uia2)
Month 4-5: Phase 3 (flaui.uia3)
Month 5-6: Phase 4 (Python integration)
Month 6-7: Phase 5 (Documentation)
Month 7-8: Phase 6 (Polish) + Phase 7 (Release)
```

---

## Resources & References

### FlaUI C# Repository
- **Location**: `c:\Users\Amruth.Vithala\projects\FlaUI`
- **Key Folders**:
  - `src/FlaUI.Core/` - Core implementation
  - `src/FlaUI.UIA2/` - UIA2 provider
  - `src/FlaUI.UIA3/` - UIA3 provider
  - `src/FlaUI.Core.UITests/` - C# tests to port

### Similar Projects for Inspiration
- **Playwright Python**: Clean API, excellent documentation
- **Selenium Python**: Mature locator strategies, wait mechanisms
- **pywinauto**: Windows automation patterns
- **Robot Framework**: Keyword-driven approach

### Documentation Tools
- **mkdocs-material**: Modern documentation theme
- **mkdocstrings**: Auto-generate API docs from docstrings
- **mermaid**: Diagrams and flowcharts
- **admonitions**: Callouts for notes/warnings

---

## Notes

**Last Updated**: December 15, 2025

**Project Status**: Phase 1 in progress - Basic unit tests established, bug tracking implemented, CI/CD functional

**Next Immediate Actions**:
1. Run coverage report to identify gaps in flaui.core
2. Create GitHub project board for tracking these tasks
3. Start Phase 1.1 - Complete missing element tests
4. Fix high-priority bugs (GH-74 to GH-83)

**Questions to Resolve**:
- Should we support Python 3.8-3.13 or drop older versions?
- Should we maintain strict 1:1 C# API parity or optimize for Python idioms?
- Should we include async/await patterns or keep it synchronous?
- Should we create a separate "high-level" API in addition to low-level?

**Risks**:
- PythonNet compatibility with future Python versions
- Windows API changes breaking UIA2/UIA3
- FlaUI C# updates requiring re-sync
- Test application maintenance (WinForms/WPF apps)

---

*This roadmap is a living document and will be updated as the project progresses.*
