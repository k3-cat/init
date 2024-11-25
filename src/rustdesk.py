from pathlib import Path

from firewalld import FIREWALLD_SERVICE_D
from utils import shell

_RUSTDESK_PATH = Path("/var/lib/rustdesk")
_COMPOSE_CFG_PATH = _RUSTDESK_PATH / "compose.yaml"
_COMPOSE_CFG_TXT = """
services:
  hbbs:
    container_name: hbbs
    image: rustdesk/rustdesk-server:latest
    command: hbbs
    volumes:
      - ./hbbs:/root
    network_mode: host
    environment:
      - "ENCRYPTED_ONLY=1"
    depends_on:
      - hbbr
    restart: unless-stopped


  hbbr:
    container_name: hbbr
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    volumes:
      - ./hbbs:/root
    network_mode: host
    restart: unless-stopped


  rustdesk-api:
    container_name: rustdesk-api
    image: ghcr.io/kingmo888/rustdesk-api-server:latest
    environment:
      - TZ=UTC
      - LANGUAGE_CODE=en
    volumes:
      - ./api:/rustdesk-api-server/db
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    network_mode: host
    restart: unless-stopped
"""
SERVICE_PATH = Path("/etc/systemd/system/rustdeskd.service")
_SERVICE_TXT = f"""
[Unit]
Description=Rustdesk ID/Relay/API Service Service
Requires=docker.service
After=docker.service
StartLimitIntervalSec=60

[Service]
WorkingDirectory={_RUSTDESK_PATH}
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose stop
TimeoutStartSec=0
Restart=on-failure
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
"""


def _patch_config():
    with _COMPOSE_CFG_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_COMPOSE_CFG_TXT)
    with SERVICE_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_SERVICE_TXT)


def _enable():
    shell.run("systemctl", "enable", "--now", "rustdeskd")


_FIREWALLD_SERVICE_PATH = FIREWALLD_SERVICE_D / "rustdesk.xml"
_FIREWALLD_SERVICE_TXT = """
<?xml version="1.0" encoding="utf-8"?>
<service>
  <port port="21116" protocol="udp"/>
  <port port="21115-21117" protocol="tcp"/>
</service>
"""


def _firewalld():
    if not Path("/usr/bin/firewall-cmd").exists():
        return
    with _FIREWALLD_SERVICE_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_FIREWALLD_SERVICE_TXT)
    shell.run("firewall-cmd", "--reload")
    shell.run("firewall-cmd", "--zone public", "--add-service rustdesk", "--permanent")


def run(_):
    _patch_config()
    _enable()
    _firewalld()


if __name__ == "__main__":
    run(None)
