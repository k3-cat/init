from utils import shell, prompt
from . import pacman

@prompt.auto
def install_rustup() -> None:
    pacman.install_pkg("rustup")


@prompt.auto
def install_rust() -> None:
    shell.run(["rustup", "install", "stable"])
