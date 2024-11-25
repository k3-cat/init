import json
import os
from pathlib import Path
from typing import TypedDict, Unpack

import paru
from caddy import CONFIG_D as CADDY_CONFIG_D
from utils import shell


class RunCfg(TypedDict):
    hy_port: int
    hy_stats_port: int
    cert_path: str
    key_path: str
    tj_port: int
    tj_service_name: str
    domain: str


_HY_CONFIG_PATH = Path("/etc/hysteria/config.yaml")
_HY_TXT = """
listen: :{hy_port}

tls:
  cert: {cert_path}
  key: {key_path}

bandwidth:
  up: 1200 mbps
  down: 800 mbps

trafficStats:
  listen: "[::1]:{hy_stats_port}"
  secret: ''

masquerade:
  type: proxy
  proxy:
    url: https://quic.nginx.org/
    rewriteHost: true

outbounds:
  - name: default
    type: direct
    direct:
      mode: 64

auth:
  type: userpass
  userpass:
"""
_TJ_CONFIG_PATH = Path("/etc/sing-box/config.json")
_TJ_TXT = """
{
  "log": {
    "level": "warn"
  },
  "inbounds": [
    {
      "type": "trojan",
      "tag": "trojan-in",
      "listen": "::1",
      "listen_port": {tj_port},
      "tcp_multi_path": true,
      "users": [
      ],
      "transport": {
        "type": "grpc",
        "service_name": "{tj_service_name}"
      }
    }
  ],
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct"
    }
  ],
  "route": {
    "auto_detect_interface": true
  }
}
"""
_CADDY_SITE_PATH = CADDY_CONFIG_D / "nekobulb.conf"
_CADDY_SITE_TXT = """
{domain} {
  handle_path /admin/hy2/* {
    reverse_proxy localhost:{hy_stats_port}
  }

  handle /{tj_service_name}/* {
    reverse_proxy localhost:{tj_port} {
      flush_interval -1
      transport http {
        versions h2c
      }
    }
  }

  handle {
    error "Not Found" 404
  }
}
"""


def _install():
    paru.install_aur_package("sing-box-bin hysteria-bin")


def _patch_config(cfg: RunCfg):
    with _HY_CONFIG_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_HY_TXT.format_map(cfg))
    with _TJ_CONFIG_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_TJ_TXT.format_map(cfg))
    with _CADDY_SITE_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_CADDY_SITE_TXT.format_map(cfg))


def _fix_permission():
    shell.run("usermod", "-a", "-G acme", "hysteria")


def _enable():
    shell.run("systemctl", "enable", "--now", "sing-box@config")
    shell.run("systemctl", "enable", "--now", "hysteria@config")
    shell.run("systemctl", "enable", "--now", "caddy")


def _firewalld(cfg: RunCfg):
    if not Path("/usr/bin/firewall-cmd").exists():
        return
    shell.run(
        "firewall-cmd",
        "--zone public",
        "--add-port {hy_port}/udp".format_map(cfg),
        "--permanent",
    )


def run(**cfg: Unpack[RunCfg]):
    _install()
    _patch_config(cfg)
    _fix_permission()
    _enable()
    _firewalld(cfg)


if __name__ == "__main__":
    with Path(os.environ["INIT_CFG_PATH"]).open("rb") as fp:
        main_cfg = json.load(fp)
        run(**main_cfg[Path(__file__).stem])
