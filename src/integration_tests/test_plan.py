import sys

from testplan import test_plan
from testplan.testing.multitest import MultiTest
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
from integration_tests.bank_system.bank_system_main_window_tests import BankSystemMainWindowTests
from integration_tests.drivers.bank_system import BankSystemDriver


@test_plan(name='Multiply')
def main(plan):
    setup_pythonnet_bridge(dll_list=[
        'FlaUI.Core', 'FlaUI.UIA2', 'FlaUI.UIA3', 'Interop.UIAutomationClient'
    ])
    bank_system_tests = MultiTest(
        name='MultiplyTest',
        suites=[BankSystemMainWindowTests()],
        environment=[BankSystemDriver(name='bank_system_driver')])
    plan.add(bank_system_tests)


if __name__ == '__main__':
    sys.exit(not main())
