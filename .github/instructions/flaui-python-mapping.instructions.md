---
applyTo: "flaui/core/**/*.py"
---

# Mapping C# FlaUI Classes to Python

- Ensure every Python class in `flaui/core` mirrors its C# counterpart in naming, properties, and methods.
- Use Pydantic models for all Python classes to provide validation and type hints.
- Decorate properties and methods with appropriate validators and exception handlers.
- Translate C# types to Python types, using custom wrappers for complex types (e.g., Rectangle, Point).
- Maintain 1:1 mapping for method signatures and documentation.
- Add clear docstrings for IDE intellisense.
- Validate input and output data formats for PythonNet interop.
- Reference C# source files for implementation details.
- All new code must be covered by unit tests in `tests/`.
