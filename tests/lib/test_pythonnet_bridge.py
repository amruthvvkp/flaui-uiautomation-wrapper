from pathlib import Path

import pytest
from loguru import logger


def test_setup_pythonnet_bridge() -> None:
    try:
        import config
        from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

        assert Path(config.settings.BIN_HOME).exists()
        setup_pythonnet_bridge()
    except Exception as err:
        logger.exception(f"{err}")
        pytest.fail("Failed to setup Pythonnet bridge for FlaUI dependencies")
