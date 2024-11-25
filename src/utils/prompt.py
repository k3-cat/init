from typing import Callable, TypeVar, cast

TCallable = TypeVar("TCallable", bound=Callable)


def done():
    print("- - - Done - - -")


def start(*args):
    print(">", *args, end="")
    print(" ...")


def error(*args) -> Exception:
    return Exception("!!", *args)


def auto(fun: TCallable) -> TCallable:
    def wrapper(*args, **kwargs):
        start(fun.__name__, args, kwargs)
        fun(*args, **kwargs)
        done()

    return cast(TCallable, wrapper)
