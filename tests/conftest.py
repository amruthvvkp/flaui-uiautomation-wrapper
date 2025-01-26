"""Fixtures for the test suite."""

from typing import Any, Generator

# isort: on
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge
import pytest

# isort: off

setup_pythonnet_bridge()

from loguru import logger
from _pytest.logging import LogCaptureFixture


@pytest.fixture
def caplog(caplog: LogCaptureFixture) -> Generator[LogCaptureFixture, Any, None]:
    """Replaces caplog fixture from Pytest to Loguru

    :param caplog: Pytest Caplog fixture
    :yield: Caplog fixture
    """
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)
