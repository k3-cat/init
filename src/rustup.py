import platform
from utils import shell


def _install_on_arch():
    import pacman

    pacman.install_pkg("rustup")


def _install_on_win():
    shell.run("winget", "install", "Rustlang.Rustup")


_INSTALL_MAP = {"Linux": _install_on_arch, "Windows": _install_on_win}


def _configure():
    shell.run("rustup", "install", "stable")


def run(_):
    _INSTALL_MAP[platform.system()]
    _configure()


if __name__ == "__main__":
    run(None)
