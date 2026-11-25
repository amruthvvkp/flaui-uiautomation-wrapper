"""Gallery: automate the built-in Windows Calculator (a UWP / Store app).

Shows how to launch a Store app by its AppUserModelId, address buttons by AutomationId, and read a
result back. Calculator's AutomationIds are stable across Windows 10 and Windows 11.

Run it from the project root::

    uv run python examples/scripts/calculator.py
"""

from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()  # must run before any C#-backed FlaUI import

from flaui.core.tools import Retry
from flaui.lib.enums import UIAutomationTypes
from flaui.modules.automation import Automation

CALCULATOR_AUMID = "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"


def main() -> None:
    """Compute ``12 + 30`` in Calculator and print the display."""
    # Store apps want UIA3; UIA2 cannot see inside the XAML island.
    with Automation(UIAutomationTypes.UIA3) as automation:
        automation.application.launch_store_app(CALCULATOR_AUMID)
        window = automation.application.get_main_window(automation)
        cf = automation.cf

        def press(automation_id: str) -> None:
            """Invoke the Calculator button with the given AutomationId."""
            window.find_first_descendant(cf.by_automation_id(automation_id)).as_button().invoke()

        press("clearButton")
        for key in ("num1Button", "num2Button", "plusButton", "num3Button", "num0Button", "equalButton"):
            press(key)

        display = window.find_first_descendant(cf.by_automation_id("CalculatorResults"))
        # The display's Name reads e.g. "Display is 42"; wait for the result to settle.
        Retry.WhileFalse(lambda: display.name.endswith("42"), timeout=2000)
        print(display.name)
        assert display.name.endswith("42"), display.name
    # Leaving the `with` block closes Calculator and disposes the automation.


if __name__ == "__main__":
    main()
