- For conditional skips based on the UIA/WinForms/WPF matrix, implement the skip logic in a fixture (such as `test_application_type`, `ui_automation_type`, or a custom fixture that combines both). This ensures the test is skipped as early as possible and keeps test logic clean. Do not place skip logic directly in the test body.
- If a test is not supported for a specific UIA/WinForms/WPF matrix combination (e.g., the C# test does not exist for that combination), use `pytest.skip()` at runtime inside the relevant fixture (not the test body) to skip the test for that combination. This ensures the test is skipped as early as possible and avoids running unnecessary setup. Use `@pytest.mark.xfail` only for known failures where the test is expected to fail but should still be tracked in reports. This ensures unsupported cases are clearly marked as skipped, while known failures remain visible as xfail in test reports.
---
applyTo: "tests/**/*.py"
---


# Testing Guidelines for Python Automation Elements

- Port all relevant C# UI and unit tests from FlaUI to Python using PyTest.
- **Always use the fixtures provided in `tests/conftest.py` for setup and teardown of WinForms and WPF test applications.**
  - For example, use the `test_application`, `ui_automation_type`, and `test_application_type` fixtures as seen in `automation_elements` test files.
  - When using the `test_application` fixture, always provide type hints (e.g., `test_application: WinFormsApplicationElements | WPFApplicationElements`) and import these types at the top of your test file for clarity and IDE support.
  - **Parametrization for UIA/WinForms/WPF should be handled at the fixture level (see calendar and automation_elements tests), not with `@pytest.mark.parametrize` at the test function.**
- When using `ControlType` or any mapped Enum, always use the Enum type (e.g., `ControlType.Tab`) instead of string literals (e.g., `"Tab"`). This ensures type safety and parity with the C# API.
- All type hints must be compatible with Python 3.8 and above. Use types from the `typing` module (e.g., `List`, `Optional`, `Union`) wherever possible for maximum compatibility and clarity.
- Validate both Python and C# behaviors through PythonNet interop.
- Ensure tests cover all major behaviors, edge cases, and error handling.
- Add clear docstrings and assertions for each test.
- Reference original C# test logic for parity.
- Place new tests in the appropriate subfolder (e.g., `test_utilities/`).
- All new features and bug fixes must be covered by tests.
- **Prefix all test commands with `uv run` (e.g., `uv run pytest ...`) to ensure the correct environment is used.**
