---
applyTo: "tests/**/*.py"
---


# Testing Guidelines for Python Automation Elements

- Port all relevant C# UI and unit tests from FlaUI to Python using PyTest.
- **Always use the fixtures provided in `tests/conftest.py` for setup and teardown of WinForms and WPF test applications.**
  - For example, use the `test_application`, `ui_automation_type`, and `test_application_type` fixtures as seen in `automation_elements` test files.
  - **Parametrization for UIA/WinForms/WPF should be handled at the fixture level (see calendar and automation_elements tests), not with `@pytest.mark.parametrize` at the test function.**
- Validate both Python and C# behaviors through PythonNet interop.
- Ensure tests cover all major behaviors, edge cases, and error handling.
- Add clear docstrings and assertions for each test.
- Reference original C# test logic for parity.
- Place new tests in the appropriate subfolder (e.g., `test_utilities/`).
- All new features and bug fixes must be covered by tests.
- **Prefix all test commands with `uv run` (e.g., `uv run pytest ...`) to ensure the correct environment is used.**
