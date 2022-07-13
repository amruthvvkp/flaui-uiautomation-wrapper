import os
from typing import List
import clr
from pathlib import Path
from loguru import logger

ASSEMBLY_PATH = os.path.join(Path(__file__).parent.parent.resolve(), 'bin')
FLAUI_DLL_PATH = str(Path(os.environ.get('FLAUI_DLL_PATH', ASSEMBLY_PATH)))
assert os.path.isdir(FLAUI_DLL_PATH)


def setup_pythonnet_bridge(dll_list: List[str]):
    """Sets up PythonNet bridge

    Sets up PythonNet bridge for FlaUI and automation dependencies for UI Automation 
    so that the interlinked C# .NET dependencies are injected into the Python environment 
    listed under flaui/bin folder.

    :param dll_list: List of DLL's to add to the PythonNet wrapper
    :raises err: On failure to load the existing C# dependencies listed under flaui/bin
    """
    try:
        for dll in dll_list:
            path = os.path.join(FLAUI_DLL_PATH, f'{dll}.dll')
            clr.AddReference(path)
            clr.AddReference(dll)
            logger.info(f'Added {dll} DLL from {path} to PythonNet bridge')
    except Exception as err:
        logger.exception(f'{err}')
        raise err
