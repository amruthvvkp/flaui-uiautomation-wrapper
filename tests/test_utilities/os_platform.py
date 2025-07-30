import platform
import sys

is_windows_11 = (
    sys.platform == "win32"
    and platform.release() == "10"  # Windows 11 reports as 10
    and "11" in platform.version()
)
