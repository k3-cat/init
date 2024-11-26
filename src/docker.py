import os
import platform
from pathlib import Path

from utils import shell

_DOCKER_DIR = Path("/etc/docker")
CONFIG_PATH = _DOCKER_DIR / "daemon.json"

_TXT = """
{
  "iptables": true,
  "live-restore": true,
  "log-driver": "journald"
}
"""


def _install_on_arch():
    import pacman

    pacman.install_pkg("docker docker-compose")


def _install_on_win():
    pass


_INSTALL_MAP = {"Linux": _install_on_arch, "Windows": _install_on_win}


def _patch_config():
    os.mkdir(_DOCKER_DIR)
    with CONFIG_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_TXT)


def _enable():
    shell.run("systemctl", "enable", "--now", "docker")


def run(_):
    _INSTALL_MAP[platform.system()]
    _patch_config()
    _enable()


if __name__ == "__main__":
    run(None)
