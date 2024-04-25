from utils import prompt, config_mod

PACMAN_CONFIG_PATH = "/etc/ssh/sshd_config"
ENABLED_FEATS = {"HostKey /etc/ssh/ssh_host_ed25519_key", "VerbosePkgLists"}
CONFIG_KVS = {
    "Port": "44",
    "StrictModes": "yes",
    "PasswordAuthentication": "no",
    "KbdInteractiveAuthentication": "no",
}


@prompt.auto
def pach_pacman_config() -> None:
    with open(PACMAN_CONFIG_PATH, "r+", encoding="utf-8") as config_file:
        config_mod.uncomment(config_file, ENABLED_FEATS)
        config_mod.set_value(config_file, CONFIG_KVS, no_equ_sign=True)
