from utils import shell, config_mod, prompt
from . import rust

PARU_GIT = "https://aur.archlinux.org/paru.git"

PARU_CONFIG_PATH = "/etc/paru.conf"
ENABLED_FEATS = {"CombinedUpgrade", "CleanAfter"}
CONFIG_KVS = {"RemoveMake": "ask"}


@prompt.auto
def install_paru() -> None:
    rust.install_rust()
    shell.run(["cd", "~"])
    shell.run(["git", "clone", PARU_GIT])
    shell.run(["cd", "paru"])
    shell.run(["makepkg", "-si"])


@prompt.auto
def pach_paru_config() -> None:
    with open(PARU_CONFIG_PATH, "r+", encoding="utf-8") as config_file:
        config_mod.uncomment(config_file, ENABLED_FEATS)
        config_mod.set_value(config_file, CONFIG_KVS)


def install_aur_package(package_name: str) -> None:
    shell.run(["paru", "-S", package_name])
