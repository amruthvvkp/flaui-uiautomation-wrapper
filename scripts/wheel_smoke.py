"""Smoke-test an *installed* flaui-uiautomation-wrapper wheel from outside the source tree.

CI installs the built wheel into a fresh virtual environment with no dev dependencies, then runs
this script in isolated mode from a directory outside the checkout, so ``flaui`` can only resolve
from site-packages::

    python -I C:\\path\\to\\repo\\scripts\\wheel_smoke.py
    python -I C:\\path\\to\\repo\\scripts\\wheel_smoke.py --apps-dir C:\\path\\to\\repo\\test_applications

The packaging checks always run:

* ``flaui`` is imported from site-packages, not from a source checkout;
* the five bundled DLLs and ``py.typed`` ship inside the installed package, and the ``LICENSE``
  and ``COPYING`` files ship in ``dist-info/licenses``;
* ``setup_pythonnet_bridge()`` loads the DLLs and reports FlaUI 5.x.

With ``--apps-dir`` (needs an interactive desktop, e.g. AppVeyor), the script also launches the
bundled WPF and WinForms test applications on UIA2 and UIA3 and finds a checkbox, toggles it, and
sets text in the TextBox.

The script only uses the standard library plus the installed wheel and its runtime dependencies.
Exit code 0 means every check passed.
"""

import argparse
from importlib import metadata
import os
from pathlib import Path
import platform
import struct
import sys
import sysconfig

EXPECTED_DLLS = (
    "FlaUI.Core.dll",
    "FlaUI.UIA2.dll",
    "FlaUI.UIA3.dll",
    "Interop.UIAutomationClient.dll",
    "System.CodeDom.dll",
)
LICENSE_FILES = ("LICENSE", "COPYING")
DISTRIBUTION = "flaui-uiautomation-wrapper"
APPS = {
    "WPF": Path("WPFApplication") / "WpfApplication.exe",
    "WinForms": Path("WinFormsApplication") / "WinFormsApplication.exe",
}


class SmokeFailure(AssertionError):
    """Raised when a smoke check fails."""


def check(condition: bool, message: str) -> None:
    """Fail the smoke run with ``message`` unless ``condition`` holds.

    :param condition: The condition that must be true.
    :param message: Explanation printed when the check fails.
    :raises SmokeFailure: If ``condition`` is false.
    """
    if not condition:
        raise SmokeFailure(message)
    print(f"  ok   {message}")


def describe_interpreter() -> None:
    """Print which interpreter is running, so CI logs show the installation type under test."""
    print(f"Python      {platform.python_version()} ({platform.python_implementation()})")
    print(f"Bits        {struct.calcsize('P') * 8}-bit")
    print(f"Executable  {sys.executable}")
    print(f"Base prefix {sys.base_prefix}")
    print(f"Venv        {sys.prefix != sys.base_prefix}")
    print(f"Isolated    {bool(sys.flags.isolated)}")
    print(f"CWD         {Path.cwd()}")


def check_installed_package() -> Path:
    """Check that ``flaui`` comes from site-packages and ships its DLLs and ``py.typed``.

    :raises SmokeFailure: If the package resolves from a source tree or is missing files.
    :return: The directory of the installed ``flaui`` package.
    """
    import flaui

    package_dir = Path(flaui.__file__).resolve().parent
    purelib = Path(sysconfig.get_paths()["purelib"]).resolve()
    print(f"flaui       {package_dir}")
    print(f"Version     {metadata.version(DISTRIBUTION)}")

    check(package_dir.parent == purelib, f"flaui resolves from site-packages ({purelib})")
    check(not (package_dir.parent / "pyproject.toml").exists(), "flaui is not imported from a source checkout")

    bin_dir = package_dir / "bin"
    for dll in EXPECTED_DLLS:
        check((bin_dir / dll).is_file(), f"bundled {dll} is installed")
    check((package_dir / "py.typed").is_file(), "py.typed marker is installed")

    files = metadata.files(DISTRIBUTION) or []
    licenses = {f.name for f in files if f.parent.name == "licenses"}
    for name in LICENSE_FILES:
        check(name in licenses, f"license file {name} is installed in dist-info/licenses")
    return package_dir


def check_bridge() -> str:
    """Load the bundled DLLs through PythonNet and check the FlaUI version.

    :raises SmokeFailure: If the bridge does not report a FlaUI 5.x assembly.
    :return: The FlaUI.Core assembly version.
    """
    import flaui.lib.pythonnet_bridge as bridge

    bridge.setup_pythonnet_bridge()
    version = bridge.FLAUI_CSHARP_VERSION or ""
    print(f"FlaUI.Core  {version}")
    check(version.startswith("5."), f"setup_pythonnet_bridge() loaded FlaUI 5.x (got {version!r})")
    return version


def drive_application(executable: Path, app_name: str, uia_name: str) -> None:
    """Launch one test application and find a checkbox, toggle it, and set text in the TextBox.

    :param executable: Path to the test application executable.
    :param app_name: ``"WPF"`` or ``"WinForms"``, for log output.
    :param uia_name: ``"UIA2"`` or ``"UIA3"``.
    :raises SmokeFailure: If an element is missing or an interaction has no effect.
    """
    from flaui.core.definitions import ToggleState
    from flaui.lib.enums import UIAutomationTypes
    from flaui.modules.automation import Automation

    print(f"[{app_name} / {uia_name}]")
    with Automation(UIAutomationTypes[uia_name]) as automation:
        automation.application.launch(str(executable))
        automation.application.wait_while_main_handle_is_missing(5000)
        window = automation.application.get_main_window(automation)
        check(window is not None, f"main window found ({window.title!r})")
        cf = automation.cf

        checkbox = window.find_first_descendant(cf.by_name("Test Checkbox")).as_check_box()
        before = checkbox.toggle_state
        checkbox.toggle()
        after = checkbox.toggle_state
        check(after != before, f"checkbox toggled ({before.name} -> {after.name})")
        checkbox.toggle()
        check(checkbox.toggle_state == before or before == ToggleState.Indeterminate, "checkbox toggled back")

        text = f"flaui wheel smoke {app_name} {uia_name}"
        text_box = window.find_first_descendant(cf.by_automation_id("TextBox")).as_text_box()
        text_box.text = text
        check(text_box.text == text, "TextBox text set and read back")


def run_ui_checks(apps_dir: Path) -> None:
    """Drive both test applications on both UI Automation backends.

    :param apps_dir: The repository's ``test_applications`` directory.
    :raises SmokeFailure: If an executable is missing or any interaction fails.
    """
    for app_name, relative in APPS.items():
        executable = (apps_dir / relative).resolve()
        check(executable.is_file(), f"{app_name} test application exists ({executable})")
        for uia_name in ("UIA2", "UIA3"):
            drive_application(executable, app_name, uia_name)


def main(argv: list[str] | None = None) -> int:
    """Run the smoke checks.

    :param argv: Command-line arguments; defaults to ``sys.argv[1:]``.
    :return: Process exit code (0 on success, 1 on a failed check).
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--apps-dir",
        type=Path,
        default=os.environ.get("FLAUI_SMOKE_APPS_DIR") or None,
        help="test_applications directory; when given, also drive the WPF/WinForms apps on UIA2 and UIA3",
    )
    args = parser.parse_args(argv)

    describe_interpreter()
    try:
        print("Packaging checks")
        check_installed_package()
        print("PythonNet bridge")
        check_bridge()
        if args.apps_dir is not None:
            print("UI checks")
            run_ui_checks(args.apps_dir)
        else:
            print("UI checks skipped (no --apps-dir)")
    except SmokeFailure as failure:
        print(f"  FAIL {failure}", file=sys.stderr)
        return 1
    print("Wheel smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
