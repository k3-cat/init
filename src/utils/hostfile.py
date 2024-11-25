import sys

from . import prompt

INIT_MARK = "# ---------- init-ed ("
INIT_MARK_END = ") ----------\n\n"


def _get_host_path() -> str:
    if sys.platform == "win32":
        return "C:/Windows/System32/drivers/etc/hosts"
    if sys.platform == "linux":
        return "/etc/hosts"
    raise ValueError("platfrom not supported")


@prompt.auto
def add_rules(rules: str, indictor: str):
    with open(_get_host_path(), "r+", encoding="utf-8") as host_fp:
        buffer = ""
        skip_line = False
        while line := host_fp.readline():
            if line.startswith(INIT_MARK):
                skip_line = indictor in line

            if not skip_line:
                buffer += line

        host_fp.seek(0)
        host_fp.write(buffer.rstrip())
        host_fp.write("\n\n\n")
        host_fp.write(INIT_MARK)
        host_fp.write(indictor)
        host_fp.write(INIT_MARK_END)
        host_fp.write(rules)


@prompt.auto
def restore_default():
    with open(_get_host_path(), "w", encoding="utf-8") as host_fp:
        host_fp.writelines("""
# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
# 102.54.94.97 rhino.acme.com # source server
# 38.25.63.10 x.acme.com # x client host
# localhost name resolution is handled within DNS itself.
# 127.0.0.1 localhost
# ::1 localhost
""")
