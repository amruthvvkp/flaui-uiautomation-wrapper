import os

import clr
from loguru import logger

import config


def setup_pythonnet_bridge() -> None:
    """Sets up PythonNet bridge

    Sets up PythonNet bridge for FlaUI and automation dependencies for UI Automation so that the interlinked C# .NET dependencies are injected into the Python environment listed under flaui/bin folder.

    :raises err: On failure to load the existing C# dependencies listed under flaui/bin
    """
    BIN_HOME = config.settings.BIN_HOME
    try:
        for _ in os.listdir(BIN_HOME):
            path, dll = os.path.join(BIN_HOME, _), _.replace(".dll", "")
            clr.AddReference(path)
            clr.AddReference(dll)
            logger.info(f"Added {dll} DLL from {path} to PythonNet bridge")
    except Exception as err:
        logger.exception(f"{err}")
        raise err
