from typing import ParamSpec, TypeVar, Generator, Callable


class _Empty:
    def __str__(self) -> str:
        return "<_Empty>"


P = ParamSpec("P")
R = TypeVar("R")


Function = Callable[P, R]
MicroThread = Generator[_Empty | R, None, None]
MicroThreadCreator = Callable[P, MicroThread]
