from typing import TypeVar, Generic
from dataclasses import dataclass, field

T = TypeVar("T")


class _Undefined:
    def __str__(self) -> str:
        return "<_Undefined>"


@dataclass(slots=True)
class _Future(Generic[T]):
    _value: T | _Undefined = field(default_factory=_Undefined)

    def is_done(self) -> bool:
        return not isinstance(self._value, _Undefined)
