from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

Result = TypeVar("Result")


@dataclass(slots=True)
class AbstractCommand(ABC, Generic[Result]):

    @abstractmethod
    def is_done(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def result(self) -> Result:
        raise NotImplementedError
