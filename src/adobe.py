from utils import hostfile, kget

_HOSTFILE_URL = "https://a.dove.isdumb.one/list.txt"

INIT_INDICATOR = "Adobe Unlicensed Popup"


def _ban_unlicensed_popup():
    rules = kget.fetch(_HOSTFILE_URL)
    hostfile.add_rules(rules, INIT_INDICATOR)


def run(_):
    _ban_unlicensed_popup()


if __name__ == "__main__":
    run(None)
