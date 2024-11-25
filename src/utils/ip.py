import kget
import prompt

IPV4_ENDPOINT = "https://ipv4.seeip.org"
IPV6_ENFPOINT = "https://ipv6.seeip.org"


@prompt.auto
def get_ip() -> tuple[str, str]:
    ipv4 = kget.fetch(IPV4_ENDPOINT)
    ipv6 = kget.fetch(IPV6_ENFPOINT)
    return ipv4, ipv6
