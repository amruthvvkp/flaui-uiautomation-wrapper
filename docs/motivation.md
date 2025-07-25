# Motivation

## Why was this library created?

While RobotFlaUI provided some UI automation capabilities for Python, it was limited to Robot Framework and XPath-based element finding. There was no solution that offered full access to the FlaUI C# API for Python developers.

This library was created to:

- Enable Python developers to use the complete FlaUI API for Windows UI automation
- Provide robust, validated, and type-safe Python wrappers for all automation elements and patterns
- Achieve feature parity with the original C# library
- Support plug-and-play usage by packaging all required C# binaries
- Make it easy to port and run C# UI and unit tests in Python

## Advantages over alternatives

- 1:1 mapping of C# endpoints, not just limited to XPath or Robot Framework
- Built on Pydantic for validation and type hints
- PythonNet for seamless C# interop
- Designed for extensibility and future support of other test frameworks

## Who should use this library?

- Python developers needing advanced Windows UI automation
- Teams migrating C# FlaUI tests to Python
- Anyone seeking a modern, validated, and extensible automation solution for Windows applications
