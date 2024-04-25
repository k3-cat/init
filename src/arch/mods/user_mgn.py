from utils import shell, prompt


@prompt.auto
def new_user(username: str) -> None:
    shell.run(["useradd", "--create-home", username])


@prompt.auto
def new_system_user(username: str) -> None:
    shell.run(["useradd", "--system", username])


@prompt.auto
def add_user_to_group(username: str, group: str) -> None:
    shell.run(["usermod", "--append", "--groups", group, username])
