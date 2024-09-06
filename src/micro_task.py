from typing import ParamSpec, TypeVar, Generator, Callable, Generic, Type
from dataclasses import dataclass, field
from commands import AbstractCommand


class _Empty:
    def __str__(self) -> str:
        return "<_Empty>"


class _Undefined:
    def __str__(self) -> str:
        return "<_Undefined>"


P = ParamSpec("P")
R = TypeVar("R")


Function = Callable[P, R]
MicroTaskGen = Generator[_Empty | R, None, None]


@dataclass(slots=True)
class Future(Generic[R]):
    _value: R | _Undefined = field(default_factory=_Undefined)

    def is_done(self) -> bool:
        return not isinstance(self._value, _Undefined)


@dataclass(slots=True)
class MicroTask(Generic[R]):
    _generator: MicroTaskGen
    _command: AbstractCommand | None = field(default=None)
    _future: Future[R] = field(default_factory=Future)


MicroTaskGenCreator = Callable[P, MicroTaskGen]
