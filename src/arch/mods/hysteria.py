import io

from arch.mods import user_mgn
from . import paru
from utils import shell, prompt

HYSTERIA_SERVICE_PATH = ""
HYSTERIA_CONFIG_PATH = ""

HYSTERIA_SERVICE = ""
HYSTERIA_CONFIG = ""


@prompt.auto
def install_hysteria():
    paru.install_aur_package("hysteria-bin")
    with open(HYSTERIA_SERVICE_PATH, "w", encoding="utf-8") as service_file:
        service_file.write(HYSTERIA_SERVICE)
    with open(HYSTERIA_CONFIG_PATH, "w", encoding="utf-8") as config_file:
        config_file.write(HYSTERIA_CONFIG)
    shell.run(["systemctl", "daemon-reload"])
    shell.run(["systemctl", "enable", "hysteria"])

    user_mgn.add_user_to_group("hysteria", "acme")
    shell.run(["systemctl", "start", "hysteria"])


@prompt.auto
def add_userpass(config_file: io.TextIOWrapper, logins: dict[str, str]):
    for (k, v) in logins.items():
        config_file.write(f"    {k}: {v}\n")
