from abc import ABC, abstractmethod
from typing import Callable
from ..models.future import _Future
from ..models.micro_task import MicroTaskGen


class AbstractScheduler(ABC):

    @abstractmethod
    def add(self, generator: MicroTaskGen) -> _Future:
        raise NotImplementedError

    @abstractmethod
    def start(self, entry: Callable[..., _Future]) -> None:
        raise NotImplementedError
