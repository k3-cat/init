import io
import re

from . import prompt

UNCOMMENT_PAT = "^#[\\t ]*({})([\\t ]*(?:#.*?)?)$"
SET_VALUE_PAT1 = "^#?[\\t ]*({})[\\t ]+=[\\t ]+\\S+([\\t ]*(?:#.*?)?)$"
SET_VALUE_PAT2 = "^#?[\\t ]*({})[\\t ]+\\S+([\\t ]*(?:#.*?)?)$"


def _attach_missing_key_if_needed(file: io.TextIOWrapper, new_contents: str):
    if new_contents:
        file.seek(0, io.SEEK_END)
        prompt.start("Adding missing targets")
        print(new_contents)
        file.write("\n\n\n")
        file.write("# missing values")
        file.write(new_contents)


@prompt.auto
def uncomment(file: io.TextIOWrapper, targets: set[str]):
    file.seek(0)
    content = file.read()
    new_contents = ""
    for target in targets:
        search = re.search(UNCOMMENT_PAT.format(target), content, re.M)
        if search:
            content.replace(search.string, search.group(1) + search.group(2))
        else:
            new_contents += target

    file.seek(0)
    file.write(content.strip())
    _attach_missing_key_if_needed(file, new_contents.strip())
    file.write("\n")


@prompt.auto
def set_value(file: io.TextIOWrapper, kvs: dict[str, str], no_equ_sign=False):
    file.seek(0)
    content = file.read()
    new_contents = ""
    for key, value in kvs.items():
        search = re.search(
            (SET_VALUE_PAT2 if no_equ_sign else SET_VALUE_PAT1).format(key),
            content,
            re.M,
        )
        if search:
            content.replace(search.string, f"{search.group(1)} {value}{search.group(2)}")
        else:
            new_contents += f"{key} {value}"

    file.seek(0)
    file.write(content.strip())
    _attach_missing_key_if_needed(file, new_contents.strip())
    file.write("\n")
