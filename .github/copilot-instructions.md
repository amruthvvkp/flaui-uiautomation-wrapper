# Project Overview

This project is a Python port of the FlaUI C# library for Windows UI automation. It provides a 1:1 mapping of all exposed C# endpoints using PythonNet, enabling full FlaUI capabilities in Python. Unlike RobotFlaUI, which is limited to Robot Framework and XPath, this project aims for complete feature parity and plug-and-play usage for Python developers.

## Folder Structure

- `flaui/`: Contains all translated FlaUI code, built on top of Pydantic for validation and type safety.
  - `core/`: Core automation element wrappers and logic.
  - `lib/`: Supporting libraries and system wrappers.
  - `bin/`: Disted C# binaries packaged into the Python wheel.
  - `modules/`: Additional automation modules.
- `tests/`: Unit tests for the test applications (WinForms, WPF) ported from FlaUI C#.
  - `test_utilities/`: PyTest mappings for test application elements.
- `test_applications/`: Contains WinForms and WPF test apps for validation.
- `FlaUI/`: Original C# source and test projects for reference.

## Libraries and Tools

- PythonNet for C# interop.
- Pydantic for data validation and type hints.
- UV for dependency management (`uv sync --all-groups --all-extras` to install, `uv build` to build, `uv version <version>` to bump version).

## Coding Standards

- All classes and methods should closely mirror the C# FlaUI API.
- Use Pydantic models and validators for all Python-side data validation.
- Ensure input/output types are translated correctly between Python and C#.
- Maintain clear docstrings and type hints for IDE intellisense.
- Follow Python naming conventions (snake_case for methods/properties, PascalCase for classes).
- Always call `setup_pythonnet_bridge()` before importing any modules that reference C# types or assemblies. This ensures the PythonNet bridge is initialized and C# assemblies are loaded before any dependent imports. Use this pattern in all test and utility files that interact with C# code.

## Testing Guidelines

- Port all C# UI and unit tests to Python using PyTest, covering both WinForms and WPF test applications.
- For each test, ensure matrix coverage for UIA2/UIA3 and WinForms/WPF, using PyTest parametrization to mirror C# [TestCase] or [Theory] attributes.
- Reference the original C# test logic for parity, including edge cases and error handling.
- Add additional tests for new features and edge cases.
- Future goal: add examples for other test frameworks using the same object mapping.

## Packaging

- Ensure all required C# binaries in `flaui/bin` are included in the wheel for plug-and-play usage.

## Example Reference

- See `flaui/core/automation_elements.py` for how C# classes like `AutomationElement.cs` and `AutomationElement.AsMethods.cs` are mapped to Python.
- Python classes should validate input data formats and translate them to appropriate C# data classes, and vice versa, for full intellisense and type safety.

## Contribution

- Read the entire codebase if required before making changes.
- Follow the structure and mapping conventions for new features or bug fixes.
- All new code should be covered by unit tests.

## Versioning

- Use `uv version <version>` to bump the version.
- Use `uv sync --all-groups --all-extras -U` to update dependencies.

## Goals

- Achieve full feature parity with FlaUI C#.
- Provide robust, validated, and type-safe Python wrappers for all automation elements and patterns.
- Enable easy extension to other test frameworks beyond PyTest.
