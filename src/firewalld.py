from pathlib import Path

import pacman
from utils import kget, shell

_FIREWALLD_DIR = Path("/etc/firewalld")
FIREWALLD_SERVICE_D = _FIREWALLD_DIR / "services"

_FIREWALLD_CFV4_SET_PATH = _FIREWALLD_DIR / "ipsets/Cloudflarev4.xml"
_CFV4_LIST_URL = "https://www.cloudflare.com/ips-v4/#"
_FIREWALLD_CFV6_SET_PATH = _FIREWALLD_DIR / "ipsets/Cloudflarev6.xml"
_CFV6_LIST_URL = "https://www.cloudflare.com/ips-v6/#"
_TXT1 = """
<?xml version="1.0" encoding="utf-8"?>
<ipset type="hash:net">
{entry}
</ipset>
"""
_FIREWALLD_DMZ_ZONE_PATH = _FIREWALLD_DIR / "zones/dmz.xml"
_TXT2 = """
<?xml version="1.0" encoding="utf-8"?>
<zone target="DROP">
  <short>DMZ</short>
  <description>For computers in your demilitarized zone that are publicly-accessible with limited access to your internal network. Only selected incoming connections are accepted.</description>
  <service name="https"/>
  <service name="http3"/>
  <service name="postgresql"/>
  <service name="samba"/>
  <source ipset="Cloudflarev4"/>
  <source ipset="Cloudflarev6"/>
  <forward/>
</zone>
"""
_FIREWALLD_PUBLIC_ZONE_PATH = _FIREWALLD_DIR / "zones/public.xml"
_TXT3 = """
<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Public</short>
  <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
  <service name="dhcpv6-client"/>
  <icmp-block-inversion/>
  <forward/>
</zone>
"""


def _install():
    pacman.install_pkg("firewalld")


def _patch_config():
    with _FIREWALLD_CFV4_SET_PATH.open("w", encoding="utf-8") as fp:
        fp.write(
            _TXT1.format(
                entry="\n".join(
                    f"  <entry>{line}</entry>" for line in kget.fetch(_CFV4_LIST_URL).split("\n")
                )
            )
        )
    with _FIREWALLD_CFV6_SET_PATH.open("w", encoding="utf-8") as fp:
        fp.write(
            _TXT1.format(
                entry=(
                    """  <option name="family" value="inet6"/>"""
                    + "\n".join(
                        f"  <entry>{line}</entry>"
                        for line in kget.fetch(_CFV6_LIST_URL).split("\n")
                    )
                )
            )
        )
    with _FIREWALLD_DMZ_ZONE_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_TXT2)
    with _FIREWALLD_PUBLIC_ZONE_PATH.open("w", encoding="utf-8") as fp:
        fp.write(_TXT3)


def _enable():
    shell.run("systemctl", "enable", "--now", "firewalld")
    shell.run("firewall-cmd", "--reload")


def run(_):
    _install()
    _patch_config()
    _enable()


if __name__ == "__main__":
    run(None)
