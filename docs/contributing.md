# Contributing

Welcome! Follow these steps to keep parity with FlaUI C# and maintain quality.

## Getting started
- Fork and branch from `master` (dev docs are published as "dev").
- Run `uv sync --all-groups --all-extras`.
- Read `CLAUDE.md` and `AGENTS.md` for standards and workflows.

## Adding/Updating elements
- Locate the C# source in `FlaUI.Core/AutomationElements` and mirror structure.
- Use snake_case for methods/properties; keep class names PascalCase.
- Add `as_*()` conversion in `AutomationElement` when introducing a new element class.
- Decorate interop methods with `@handle_csharp_exceptions`; use late imports to avoid cycles.
- Add docstrings (Sphinx style) and type hints (Python 3.10+ compatible).

## Tests (matrix: UIA2/UIA3 × WinForms/WPF)
- Use fixtures from `tests/conftest.py` (`test_application`, `ui_automation_type`, `test_application_type`).
- Keep skip logic in fixtures (`skip_notepad_on_win11`, `skip_if_matrix`), not inside tests.
- Use `pytest.mark.xfail` for tracked failures (see Troubleshooting for current list).
- Port C# tests from `FlaUI.Core.UITests` and mirror logic.

### Matrix fixtures example

All UI tests run 4x: UIA2/UIA3 × WinForms/WPF. Use the fixtures in `tests/conftest.py`:

```python
from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements

def test_button(test_application: WinFormsApplicationElements | WPFApplicationElements):
    test_application.simple_controls_tab.invoke_button.invoke()
```

The `test_application` fixture is parametrized to provide both WinForms and WPF element maps, and combined with the `ui_automation_type` fixture (UIA2/UIA3), each test automatically runs in all 4 combinations.

## Code quality
- `ruff check --fix .` and `ruff format .`
- Docstring coverage 95%+ (`interrogate`)
- Python 3.10+ typing (`|` unions, `match`, and built-in generics are allowed)

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
