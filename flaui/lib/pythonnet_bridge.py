"""This module provides a bridge between Python and .NET using Python.NET."""

import logging

import clr
from System.Reflection import Assembly  # pyright: ignore[reportMissingImports]

import flaui.lib.config as config

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
    # logging.info("Looking for valid binaries at - %s", BIN_HOME)
    global FLAUI_CSHARP_VERSION
    try:
        for _ in BIN_HOME.glob("*.dll"):
            clr.AddReference(_.as_posix())  # pyright: ignore
            clr.AddReference(_.stem)  # pyright: ignore
            assembly = Assembly.LoadFile(_.as_posix())
            version = assembly.GetName().Version
            logging.info("Added %s v%s DLL to Python.NET bridge", _.name, version)
            if _.name == "FlaUI.Core.dll":
                FLAUI_CSHARP_VERSION = str(version)
    except Exception as err:
        logging.exception("Failed to setup Python.NET bridge: %s", err)
        raise err
    logging.info("Python.NET bridge setup complete")
