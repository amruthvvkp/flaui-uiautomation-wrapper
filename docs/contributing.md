# Contributing

Welcome! Follow these steps to keep parity with FlaUI C# and maintain quality.

## In this section
- [Development Workflow](contributing/development.md) — UV commands, code quality, pre-commit, exception handling, CI/CD, docs build.
- [Testing](contributing/testing.md) — the UIA2/UIA3 × WinForms/WPF pytest matrix, fixtures, `post_wait`, assertions.
- [Porting C# Tests](contributing/porting-tests.md) — step-by-step process for porting from `FlaUI.Core.UITests`.
- [Bug Tracking](bug-tracking.md) — `pytest-bug` markers and the current list of known issues.

## Getting started
- Fork and branch from `master` (dev docs are published as "dev").
- Run `uv sync --all-groups --all-extras`.
- Read `CLAUDE.md` and `AGENTS.md` for standards and workflows.

## Adding/Updating elements
- Locate the C# source in `FlaUI.Core/AutomationElements` and mirror structure.
- Use snake_case for methods/properties; keep class names PascalCase.
- Add `as_*()` conversion in `AutomationElement` when introducing a new element class.
- Decorate interop methods with `@handle_csharp_exceptions`; use late imports to avoid cycles.
- Add docstrings (Sphinx style) and type hints. The project targets Python 3.10+, so `|` unions, `match`/`case`, and built-in generics (`list[str]`) are allowed.

## Tests (matrix: UIA2/UIA3 × WinForms/WPF)
- Use fixtures from `tests/conftest.py` (`test_application`, `ui_automation_type`, `test_application_type`).
- Keep skip logic in fixtures (`skip_notepad_on_win11`, `skip_if_matrix`), not inside tests.
- Use `pytest.mark.xfail` for tracked failures (see Troubleshooting for current list).
- Port C# tests from `FlaUI.Core.UITests` and mirror logic.

See [Testing](contributing/testing.md) for the full fixture walkthrough, `post_wait`, and assertions, and [Porting C# Tests](contributing/porting-tests.md) for the step-by-step port process.

## Code quality
- `ruff check --fix .` and `ruff format .`
- Docstring coverage 95%+ (`interrogate`)
- Python 3.10+ typing (modern `|` unions / `match`/`case` allowed; existing `typing` imports are fine too)

See [Development Workflow](contributing/development.md) for full command reference, pre-commit hooks, and CI/CD.

## Packaging & dependencies
- Build: `uv build`
- Version bump: `uv version <version>`
- Ensure `flaui/bin` DLLs stay packaged; update `Version.md` when DLLs change and regenerate `docs/includes/flaui_versions.md` via `scripts/extract_versions.py`.

## Documentation
- The site is built with [Zensical](https://zensical.org), configured by `zensical.toml`.
- Build locally: `uv run python scripts/extract_versions.py && uv run zensical build -f zensical.toml` (preview with `uv run zensical serve -f zensical.toml`).
- Update mkdocstrings docstrings when adding APIs.
- Basics page stays simple and focused; Advanced gets full detail; API Reference is auto-generated.
- Add C# tabs for parity when helpful.

## Pull requests
- Include tests for new features/bug fixes.
- Link issues/bug markers if applicable.
- Describe matrix coverage and any skips/xfails used.

## Useful references
- `tests/test_utilities` element maps (page objects)
- `tests/ui/core` for usage patterns
- `Agentic Guidelines` for LLM-ready prompts
