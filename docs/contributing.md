# Contributing

We welcome contributions to the FlaUI Python port! Please read the guidelines below to get started.

## How to contribute

- Fork the repository and create a feature branch from `master`.
- Read the entire codebase if required before making changes.
- Follow the structure and mapping conventions for new features or bug fixes.
- All new code should be covered by unit tests (see `tests/` and `test_utilities/`).
- Use Pydantic models and validators for all Python-side data validation.
- Ensure input/output types are translated correctly between Python and C#.
- Maintain clear docstrings and type hints for IDE intellisense.
- Follow Python naming conventions (snake_case for methods/properties, PascalCase for classes).
- Reference C# source files for implementation details and parity.

## Testing

- Port all C# UI and unit tests to Python using PyTest.
- Add additional tests for new features and edge cases.
- Use fixtures for setup/teardown as needed.
- Validate both Python-side and C#-side behaviors through PythonNet interop.

## Packaging and Dependencies

- Use UV for dependency management (`uv sync --all-groups --all-extras` to install, `uv build` to build, `uv version <version>` to bump version).
- Ensure all required C# binaries in `flaui/bin` are included in the wheel for plug-and-play usage.

## Code Review and Pull Requests

- Ensure your code follows the repository Copilot instructions and mapping guidelines.
- Submit a pull request and respond to feedback from maintainers.

Thank you for helping improve the FlaUI Python port!
