# Agentic Guidelines

Copy-paste snippets for LLMs (Claude/GPT/Gemini) so generated code follows project rules.

## Use with AI agents and MCP

FlaUI for Python is a clean, typed foundation for **building agent tools** on top of Windows UI
automation. Because every element, pattern, and input method is exposed as a plain Python call with
Pydantic-backed types, wrapping `find`, `click`, `type`, and pattern actions as
[MCP](https://modelcontextprotocol.io/) tools (or any other agent-tool interface) is
straightforward — an agent can then drive arbitrary Windows applications.

!!! note "An enabling foundation, not a shipped feature"

    This library does **not** ship an MCP server or any built-in agent control. It is the
    *substrate* you would build one on. A reference MCP server / agent-tool example is tracked as a
    post-v1 item on the [Roadmap](roadmap.md#wishlist-postv1).

!!! warning "Responsible use"

    Letting an agent click and type into live applications is powerful and risky. If you build
    agent tooling on this library:

    - Only automate applications and environments you are **authorized** to control.
    - Prefer scoping tools to a known target window/process rather than the whole desktop.
    - Add confirmation or dry-run modes for destructive actions, and keep a human in the loop for
      anything irreversible.

## System prompt template
- Call `setup_pythonnet_bridge()` before importing any C# types.
- Use snake_case for methods/properties; classes stay PascalCase.
- Decorate C# interop methods with `@handle_csharp_exceptions`.
- Target Python 3.10–3.14 (`|` unions, `match`, and built-in generics like `list[str]` are allowed).
- Use fixtures from `tests/conftest.py` for matrix (UIA2/UIA3 × WinForms/WPF).
- Prefer `ConditionFactory` for finding elements; use XPath for complex hierarchies.
- Support `post_wait` on mouse/keyboard/element input methods.
- Provide docstrings (Sphinx style) and type hints everywhere.

## Context snippet for LLMs
```
Project: FlaUI Python wrapper (1:1 C# API parity). Call setup_pythonnet_bridge() first. Use @handle_csharp_exceptions on interop. Python 3.10+ typing. Use ConditionFactory / XPath. Post-wait support on input. Fixtures provide matrix UIA2/UIA3 × WinForms/WPF.
```

## Common mistakes to avoid
- Importing C# assemblies before `setup_pythonnet_bridge()`.
- Skipping exception decorator on interop methods.
- Targeting Python below 3.10 (the project requires `>=3.10,<3.15`).
- Adding skip/xfail in test bodies instead of fixtures.
- Omitting `post_wait` when automating UI that needs time to settle.

## Documentation expectations
- Update mkdocstrings docstrings when adding APIs (Sphinx style).
- Keep examples with Python/C# tabs when relevant.
- Note UIA2/UIA3 port-in-progress warnings for unstable areas.

## Where to look
- `CLAUDE.md` (project standards)
- `AGENTS.md` (workflow for agents)
- `tests/test_utilities` (element maps/page objects)
- `tests/ui/core` (usage patterns)

## When generating tests
- Use fixtures: `test_application`, `ui_automation_type`, `test_application_type`.
- Provide type hints for element maps (WinForms/WPF).
- Keep skip logic in fixtures; use `pytest.mark.xfail` for tracked failures.

## When generating docs
- Add simple, clear usage examples to Basics; deep detail to Advanced; full coverage in API pages.
- Include inspector guidance (FlaUIInspect, Accessibility Insights).
- Keep Troubleshooting updated with known skips/xfails.
