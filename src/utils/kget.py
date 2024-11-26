import tarfile
from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryFile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from . import prompt

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/58.0.3029.110 "
    "Safari/537.36"
)


def _raw_fetch(req: Request) -> str:
    try:
        with urlopen(req) as res:
            return res.read().decode("utf-8")

    except HTTPError as e:
        raise prompt.error("HTTP Error, code: ", e.code)
    except URLError as e:
        raise prompt.error("Connect failed: ", e.reason)
    except Exception as e:
        raise e


@prompt.auto
def fetch(url: str) -> str:
    req = Request(url, headers={"User-agent": UA})
    return _raw_fetch(req)


@prompt.auto
def download(url: str, file_path: Path, token: str = ""):
    req = Request(url, headers={"User-agent": UA})
    if token:
        req.add_header("Authorization", token)
    with urlopen(req) as in_stream, file_path.open("wb") as fp:
        copyfileobj(in_stream, fp)


@prompt.auto
def extract_from_tar_gz(tar_url: str, filename: str, file_path: Path):
    req = Request(tar_url, headers={"User-agent": UA})
    with TemporaryFile() as tmp_fp, file_path.open("wb") as fp:
        with urlopen(req) as in_stream:
            copyfileobj(in_stream, tmp_fp)
        tmp_fp.seek(0)
        with tarfile.open(None, "r:gz", fileobj=tmp_fp) as tar:
            member_p = tar.extractfile(filename)
            if member_p is None:
                raise Exception()
            copyfileobj(member_p, fp)


def api_get(url: str, token: tuple[str, str]) -> str:
    req = Request(
        url,
        headers={
            token[0]: token[1],
            "Content-Type": "application/json",
        },
    )
    return _raw_fetch(req)


def api_post(url: str, data: str, token: tuple[str, str]) -> str:
    req = Request(
        url,
        data=data.encode("utf-8"),
        headers={
            token[0]: token[1],
            "Content-Type": "application/json",
        },
    )
    return _raw_fetch(req)
