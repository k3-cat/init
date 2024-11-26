from pathlib import Path
from utils import shell, config_mod
import rustup

CONFIG_PATH = Path("/etc/paru.conf")
ENABLE_FEATS = {"CombinedUpgrade", "CleanAfter"}
CONFIG_KVS = {"RemoveMake": "ask"}

_PARU_GIT = "https://aur.archlinux.org/paru.git"


def _install():
    rustup.run(None)
    shell.run("cd", "~")
    shell.run("git", "clone", _PARU_GIT)
    shell.run("cd", "paru")
    shell.run("makepkg", "-si")


def _patch_config():
    with CONFIG_PATH.open("r+", encoding="utf-8") as config_file:
        config_mod.uncomment(config_file, ENABLE_FEATS)
        config_mod.set_value(config_file, CONFIG_KVS)


def install_aur_package(package_name: str):
    shell.run("paru", "-S", package_name)


def run(_):
    _install()
    _patch_config()


if __name__ == "__main__":
    run(None)
