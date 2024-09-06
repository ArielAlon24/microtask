from typing import Generic, TypeVar
from .abstract_command import AbstractCommand
from dataclasses import dataclass
from ..models.future import _Future, _Undefined

T = TypeVar("T")


@dataclass
class Wait(Generic[T], AbstractCommand[T]):
    future: _Future[T]

    def is_done(self) -> bool:
        return self.future.is_done()

    def result(self) -> T:
        if isinstance(self.future._value, _Undefined):
            raise RuntimeError(f"Future result was {_Undefined.__name__}")
        return self.future._value
