from utils import hostfile, prompt, kget

HOSTFILE_URL = "https://a.dove.isdumb.one/list.txt"

INIT_INDICATOR = "Adobe Unlicensed Popup"


@prompt.auto
def ban_unlicensed_popup() -> None:
    rules = kget.fetch(HOSTFILE_URL)
    hostfile.add_rules(rules, INIT_INDICATOR)
