# Agent Instructions for FlaUI Python Wrapper

## Primary Reference Document

**All development, testing, and contribution guidelines are consolidated in [CLAUDE.md](CLAUDE.md).**

CLAUDE.md is the **single source of truth** for this project and contains:

- Complete architecture overview
- PythonNet bridge initialization patterns
- C# to Python mapping conventions
- Pydantic validation patterns
- Comprehensive pytest matrix configuration for UIA2/UIA3 × WinForms/WPF testing
- Test porting methodology from FlaUI C#
- Development workflow with UV package manager
- CI/CD configuration and compatibility matrix
- Coding standards and best practices
- Quick reference guides and troubleshooting

## Agent Guidelines

When working on this project:

1. **Always read [CLAUDE.md](CLAUDE.md) first** to understand the project structure and conventions
2. **Follow the PythonNet bridge pattern** - `setup_pythonnet_bridge()` must be called before any C# imports
3. **Use fixture-based parametrization** for pytest matrix testing (not `@pytest.parametrize`)
4. **Apply `@handle_csharp_exceptions`** decorator to all C# interop methods
5. **Maintain 1:1 mapping** with FlaUI C# API structure
6. **Use Pydantic models** for all element classes
7. **Write comprehensive docstrings** (95% coverage required)
8. **Add type hints** to all functions and test fixtures

## Agent Specializations

### Plan Agent
**Purpose**: Researches and outlines multi-step plans

**When to use**:
- Complex feature additions requiring architectural changes
- Test suite expansion across multiple elements
- Refactoring tasks affecting multiple modules

**What to provide**:
- Clear outline of the goal or problem
- Reference to relevant sections in CLAUDE.md
- Expected outcomes and success criteria

### Default Agent
**Purpose**: Implementation and code development

**Responsibilities**:
- Read CLAUDE.md before starting any task
- Follow all coding standards and conventions
- Implement C# to Python mappings
- Write tests with proper matrix configuration
- Update documentation when patterns change

## Common Tasks

### Adding a New Automation Element

1. Locate C# class in `FlaUI/src/FlaUI.Core/AutomationElements/`
2. Review "C# to Python Mapping Patterns" section in CLAUDE.md
3. Create Python class with appropriate mixins
4. Add all properties and methods with decorators
5. Add `as_*` conversion method to AutomationElement
6. Create tests following matrix configuration pattern
7. Update element maps in `test_utilities/elements/`

### Porting C# Tests

1. Reference "Test Porting Methodology" section in CLAUDE.md
2. Locate original test in `FlaUI/src/FlaUI.Core.UITests/`
3. Create test class with proper fixtures
4. Port test methods maintaining logic parity
5. Add matrix skip logic if needed (see "Pytest Matrix Configuration")
6. Run all 4 parametrizations to verify

### Debugging PythonNet Issues

1. Verify `setup_pythonnet_bridge()` is called first
2. Check "PythonNet Bridge" section in CLAUDE.md
3. Use late imports for circular dependencies
4. Review exception translation in `flaui/lib/exceptions.py`

## Important Reminders

- ⚠️ **Never** import C# types before calling `setup_pythonnet_bridge()`
- ⚠️ **Always** use `uv run` prefix for commands (not direct `pytest`)
- ⚠️ **Always** add type hints to test fixtures
- ⚠️ **Always** use fixture parametrization for matrix, not `@pytest.parametrize`
- ⚠️ **Always** convert C# exceptions with `@handle_csharp_exceptions`

## Quick Links

- [CLAUDE.md - Complete Development Guide](CLAUDE.md)
- [Project README](README.md)
- [Contributing Guidelines](docs/contributing.md)
- [Copilot Instructions](.github/copilot-instructions.md)

---

**Remember**: When in doubt, refer to [CLAUDE.md](CLAUDE.md). It contains all the patterns, examples, and guidelines you need.
