import grp
import json
import os
from pathlib import Path
import pwd
from utils import prompt, shell
from . import pacman

LEGO_DIR = Path("/etc/lego")
ACCOUNT_DIR = LEGO_DIR / "accounts"
CERT_DIR = LEGO_DIR / "certificates"
ACME_DOMAIN = "acme-v02.api.letsencrypt.org"

ACME_USER = "acme"


@prompt.auto
def install_lego():
    pacman.install_pkg("lego")


@prompt.auto
def place_account(userinfo: str, key: str):
    user_json = json.loads(userinfo)
    account_dir = ACCOUNT_DIR / ACME_DOMAIN / user_json["email"]
    os.mkdir(account_dir)
    os.mkdir(account_dir / "keys")
    with open(account_dir / "account.json", "w", encoding="utf-8") as account_file:
        account_file.write(userinfo)
    with open(account_dir / "keys" / user_json["email"], "w", encoding="utf-8") as key_file:
        key_file.write(key)


@prompt.auto
def apply_cert(domain: str):
    users = os.listdir(ACCOUNT_DIR / ACME_DOMAIN)
    if len(users) > 1:
        raise ValueError("more than one user")
    shell.run(
        [
            "lego",
            "--path",
            str(LEGO_DIR),
            "--email",
            Path(users[0]).name,
            "--domains",
            domain,
            "--dns run",
        ]
    )


@prompt.auto
def fix_permission():
    root_uid = pwd.getpwnam("root").pw_uid
    root_gid = grp.getgrnam("root").gr_gid
    acme_gid = grp.getgrnam(ACME_USER).gr_gid

    ACCOUNT_DIR.chmod(0o700)
    for path in ACCOUNT_DIR.rglob("*"):
        if path.is_dir():
            path.chmod(0o700)
        elif path.is_file():
            path.chmod(0o600)
        else:
            raise Exception("unknown type")

        os.chown(path, root_uid, root_gid)

    CERT_DIR.chmod(0o740)
    for path in CERT_DIR.rglob("*"):
        if path.is_dir():
            path.chmod(0o740)
        elif path.is_file():
            path.chmod(0o640)

        os.chown(path, root_uid, acme_gid)

    os.chown(ACCOUNT_DIR, root_uid, root_gid)
    os.chown(CERT_DIR, root_uid, acme_gid)
    os.chown(LEGO_DIR, root_uid, acme_gid)
    LEGO_DIR.chmod(0o740)
