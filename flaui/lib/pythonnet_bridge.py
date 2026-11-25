"""This module provides a bridge between Python and .NET using Python.NET."""

import logging

import clr
from System.Reflection import Assembly  # pyright: ignore[reportMissingImports]

import flaui.lib.config as config

logger = logging.getLogger(__name__)

# Global variable to hold the FlaUI C# version
FLAUI_CSHARP_VERSION = None


def setup_pythonnet_bridge() -> None:
    """
    Sets up Python.NET bridge for FlaUI and automation dependencies for UI Automation
    so that the interlinked C# .NET dependencies are injected into the Python environment
    listed under flaui/bin folder.

    :raises err: On failure to load the existing C# dependencies listed under flaui/bin
    """
    BIN_HOME = config.settings.BIN_HOME
    if BIN_HOME != config.DEFAULT_BIN_HOME:
        logger.warning("Loading FlaUI assemblies from FLAUI_BIN_HOME=%s instead of the bundled DLLs", BIN_HOME)
    global FLAUI_CSHARP_VERSION
    try:
        for _ in BIN_HOME.glob("*.dll"):
            clr.AddReference(_.as_posix())  # pyright: ignore
            clr.AddReference(_.stem)  # pyright: ignore
            assembly = Assembly.LoadFile(_.as_posix())
            version = assembly.GetName().Version
            logger.debug("Added %s v%s DLL to Python.NET bridge", _.name, version)
            if _.name == "FlaUI.Core.dll":
                FLAUI_CSHARP_VERSION = str(version)
    except Exception as err:
        logger.exception("Failed to setup Python.NET bridge: %s", err)
        raise err
    logger.info("Python.NET bridge setup complete (FlaUI %s)", FLAUI_CSHARP_VERSION)

    # Opt-in: route C# logging into Python logging when FLAUI_LOG_CSHARP is set. Imported lazily
    # because it depends on the FlaUI DLLs that were just loaded above.
    from flaui.core.logging import maybe_enable_from_settings

    maybe_enable_from_settings()
