import json
import os
from pathlib import Path
from typing import TypedDict, Unpack

import pacman
from utils import kget


class RunCfg(TypedDict):
    cf_account_id: str
    cf_api_token: str


_SSH_DIR = Path("/etc/ssh")
CONFIG_D = _SSH_DIR / "sshd_config.d"
CONFIG_PATH = CONFIG_D / "10-custom.conf"

_SSHD_CONFIG_SOURCE_URL = (
    "https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-{ver}.tar.gz"
)
_SSHD_CONFIG_PATCH = f"""
# Include drop-in configurations
Include {CONFIG_D}/*.conf
"""
_CA_PATH = _SSH_DIR / "ca.pub"
_TXT = f"""
PasswordAuthentication no
KbdInteractiveAuthentication no

PubkeyAuthentication yes
TrustedUserCAKeys {_CA_PATH}
"""


def _normalize():
    os.mkdir(CONFIG_D)
    kget.extract_from_tar_gz(
        _SSHD_CONFIG_SOURCE_URL.format(ver=pacman.get_field_from_pkgbuild("openssh", "pkgver")),
        "sshd_config",
        (_SSH_DIR / "sshd_config"),
    )
    with (_SSH_DIR / "sshd_config").open("r+", encoding="utf-8") as fp:
        content = fp.read()
        fp.seek(0)
        fp.write(_SSHD_CONFIG_PATCH)
        fp.write("\n")
        fp.write(content)


def _patch_config(cfg: RunCfg):
    with CONFIG_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_TXT)
    kget.download(
        (
            "https://api.cloudflare.com/client/v4/accounts/"
            "{cf_account_id}/access/gateway_ca".format_map(cfg)
        ),
        _CA_PATH,
        "Bearer {cf_api_token}".format_map(cfg),
    )


def run(**cfg: Unpack[RunCfg]):
    _normalize()
    _patch_config(cfg)


if __name__ == "__main__":
    with Path(os.environ["INIT_CFG_PATH"]).open("rb") as fp:
        main_cfg = json.load(fp)
        run(**main_cfg[Path(__file__).stem])
