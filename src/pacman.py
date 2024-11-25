from pathlib import Path

from utils import config_mod, kget, shell

CONFIG_PATH = Path("/etc/pacman.conf")
ENABLE_FEATS = {"Color", "VerbosePkgLists"}
CONFIG_KVS = {"ParallelDownloads": "50"}


def _patch_config():
    with CONFIG_PATH.open("r+", encoding="utf-8") as config_file:
        config_mod.uncomment(config_file, ENABLE_FEATS)
        config_mod.set_value(config_file, CONFIG_KVS)


def install_pkg(package_name: str):
    shell.run("pacman", "-S", "--noconfirm", package_name)


def get_field_from_pkgbuild(package_name: str, field: str):
    pkgbuild = kget.fetch(
        f"https://gitlab.archlinux.org/archlinux/packaging/packages/{package_name}/-/blob/main/PKGBUILD"
    )
    for line in pkgbuild.split("\n"):
        if line.startswith(f"{field}="):
            return line.strip()[len(field) + 1 :]
    else:
        raise ValueError()


def run(_):
    _patch_config()


if __name__ == "__main__":
    run(None)
