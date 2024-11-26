import json
import os
from pathlib import Path
from typing import TypedDict, Unpack

import paru
from utils import kget


class RunCfg(TypedDict):
    email: str
    cf_token: str


_CADDY_DIR = Path("/etc/caddy")
CONFIG_D = _CADDY_DIR / "conf.d"

_PLUGIN_LIST_PATH = Path("~/caddy-plugin-list")
_PLUGIN_LIST_TXT = """
github.com/caddy-dns/cloudflare
"""
_CADDY_TMP_URL = (
    "https://gitlab.archlinux.org/archlinux/packaging/packages/caddy/-/raw/main/caddy.tmpfiles"
)
_CADDYFILE_TXT = f"""
# The Caddyfile is an easy way to configure your Caddy web server.
#
# https://caddyserver.com/docs/caddyfile
#
# The configuration below serves a welcome page over HTTP on port 80.
# To use your own domain name (with automatic HTTPS), first make
# sure your domain's A/AAAA DNS records are properly pointed to
# this machine's public IP, then replace the line below with your
# domain name.
#
# https://caddyserver.com/docs/caddyfile/concepts#addresses

{{
	# Restrict the admin interface to a local unix file socket whose directory
	# is restricted to caddy:caddy. By default the TCP socket allows arbitrary
	# modification for any process and user that has access to the local
	# interface. If admin over TCP is turned on one should make sure
	# implications are well understood.
	admin "unix//run/caddy/admin.socket"

	# TLS
	auto_https disable_redirects
	email {{email}}
	acme_dns cloudflare {{cf_token}}
}}

https:// {{
    error "Not Found" 404
}}

# Import additional caddy config files in /etc/caddy/conf.d/
import {CONFIG_D}/*
"""


def _pre_config():
    with _PLUGIN_LIST_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_PLUGIN_LIST_TXT)
    os.environ["PLUGIN_LIST_PATH"] = str(_PLUGIN_LIST_PATH)


def _install():
    paru.install_aur_package("caddy-custom")


def _normalize():
    os.mkdir(CONFIG_D)
    kget.download(
        _CADDY_TMP_URL,
        Path("/usr/lib/tmpfiles.d/caddy.conf"),
    )


def _patch_config(cfg: RunCfg):
    with (_CADDY_DIR / "Caddyfile").open("w", encoding="utf-8") as fp:
        fp.write(_CADDYFILE_TXT.format_map(cfg))


def run(**cfg: Unpack[RunCfg]):
    _pre_config()
    _install()
    _normalize()
    _patch_config(cfg)


if __name__ == "__main__":
    with Path(os.environ["INIT_CFG_PATH"]).open("rb") as fp:
        main_cfg = json.load(fp)
        run(**main_cfg[Path(__file__).stem])
