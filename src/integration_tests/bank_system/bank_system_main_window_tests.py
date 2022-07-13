from testplan.testing.multitest import testsuite, testcase
from testplan.environment import Environment
from testplan.testing.multitest.result import Result


@testsuite
class BankSystemMainWindowTests(object):

    @testcase
    def check_main_window_controls(self, env: Environment, result: Result):
        result.true(True, 'This is a sample assertion')
