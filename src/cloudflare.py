import json
from enum import Enum

from utils import ip, kget, prompt

_BASE_ENDPOINT = "https://api.cloudflare.com/client/v4"


class DNSRecordType(Enum):
    A = "A"
    AAAA = "AAAA"


def _inj_token():
    return ("X-Auth-Key", "token")


def _check_success(res: str):
    res_json = json.loads(res)
    if not res_json["success"]:
        raise prompt.error(res_json["errors"])
    return res_json


def _add_dns_record(
    zone_id: str,
    record_type: DNSRecordType,
    name: str,
    content: str,
    proxied: bool = True,
    TTL: int = 1,
):
    data = json.dumps(
        {
            "type": record_type.value,
            "name": name,
            "content": content,
            "proxied": proxied,
            "ttl": TTL,
        }
    )
    res = kget.api_post(f"{_BASE_ENDPOINT}/zones/{zone_id}/dns_records", data, _inj_token())
    _check_success(res)


def _obtain_zone_id(domain: str) -> str:
    res = kget.api_get(f"{_BASE_ENDPOINT}/zones?name={domain}", _inj_token())
    res_json = _check_success(res)
    if res_json["result_info"]["count"] > 1:
        raise prompt.error("More than one possible result", res_json["result_info"]["count"])
    return res_json["result"]["id"]


@prompt.auto
def set_dns(
    name: str,
    domain: str,
    proxied: bool = True,
):
    (ipv4, ipv6) = ip.get_ip()
    zone_id = _obtain_zone_id(domain)
    _add_dns_record(zone_id, DNSRecordType.A, name, ipv4, proxied=proxied)
    _add_dns_record(zone_id, DNSRecordType.AAAA, name, ipv6, proxied=proxied)
