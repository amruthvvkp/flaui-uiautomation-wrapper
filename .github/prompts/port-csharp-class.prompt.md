# Port a C# AutomationElement class to Python

This prompt helps you port a C# class from FlaUI (such as `AutomationElement.cs` or `AutomationElement.AsMethods.cs`) to Python, following the repository's conventions.

## Instructions

- Map all public properties and methods from the C# class to Python, using Pydantic models for validation.
- Use type hints and docstrings for all Python methods and properties.
- Ensure input/output types are translated correctly between Python and C# using PythonNet.
- Use decorators for exception handling and validation as shown in `flaui/core/automation_elements.py`.
- Follow the naming conventions: PascalCase for classes, snake_case for methods/properties.
- Add validators for input data formats where needed.
- Reference the C# source for method signatures and documentation.
- Ensure the Python class provides full intellisense and type safety for IDEs.

## Example

See `flaui/core/automation_elements.py` for a sample mapping of C# classes to Python.

## Output

- Provide the full Python class code, ready to be added to the appropriate module.
- Include any necessary imports and decorators.
- Add a short summary of the mapping choices if needed.
