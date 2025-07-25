---
applyTo: "tests/**/*.py"
---

# Testing Guidelines for Python Automation Elements

- Port all relevant C# UI and unit tests from FlaUI to Python using PyTest.
- Use fixtures for setup and teardown of test applications.
- Validate both Python and C# behaviors through PythonNet interop.
- Ensure tests cover all major behaviors, edge cases, and error handling.
- Add clear docstrings and assertions for each test.
- Reference original C# test logic for parity.
- Place new tests in the appropriate subfolder (e.g., `test_utilities/`).
- All new features and bug fixes must be covered by tests.
