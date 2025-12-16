# Add a Unit Test for a Python Automation Element

This prompt helps you add a unit test for a Python automation element class that wraps a C# endpoint.

## Instructions

- Use PyTest for all unit tests.
- Reference the original C# test in FlaUI if available, and port its logic to Python, covering both WinForms and WPF test applications.
- For each test, ensure matrix coverage for UIA2/UIA3 and WinForms/WPF, using PyTest parametrization to mirror C# [TestCase] or [Theory] attributes.
- Use the test applications in `test_applications/WinFormsApplication` and `test_applications/WPFApplication` for UI validation.
- Place new tests in the appropriate subfolder under `tests/` (e.g., `test_utilities/`).
- Ensure tests cover all major behaviors, edge cases, and error handling.
- Use fixtures for setup/teardown as needed.
- Validate both Python-side and C#-side behaviors through PythonNet interop.
- Add clear docstrings and assertions for each test.
- **Prefix all test commands with `uv run` (e.g., `uv run pytest ...`) to ensure the correct environment is used.**
- Always call `setup_pythonnet_bridge()` before importing any modules that reference C# types or assemblies in your test files. This ensures the PythonNet bridge is initialized and C# assemblies are loaded before any dependent imports.

## Example

See `tests/test_utilities/` for sample mappings and test structure.

## Output

- Provide the full test code, ready to be added to the appropriate test module.
- Include any necessary imports and fixtures.
- Add a short summary of the test coverage if needed.
