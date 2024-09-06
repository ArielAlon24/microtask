from typing import ParamSpec, TypeVar, Generic, Callable, Generator
from dataclasses import dataclass, field
from ..commands import AbstractCommand
from .future import _Future


class _Empty:
    def __str__(self) -> str:
        return "<_Empty>"


P = ParamSpec("P")
R = TypeVar("R")


Function = Callable[P, R]
MicroTaskGen = Generator[_Empty | R, None, None]


@dataclass(slots=True)
class MicroTask(Generic[R]):
    _generator: MicroTaskGen
    _command: AbstractCommand | None = field(default=None)
    _future: _Future[R] = field(default_factory=_Future)


MicroTaskGenCreator = Callable[P, MicroTaskGen]
