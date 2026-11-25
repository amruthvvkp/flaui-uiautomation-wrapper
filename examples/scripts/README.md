# Gallery scripts

Plain Python scripts, with no test framework, that automate real applications. Each one appears
in the docs' **Examples → Gallery** page next to the equivalent C# program.

| Script | What it automates | Run it |
|--------|-------------------|--------|
| `quickstart.py` | The bundled WPF or WinForms test app, on UIA2 or UIA3 (the *Basics* guide) | `uv run python examples/scripts/quickstart.py --app wpf --uia 3` |
| `calculator.py` | Windows Calculator (Store / UWP app): computes `12 + 30` | `uv run python examples/scripts/calculator.py` |
| `notepad.py` | Notepad (classic on Windows 10, Store on Windows 11): writes and reads text | `uv run python examples/scripts/notepad.py` |

The `# --8<-- [start:…]` / `# --8<-- [end:…]` comments mark the sections the docs include. Keep
them in place when you edit a script.
