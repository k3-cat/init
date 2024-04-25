from enum import Enum
from utils import shell, prompt

class Protocal(Enum):
    TCP = "tcp"
    UDP = "udp"


@prompt.auto
def configure_ufw_default() -> None:
    shell.run(["ufw", "default", "deny", "incoming"])
    shell.run(["ufw", "default", "allow", "outgoing"])


@prompt.auto
def add_rule(port: int, protocal: Protocal) -> None:
    shell.run(["ufw", "allow", f"{port}/{protocal.value}"])
