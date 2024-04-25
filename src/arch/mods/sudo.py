from utils import prompt, config_mod

PACMAN_CONFIG_PATH = "/etc/pacman.conf"
ENABLED_FEATS = {"%wheel ALL=(ALL:ALL) NOPASSWD: ALL"}


@prompt.auto
def garner_wheel_nopwd() -> None:
    with open(PACMAN_CONFIG_PATH, "r+", encoding="utf-8") as config_file:
        config_mod.uncomment(config_file, ENABLED_FEATS)
