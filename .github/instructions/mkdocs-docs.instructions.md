---
applyTo: "docs/**/*.md"
---

# Documentation Guidelines (Zensical)

> The docs site is built with [Zensical](https://zensical.org) configured by `zensical.toml`.
> Build locally with `uv run python scripts/extract_versions.py && uv run zensical build -f zensical.toml`
> (or `uv run zensical serve -f zensical.toml` for live preview). API reference is auto-generated via mkdocstrings.

- All documentation should be written in Markdown and placed in the `docs/` folder.
- The documentation must include:
  - An **Introduction** page describing the project, its goals, and background.
  - A **Motivation** page explaining why this library was created, its advantages over alternatives (e.g., RobotFlaUI), and its unique features.
  - A **Contributing** page with clear instructions for contributing, including code standards, mapping conventions, and testing requirements.
- Use code blocks, lists, and headings for clarity.
- Reference the repository's Copilot instructions and prompt files for standards and examples.
- Ensure all new features and changes are documented.
- Keep documentation up to date with codebase changes.
