# Pytest Example

A minimal but realistic flow using the provided fixtures and element maps.

```python
from flaui.lib.enums import UIAutomationTypes
from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements


def test_button_invokes(test_application: WinFormsApplicationElements | WPFApplicationElements) -> None:
    button = test_application.simple_controls_tab.invoke_button
    button.invoke()
```

Session fixtures in `tests/conftest.py` launch all four combinations (UIA2/UIA3 × WinForms/WPF). Keep skips/xfails in fixtures, not in tests.
