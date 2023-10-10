"""This module provides a bridge between Python and .NET using Python.NET."""

import clr
from loguru import logger

import flaui.lib.config as config

def setup_pythonnet_bridge() -> None:
    """
    Sets up Python.NET bridge for FlaUI and automation dependencies for UI Automation
    so that the interlinked C# .NET dependencies are injected into the Python environment
    listed under flaui/bin folder.

    :raises err: On failure to load the existing C# dependencies listed under flaui/bin
    """
    BIN_HOME = config.settings.BIN_HOME
    logger.info(f"Looking for valid binaries at - {BIN_HOME}")
    try:
        for _ in BIN_HOME.glob("*.dll"):
            clr.AddReference(_.as_posix())  # pyright: ignore
            clr.AddReference(_.stem)  # pyright: ignore
            logger.info(f"Added {_.name} DLL to Python.NET bridge")
    except Exception as err:
        logger.exception(f"{err}")
        raise err
    logger.info("Python.NET bridge setup complete")
