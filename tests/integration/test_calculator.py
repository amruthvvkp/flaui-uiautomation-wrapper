"""Integration tests for Calculator application, ported from C# CalculatorTests.cs."""

from flaui.core.application import Application
from flaui.modules.automation import Automation
import pytest


@pytest.mark.integration
@pytest.mark.skipif(
    True,  # Skip by default - Calculator UI varies significantly by Windows version
    reason="Calculator UI varies significantly between Windows versions",
)
class TestCalculator:
    """Integration tests for Windows Calculator application."""

    def test_calculator_basic_operations(self, automation: Automation) -> None:
        """Test basic calculator operations.

        Ported from CalculatorTests.cs (basic test structure)
        Note: Calculator UI is highly dependent on Windows version
        """
        app = None
        try:
            app = Application()
            app.launch("calc.exe")
            window = app.get_main_window(automation)

            assert window is not None
            assert window.title is not None

            # Calculator UI automation would require element mapping specific to Windows version
            # This is a placeholder for full implementation

        finally:
            try:
                if app is not None:
                    app.close()
            except Exception:
                pass
