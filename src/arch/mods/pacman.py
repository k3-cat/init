from utils import shell, config_mod, prompt

PACMAN_CONFIG_PATH = "/etc/pacman.conf"
ENABLED_FEATS = {"Color", "VerbosePkgLists"}
CONFIG_KVS = {"ParallelDownloads": "50"}


@prompt.auto
def pach_pacman_config() -> None:
    with open(PACMAN_CONFIG_PATH, "r+", encoding="utf-8") as config_file:
        config_mod.uncomment(config_file, ENABLED_FEATS)
        config_mod.set_value(config_file, CONFIG_KVS)


@prompt.auto
def install_pkg(package_name: str) -> None:
    shell.run(["pacman", "-S", "--noconfirm", package_name])
