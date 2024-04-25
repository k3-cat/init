import sys


def check_platform() -> bool:
    return sys.platform == "win32"
