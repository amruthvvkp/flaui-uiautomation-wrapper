# Unittest Example

```python
import unittest
from flaui.modules.automation import Automation
from flaui.lib.enums import UIAutomationTypes
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge


class TestNotepad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_pythonnet_bridge()
        cls.automation = Automation(UIAutomationTypes.UIA3)

    def test_title(self):
        app = self.automation.application.launch("notepad.exe")
        window = app.get_main_window(self.automation)
        self.assertIsNotNone(window.title)
        app.close()


if __name__ == "__main__":
    unittest.main()
```
