# Add a Unit Test for a Python Automation Element

This prompt helps you add a unit test for a Python automation element class that wraps a C# endpoint.

## Instructions

- Use PyTest for all unit tests.
- Reference the original C# test in FlaUI if available, and port its logic to Python.
- Use the test applications in `test_applications/WinFormsApplication` and `test_applications/WPFApplication` for UI validation.
- Place new tests in the appropriate subfolder under `tests/` (e.g., `test_utilities/`).
- Ensure tests cover all major behaviors, edge cases, and error handling.
- Use fixtures for setup/teardown as needed.
- Validate both Python-side and C#-side behaviors through PythonNet interop.
- Add clear docstrings and assertions for each test.

## Example

See `tests/test_utilities/` for sample mappings and test structure.

## Output

- Provide the full test code, ready to be added to the appropriate test module.
- Include any necessary imports and fixtures.
- Add a short summary of the test coverage if needed.
