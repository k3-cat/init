import subprocess
from typing import IO, cast

from . import prompt


def _run_iter(command: tuple[str, ...]):
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        while line := cast(IO[bytes], process.stdout).readline().rstrip():
            yield line.decode("utf-8")


@prompt.auto
def run(*command: str):
    for output in _run_iter(command):
        print(output)
