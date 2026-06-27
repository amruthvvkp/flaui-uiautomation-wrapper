# Patterns

Python wrappers around the C# `FlaUI.Core.Patterns` types. The `Patterns` facade (exposed as
`element.patterns`) gives typed, snake_case access to each UI Automation pattern, mirroring the C#
`element.Patterns.<Pattern>.Pattern` shape one-to-one:

```python
# C#:  element.Patterns.Value.Pattern.Value.Value
element.patterns.value.pattern.value.value

# C#:  element.Patterns.Toggle.IsSupported
element.patterns.toggle.is_supported
```

Each pattern wraps a native C# pattern object, always reachable via `raw_pattern` as an escape
hatch for members that are not yet wrapped. Patterns are ported incrementally by family.

::: flaui.core.patterns

## Text ranges

The Text patterns (`TextPattern`, `Text2Pattern`, `TextEditPattern`, `TextChildPattern`) return
`TextRange` objects, the Python wrapper around C# `ITextRange`.

::: flaui.core.text_range
