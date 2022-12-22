from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

import FlaUI.Core, FlaUI.UIA2, FlaUI.UIA3  # type: ignore
from flaui.wrapper_generator.build.read_source import traverse_namespace
from flaui.wrapper_generator.tools import prep_wrapper_generation


def main() -> None:
    prep_wrapper_generation()
    traverse_namespace("FlaUI.Core", FlaUI.Core)
    traverse_namespace("FlaUI.UIA2", FlaUI.UIA2)
    traverse_namespace("FlaUI.UIA3", FlaUI.UIA3)


if __name__ == "__main__":
    main()
