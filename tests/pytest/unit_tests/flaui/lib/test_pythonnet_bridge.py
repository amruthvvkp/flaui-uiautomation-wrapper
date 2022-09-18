import pytest
from loguru import logger


def test_setup_pythonnet_bridge() -> None:
    try:
        from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

        setup_pythonnet_bridge()
    except Exception as err:
        logger.exception(f"{err}")
        pytest.fail("Failed to setup PythonNet bridge for FlaUI dependencies")
