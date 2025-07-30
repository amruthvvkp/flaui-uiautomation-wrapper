"""UIAutomation test fixtures."""



# @pytest.fixture(scope="function")
# def restart_test_app(request: pytest.FixtureRequest, test_app: Automation) -> Generator[Automation, Any, None]:
#     """Fixture to restart the test application for the UIAutomation tests.

#     :param test_app: Application object.
#     :yield: Application object.
#     """
#     ui_automation_type, test_application_type = request.param
#     test_base = FlaUITestBase(ui_automation_type, test_application_type)
#     test_base.restart_test_app()
#     yield test_base.automation
#     # tes
