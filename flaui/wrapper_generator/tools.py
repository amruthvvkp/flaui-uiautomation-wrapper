import os, shutil, importlib
from pathlib import Path
from re import sub
from typing import List

from loguru import logger

import FlaUI, config


def prep_wrapper_generation() -> None:
    wrapper_home = Path(config.settings.WRAPPERS_HOME)
    _clear_wrapper_folder(wrapper_home)
    lines = [f'# {FlaUI.__dict__["__doc__"]}', f'# - {FlaUI.__dict__["__name__"]}']  # type: ignore
    _safe_build_python_folder(wrapper_home, "FlaUI", lines)


def _safe_build_python_folder(folder: Path, module: str, lines: List[str]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    lines = [f"# Auto generated wrapper for {module}\n\n"] + lines
    write_lines(os.path.join(folder, "__init__.py"), lines)
    logger.debug(f"Folder created -{folder}")


def write_lines(file: str, lines: List[str]) -> None:
    with open(file, "w") as _:
        _.writelines(lines)
    _.close()
    logger.debug(f"File updated - {file}")


def _clear_wrapper_folder(folder: Path) -> None:
    if not folder.exists():
        return

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error(f"Failed to delete {file_path}. Reason: {e}")


def snake_case(string: str) -> str:
    return "_".join(sub("([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", string.replace("-", " "))).split()).lower()
